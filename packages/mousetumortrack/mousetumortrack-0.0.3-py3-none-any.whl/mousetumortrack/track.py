from itertools import product
import numpy as np
import pandas as pd
from skimage.measure import regionprops_table
from skimage.util import map_array
import trackpy as tp
from laptrack import LapTrack

from mousetumortrack.register import register_timeseries_from_lungs_mask


def _initialize_df(labels_timeseries, properties):
    dfs = []
    for t, frame in enumerate(labels_timeseries):
        if frame.sum() == 0:
            continue
        df = pd.DataFrame(regionprops_table(frame, properties=properties))
        df["frame_forward"] = t
        dfs.append(df)
    coordinate_df = pd.concat(dfs)
    # Invert the frame IDs to be able to track particles from the end
    coordinate_df["frame"] = (
        coordinate_df["frame_forward"].max() - coordinate_df["frame_forward"]
    )

    return coordinate_df


def _track_laptrack(
    df: pd.DataFrame,
    labels_timeseries: np.ndarray,
    max_dist_px,
    memory,
    dist_weight_ratio,
    max_volume_diff_rel,
):
    """Tracking with Laptrack."""
    n_frames = len(labels_timeseries)
    overlap_records = []
    for f in range(n_frames - 1):
        l1s = np.delete(
            np.unique(labels_timeseries[::-1][f]), 0
        )  # Invert the timeseries to track particles from the end.
        l2s = np.delete(np.unique(labels_timeseries[::-1][f + 1]), 0)
        for l1, l2 in product(l1s, l2s):
            sub_df1 = df.loc[
                (df["label"] == l1) & (df["frame"] == f), ["volume", "z", "y", "x"]
            ]
            sub_df2 = df.loc[
                (df["label"] == l2) & (df["frame"] == f + 1), ["volume", "z", "y", "x"]
            ]

            volume_l1 = sub_df1["volume"].values[0]
            volume_l2 = sub_df2["volume"].values[0]
            volume_diff_l1_l2 = np.abs(volume_l2 - volume_l1) / max(
                volume_l1, volume_l2
            )

            coord_l1 = sub_df1[["z", "y", "x"]].values[0]
            coord_l2 = sub_df2[["z", "y", "x"]].values[0]
            euclidean_dist_l1_l2 = np.linalg.norm(coord_l1 - coord_l2)

            overlap_records.append(
                {
                    "frame": f,
                    "label1": l1,
                    "label2": l2,
                    "volume_diff": volume_diff_l1_l2,
                    "euclidean_dist": euclidean_dist_l1_l2,
                }
            )

    overlap_df = pd.DataFrame.from_records(overlap_records)
    overlap_df["euclidean_dist_normalized"] = (
        overlap_df["euclidean_dist"] - overlap_df["euclidean_dist"].mean()
    ) / overlap_df["euclidean_dist"].std()
    overlap_df["volume_diff_normalized"] = (
        overlap_df["volume_diff"] - overlap_df["volume_diff"].mean()
    ) / overlap_df["volume_diff"].std()
    overlap_df = overlap_df.set_index(["frame", "label1", "label2"]).copy()

    def metric(c1, c2):
        (frame1, label1), (frame2, label2) = c1, c2
        if frame1 == frame2 + 1:
            tmp = (frame1, label1)
            (frame1, label1) = (frame2, label2)
            (frame2, label2) = tmp
        assert frame1 + 1 == frame2

        ind = (frame1, label1, label2)
        dist = overlap_df.loc[ind]["euclidean_dist_normalized"]
        vols = overlap_df.loc[ind]["volume_diff_normalized"]

        return dist * dist_weight_ratio + vols * (1 - dist_weight_ratio)

    max_dist_normalized = (
        max_dist_px - overlap_df["euclidean_dist"].mean()
    ) / overlap_df["euclidean_dist"].std()
    max_volume_diff_normalized = (
        max_volume_diff_rel - overlap_df["volume_diff"].mean()
    ) / overlap_df["volume_diff"].std()
    max_metric_cutoff = (
        max_dist_normalized * dist_weight_ratio
        + max_volume_diff_normalized * (1 - dist_weight_ratio)
    )

    lt = LapTrack(
        track_dist_metric=metric,  # custom metric
        gap_closing_max_frame_count=memory,  # "memory" parameter
        track_cost_cutoff=max_metric_cutoff,  # Maximum difference criterion between two linkages
        splitting_cost_cutoff=False,  # non-splitting case
        merging_cost_cutoff=False,  # non-merging case
    )

    linkage_df, *_ = lt.predict_dataframe(
        df, coordinate_cols=["frame", "label"], only_coordinate_cols=False
    )
    linkage_df.reset_index(inplace=True)
    linkage_df.rename(
        columns={"tree_id": "tumor", "frame_forward": "scan"}, inplace=True
    )
    linkage_df.drop(["frame_y", "track_id", "index"], axis="columns", inplace=True)

    return linkage_df


