import numpy as np
from .internal.gridgen import rect_grid
from .internal.gridgen import bent_corner_grid
from .internal.gridmap import GridMap
from .internal.warp import warp_by_grid


def calc_base_dim(
        border: np.ndarray
) -> int:
    x = border[:, 0]
    y = border[:, 1]

    return (x.max() - x.min() + y.max() - y.min()) // 2


def rectify_perspective(
        img_src: np.ndarray,
        border: np.ndarray,
        x_ratio: int = 1,
        y_ratio: int = 1
) -> (np.ndarray, GridMap):
    dim = calc_base_dim(border)
    dim_x = dim
    dim_y = dim * y_ratio // x_ratio

    gridmap = rect_grid(border, dim_x, dim_y)

    return warp_by_grid(img_src, gridmap.src, gridmap.dest, dim_x, dim_y), gridmap


def rectify_bent_corner(
        img_src: np.ndarray,
        border: np.ndarray,
        corner_idx: int,
        x_ratio: int = 1,
        y_ratio: int = 1
) -> (np.ndarray, GridMap):
    dim = calc_base_dim(border)
    dim_x = dim
    dim_y = dim * y_ratio // x_ratio

    gridmap = bent_corner_grid(border, corner_idx, dim_x, dim_y)

    return warp_by_grid(img_src, gridmap.src, gridmap.dest, dim_x, dim_y), gridmap
