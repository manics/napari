import numpy as np
from xml.etree.ElementTree import Element

import pytest
from vispy.color import Colormap
from napari.layers import Image


def test_random_image():
    """Test instantiating Image layer with random 2D data."""
    shape = (10, 15)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.dims.range == [(0, m, 1) for m in shape]
    assert layer.rgb == False
    assert layer.is_pyramid == False
    assert layer._data_pyramid == None
    assert layer._data_view.shape == shape[-2:]


def test_negative_image():
    """Test instantiating Image layer with negative data."""
    shape = (10, 15)
    np.random.seed(0)
    # Data between -1.0 and 1.0
    data = 2 * np.random.random(shape) - 1.0
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.dims.range == [(0, m, 1) for m in shape]
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]

    # Data between -10 and 10
    data = 20 * np.random.random(shape) - 10
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.dims.range == [(0, m, 1) for m in shape]
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_all_zeros_image():
    """Test instantiating Image layer with all zeros data."""
    shape = (10, 15)
    data = np.zeros(shape, dtype=float)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_integer_image():
    """Test instantiating Image layer with integer data."""
    shape = (10, 15)
    np.random.seed(0)
    data = np.round(10 * np.random.random(shape)).astype(int)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_bool_image():
    """Test instantiating Image layer with bool data."""
    shape = (10, 15)
    data = np.zeros(shape, dtype=bool)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_3D_image():
    """Test instantiating Image layer with random 3D data."""
    shape = (10, 15, 6)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_3D_image_shape_1():
    """Test instantiating Image layer with random 3D data with shape 1 axis."""
    shape = (1, 10, 15)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_4D_image():
    """Test instantiating Image layer with random 4D data."""
    shape = (10, 15, 6, 8)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_5D_image_shape_1():
    """Test instantiating Image layer with random 5D data with shape 1 axis."""
    shape = (4, 1, 2, 10, 15)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_rgb_image():
    """Test instantiating Image layer with RGB data."""
    shape = (10, 15, 3)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape) - 1
    assert layer.shape == shape[:-1]
    assert layer.rgb == True
    assert layer._data_view.shape == shape[-3:]


def test_rgba_image():
    """Test instantiating Image layer with RGBA data."""
    shape = (10, 15, 4)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape) - 1
    assert layer.shape == shape[:-1]
    assert layer.rgb == True
    assert layer._data_view.shape == shape[-3:]


def test_negative_rgba_image():
    """Test instantiating Image layer with negative RGBA data."""
    shape = (10, 15, 4)
    np.random.seed(0)
    # Data between -1.0 and 1.0
    data = 2 * np.random.random(shape) - 1
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape) - 1
    assert layer.shape == shape[:-1]
    assert layer.rgb == True
    assert layer._data_view.shape == shape[-3:]

    # Data between -10 and 10
    data = 20 * np.random.random(shape) - 10
    layer = Image(data)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape) - 1
    assert layer.shape == shape[:-1]
    assert layer.rgb == True
    assert layer._data_view.shape == shape[-3:]


def test_non_rgb_image():
    """Test forcing Image layer to be 3D and not rgb."""
    shape = (10, 15, 3)
    np.random.seed(0)
    data = np.random.random(shape)
    layer = Image(data, rgb=False)
    assert np.all(layer.data == data)
    assert layer.ndim == len(shape)
    assert layer.shape == shape
    assert layer.rgb == False
    assert layer._data_view.shape == shape[-2:]


def test_error_non_rgb_image():
    """Test error on trying non rgb as rgb."""
    # If rgb is set to be True in constructor but the last dim has a
    # size > 4 then data cannot actually be rgb
    shape = (10, 15, 6)
    np.random.seed(0)
    data = np.random.random(shape)
    with pytest.raises(ValueError):
        layer = Image(data, rgb=True)


def test_changing_image():
    """Test changing Image data."""
    shape_a = (10, 15)
    shape_b = (20, 12)
    np.random.seed(0)
    data_a = np.random.random(shape_a)
    data_b = np.random.random(shape_b)
    layer = Image(data_a)
    layer.data = data_b
    assert np.all(layer.data == data_b)
    assert layer.ndim == len(shape_b)
    assert layer.shape == shape_b
    assert layer.dims.range == [(0, m, 1) for m in shape_b]
    assert layer.rgb == False
    assert layer._data_view.shape == shape_b[-2:]


def test_changing_image_dims():
    """Test changing Image data including dimensionality."""
    shape_a = (10, 15)
    shape_b = (20, 12, 6)
    np.random.seed(0)
    data_a = np.random.random(shape_a)
    data_b = np.random.random(shape_b)
    layer = Image(data_a)

    # Prep indices for switch to 3D
    layer.data = data_b
    assert np.all(layer.data == data_b)
    assert layer.ndim == len(shape_b)
    assert layer.shape == shape_b
    assert layer.dims.range == [(0, m, 1) for m in shape_b]
    assert layer.rgb == False
    assert layer._data_view.shape == shape_b[-2:]


def test_name():
    """Test setting layer name."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.name == 'Image'

    layer = Image(data, name='random')
    assert layer.name == 'random'

    layer.name = 'img'
    assert layer.name == 'img'


def test_visiblity():
    """Test setting layer visiblity."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.visible == True

    layer.visible = False
    assert layer.visible == False

    layer = Image(data, visible=False)
    assert layer.visible == False

    layer.visible = True
    assert layer.visible == True


