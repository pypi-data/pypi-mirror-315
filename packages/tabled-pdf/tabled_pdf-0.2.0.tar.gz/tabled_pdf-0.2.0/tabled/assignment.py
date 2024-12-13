from typing import List

import numpy as np
from surya.schema import TableResult, Bbox

from tabled.heuristics import heuristic_layout
from tabled.schema import SpanTableCell


def is_rotated(rows, cols):
    # Determine if the table is rotated by looking at row and column width / height ratios
    # Rows should have a >1 ratio, cols <1
    widths = sum([r.width for r in rows])
    heights = sum([c.height for c in rows]) + 1
    r_ratio = widths / heights

    widths = sum([c.width for c in cols])
    heights = sum([r.height for r in cols]) + 1
    c_ratio = widths / heights

    return r_ratio * 2 < c_ratio


def overlapper_idxs(rows, field, thresh=.3):
    overlapper_rows = set()
    for row in rows:
        row_id = getattr(row, field)
        if row_id in overlapper_rows:
            continue

        for row2 in rows:
            row2_id = getattr(row2, field)
            if row2_id == row_id or row2_id in overlapper_rows:
                continue

            if row.intersection_pct(row2) > thresh:
                i_bigger = row.area > row2.area
                overlapper_rows.add(row_id if i_bigger else row2_id)
    return overlapper_rows


def initial_assignment(detection_result: TableResult, thresh=.5) -> List[SpanTableCell]:
    overlapper_rows = overlapper_idxs(detection_result.rows, field="row_id")
    overlapper_cols = overlapper_idxs(detection_result.cols, field="col_id")

    cells = []
    for cell in detection_result.cells:
        max_intersection = 0
        row_pred = None
        for row in detection_result.rows:
            if row.row_id in overlapper_rows:
                continue

            intersection_pct = Bbox(bbox=cell.bbox).intersection_pct(row)
            if intersection_pct > max_intersection and intersection_pct > thresh:
                max_intersection = intersection_pct
                row_pred = row.row_id

        max_intersection = 0
        col_pred = None
        for col in detection_result.cols:
            if col.col_id in overlapper_cols:
                continue

            intersection_pct = Bbox(bbox=cell.bbox).intersection_pct(col)
            if intersection_pct > max_intersection and intersection_pct > thresh:
                max_intersection = intersection_pct
                col_pred = col.col_id

        cells.append(
            SpanTableCell(
                bbox=cell.bbox,
                text=cell.text,
                row_ids=[row_pred],
                col_ids=[col_pred]
            )
        )
    return cells


def assign_overlappers(cells: List[SpanTableCell], detection_result: TableResult, thresh=.5):
    overlapper_rows = overlapper_idxs(detection_result.rows, field="row_id")
    overlapper_cols = overlapper_idxs(detection_result.cols, field="col_id")

    for cell in cells:
        max_intersection = 0
        row_pred = None
        for row in detection_result.rows:
            if row.row_id not in overlapper_rows:
                continue

            intersection_pct = Bbox(bbox=cell.bbox).intersection_pct(row)
            if intersection_pct > max_intersection and intersection_pct > thresh:
                max_intersection = intersection_pct
                row_pred = row.row_id

        max_intersection = 0
        col_pred = None
        for col in detection_result.cols:
            if col.col_id not in overlapper_cols:
                continue

            intersection_pct = Bbox(bbox=cell.bbox).intersection_pct(col)
            if intersection_pct > max_intersection and intersection_pct > thresh:
                max_intersection = intersection_pct
                col_pred = col.col_id

        if cell.row_ids[0] is None:
            cell.row_ids = [row_pred]
        if cell.col_ids[0] is None:
            cell.col_ids = [col_pred]


def assign_unassigned(table_cells: list, detection_result: TableResult):
    rotated = is_rotated(detection_result.rows, detection_result.cols)
    for cell in table_cells:
        if cell.row_ids[0] is None:
            closest_row = None
            min_dist = None
            for row in detection_result.rows:
                if rotated:
                    dist = cell.center_x_distance(row)
                else:
                    dist = cell.center_y_distance(row)

                if min_dist is None or dist < min_dist:
                    closest_row = row.row_id
                    min_dist = dist
            cell.row_ids = [closest_row]

        if cell.col_ids[0] is None:
            closest_col = None
            min_dist = None
            for col in detection_result.cols:
                if rotated:
                    dist = cell.center_y_distance(col)
                else:
                    dist = cell.center_x_distance(col)

                if min_dist is None or dist < min_dist:
                    closest_col = col.col_id
                    min_dist = dist

            cell.col_ids = [closest_col]


