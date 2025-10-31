import pytest
import math
from PIL import Image
from utils.helpers import calculate_angle_between_points, tint_image, load_image, key_mapping
import arcade

def test_calculate_angle_between_points():
    # Test horizontal line
    assert calculate_angle_between_points((0, 0), (10, 0)) == 0
    # Test vertical line
    assert calculate_angle_between_points((0, 0), (0, 10)) == math.pi / 2
    # Test 45-degree line
    assert calculate_angle_between_points((0, 0), (10, 10)) == pytest.approx(math.pi / 4)
    # Test another angle
    assert calculate_angle_between_points((0, 0), (-10, 10)) == pytest.approx(3 * math.pi / 4)

def test_key_mapping():
    assert key_mapping[arcade.key.A] == "a"
    assert key_mapping[arcade.key.Z] == "z"
    assert key_mapping[arcade.key.SPACE] == " "
    assert key_mapping[arcade.key.PERIOD] == "."

def test_tint_image():
    # Create a dummy image
    img = Image.new('RGBA', (100, 100), color = 'white')
    # Tint it blue
    tinted_img = tint_image(img, (0, 0, 255))
    # Check that the image is now blue
    # We check a single pixel, e.g., at (50, 50)
    pixel = tinted_img.getpixel((50, 50))
    assert pixel[2] == 255 # Blue channel should be max
    assert pixel[0] == 0 and pixel[1] == 0 # Red and Green should be 0

def test_load_image():
    # Test loading, inverting, and tinting
    img = load_image('tests/temp_assets/test_image.png', invert=True, tint_color=(0, 255, 0))
    # Original was red (255, 0, 0). Inverted is cyan (0, 255, 255). Tinted with green (0, 255, 0)
    # The tint is multiplicative, so the result should be green.
    pixel = img.getpixel((50, 50))
    assert pixel[1] == 255
    assert pixel[0] == 0 and pixel[2] == 0
