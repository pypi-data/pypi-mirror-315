import cv2 as cv
import numpy as np
from typing import Union

from scipy.spatial.distance import cdist
from cellbin.image.augmentation import f_ij_16_to_8, dapi_enhance, he_enhance

pt_enhance_method = {
    'ssDNA': dapi_enhance,
    'DAPI': dapi_enhance,
    'HE': he_enhance
}


def get_tissue_corner_points(
        tissue_data: np.ndarray,
        k: int = 9
):
    _tissue = tissue_data.copy()

    _tissue = cv.dilate(
        _tissue,
        kernel = np.ones([k, k], dtype = np.uint8)
    )

    contours, _ = cv.findContours(
        _tissue,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_NONE
    )

    max_contours = sorted(contours, key = cv.contourArea, reverse = True)[0]

    x, y, w, h = cv.boundingRect(max_contours)

    corner_points = np.array(
        [[x, y], [x, y + h], [x + w, y], [x + w, y + h]]
    )

    dis = cdist(
        max_contours.squeeze(),
        corner_points
    )

    result_points = max_contours.squeeze()[np.argmin(dis, axis = 0)]

    return result_points


def crop_image(
        corner_temp_points, points, image,
        image_size, image_type,
):
    height, width = image.shape[:2]
    cp_image_dict = dict()

    for ind, cp in enumerate(corner_temp_points):
        x, y = map(int, cp[:2])
        if x <= image_size // 2:
            x_left = 0
            x_right = image_size
        elif x + image_size // 2 > width:
            x_left = width - image_size
            x_right = width
        else:
            x_left = x - image_size // 2
            x_right = x + image_size // 2

        if y <= image_size // 2:
            y_up = 0
            y_down = image_size
        elif y + image_size // 2 > height:
            y_up = height - image_size
            y_down = height
        else:
            y_up = y - image_size // 2
            y_down = y + image_size // 2

        _ci = image[y_up: y_down, x_left: x_right]
        enhance_func = pt_enhance_method.get(image_type, "DAPI")
        _ctp = [i for i in points if (i[0] > x_left) and
                (i[1] > y_up) and
                (i[0] < x_right) and
                (i[1] < y_down)]
        local_ctp = np.array(_ctp)[:, :2] - [x_left, y_up]
        _ci = enhance_func(_ci)

        cp_image_dict[ind] = {
            "image": _ci, "image_xy": [x_left, y_up], "image_size": image_size,
            "template_local": np.array(local_ctp), "template_global": np.array(_ctp)
        }

    return cp_image_dict


def get_view_image(
        image_data: Union[str, np.ndarray],
        tissue_data: Union[str, np.ndarray],
        template: np.ndarray = None,
        image_size: int = 2000,
        image_type: str = "DAPI"
) -> dict:
    """

    Args:
        image_data: 配准图
        tissue_data: 配准图的 tissue cut图
        template: 矩阵模板点
        image_size: int - 图像尺寸
        image_type: str - ssDNA | HE | DAPI

    Returns:
        tissue_image_dict: len == 4
            - image: 小图增强图像
            - image_xy: 小图位于配准图左上角坐标
            - image_size: 图像尺寸
            - template_local: 小图局部模板坐标点
            - template_global: 小图全局模板坐标点

    """
    image, tissue_image = map(
        lambda x: cv.imread(x, -1) if isinstance(x, str) else x,
        (image_data, tissue_data)
    )

    tissue_corner_points = get_tissue_corner_points(tissue_image)

    tissue_image_dict = crop_image(
        tissue_corner_points, template, image,
        image_size, image_type,
    )

    return tissue_image_dict


if __name__ == '__main__':
    temp = np.loadtxt(r"D:\02.data\temp\A03599D1\cellbin2\A03599D1_Transcriptomics_matrix_template.txt")
    get_view_image(image_data = r"D:\02.data\temp\A03599D1\cellbin2\A03599D1_DAPI_regist.tif",
                   tissue_data = r"D:\02.data\temp\A03599D1\cellbin2\A03599D1_Transcriptomics_tissue_cut.tif",
                   template = temp)
