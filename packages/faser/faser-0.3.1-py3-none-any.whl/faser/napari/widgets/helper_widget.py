import itertools
import os
import typing
from enum import Enum
from typing import Any, Callable, Type

import dask
import dask.array as da
import napari
import numpy as np
import pydantic
import tifffile
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from qtpy import QtGui, QtWidgets
from scipy import ndimage
from scipy import signal    
from slugify import slugify
from superqt import (
    QDoubleRangeSlider,
    QEnumComboBox,
    QLabeledDoubleRangeSlider,
    QLabeledDoubleSlider,
)
from superqt.utils import thread_worker

import skimage.draw as draw
from faser.env import get_asset_file
from faser.generators.base import AberrationFloat, PSFConfig
from faser.generators.vectorial.stephane.tilted_coverslip import generate_psf
from faser.napari.widgets.fields import generate_single_widgets_from_model


class HelperTab(QtWidgets.QWidget):
    def __init__(
        self,
        viewer: napari.Viewer,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.mylayout = QtWidgets.QVBoxLayout()
        self.mylayout.setContentsMargins(0, 0, 0, 0)
        self.mylayout.setSpacing(1)
        self.setLayout(self.mylayout)


# Step 1: Create a worker class
class ExportWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self, layers, export_dir):
        super().__init__()
        self.layers = layers
        self.export_dir = export_dir

    def export_layer_with_config_data_to_file(
        self, data, export_dir, layer_name, config
    ):
        export_file_dir = os.path.join(export_dir, slugify(layer_name))
        # export_file_dir = os.path.join(export_dir, "test")
        os.makedirs(export_file_dir, exist_ok=True)
        with open(
            os.path.join(export_file_dir, "config.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(config.json())

        tifffile.imsave(os.path.join(export_file_dir, "psf.tif"), data)
        print("Exported")

    def run(self):
        """Long-running task."""
        print("Running")
        for layer in self.layers:
            if layer.metadata.get("is_psf", False) is True:
                if layer.metadata.get("is_batch", False) is True:
                    first_dim = layer.data.shape[0]
                    for i in range(first_dim):

                        self.progress.emit(i + 1)
                        self.export_layer_with_config_data_to_file(
                            layer.data[i, :, :, :],
                            self.export_dir,
                            layer.name,
                            layer.metadata["configs"][i],
                        )
                else:
                    print("Exporting this one")
                    self.export_layer_with_config_data_to_file(
                        layer.data,
                        self.export_dir,
                        layer.name,
                        layer.metadata["config"],
                    )

        self.finished.emit()


@thread_worker
def export_layer_with_config_data_to_file(data, export_dir, layer_name, config):
    export_file_dir = os.path.join(export_dir, "test")
    os.makedirs(export_file_dir, exist_ok=True)
    with open(os.path.join(export_file_dir, "config.txt"), "w", encoding="utf-8") as f:
        f.write(config.json())

    tifffile.imsave(os.path.join(export_file_dir, "psf.tif"), data)
    print("Exported")


class ExportTab(HelperTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show = QtWidgets.QPushButton("Select PSF Layers")
        self.show.setEnabled(False)
        self.show.clicked.connect(self.export_pressed)
        self.mylayout.addStretch()

        self.viewer.layers.selection.events.connect(self.update_selection)

        self.mylayout.addWidget(self.show)

    def on_worker_done(self):
        print("done")
        self.show.setEnabled(True)

    def on_worker_progress(self, value):
        print(value)

    def update_selection(self, event):
        selection = self.viewer.layers.selection

        if not selection:
            self.show.setEnabled(False)
            self.show.setText("Select PSF")

        else:
            layers = [
                layer for layer in selection if layer.metadata.get("is_psf", False)
            ]
            if len(layers) == 0:
                self.show.setEnabled(False)
                self.show.setText("Select PSF Layers")

            else:
                self.show.setEnabled(True)
                self.show.setText("Export PSF" if len(layers) == 1 else "Export PSFs")

        print(self.viewer.layers.selection.active)

    def export_layer_with_config_data_to_file(data, export_dir, layer_name, config):
        export_file_dir = os.path.join(export_dir, layer_name)
        os.makedirs(export_file_dir, exist_ok=True)
        with open(
            os.path.join(export_file_dir, "config.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(config.json())

        tifffile.imsave(os.path.join(export_file_dir, "psf.tif"), data)
        print("Exported")

    def export_active_selection(self, export_dir):
        layers = []
        for layer in self.viewer.layers.selection:
            if layer.metadata.get("is_psf", False) == True:
                layers.append(layer)

        self.thread = QtCore.QThread()
        self.worker = ExportWorker(layers, export_dir)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.on_worker_progress)
        self.thread.start()

    def export_pressed(self):
        export_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory"
        )

        if export_dir:
            self.export_active_selection(export_dir=export_dir)


class SpaceModel(pydantic.BaseModel):
    x_size: int = 1000
    y_size: int = 1000
    z_size: int = 10
    dots: int = 50


class SampleTab(HelperTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_space = QtWidgets.QPushButton("Space")
        self.create_space.clicked.connect(self.generate_space)

        self.create_lines = QtWidgets.QPushButton("Grid")
        self.create_lines.clicked.connect(self.generate_lines)


        self.create_circles = QtWidgets.QPushButton("Circles")
        self.create_circles.clicked.connect(self.generate_circles)




        self.managed_widgets = generate_single_widgets_from_model(
            SpaceModel,
            callback=self.callback,
            range_callback=None,
            parent=self,
        )

        print(self.managed_widgets)

        for widget in self.managed_widgets:
            widget.init_ui_helper()
            self.mylayout.addWidget(widget)

        self.mylayout.addStretch()

        self.mylayout.addWidget(self.create_space)
        self.mylayout.addWidget(self.create_lines)
        self.mylayout.addWidget(self.create_circles)
        self.space_model = SpaceModel()

    def callback(self, name, value):
        split = name.split(".")
        if len(split) > 1:
            self.space_model.__getattribute__(split[0]).__setattr__(split[1], value)
        else:
            self.space_model.__setattr__(name, value)

    def show_wavefront(self):
        raise NotImplementedError()

    def generate_space(self):
        x = np.random.randint(0, self.space_model.x_size, size=(self.space_model.dots))
        y = np.random.randint(0, self.space_model.y_size, size=(self.space_model.dots))
        z = np.random.randint(0, self.space_model.z_size, size=(self.space_model.dots))

        M = np.zeros(
            (
                self.space_model.z_size,
                self.space_model.y_size,
                self.space_model.y_size,
            )
        )
        for p in zip(z, x, y):
            M[p] = 1

        self.viewer.add_image(M, name="Space")


    def generate_lines(self):
        x = np.linspace(0, self.space_model.x_size - 1, num=int(self.space_model.x_size / self.space_model.dots))
        y = np.linspace(0, self.space_model.y_size - 1, num=int(self.space_model.y_size / self.space_model.dots))
        z = np.linspace(0, self.space_model.z_size - 1, num=int(self.space_model.z_size / self.space_model.dots))

        M = np.zeros(
            (
            self.space_model.z_size,
            self.space_model.y_size,
            self.space_model.x_size,
            )
        )

        for xi in x:
            M[:, :, int(xi)] = 1  # Draw lines along z-axis

        for yi in y:
            M[:, int(yi), :] = 1

        for zi in z:
            M[int(zi), :, :] = 1

        self.viewer.add_image(M, name="3D Grid")

    def generate_circles(self):
        center_x = self.space_model.x_size // 2
        center_y = self.space_model.y_size // 2

        M = np.zeros(
            (
                self.space_model.x_size,
                self.space_model.y_size,
            )
        )

        for radius in range(self.space_model.dots, min(self.space_model.x_size, self.space_model.y_size) // 2, self.space_model.dots):
            rr, cc = draw.circle_perimeter(center_y, center_x, radius)
            valid = (rr >= 0) & (rr < self.space_model.y_size) & (cc >= 0) & (cc < self.space_model.x_size)
            M[rr[valid], cc[valid]] = 1

        self.viewer.add_image(M, name="Concentric Circles")

        

class EffectiveModel(pydantic.BaseModel):
    Isat: float = pydantic.Field(default=0.1, lt=1, gt=0)


class EffectiveTab(HelperTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.managed_widgets = generate_single_widgets_from_model(
            EffectiveModel,
            callback=self.callback,
            range_callback=None,
            parent=self,
        )

        print(self.managed_widgets)

        for widget in self.managed_widgets:
            widget.init_ui_helper_eff()
            self.mylayout.addWidget(widget)

        self.label = QtWidgets.QLabel("Make Effective PSF")
        self.show = QtWidgets.QPushButton("Select exactly 2 PSFs")
        self.show.setEnabled(False)
        self.show.clicked.connect(self.make_effective_psf)

        self.show_alternate = QtWidgets.QPushButton("Select exactly 2 PSFs")
        self.show_alternate.setEnabled(False)
        self.show_alternate.clicked.connect(self.make_effective_psf_alternate)

        self.calculate_zero_intensity = QtWidgets.QPushButton("Calculate Zero Intensity")
        self.calculate_zero_intensity.clicked.connect(self.calculate_zerointensity)


        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.show)
        hlayout.addWidget(self.show_alternate)
        hlayout.addWidget(self.calculate_zero_intensity)

        # self.mylayout.addStretch()
        self.mylayout.addWidget(self.label)
        self.mylayout.addStretch()
        self.mylayout.addLayout(hlayout)

        self.effective_model = EffectiveModel()

        self.viewer.layers.selection.events.connect(self.update_selection)

    def callback(self, name, value):
        split = name.split(".")
        if len(split) > 1:
            self.effective_model.__getattribute__(split[0]).__setattr__(split[1], value)
        else:
            self.effective_model.__setattr__(name, value)

    def calculate_zerointensity(self):
        psf_layers = list(
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("is_psf", True)
        )

        assert len(psf_layers) == 1, "Select exactly one PSF"

        combined_psf = psf_layers[0]

        configs = combined_psf.metadata.get("is_combination_of", None)
        assert configs is not None, "Select a combined PSF"

        
        non_gaussian_psf = next(
            config for config in configs if config.Mode != "GAUSSIAN"
        )

        non_gaussian_but_gaussian = PSFConfig(**non_gaussian_psf.dict())
        non_gaussian_but_gaussian.Mode = "GAUSSIAN"

        psf = generate_psf(non_gaussian_but_gaussian)
        print(psf)

        arg_max_pos = np.unravel_index(np.argmax(psf), psf.shape)
        print(arg_max_pos)

        zero_intensity = combined_psf.data[arg_max_pos]

        features = {}

        self.viewer.add_points([arg_max_pos], name="Zero Intensity", size=1, face_color="red", text = {
            'string': 'Intensity: ' + str(zero_intensity),
            'size': 13,
        }, features=features)





    def make_effective_psf(self):
        I_sat = self.effective_model.Isat
        psf_layers = list(
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("is_psf", True)
        )

        assert len(psf_layers) == 2, "Select exactly 2 PSFs"

        psf_layer_one = psf_layers[0]  # Excitation PSF
        psf_layer_two = psf_layers[1]  # Depletion PSF
        new_psf = np.multiply(psf_layer_one.data, np.exp(-psf_layer_two.data / I_sat))

        return self.viewer.add_image(
            new_psf,
            name=f"Combined PSF {psf_layer_one.name} {psf_layer_two.name}",
            metadata={"is_psf": True, "is_combination_of": [psf_layer_one.metadata.get("config"), psf_layer_one.metadata.get("config")]},
            colormap="viridis",
        )

    def make_effective_psf_alternate(self):
        I_sat = self.effective_model.Isat
        psf_layers = list(
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("is_psf", True)
        )

        assert len(psf_layers) == 2, "Select exactly 2 PSFs"

        psf_layer_one = psf_layers[1]  # Excitation PSF
        psf_layer_two = psf_layers[0]  # Depletion PSF
        new_psf = np.multiply(psf_layer_one.data, np.exp(-psf_layer_two.data / I_sat))

        return self.viewer.add_image(
            new_psf,
            name=f"Combined PSF {psf_layer_one.name} {psf_layer_two.name}",
            metadata={"is_psf": True},
            colormap="viridis",
        )

    def update_selection(self, event):
        selection = self.viewer.layers.selection

        if not selection:
            self.show.setEnabled(False)
            self.show.setText("Select 2 PSFs")
            self.show_alternate.setEnabled(False)
            self.show_alternate.setText("Select 2 PSFs")

        psf_layers = list(
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("is_psf", True)
        )

        if len(psf_layers) != 2:
            self.show.setEnabled(False)
            self.show.setText("Select 2 PSFs")
            self.show_alternate.setEnabled(False)
            self.show_alternate.setText("Select 2 PSFs")
            return

        layer_one = psf_layers[0]
        layer_two = psf_layers[1]

        self.show.setText(f"{layer_one.name} -> {layer_two.name}")
        self.show_alternate.setText(f"{layer_two.name} -> {layer_one.name}")
        self.show.setEnabled(True)
        self.show_alternate.setEnabled(True)


class ConvolveModel(pydantic.BaseModel):
    pass


# Step 1: Create a worker class
class ConvolveWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, image_data, psf_data):
        super().__init__()
        self.image_data = image_data
        self.psf_data = psf_data

    def export_layer_with_config_data_to_file(
        self, data, export_dir, layer_name, config
    ):
        export_file_dir = os.path.join(export_dir, slugify(layer_name))
        os.makedirs(export_file_dir, exist_ok=True)
        with open(
            os.path.join(export_file_dir, "config.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(config.json())

        tifffile.imsave(os.path.join(export_file_dir, "psf.tif"), data)
        print("Exported")

    def run(self):
        """Long-running task."""
        if self.image_data.ndim == 2:
            psf_data = self.psf_data[self.psf_data.shape[0] // 2, :, :]

            con = signal.convolve(
                self.image_data, psf_data, mode="same", method="fft"
            )

            self.finished.emit(con)
            return

        con = signal.convolve(
            self.image_data, self.psf_data, mode="same", method="fft"
        )

        self.finished.emit(con)


class ConvolveTab(HelperTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.managed_widgets = generate_single_widgets_from_model(
            ConvolveModel,
            callback=self.callback,
            range_callback=None,
            parent=self,
        )

        print(self.managed_widgets)

        for widget in self.managed_widgets:
            widget.init_ui_helper()
            self.mylayout.addWidget(widget)

        self.show = QtWidgets.QPushButton("Select image and PSF")
        self.show.setEnabled(False)
        self.show.clicked.connect(self.convolve_psf)
        self.mylayout.addStretch()

        self.mylayout.addWidget(self.show)

        self.effective_model = EffectiveModel()

        self.viewer.layers.selection.events.connect(self.update_selection)

    def callback(self, name, value):
        split = name.split(".")
        if len(split) > 1:
            self.effective_model.__getattribute__(split[0]).__setattr__(split[1], value)
        else:
            self.effective_model.__setattr__(name, value)

    def on_worker_done(self, con: np.array):
        self.show.setText("Select image and PSF")
        return self.viewer.add_image(
            con.squeeze(),
            name=f"Convoled Image",
        )

    def on_worker_progress(self, value):
        print(value)

    def convolve_psf(self):
        print("Convolve PSF and image")
        psf_layer = next(
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("is_psf", False)
        )
        image_layer = next(
            layer
            for layer in self.viewer.layers.selection
            if not layer.metadata.get("is_psf", False)
        )

        image_data = image_layer.data
        psf_data = psf_layer.data

        self.show.setText("Convolviing...")

        self.thread = QtCore.QThread()
        self.worker = ConvolveWorker(image_data, psf_data)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_worker_done)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.on_worker_progress)
        self.thread.start()

    def update_selection(self, event):
        selection = self.viewer.layers.selection

        if not selection:
            self.show.setEnabled(False)
            self.show.setText("Select a PSF and the Image")

        else:
            layers = [
                layer for layer in selection if layer.metadata.get("is_psf", False)
            ]
            if len(layers) != 1:
                self.show.setEnabled(False)
                self.show.setText("Select only one PSF ")

            else:
                self.show.setEnabled(True)
                self.show.setText("Convolve Image")


class InspectTab(HelperTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show = QtWidgets.QPushButton("Show Intensity")
        self.show.clicked.connect(self.show_wavefront)

        self.showp = QtWidgets.QPushButton("Show Phasemask")
        self.showp.clicked.connect(self.show_wavefront)

        self.viewer.layers.selection.events.connect(self.update_selection)

        self.mylayout.addWidget(self.show)
        self.mylayout.addWidget(self.showp)

    def update_selection(self, event):
        print(self.viewer.layers.selection.active)

    def show_wavefront(self):
        raise NotImplementedError()


class HelperWidget(QtWidgets.QWidget):
    def __init__(self, viewer: napari.Viewer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.viewer = viewer
        self.effective_tab = EffectiveTab(
            self.viewer,
        )
        self.sample_tab = SampleTab(
            self.viewer,
        )
        self.inspect_tab = InspectTab(
            self.viewer,
        )
        self.convolve_tab = ConvolveTab(
            self.viewer,
        )
        self.export_tab = ExportTab(
            self.viewer,
        )

        layout = QtWidgets.QGridLayout()
        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(self.effective_tab, "Effective")
        tabwidget.addTab(self.sample_tab, "Sample")
        # tabwidget.addTab(self.inspect_tab, "Inspect")
        tabwidget.addTab(self.convolve_tab, "Convolve")
        tabwidget.addTab(self.export_tab, "Export")
        layout.addWidget(tabwidget, 0, 0)

        self.setLayout(layout)
