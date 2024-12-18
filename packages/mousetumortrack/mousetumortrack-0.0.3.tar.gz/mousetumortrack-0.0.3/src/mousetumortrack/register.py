import numpy as np
from skimage.measure import marching_cubes
from skimage.filters import gaussian
import scipy.ndimage as ndi
from vedo import Points
from mouselungseg import LungsPredictor


def _apply_transform(image, Phi, order: int = 3):
    """Applies an affine transform to warp a 3D image."""
    warped = ndi.affine_transform(
        image, matrix=Phi[:3, :3], offset=Phi[:3, 3], order=order
    )

    return warped


def _fit_affine_from_lungs_masks(lungs0, lungs1):
    """Estimates an affine transformation matrix that brings lung1 onto lung0 from two sets of corresponding masks."""
    verts0, *_ = marching_cubes(gaussian(lungs0.astype(float), sigma=1), level=0.5)

    verts1, *_ = marching_cubes(gaussian(lungs1.astype(float), sigma=1), level=0.5)

    aligned_pts1 = (
        Points(verts1).clone().align_to(Points(verts0), invert=True, use_centroids=True)
    )

    Phi = aligned_pts1.transform.matrix

    return Phi


def register_timeseries_from_lungs_mask(labels_timeseries, lungs_timeseries=None, image_timeseries=None, order=3):
    """Registers a timeseries dataset based on the lungs data."""
    if lungs_timeseries is None:
        if image_timeseries is None:
            print("No images or lungs timeseries provided for the registration.")
            return
        
        # Compute the lungs timeseries
        predictor = LungsPredictor()
        lungs_timeseries = np.array([predictor.fast_predict(frame, skip_level=8) for frame in image_timeseries])


    image0 = labels_timeseries[0]
    registered_timeseries = np.empty_like(labels_timeseries)
    registered_timeseries[0] = image0

    lung0 = lungs_timeseries[0]
    registered_lungs_timeseries = np.empty_like(lungs_timeseries)
    registered_lungs_timeseries[0] = lung0

    for k, (image1, lung1) in enumerate(zip(labels_timeseries[1:], lungs_timeseries[1:])):
        Phi = _fit_affine_from_lungs_masks(lung0, lung1)

        warped_image1 = _apply_transform(image1, Phi, order=order)
        registered_timeseries[k + 1] = warped_image1

        warped_lung1 = _apply_transform(lung1, Phi, order=0)
        registered_lungs_timeseries[k + 1] = warped_lung1

    return registered_timeseries, lungs_timeseries, registered_lungs_timeseries
