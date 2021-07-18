from pathlib import PosixPath

import ants
import numpy as np
from ants.core import ANTsImage
from rich import print


def get_coords(x: np.ndarray, margin: list = [4, 4, 2]) -> list:
    """Get coordinates of a given ROI, and apply a margin.

    Args:
        x (np.ndarray): ROI in binary format
        margin (list, optional): margin for xyz axes. Defaults to [4, 4, 2]

    Returns:
        list: Coordinates in xyzxyz format
    """
    ux, uy, uz = x.shape

    mask = np.where(x != 0)

    minx, maxx = int(np.min(mask[0])), int(np.max(mask[0]))
    miny, maxy = int(np.min(mask[1])), int(np.max(mask[1]))
    minz, maxz = int(np.min(mask[2])), int(np.max(mask[2]))

    minx = (minx - margin[0]) if (minx - margin[0]) > 0 else 0
    miny = (miny - margin[1]) if (miny - margin[1]) > 0 else 0
    minz = (minz - margin[2]) if (minz - margin[2]) > 0 else 0
    maxx = (maxx + margin[0]) if (maxx + margin[0]) < ux else ux
    maxy = (maxy + margin[1]) if (maxy + margin[1]) < uy else uy
    maxz = (maxz + margin[2]) if (maxz + margin[2]) < uz else uz

    return [minx, miny, minz, maxx, maxy, maxz]


def crop(image: ANTsImage,
         coords: list,
         output_path: PosixPath,
         log_coords: bool = True):
    """Crop an image using coordinates.

    Args:
        image (ANTsImage): image to be cropped
        coords (list): coordinates of the ROI
        output_path (PosixPath): path to save the cropped image
        log_coords (bool, optional): log the coordinates. Defaults to True.
    """
    cropped_image = ants.crop_indices(image,
                                      lowerind=coords[:3],
                                      upperind=coords[3:])

    if cropped_image.numpy().any():
        ants.image_write(cropped_image, str(output_path), ri=False)

        if log_coords:
            np.savetxt(output_path.with_suffix(".txt"), coords)

    else:
        print(
            f"[italic white]\tEmpty cropped array, skipping {output_path} for coordinates {coords}..."
        )