def handle_rowcol_spans(table_cells: list, detection_result: TableResult, thresh=.25):
    rotated = is_rotated(detection_result.rows, detection_result.cols)
    for cell in table_cells:
        for c in detection_result.cols:
            col_intersect_pct = cell.intersection_y_pct(c) if rotated else cell.intersection_x_pct(c)
            other_cell_exists = len([tc for tc in table_cells if tc.col_ids[0] == c.col_id and tc.row_ids[0] == cell.row_ids[0]]) > 0
            if col_intersect_pct > thresh and not other_cell_exists:
                cell.col_ids.append(c.col_id)
            else:
                break
        # Assign to first column header appears in
        cell.col_ids = sorted(cell.col_ids)

    for cell in table_cells:
        for r in detection_result.rows:
            row_intersect_pct = cell.intersection_x_pct(r) if rotated else cell.intersection_y_pct(r)
            other_cell_exists = len([tc for tc in table_cells if tc.row_ids[0] == r.row_id and tc.col_ids[0] == cell.col_ids[0]]) > 0
            if row_intersect_pct > thresh and not other_cell_exists:
                cell.row_ids.append(r.row_id)
            else:
                break


def merge_multiline_rows(detection_result: TableResult, table_cells: List[SpanTableCell]):
    def find_row_gap(r1, r2):
        return min([abs(r1.bbox[1] - r2.bbox[3]), abs(r2.bbox[1] - r1.bbox[3])])

    all_cols = set([tc.col_ids[0] for tc in table_cells])
    if len(all_cols) == 0:
        return

    merged_pairs = []
    row_gaps = [
        find_row_gap(r, r2)
        for r, r2 in zip(detection_result.rows, detection_result.rows[1:])
    ]
    if len(row_gaps) == 0:
        return

    gap_thresh = np.median(row_gaps)

    for idx, row in enumerate(detection_result.rows[1:]):
        prev_row = detection_result.rows[idx - 1]
        gap = find_row_gap(prev_row, row)

        # Ensure the gap between r2 and r1 is small
        if gap > gap_thresh:
            continue

        r1_cells = [tc for tc in table_cells if tc.row_ids[0] == prev_row.row_id]
        r2_cells = [tc for tc in table_cells if tc.row_ids[0] == row.row_id]
        r1_cols = set([tc.col_ids[0] for tc in r1_cells])
        r2_cols = set([tc.col_ids[0] for tc in r2_cells])

        # Ensure all columns in r2 are in r1
        if len(r2_cols - r1_cols) > 0:
            continue

        # Ensure r2 has mostly blank cells
        if len(r2_cols) / len(all_cols) > .5:
            continue

        merged_pairs.append((idx - 1, idx))

    to_remove = set()
    for r1_idx, r2_idx in merged_pairs:
        detection_result.rows[r1_idx].bbox = [
            min(detection_result.rows[r1_idx].bbox[0], detection_result.rows[r2_idx].bbox[0]),
            min(detection_result.rows[r1_idx].bbox[1], detection_result.rows[r2_idx].bbox[1]),
            max(detection_result.rows[r1_idx].bbox[2], detection_result.rows[r2_idx].bbox[2]),
            max(detection_result.rows[r1_idx].bbox[3], detection_result.rows[r2_idx].bbox[3])
        ]
        to_remove.add(r2_idx)

    new_rows = []
    row_counter = 0
    for idx, row in enumerate(detection_result.rows):
        if idx not in to_remove:
            row.row_id = row_counter
            new_rows.append(row)
            row_counter += 1
    detection_result.rows = new_rows


def assign_rows_columns(detection_result: TableResult, image_size: list, heuristic_thresh=.6) -> List[SpanTableCell]:
    table_cells = initial_assignment(detection_result)
    merge_multiline_rows(detection_result, table_cells)
    table_cells = initial_assignment(detection_result)
    assign_overlappers(table_cells, detection_result)
    total_unassigned = len([tc for tc in table_cells if tc.row_ids[0] is None or tc.col_ids[0] is None])
    unassigned_frac = total_unassigned / max(len(table_cells), 1)

    if unassigned_frac > heuristic_thresh:
        table_cells = heuristic_layout(table_cells, image_size)
        return table_cells

    assign_unassigned(table_cells, detection_result)
    handle_rowcol_spans(table_cells, detection_result)
    return table_cells
