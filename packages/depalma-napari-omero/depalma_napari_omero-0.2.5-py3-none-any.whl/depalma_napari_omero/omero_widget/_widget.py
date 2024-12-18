import os
from pathlib import Path
import tifffile
import numpy as np
import pandas as pd
from napari.layers import Image, Labels
from napari.qt.threading import thread_worker
from napari.utils.notifications import show_info, show_error
from PyQt5.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QCheckBox,
)

from depalma_napari_omero.omero_server import OmeroServer

from mousetumornet.configuration import MODELS
from mousetumornet import predict, postprocess

# from mousetumornet.roi import (
#     compute_roi,
# )  # This should be replaced by the lungs Yolo model.
from mouselungseg import LungsPredictor, extract_3d_roi
from mousetumortrack import run_tracking

OMERO_TAGS = {
    "corrected": 113885,
    "roi": 182116,
    "pred_nnunet_v4": 206192,
}


def timeseries_ids(df, specimen_name):
    """Returns the indeces of the labeled images in a timeseries. Priority to images with the #corrected tag, otherwise #raw_pred is used."""

    def filter_group(group):
        if "corrected_pred" in group["class"].values:
            return group[group["class"] == "corrected_pred"].iloc[0]
        else:
            return group[group["class"] == "raw_pred"].iloc[0]

    roi_img_ids = df[(df["specimen"] == specimen_name) & (df["class"] == "roi")][
        ["image_id", "time"]
    ]
    labels_img_ids = df[
        (df["specimen"] == specimen_name)
        & (df["class"].isin(["corrected_pred", "raw_pred"]))
    ][["image_id", "time", "class"]]
    labels_img_ids = (
        labels_img_ids.groupby("time").apply(filter_group).reset_index(drop=True)
    )

    labels_img_ids = pd.merge(
        roi_img_ids,
        labels_img_ids,
        on="time",
        how="left",
        suffixes=("_rois", "_labels"),
    )

    labels_img_ids.sort_values(by="time", ascending=True, inplace=True)

    return (
        labels_img_ids["image_id_rois"].tolist(),
        labels_img_ids["image_id_labels"].tolist(),
    )


def image_timeseries_ids(df, specimen_name):
    """Returns the indeces of the labeled images in a timeseries. Priority to images with the #corrected tag, otherwise #raw_pred is used."""
    image_img_ids = df[(df["specimen"] == specimen_name) & (df["class"] == "image")][
        ["image_id", "time"]
    ]
    image_img_ids.sort_values(by="time", ascending=True, inplace=True)

    return image_img_ids["image_id"].tolist()


def combine_images(image_array_list):
    """Inserts images at different times, of different shapes, into a single (TZYX) array."""
    n_images = len(image_array_list)
    image_shapes = np.stack([np.array(img.shape) for img in image_array_list])
    output_shape = [n_images]
    output_shape.extend(list(np.max(image_shapes, axis=0)))

    timeseries = np.empty(output_shape, dtype=np.float32)
    for k, (image, image_shape) in enumerate(zip(image_array_list, image_shapes)):
        delta = (output_shape[1:] - image_shape) // 2
        timeseries[k][
            delta[0] : delta[0] + image_shape[0],
            delta[1] : delta[1] + image.shape[1],
            delta[2] : delta[2] + image.shape[2],
        ] = image

    return timeseries


def parse_df(df):
    # Make a separate dataset out of the "other" class
    df_other = df[df["class"] == "other"].copy()
    # n_images_other = len(df_other)

    df = df[df["class"] != "other"]
    all_categories = ["image", "roi", "raw_pred", "corrected_pred"]

    df_summary = df.pivot_table(
        index=["specimen", "time"],
        columns="class",
        aggfunc="size",
        fill_value=0,
    ).reset_index()
    df_summary = df_summary.reindex(
        columns=pd.Index(["specimen", "time"] + all_categories, name="class"),
        fill_value=0,
    )

    # Remove rows with an image missing
    image_missing_anomalies = df_summary[df_summary["image"] == 0]
    n_removed_image_missing = len(image_missing_anomalies)
    if not image_missing_anomalies.empty:
        filt = df.set_index(["specimen", "time"]).index.isin(
            image_missing_anomalies.set_index(["specimen", "time"]).index
        )

        # Add the anomalies to the "df_other" dataset
        df_other = pd.concat([df_other, df[filt].copy()])

        # Remove the anomalies in df
        df = df[~filt].copy()
        df_summary = df.pivot_table(
            index=["specimen", "time"],
            columns="class",
            aggfunc="size",
            fill_value=0,
        ).reset_index()
        df_summary = df_summary.reindex(
            columns=pd.Index(["specimen", "time"] + all_categories, name="class"),
            fill_value=0,
        )

    # Remove rows with multiple images
    multiple_image_anomalies = df_summary[df_summary["image"] > 1]
    n_removed_image_duplicate = len(multiple_image_anomalies)
    if not multiple_image_anomalies.empty:
        filt = df.set_index(["specimen", "time"]).index.isin(
            multiple_image_anomalies.set_index(["specimen", "time"]).index
        )
        multiple_images_to_check = df[filt][df[filt]["class"] == "image"][
            ["specimen", "time", "time_tag", "class", "image_id"]
        ].sort_values(["specimen", "time"])

        # Add the anomalies to the "df_other" dataset
        df_other = pd.concat([df_other, df[filt].copy()])

        # Remove the anomalies in df
        df = df[~filt].copy()
        df_summary = df.pivot_table(
            index=["specimen", "time"],
            columns="class",
            aggfunc="size",
            fill_value=0,
        ).reset_index()
        df_summary = df_summary.reindex(
            columns=pd.Index(["specimen", "time"] + all_categories, name="class"),
            fill_value=0,
        )

    # Image but no roi
    roi_missing_anomalies = df_summary[
        (df_summary["image"] > 0) & (df_summary["roi"] == 0)
    ][["specimen", "time"]]
    merged = pd.merge(df, roi_missing_anomalies, on=["specimen", "time"], how="inner")
    roi_missing = merged[merged["class"] == "image"].sort_values(["specimen", "time"])[
        ["dataset_id", "image_id", "image_name", "specimen", "time", "class"]
    ]

    # Roi but no preds or corrections
    pred_missing_anomalies = df_summary[
        (df_summary["roi"] > 0)
        & (df_summary["raw_pred"] == 0)
        & (df_summary["corrected_pred"] == 0)
    ][["specimen", "time"]]
    merged = pd.merge(df, pred_missing_anomalies, on=["specimen", "time"], how="inner")
    pred_missing = merged[merged["class"] == "roi"].sort_values(["specimen", "time"])[
        ["dataset_id", "image_id", "image_name", "specimen", "time", "class"]
    ]

    # Preds but no corrections
    correction_missing_anomalies = df_summary[
        (df_summary["raw_pred"] > 0) & (df_summary["corrected_pred"] == 0)
    ][["specimen", "time"]]
    merged = pd.merge(
        df, correction_missing_anomalies, on=["specimen", "time"], how="inner"
    )
    correction_missing = merged[merged["class"] == "raw_pred"].sort_values(
        ["specimen", "time"]
    )[["dataset_id", "image_id", "specimen", "time", "class"]]
    n_correction_missing = len(correction_missing)

    # Print a small report
    print(f"\n### Dataset summary ###")
    n_images_other = len(df_other)
    n_specimens = df["specimen"].nunique()
    n_times = df["time"].nunique()
    valid_times = df["time"].unique()
    print(f"{n_specimens} valid specimens found.")
    print(f"{n_times} valid scan times found ({valid_times})")
    if len(roi_missing) > 0:
        print(f"{len(roi_missing)} ROIs are missing for these image IDs:")
        print(roi_missing["image_id"].tolist())
    if len(pred_missing) > 0:
        print(f"{len(pred_missing)} model predictions are missing for these image IDs:")
        print(pred_missing["image_id"].tolist())
    if n_correction_missing > 0:
        print(
            f"{n_correction_missing} corrected predictions are missing for these image IDs:"
        )
        print(correction_missing["image_id"].tolist())
    if n_images_other > 0:
        print(
            f"{n_images_other} files could not be reliably tagged in {all_categories} and were added to the `Other files` list."
        )
    if n_removed_image_duplicate > 0:
        print(
            f"{n_removed_image_duplicate} specimen-time combinations have multiple associated `image` files matching and were skipped:"
        )
        print(multiple_images_to_check)
    if n_removed_image_missing > 0:
        print(
            f"{n_removed_image_missing} specimen-time combinations have no associated `image` files matching and were skipped:"
        )
        print(image_missing_anomalies)
    print()

    return df, df_other, roi_missing, pred_missing


class OMEROWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        server = OmeroServer()

        self.viewer = napari_viewer
        self.server = server

        self.roi_missing = None
        self.pred_missing = None
        self.grouped_df = None

        self.grayout_ui_list = []
        self.active_batch_workers = []

        ### Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        qwidget = QWidget(self)
        layout.addWidget(qwidget)

        ### Login
        login_layout = QGridLayout()
        login_layout.setContentsMargins(10, 10, 10, 10)
        login_layout.setAlignment(Qt.AlignTop)

        # Username
        login_layout.addWidget(QLabel("Username", self), 0, 0)
        self.username = QLineEdit(self)
        self.username.setText("imaging-robot")
        login_layout.addWidget(self.username, 0, 1)

        # Password
        login_layout.addWidget(QLabel("Password", self), 1, 0)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password, 1, 1)

        # Connect
        connect_btn = QPushButton("Login", self)
        connect_btn.clicked.connect(self._login)
        login_layout.addWidget(connect_btn, 2, 0, 1, 2)

        select_layout = QGridLayout()
        select_layout.setContentsMargins(10, 10, 10, 10)
        select_layout.setAlignment(Qt.AlignTop)

        # Experiment group
        experiment_group = QGroupBox(qwidget)
        experiment_group.setTitle("Experiment")
        experiment_layout = QGridLayout()
        experiment_group.setLayout(experiment_layout)
        experiment_group.layout().setContentsMargins(10, 10, 10, 10)
        select_layout.addWidget(experiment_group, 0, 0)

        # Image data group
        image_group = QGroupBox(qwidget)
        image_group.setTitle("Scan data")
        image_layout = QGridLayout()
        image_group.setLayout(image_layout)
        image_group.layout().setContentsMargins(10, 10, 10, 10)
        select_layout.addWidget(image_group, 2, 0)

        # Project (experiment)
        self.cb_project = QComboBox()
        self.cb_project.currentTextChanged.connect(self._handle_project_changed)
        experiment_layout.addWidget(self.cb_project, 0, 0, 1, 3)

        # Model selection
        self.cb_models = QComboBox()
        for model_name in reversed(MODELS.keys()):
            self.cb_models.addItem(model_name, model_name)
        experiment_layout.addWidget(QLabel("Model", self), 1, 0)
        experiment_layout.addWidget(self.cb_models, 1, 1, 1, 2)

        # Batch processing on experiment
        self.btn_batch_roi = QPushButton("🔁 Batch ROI (-)", self)
        self.btn_batch_roi.clicked.connect(self._start_batch_roi)
        experiment_layout.addWidget(self.btn_batch_roi, 2, 0)

        self.btn_batch_nnunet = QPushButton("🔁 Batch detection (-)", self)
        self.btn_batch_nnunet.clicked.connect(self._start_batch_nnunet)
        experiment_layout.addWidget(self.btn_batch_nnunet, 2, 1)

        self.btn_batch_both = QPushButton("🔁 Both", self)
        self.btn_batch_both.clicked.connect(self._start_both_batches)
        experiment_layout.addWidget(self.btn_batch_both, 2, 2)

        # Cancel button
        cancel_btn = QPushButton("❌ Cancel", self)
        cancel_btn.clicked.connect(self._handle_cancel)
        experiment_layout.addWidget(cancel_btn, 3, 0, 1, 3)

        # Specimens (mouse)
        self.cb_specimen = QComboBox()
        self.cb_specimen.currentTextChanged.connect(self._update_combobox_times)
        image_layout.addWidget(QLabel("Case", self), 0, 0)
        image_layout.addWidget(self.cb_specimen, 0, 1)

        # Scan time
        self.cb_time = QComboBox()
        self.cb_time.currentTextChanged.connect(self._update_combobox_classes)
        image_layout.addWidget(QLabel("Scan time", self), 1, 0)
        image_layout.addWidget(self.cb_time, 1, 1)

        # Images (data class)
        self.cb_image = QComboBox()
        image_layout.addWidget(QLabel("Data category", self), 2, 0)
        image_layout.addWidget(self.cb_image, 2, 1)

        # Download button
        btn_download = QPushButton("⏬ Download", self)
        btn_download.clicked.connect(self._trigger_download)
        image_layout.addWidget(btn_download, 3, 0, 1, 2)

        # Upload layer input
        self.cb_upload = QComboBox()
        image_layout.addWidget(QLabel("Corrected data", self), 4, 0)
        image_layout.addWidget(self.cb_upload, 4, 1)

        # Upload button
        btn_upload_corrections = QPushButton("⏫ Upload", self)
        btn_upload_corrections.clicked.connect(self._trigger_upload_corrections)
        image_layout.addWidget(btn_upload_corrections, 5, 0, 1, 2)

        ### Tracking tab
        tracking_layout = QGridLayout()
        tracking_layout.setContentsMargins(10, 10, 10, 10)
        tracking_layout.setAlignment(Qt.AlignTop)

        tracking_layout.addWidget(QLabel("Selected case:", self), 0, 0)
        self.label_selected_case_value = QLabel("-", self)
        tracking_layout.addWidget(self.label_selected_case_value, 0, 1)

        self.cb_track_labels = QComboBox()
        tracking_layout.addWidget(QLabel("Tumor series", self), 1, 0)
        tracking_layout.addWidget(self.cb_track_labels, 1, 1)

        # Download tumor labels timeseries
        self.btn_download_labels_series = QPushButton("⏬ (-)", self)
        self.btn_download_labels_series.clicked.connect(
            self._trigger_download_timeseries_labels
        )
        tracking_layout.addWidget(self.btn_download_labels_series, 1, 2)

        self.cb_track_images = QComboBox()
        tracking_layout.addWidget(QLabel("Image series", self), 2, 0)
        tracking_layout.addWidget(self.cb_track_images, 2, 1)

        # Download ROIs timeseries
        self.btn_download_roi_series = QPushButton("⏬ (-)", self)
        self.btn_download_roi_series.clicked.connect(
            self._trigger_download_timeseries_rois
        )
        tracking_layout.addWidget(self.btn_download_roi_series, 2, 2)

        tracking_layout.addWidget(
            QLabel("Align the scans before tracking", self), 3, 0, 1, 2
        )
        self.with_lungs_checkbox = QCheckBox()
        self.with_lungs_checkbox.setChecked(True)
        tracking_layout.addWidget(self.with_lungs_checkbox, 3, 2)
        track_btn = QPushButton("Run tracking", self)
        track_btn.clicked.connect(self._trigger_tracking)
        tracking_layout.addWidget(track_btn, 4, 0, 1, 3)
        track_csv_btn = QPushButton("Save as CSV", self)
        track_csv_btn.clicked.connect(self._save_track_csv)
        tracking_layout.addWidget(track_csv_btn, 5, 0, 1, 3)

        track_csv_btn = QPushButton("Run full pipeline on selected case (demo)", self)
        track_csv_btn.clicked.connect(self._start_full_pipeline)
        tracking_layout.addWidget(track_csv_btn, 6, 0, 1, 3)

        ### Generic upload tab
        generic_upload_layout = QGridLayout()
        generic_upload_layout.setContentsMargins(10, 10, 10, 10)
        generic_upload_layout.setAlignment(Qt.AlignTop)

        self.cb_dataset = QComboBox()
        self.cb_dataset.currentTextChanged.connect(self._handle_dataset_changed)
        generic_upload_layout.addWidget(QLabel("Dataset", self), 0, 0)
        generic_upload_layout.addWidget(self.cb_dataset, 0, 1)

        self.cb_download_generic = QComboBox()
        generic_upload_layout.addWidget(QLabel("Files", self), 1, 0)
        generic_upload_layout.addWidget(self.cb_download_generic, 1, 1)
        btn_download_generic = QPushButton("⏬ Download", self)
        btn_download_generic.clicked.connect(self._trigger_download_generic)
        generic_upload_layout.addWidget(btn_download_generic, 1, 2)

        self.cb_upload_generic = QComboBox()
        generic_upload_layout.addWidget(QLabel("Layer", self), 2, 0)
        generic_upload_layout.addWidget(self.cb_upload_generic, 2, 1)
        btn_upload_generic = QPushButton("⏫ Upload", self)
        btn_upload_generic.clicked.connect(self._trigger_upload_generic)
        generic_upload_layout.addWidget(btn_upload_generic, 2, 2)

        ### Tabs
        tab1 = QWidget(self)
        tab1.setLayout(login_layout)
        tab2 = QWidget(self)
        tab2.setLayout(select_layout)
        tab3 = QWidget(self)
        tab3.setLayout(tracking_layout)
        tab4 = QWidget(self)
        tab4.setLayout(generic_upload_layout)
        self.tabs = QTabWidget()
        self.tabs.addTab(tab1, "Login")
        self.tabs.addTab(tab2, "Data selection")
        self.tabs.addTab(tab4, "Download / Upload")
        self.tabs.addTab(tab3, "Track tumors")
        layout.addWidget(self.tabs)

        # Progress bar
        self.pbar = QProgressBar(self, minimum=0, maximum=1)
        layout.addWidget(self.pbar)

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

        # Add elements that should be grayed out to the list
        self.grayout_ui_list.append(self.btn_batch_nnunet)
        self.grayout_ui_list.append(self.btn_batch_roi)
        self.grayout_ui_list.append(self.btn_batch_both)
        self.grayout_ui_list.append(self.btn_download_labels_series)
        self.grayout_ui_list.append(self.btn_download_roi_series)
        self.grayout_ui_list.append(btn_download)
        self.grayout_ui_list.append(btn_upload_corrections)
        self.grayout_ui_list.append(btn_download_generic)
        self.grayout_ui_list.append(btn_upload_generic)
        self.grayout_ui_list.append(self.cb_project)
        self.grayout_ui_list.append(self.cb_specimen)
        self.grayout_ui_list.append(self.cb_image)
        self.grayout_ui_list.append(self.cb_time)
        self.grayout_ui_list.append(self.cb_download_generic)
        self.grayout_ui_list.append(self.cb_upload)
        # self.grayout_ui_list.append(self.check_add_corrected_tag)
        self.grayout_ui_list.append(self.cb_dataset)
        self.grayout_ui_list.append(self.cb_download_generic)
        self.grayout_ui_list.append(self.cb_upload_generic)

    def _on_layer_change(self, e):
        self.cb_upload_generic.clear()
        for x in self.viewer.layers:
            if isinstance(x, Labels) | isinstance(x, Image):
                self.cb_upload_generic.addItem(x.name, x.data)

        self.cb_upload.clear()
        self.cb_track_labels.clear()
        self.cb_track_images.clear()
        for x in self.viewer.layers:
            if isinstance(x, Labels):
                if len(x.data.shape) == 3:
                    self.cb_upload.addItem(x.name, x.data)
                if len(x.data.shape) == 4:  # Timeseries labels
                    self.cb_track_labels.addItem(x.name, x.data)
            elif isinstance(x, Image):
                if len(x.data.shape) == 4:  # Timeseries images
                    self.cb_track_images.addItem(x.name, x.data)

    def _login(self):
        self.server.login(user=self.username.text(), password=self.password.text())

        ### Trigger connection upon startup
        connect_status = self.server.connect()
        if connect_status:
            all_projects_list = list(self.server.projects.keys())
            all_projects_list.insert(0, "Select from list")
            self.cb_project.clear()
            self.cb_project.addItems(all_projects_list)

            # Select the data selection tab
            self.tabs.setCurrentIndex(1)
        else:
            show_info("Could not connect. Try again?")

        # Clear the input
        self.password.clear()

    def _handle_dataset_changed(self, selected_dataset_title):
        dataset_id = int(self.cb_dataset.currentData())

        self.cb_download_generic.clear()
        df_sorted = self.df_all[self.df_all["dataset_id"] == dataset_id].sort_values(
            by="image_id"
        )[["image_id", "image_name"]]
        df_sorted["title"] = df_sorted.apply(
            lambda row: f"{row['image_id']} - {row['image_name']}", axis=1
        )
        other_files_titles = df_sorted["title"].tolist()
        other_files_data = df_sorted["image_id"].tolist()
        for title, data in zip(other_files_titles, other_files_data):
            self.cb_download_generic.addItem(title, data)

    def _handle_project_changed(self, selected_project_name):
        if selected_project_name in ["", "Select from list"]:
            return

        self.server.connect()
        self.project_id = self.server.projects[selected_project_name]

        n_datasets = self.server.get_n_datasets_in_project(self.project_id)

        worker = self._threaded_project_update()
        worker.returned.connect(self._ungrayout_ui)
        worker.aborted.connect(self._ungrayout_ui)
        worker.yielded.connect(lambda step: self.pbar.setValue(step))
        self.active_batch_workers.append(worker)
        self.pbar.setMaximum(n_datasets)
        self.pbar.setValue(0)
        self._grayout_ui()
        worker.start()

    @thread_worker
    def _threaded_project_update(self):
        dataset_ids = []
        dataset_names = []
        image_ids = []
        image_names = []
        specimens = []
        times = []
        time_tags = []
        image_classes = []
        previous_dataset_id = None
        k_dataset = 0
        for (
            dataset_id,
            dataset_name,
            image_id,
            image_name,
            specimen,
            time,
            time_tag,
            image_class,
        ) in self.server.project_data_generator(self.project_id):
            dataset_ids.append(dataset_id)
            dataset_names.append(dataset_name)
            image_ids.append(image_id)
            image_names.append(image_name)
            specimens.append(specimen)
            times.append(time)
            time_tags.append(time_tag)
            image_classes.append(image_class)

            # For the progressbar update:
            if (previous_dataset_id is None) | (previous_dataset_id != dataset_id):
                previous_dataset_id = dataset_id
                k_dataset += 1
                yield k_dataset

        self.df_all = pd.DataFrame(
            {
                "dataset_id": dataset_ids,
                "dataset_name": dataset_names,
                "image_id": image_ids,
                "image_name": image_names,
                "specimen": specimens,
                "time": np.array(times, dtype=float),  # .astype(int),
                "time_tag": time_tags,
                "class": image_classes,
            }
        )

        self.df, self.df_other, self.roi_missing, self.pred_missing = parse_df(
            self.df_all
        )

        # Update the UI
        self.cb_specimen.clear()
        self.cb_download_generic.clear()
        self._update_combobox_specimens()
        self._update_combobox_datasets()
        self.btn_batch_roi.setText(f"🔁 Batch ROI ({len(self.roi_missing)})")
        self.btn_batch_nnunet.setText(f"🔁 Batch detection ({len(self.pred_missing)})")

    def _update_combobox_datasets(self):
        self.cb_dataset.clear()

        df_sorted = (
            self.df_all[["dataset_id", "dataset_name"]]
            .drop_duplicates()
            .sort_values(by="dataset_id")
        )
        df_sorted["title"] = df_sorted.apply(
            lambda row: f"{row['dataset_id']} - {row['dataset_name']}", axis=1
        )
        dataset_titles = df_sorted["title"].tolist()
        dataset_data = df_sorted["dataset_id"].tolist()
        for title, data in zip(dataset_titles, dataset_data):
            self.cb_dataset.addItem(title, data)

    def _update_combobox_specimens(self):
        self.cb_time.clear()
        project_specimens = np.unique(self.df["specimen"].tolist())
        self.cb_specimen.clear()
        self.cb_specimen.addItems(project_specimens)

    def _update_combobox_times(self, specimen):
        self.label_selected_case_value.setText(f"{specimen}")

        self.cb_image.clear()
        sub_df = self.df[self.df["specimen"] == specimen]
        times = np.unique(sub_df["time"].tolist()).astype(str)
        self.cb_time.clear()
        self.cb_time.addItems(times)

        # Timeseries
        self.roi_timeseries_ids, self.labels_timeseries_ids = timeseries_ids(
            self.df, specimen
        )

        n_rois_timeseries = len(self.roi_timeseries_ids)
        n_nans_labels_timeseries = np.isnan(self.labels_timeseries_ids).any().sum()
        n_labels_timeseries = len(self.labels_timeseries_ids) - n_nans_labels_timeseries

        self.btn_download_roi_series.setText(f"⏬ {n_rois_timeseries} scans")
        self.btn_download_labels_series.setText(f"⏬ {n_labels_timeseries} scans")

    def _update_combobox_classes(self, *args, **kwargs):
        specimen = self.cb_specimen.currentText()
        if specimen == "":
            return

        time = self.cb_time.currentText()
        if time == "":
            return
        else:
            time = int(
                float(time)
            )  # the value can be '-1.0' which needs to be cast into a float first.

        sub_df = self.df[(self.df["specimen"] == specimen) & (self.df["time"] == time)]

        image_classes = sub_df["class"].tolist()

        if ((sub_df["class"] == "roi").sum() > 1) | (
            (sub_df["class"] == "image").sum() > 1
        ):
            show_error("Duplicate images!")
            image_classes = []
        else:
            n_matches = len(image_classes)
            image_classes = np.unique(image_classes)
            if len(image_classes) != n_matches:
                print("Warning - Duplicate predictions found!")

        self.cb_image.clear()
        self.cb_image.addItems(image_classes)

    @thread_worker
    def _threaded_download(self, image_id, image_name, image_class):
        self.server.connect()
        return (self.server.download_image(image_id), image_name, image_class)

    def _trigger_download_generic(self):
        if self.cb_download_generic.currentText() == "":
            return

        image_id = self.cb_download_generic.currentData()
        image_name = self.df_all[self.df_all["image_id"] == image_id][
            "image_name"
        ].tolist()[0]
        image_class = self.df_all[self.df_all["image_id"] == image_id][
            "class"
        ].tolist()[0]

        show_info(f"Downloading {image_id=} ({image_class})")
        worker = self._threaded_download(image_id, image_name, image_class)
        worker.returned.connect(self._download_thread_returned)
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    def _trigger_download(self):
        image_class = self.cb_image.currentText()
        if image_class == "":
            return

        specimen = self.cb_specimen.currentText()
        if specimen == "":
            return

        time = self.cb_time.currentText()
        if time == "":
            return
        else:
            time = int(
                float(time)
            )  # the value can be '-1.0' which needs to be cast into a float first.

        sub_df = self.df[
            (self.df["specimen"] == specimen)
            & (self.df["time"] == time)
            & (self.df["class"] == image_class)
        ]

        image_id = sub_df["image_id"].tolist()[0]
        image_name = sub_df["image_name"].tolist()[0]

        show_info(f"Downloading {image_id=}")
        worker = self._threaded_download(image_id, image_name, image_class)
        worker.returned.connect(self._download_thread_returned)
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    def _download_thread_returned(self, payload):
        """Callback from download thread returning."""
        self._ungrayout_ui()
        image_data, image_name, image_class = payload
        if image_class in ["corrected_pred", "raw_pred"]:
            self.viewer.add_labels(image_data, name=image_name)
        elif image_class in ["roi", "image"]:
            self.viewer.add_image(image_data, name=image_name)
        else:
            print(f"Unknown image class: {image_class}. Attempting to load an image.")
            self.viewer.add_image(image_data, name=image_name)

    @thread_worker
    def _threaded_upload(self, posted_image_data, posted_image_name, dataset_id):
        self.server.connect()

        # posted_image_id = self.server.post_image_to_ds(
        #     posted_image_data, dataset_id, posted_image_name
        # )

        posted_image_id = self.server.import_image_to_ds(
            posted_image_data, self.project_id, dataset_id, posted_image_name
        )

        return posted_image_id

    def _trigger_upload_corrections(self):
        """Handles uploading images to the OMERO server."""
        layer_name = self.cb_upload.currentText()
        if layer_name == "":
            return

        layer = self.viewer.layers[layer_name]
        if not isinstance(layer, Labels):
            show_info(f"Layer has an unrecognized type: {layer.__class__}.")
            return

        # When uploading a corrected prediction, tag it like the original image, without the image tag itself.
        layer_name = f"{os.path.splitext(layer_name)[0]}_corrected.tif"

        updated_data = layer.data.astype("uint8")  # No higher ints for OMERO

        image_class = self.cb_image.currentText()
        if image_class == "":
            return

        specimen = self.cb_specimen.currentText()
        if specimen == "":
            return

        time = self.cb_time.currentText()
        if time == "":
            return
        else:
            time = int(
                float(time)
            )  # the value can be '-1.0' which needs to be cast into a float first.

        sub_df = self.df[
            (self.df["specimen"] == specimen)
            & (self.df["time"] == time)
            & (self.df["class"] == image_class)
        ]

        dataset_id = sub_df["dataset_id"].tolist()[0]
        image_id = sub_df["image_id"].tolist()[0]

        worker = self._threaded_upload(updated_data, layer_name, dataset_id)
        worker.returned.connect(self._upload_thread_returned)
        worker.returned.connect(
            lambda posted_image_id: self._upload_thread_returned_handle_image_tags(
                posted_image_id, image_id
            )
        )
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    def _upload_thread_returned_handle_image_tags(self, posted_image_id, image_id):
        self.server.connect()

        img_tags = self.server.get_image_tags(image_id)
        image_tags_list = self.server.find_image_tag(img_tags)
        image_tags_list.append("roi")

        self.server.copy_image_tags(
            src_image_id=image_id,
            dst_image_id=posted_image_id,
            exclude_tags=image_tags_list,
        )

        self.server.tag_image_with_tag(posted_image_id, tag_id=OMERO_TAGS["corrected"])

    def _upload_thread_returned(self, posted_image_id):
        # Save the current indeces
        current_specimen_idx = self.cb_specimen.currentIndex()
        current_time_idx = self.cb_time.currentIndex()
        current_dataset_idx = self.cb_dataset.currentIndex()

        self.server.connect()
        n_datasets = self.server.get_n_datasets_in_project(self.project_id)
        worker = self._threaded_project_update()
        worker.returned.connect(self._ungrayout_ui)
        worker.aborted.connect(self._ungrayout_ui)
        worker.yielded.connect(lambda step: self.pbar.setValue(step))

        # Select the dataset and time that was previously selected
        worker.returned.connect(
            lambda _: self.cb_specimen.setCurrentIndex(current_specimen_idx)
        )
        worker.returned.connect(
            lambda _: self.cb_time.setCurrentIndex(current_time_idx)
        )
        worker.returned.connect(
            lambda _: self.cb_dataset.setCurrentIndex(current_dataset_idx)
        )

        self.active_batch_workers.append(worker)
        self.pbar.setMaximum(n_datasets)
        self.pbar.setValue(0)
        self._grayout_ui()
        worker.start()

        show_info(f"Uploaded image {posted_image_id}.")

    def _trigger_upload_generic(self):
        layer_name = self.cb_upload_generic.currentText()
        if layer_name == "":
            return

        selected_dataset_text = self.cb_dataset.currentText()
        if selected_dataset_text == "":
            show_info("No dataset selected!")
            return

        layer = self.viewer.layers[layer_name]
        if not (isinstance(layer, Image) or isinstance(layer, Labels)):
            show_info(f"Layer has an unrecognized type: {layer.__class__}.")
            return

        updated_data = layer.data
        if isinstance(layer, Labels):
            updated_data = updated_data.astype(np.uint8)

        dataset_id = int(self.cb_dataset.currentData())

        worker = self._threaded_upload(updated_data, layer_name, dataset_id)
        worker.returned.connect(self._upload_thread_returned)
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    def _start_both_batches(self):
        # Copy of the code for batch roi (for now)
        if self.roi_missing is None:
            return

        n_rois_to_compute = len(self.roi_missing)
        if n_rois_to_compute:
            worker = self._batch_roi(n_rois_to_compute)
            worker.returned.connect(
                self._project_update_after_batch_roi
            )  # Change the thread return event
            worker.aborted.connect(self._threaded_project_update)
            worker.yielded.connect(lambda step: self.pbar.setValue(step))
            self.active_batch_workers.append(worker)
            self.pbar.setMaximum(n_rois_to_compute)
            self.pbar.setValue(0)
            self._grayout_ui()
            worker.start()
        else:
            print("No ROIs to compute.")

    def _project_update_after_batch_roi(self):
        # Update the projects before running a batch nnunet prediction (used when "Both" is clicked)
        selected_project_name = self.cb_project.currentText()
        if selected_project_name in ["", "Select from list"]:
            return

        self.server.connect()
        self.project_id = self.server.projects[selected_project_name]
        n_datasets = self.server.get_n_datasets_in_project(self.project_id)

        worker = self._threaded_project_update()
        worker.returned.connect(self._start_batch_nnunet)
        worker.aborted.connect(self._ungrayout_ui)
        worker.yielded.connect(lambda step: self.pbar.setValue(step))
        self.active_batch_workers.append(worker)
        self.pbar.setMaximum(n_datasets)
        self.pbar.setValue(0)
        self._grayout_ui()
        worker.start()

    @thread_worker
    def _batch_nnunet(self, n_preds_to_compute):
        self.server.connect()

        # model = list(MODELS.keys())[0]
        model = self.cb_models.currentData()
        if model is None:
            print("Could not select a model for prediction.")
            return

        for k, (_, row) in enumerate(
            self.pred_missing[["dataset_id", "image_id", "image_name"]].iterrows()
        ):
            image_id = row["image_id"]
            dataset_id = row["dataset_id"]
            image_name = row["image_name"]

            print(
                f"Computing {k+1} / {n_preds_to_compute} tumor predictions. Image ID = {image_id}"
            )

            image_name_stem = os.path.splitext(image_name)[0]
            posted_image_name = f"{image_name_stem}_pred_nnunet_{model}.tif"

            image = self.server.download_image(image_id)

            try:
                image_pred = predict(
                    image, model=model
                )  # Note: No external normalization for nnUNet-v4
                image_pred = postprocess(image_pred)
            except:
                print(
                    f"An error occured while computing the NNUNET prediction in this image: ID={image_id}."
                )
                continue

            self.server.connect()
            posted_image_id = self.server.post_image_to_ds(
                image_pred, dataset_id, posted_image_name
            )
            self.server.tag_image_with_tag(
                posted_image_id, tag_id=OMERO_TAGS["pred_nnunet_v4"]
            )
            self.server.copy_image_tags(
                src_image_id=image_id,
                dst_image_id=posted_image_id,
                exclude_tags=["roi"],
            )

            yield k + 1

    def _start_batch_nnunet(self):
        if self.pred_missing is None:
            print(f"{self.pred_missing=}")
            return

        n_preds_to_compute = len(self.pred_missing)
        if n_preds_to_compute:
            worker = self._batch_nnunet(n_preds_to_compute)
            worker.returned.connect(self._reset_ui_and_project_state)
            worker.aborted.connect(self._reset_ui_and_project_state)
            worker.yielded.connect(lambda step: self.pbar.setValue(step))
            self.active_batch_workers.append(worker)
            self.pbar.setMaximum(n_preds_to_compute)
            self.pbar.setValue(0)
            self._grayout_ui()
            worker.start()
        else:
            print("No predictions to compute.")

    @thread_worker
    def _batch_roi(self, n_rois_to_compute):
        self.server.connect()
        predictor = LungsPredictor()
        for k, (_, row) in enumerate(
            self.roi_missing[["dataset_id", "image_id", "image_name"]].iterrows()
        ):
            image_id = row["image_id"]
            dataset_id = row["dataset_id"]
            image_name = row["image_name"]

            print(f"Computing {k+1} / {n_rois_to_compute} ROIs. Image ID = {image_id}")

            image_name_stem = os.path.splitext(image_name)[0]
            posted_image_name = f"{image_name_stem}_roi.tif"

            image = self.server.download_image(image_id)

            try:
                # *_, roi = compute_roi_bones(image)
                # *_, roi = compute_roi(image)
                roi, lungs_roi = extract_3d_roi(
                    image, predictor.fast_predict(image, skip_level=2)
                )
            except:
                print(
                    f"An error occured while computing the ROI in this image: ID={image_id}. Skipping..."
                )
                continue

            self.server.connect()
            posted_image_id = self.server.post_image_to_ds(
                roi, dataset_id, posted_image_name
            )
            self.server.tag_image_with_tag(posted_image_id, tag_id=OMERO_TAGS["roi"])

            image_tags_list = self.server.find_image_tag(
                self.server.get_image_tags(image_id)
            )
            self.server.copy_image_tags(
                src_image_id=image_id,
                dst_image_id=posted_image_id,
                exclude_tags=image_tags_list,
            )

            yield k + 1

    def _start_batch_roi(self):
        if self.roi_missing is None:
            return

        n_rois_to_compute = len(self.roi_missing)
        if n_rois_to_compute:
            worker = self._batch_roi(n_rois_to_compute)
            worker.returned.connect(self._reset_ui_and_project_state)
            worker.aborted.connect(self._reset_ui_and_project_state)
            worker.yielded.connect(lambda step: self.pbar.setValue(step))
            self.active_batch_workers.append(worker)
            self.pbar.setMaximum(n_rois_to_compute)
            self.pbar.setValue(0)
            self._grayout_ui()
            worker.start()
        else:
            print("No ROIs to compute.")

    ### Tracking
    @thread_worker
    def _threaded_download_timeseries(self, to_download_ids, specimen_name):
        self.server.connect()

        images = []
        for k, img_id in enumerate(to_download_ids):
            print(f"Downloading image ID = {img_id}")
            images.append(self.server.download_image(img_id))
            yield k + 1

        return (combine_images(images), specimen_name)

    def _trigger_download_timeseries_rois(self):
        specimen_name = self.cb_specimen.currentText()
        if specimen_name == "":
            return

        if len(self.roi_timeseries_ids) == 0:
            print("No data to download.")
            return

        worker = self._threaded_download_timeseries(
            self.roi_timeseries_ids, specimen_name
        )
        worker.returned.connect(self._timeseries_rois_download_returned)
        worker.yielded.connect(lambda step: self.pbar.setValue(step))
        worker.aborted.connect(self._ungrayout_ui)
        self.pbar.setMaximum(len(self.roi_timeseries_ids))
        self.active_batch_workers.append(worker)
        self._grayout_ui()
        worker.start()

    def _timeseries_rois_download_returned(self, payload):
        self._ungrayout_ui()
        timeseries, specimen_name = payload
        self.viewer.add_image(timeseries, name=f"{specimen_name}_rois")

    def _trigger_download_timeseries_labels(self):
        specimen_name = self.cb_specimen.currentText()
        if specimen_name == "":
            return

        if len(self.labels_timeseries_ids) == 0:
            print("No data to download.")
            return
        elif np.isnan(self.labels_timeseries_ids).any():
            show_error("Labels/Images mismatch!")
            print("IDs to download have NaNs! Run model predictions?")
            return

        worker = self._threaded_download_timeseries(
            self.labels_timeseries_ids, specimen_name
        )
        worker.returned.connect(self._timeseries_labels_download_returned)
        worker.yielded.connect(lambda step: self.pbar.setValue(step))
        worker.aborted.connect(self._ungrayout_ui)
        self.pbar.setMaximum(len(self.labels_timeseries_ids))
        self.active_batch_workers.append(worker)
        self._grayout_ui()
        worker.start()

    def _timeseries_labels_download_returned(self, payload):
        self._ungrayout_ui()
        timeseries, specimen_name = payload
        timeseries = timeseries.astype(np.uint16)
        self.viewer.add_labels(timeseries, name=f"{specimen_name}_labels")

    @thread_worker
    def _threaded_tracking(
        self, labels_timeseries, labels_timeseries_name, image_timeseries=None
    ):
        with_lungs_registration = image_timeseries is not None
        linkage_df, grouped_df, timeseries_corrected = run_tracking(
            labels_timeseries,
            image_timeseries,
            with_lungs_registration=with_lungs_registration,
            method="laptrack",
            max_dist_px=30,
            dist_weight_ratio=0.9,
            max_volume_diff_rel=1.0,
            memory=0,
        )

        return (labels_timeseries_name, timeseries_corrected, grouped_df)

    def _trigger_tracking(self):
        timeseries_name = self.cb_track_labels.currentText()
        if timeseries_name == "":
            print("No tumor series found.")
            return
        timeseries = self.cb_track_labels.currentData()

        image_timeseries = None
        if self.with_lungs_checkbox.isChecked():
            if self.cb_track_images.currentText() == "":
                show_info("No image series found.")
            else:
                image_timeseries = self.cb_track_images.currentData()

        worker = self._threaded_tracking(timeseries, timeseries_name, image_timeseries)
        worker.returned.connect(self._tracking_returned)
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    def _tracking_returned(self, payload):
        self._ungrayout_ui()
        timeseries_name, timeseries_corrected, grouped_df = payload
        self.grouped_df = grouped_df
        # Add layers to the viewer
        self.viewer.add_labels(
            timeseries_corrected, name=f"{timeseries_name}_tracked", opacity=1.0
        )
        self.viewer.layers[timeseries_name].visible = (
            False  # Turn off visibility of the untracked labels layer
        )

    def _save_track_csv(self):
        if self.grouped_df is None:
            show_info("No tracking data found.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save as CSV", ".", "*.csv")
        if not filename.endswith(".csv"):
            filename += ".csv"

        formatted_df = self.grouped_df.reset_index()[
            ["tumor", "scan", "volume", "label"]
        ]
        pivoted = formatted_df.pivot(
            index="tumor", columns="scan", values=["volume", "label"]
        ).reset_index()
        pivoted.columns = ["Tumor ID"] + [
            f"{i} - SCAN{scan_id:02d}" for (i, scan_id) in pivoted.columns[1:]
        ]

        volume_columns = [col for col in pivoted.columns if "volume" in col]
        label_columns = [col for col in pivoted.columns if "label" in col]

        # Fold change
        initial_volume_col = volume_columns[0]
        for k, volume_col in enumerate(volume_columns[1:]):
            pivoted[f"fold change - SCAN01 to SCAN{(k+2):02d}"] = (
                pivoted[volume_col] - pivoted[initial_volume_col]
            ) / pivoted[initial_volume_col]

        # Re-order the columns
        columns_order = ["Tumor ID"]
        for volume_col, label_col in zip(volume_columns, label_columns):
            columns_order.append(label_col)
            columns_order.append(volume_col)
        fold_change_columns = [col for col in pivoted.columns if "fold" in col]
        for fold_col in fold_change_columns:
            columns_order.append(fold_col)
        pivoted = pivoted[columns_order]

        pivoted.to_csv(filename)
        show_info(f"Saved {filename}.")

    # Others
    def _grayout_ui(self):
        for ui_element in self.grayout_ui_list:
            ui_element.setEnabled(False)

    def _ungrayout_ui(self, *args, **kwargs):
        for ui_element in self.grayout_ui_list:
            ui_element.setEnabled(True)
        # This should be in another function, but whatever..
        self.pbar.setMaximum(1)
        self.active_batch_workers.clear()

    def _handle_cancel(self):
        if len(self.active_batch_workers) == 0:
            print("Nothing to cancel.")

        for worker in self.active_batch_workers:
            show_info("Cancelling...")
            worker.quit()

    def _reset_ui_and_project_state(self):
        self._handle_project_changed(
            selected_project_name=self.cb_project.currentText()
        )
        self._ungrayout_ui()

    def _start_full_pipeline(self):
        """Experimental - running everything automatically for a specimen and saving the outputs to a local directory."""
        specimen = self.cb_specimen.currentText()
        if specimen == "":
            return

        dirname = QFileDialog.getExistingDirectory(self, "Output directory", ".")
        dirname = Path(dirname)
        print(dirname)

        worker = self._full_pipeline_thread(dirname, specimen)
        worker.returned.connect(self._full_pipeline_returned)
        self.pbar.setMaximum(0)
        self._grayout_ui()
        worker.start()

    @thread_worker
    def _full_pipeline_thread(self, dirname, specimen):
        to_download_image_timeseries_ids = image_timeseries_ids(self.df, specimen)
        images = [
            self.server.download_image(img_id)
            for img_id in to_download_image_timeseries_ids
        ]
        for k, image in enumerate(images):
            tifffile.imwrite(str(dirname / f"SCAN{k:02d}.tif"), image)

        predictor = LungsPredictor()

        # model = list(MODELS.keys())[0]
        model = self.cb_models.currentData()
        if model is None:
            print("Could not select a model for prediction.")
            return

        rois = []
        lungs_rois = []
        tumors_rois = []
        for k, image in enumerate(images):
            roi, lungs_roi = extract_3d_roi(
                image, predictor.fast_predict(image, skip_level=2)
            )

            tumors_mask = predict(roi, model)
            tumors_mask = postprocess(tumors_mask)

            rois.append(roi)
            lungs_rois.append(lungs_roi)
            tumors_rois.append(tumors_mask)

        rois_timeseries = combine_images(rois)
        lungs_timeseries = combine_images(lungs_rois)
        tumor_timeseries = combine_images(tumors_rois)

        tumor_timeseries = tumor_timeseries.astype(int)
        lungs_timeseries = lungs_timeseries.astype(int)

        tifffile.imwrite(str(dirname / "rois_timeseries.tif"), rois_timeseries)
        tifffile.imwrite(str(dirname / "lungs_timeseries.tif"), lungs_timeseries)
        tifffile.imwrite(str(dirname / "tumor_timeseries.tif"), tumor_timeseries)

        linkage_df, grouped_df, tumor_timeseries_corrected = run_tracking(
            tumor_timeseries,
            rois_timeseries,
            lungs_timeseries,
            with_lungs_registration=True,
            method="laptrack",
            max_dist_px=30,
            dist_weight_ratio=0.9,
            max_volume_diff_rel=1.0,
            memory=0,
        )

        tifffile.imwrite(
            str(dirname / "tumor_timeseries_corrected.tif"), tumor_timeseries_corrected
        )

        formatted_df = grouped_df.reset_index()[["tumor", "scan", "volume", "label"]]
        pivoted = formatted_df.pivot(
            index="tumor", columns="scan", values=["volume", "label"]
        ).reset_index()
        pivoted.columns = ["Tumor ID"] + [
            f"{i} - SCAN{scan_id:02d}" for (i, scan_id) in pivoted.columns[1:]
        ]

        volume_columns = [col for col in pivoted.columns if "volume" in col]
        label_columns = [col for col in pivoted.columns if "label" in col]

        # Fold change
        initial_volume_col = volume_columns[0]
        for k, volume_col in enumerate(volume_columns[1:]):
            pivoted[f"fold change - SCAN01 to SCAN{(k+2):02d}"] = (
                pivoted[volume_col] - pivoted[initial_volume_col]
            ) / pivoted[initial_volume_col]

        # Re-order the columns
        columns_order = ["Tumor ID"]
        for volume_col, label_col in zip(volume_columns, label_columns):
            columns_order.append(label_col)
            columns_order.append(volume_col)
        fold_change_columns = [col for col in pivoted.columns if "fold" in col]
        for fold_col in fold_change_columns:
            columns_order.append(fold_col)
        pivoted = pivoted[columns_order]

        pivoted.to_csv(str(dirname / f"{specimen}_results.csv"))

        return (
            rois_timeseries,
            lungs_timeseries,
            tumor_timeseries,
            tumor_timeseries_corrected,
        )

    def _full_pipeline_returned(self, payload):
        (
            rois_timeseries,
            lungs_timeseries,
            tumor_timeseries,
            tumor_timeseries_corrected,
        ) = payload
        self.viewer.add_image(rois_timeseries)
        lungs_layer = self.viewer.add_labels(lungs_timeseries)
        lungs_layer.visible = False
        tumor_layer = self.viewer.add_labels(tumor_timeseries)
        tumor_layer.visible = False
        self.viewer.add_labels(tumor_timeseries_corrected)
        self._ungrayout_ui()
        show_info("Finished!")