def _track_trackpy(df, max_dist_px, memory):
    """Tracking with Trackpy."""
    linkage_df = tp.link(df, search_range=max_dist_px, memory=memory)
    linkage_df = linkage_df.rename(
        columns={"particle": "tumor", "frame_forward": "scan", "label": "label"}
    )
    linkage_df["tumor"] = linkage_df["tumor"] + 1

    return linkage_df


# def remap_timeseries_labels_inline(timeseries, linkage_df) -> None:
#     """Modifies the input timeseries inline (a bit faster than making a copy)."""
#     unique_times = linkage_df['scan'].unique()
#     for t in unique_times:
#         dft = linkage_df[linkage_df['scan'] == t][['scan', 'tumor', 'label']]
#         new_labels = dft['tumor'].values.astype(timeseries.dtype)
#         old_labels = dft['label'].values.astype(timeseries.dtype)
#         map_array(timeseries[t], old_labels, new_labels, out=timeseries[t])


def _remap_timeseries_labels(timeseries, linkage_df):
    corrected_timeseries = np.zeros_like(timeseries)

    unique_times = linkage_df["scan"].unique()
    for t in unique_times:
        dft = linkage_df[linkage_df["scan"] == t][["scan", "tumor", "label"]]
        new_labels = dft["tumor"].values.astype(corrected_timeseries.dtype)
        old_labels = dft["label"].values.astype(corrected_timeseries.dtype)
        map_array(timeseries[t], old_labels, new_labels, out=corrected_timeseries[t])

    return corrected_timeseries


def run_tracking(
    labels_timeseries: np.ndarray,
    image_timeseries: np.ndarray = None,
    lungs_timeseries: np.ndarray = None,
    with_lungs_registration=False,
    max_dist_px=30,
    memory=0,
    dist_weight_ratio=0.9,
    max_volume_diff_rel=1.0,
    method="trackpy",
) -> pd.DataFrame:
    """Tracking objects between frames."""
    if with_lungs_registration:
        if lungs_timeseries is not None:
            registered_labels_timeseries, *_ = register_timeseries_from_lungs_mask(
                labels_timeseries, lungs_timeseries=lungs_timeseries, order=0
            )
        else:
            registered_labels_timeseries, *_ = register_timeseries_from_lungs_mask(
                labels_timeseries, image_timeseries=image_timeseries, order=0
            )
    else:
        registered_labels_timeseries = labels_timeseries

    # Volume needs to be computed on the original labels
    df_original_labels = _initialize_df(labels_timeseries, properties=["area", "label"])

    # Positions are computed on the registered labels
    df_registered_labels = _initialize_df(registered_labels_timeseries, properties=["centroid", "label"],)

    df = pd.merge(df_original_labels, df_registered_labels, on=["label", "frame_forward", "frame"])

    df.rename(
        columns={
            "centroid-0": "z",
            "centroid-1": "y",
            "centroid-2": "x",
            "area": "volume",
        },
        inplace=True,
    )

    if method == "trackpy":
        linkage_df = _track_trackpy(df, max_dist_px, memory)
    elif method == "laptrack":
        linkage_df = _track_laptrack(
            df,
            registered_labels_timeseries,
            max_dist_px,
            memory,
            dist_weight_ratio,
            max_volume_diff_rel,
        )

    # Remove tracks (and objects) that don't appear in every frame (strong constraint!)
    linkage_df = linkage_df.merge(
        pd.DataFrame({"length": linkage_df["tumor"].value_counts()}),
        left_on="tumor",
        right_index=True,
    )
    linkage_df = linkage_df[linkage_df["length"] == len(labels_timeseries)]

    # Group the dataframe
    grouped_df = linkage_df.groupby(["tumor", "scan"]).mean()

    # Remap the labels
    remapped_labels_timeseries = _remap_timeseries_labels(labels_timeseries, linkage_df)

    return linkage_df, grouped_df, remapped_labels_timeseries
