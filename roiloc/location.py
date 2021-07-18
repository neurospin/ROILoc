from pathlib import PosixPath

import nibabel as nib
import numpy as np
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


def crop(image_path: PosixPath,
         coords: list,
         output_path: PosixPath,
         log_coords: bool = True):
    """Crop an image given some xyzxyz coordinates, and save it.

    Args:
        image_path (PosixPath): Path of the original MRI
        coords (list): xyzxyz coordinates of the ROI
        output_path (PosixPath): Path of the output file
        log_coords (bool, optional): Log the coordinates in the output file.
                                     Defaults to True.
    """
    original_image = nib.load(image_path)

    cropped_array = original_image.get_fdata()[coords[0]:coords[3] + 1,
                                               coords[1]:coords[4] + 1,
                                               coords[2]:coords[5] + 1]

    if cropped_array.any():
        cropped = nib.Nifti1Image(cropped_array,
                                  affine=original_image.affine,
                                  header=original_image.header)
        nib.save(cropped, output_path)

        if log_coords:
            np.savetxt(output_path.with_suffix(".txt"), coords)

    else:
        print(
            f"[orange]Empty cropped array, skipping {image_path} for coordinates {coords}..."
        )