def test_opacity():
    """Test setting layer opacity."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.opacity == 1

    layer.opacity = 0.5
    assert layer.opacity == 0.5

    layer = Image(data, opacity=0.6)
    assert layer.opacity == 0.6

    layer.opacity = 0.3
    assert layer.opacity == 0.3


def test_blending():
    """Test setting layer blending."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.blending == 'translucent'

    layer.blending = 'additive'
    assert layer.blending == 'additive'

    layer = Image(data, blending='additive')
    assert layer.blending == 'additive'

    layer.blending = 'opaque'
    assert layer.blending == 'opaque'


def test_interpolation():
    """Test setting image interpolation mode."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.interpolation == 'nearest'

    layer = Image(data, interpolation='bicubic')
    assert layer.interpolation == 'bicubic'

    layer.interpolation = 'bilinear'
    assert layer.interpolation == 'bilinear'


def test_colormaps():
    """Test setting test_colormaps."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.colormap[0] == 'gray'
    assert type(layer.colormap[1]) == Colormap

    layer.colormap = 'magma'
    assert layer.colormap[0] == 'magma'
    assert type(layer.colormap[1]) == Colormap

    cmap = Colormap([[0.0, 0.0, 0.0, 0.0], [0.3, 0.7, 0.2, 1.0]])
    layer.colormap = 'custom', cmap
    assert layer.colormap[0] == 'custom'
    assert layer.colormap[1] == cmap

    cmap = Colormap([[0.0, 0.0, 0.0, 0.0], [0.7, 0.2, 0.6, 1.0]])
    layer.colormap = {'new': cmap}
    assert layer.colormap[0] == 'new'
    assert layer.colormap[1] == cmap

    layer = Image(data, colormap='magma')
    assert layer.colormap[0] == 'magma'
    assert type(layer.colormap[1]) == Colormap

    cmap = Colormap([[0.0, 0.0, 0.0, 0.0], [0.3, 0.7, 0.2, 1.0]])
    layer = Image(data, colormap=('custom', cmap))
    assert layer.colormap[0] == 'custom'
    assert layer.colormap[1] == cmap

    cmap = Colormap([[0.0, 0.0, 0.0, 0.0], [0.7, 0.2, 0.6, 1.0]])
    layer = Image(data, colormap={'new': cmap})
    assert layer.colormap[0] == 'new'
    assert layer.colormap[1] == cmap


def test_contrast_limits():
    """Test setting color limits."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.contrast_limits[0] >= 0
    assert layer.contrast_limits[1] <= 1
    assert layer.contrast_limits[0] < layer.contrast_limits[1]
    assert layer.contrast_limits == layer._contrast_limits_range

    # Change contrast_limits property
    contrast_limits = [0, 2]
    layer.contrast_limits = contrast_limits
    assert layer.contrast_limits == contrast_limits
    assert layer._contrast_limits_range == contrast_limits

    # Set contrast_limits as keyword argument
    layer = Image(data, contrast_limits=contrast_limits)
    assert layer.contrast_limits == contrast_limits
    assert layer._contrast_limits_range == contrast_limits


def test_contrast_limits_range():
    """Test setting color limits range."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer._contrast_limits_range[0] >= 0
    assert layer._contrast_limits_range[1] <= 1
    assert layer._contrast_limits_range[0] < layer._contrast_limits_range[1]

    # If all data is the same value the contrast_limits_range and contrast_limits defaults to [0, 1]
    data = np.zeros((10, 15))
    layer = Image(data)
    assert layer._contrast_limits_range == [0, 1]
    assert layer.contrast_limits == [0.0, 1.0]


def test_gamma():
    """Test setting gamma."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.gamma == 1

    # Change gamma property
    gamma = 0.7
    layer.gamma = gamma
    assert layer.gamma == gamma

    # Set gamma as keyword argument
    layer = Image(data, gamma=gamma)
    assert layer.gamma == gamma


def test_metadata():
    """Test setting image metadata."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    assert layer.metadata == {}

    layer = Image(data, metadata={'unit': 'cm'})
    assert layer.metadata == {'unit': 'cm'}


def test_value():
    """Test getting the value of the data at the current coordinates."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    value = layer.get_value()
    assert layer.coordinates == (0, 0)
    assert value == data[0, 0]


def test_message():
    """Test converting value and coords to message."""
    np.random.seed(0)
    data = np.random.random((10, 15))
    layer = Image(data)
    msg = layer.get_message()
    assert type(msg) == str


def test_thumbnail():
    """Test the image thumbnail for square data."""
    np.random.seed(0)
    data = np.random.random((30, 30))
    layer = Image(data)
    layer._update_thumbnail()
    assert layer.thumbnail.shape == layer._thumbnail_shape


def test_xml_list():
    """Test the xml generation."""
    np.random.seed(0)
    data = np.random.random((15, 30))
    layer = Image(data)
    xml = layer.to_xml_list()
    assert type(xml) == list
    assert len(xml) == 1
    assert type(xml[0]) == Element


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
def test_out_of_range_image(dtype):
    data = -1.7 - 0.001 * np.random.random((10, 15)).astype(dtype)
    layer = Image(data)
    layer._update_thumbnail()


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
def test_out_of_range_no_contrast(dtype):
    data = np.full((10, 15), -3.2, dtype=dtype)
    layer = Image(data)
    layer._update_thumbnail()
