import pytest
from unittest.mock import MagicMock
import arcade
from utils.menu_view import MenuView

@pytest.fixture
def menu_view(mocker):
    """Fixture to create a MenuView instance with extensive mocking."""
    mock_window = MagicMock()
    mock_window.width = 800
    mock_window.height = 600
    mocker.patch('arcade.get_window', return_value=mock_window)

    # Mock arcade.Text to prevent it from trying to initialize fonts and graphics
    mocker.patch('arcade.Text')
    mocker.patch('utils.menu_view.Batch')
    mocker.patch('utils.menu_view.UIManager')
    mocker.patch('utils.menu_view.UIAnchorLayout')
    mocker.patch('utils.menu_view.UIBoxLayout')

    view = MenuView("Test Title", "Test Subtitle")
    view.window = mock_window
    return view

def test_create_button(mocker):
    """Test that the create_button class method returns a UIFlatButton."""
    mocker.patch('arcade.get_window', return_value=MagicMock())

    # Mock UILabel where it's instantiated to prevent rendering errors.
    # Configure the mock to have a `text` attribute for the assertion.
    mock_label_instance = MagicMock()
    mock_label_instance.text = "Test Button"
    mocker.patch('arcade.gui.widgets.text.UILabel', return_value=mock_label_instance)

    button = MenuView.create_button("Test Button")
    assert isinstance(button, arcade.gui.UIFlatButton)
    assert button.text == "Test Button"

def test_return_to_previous_view(menu_view):
    """Test that the return_to_previous_view method shows the previous view."""
    previous_view = MagicMock()
    menu_view.previous_view = previous_view
    menu_view.return_to_previous_view()
    menu_view.window.show_view.assert_called_once_with(previous_view)

def test_on_key_press_escape(menu_view):
    """Test that pressing the escape key returns to the previous view."""
    menu_view.return_to_previous_view = MagicMock()
    menu_view.on_key_press(arcade.key.ESCAPE, 0)
    menu_view.return_to_previous_view.assert_called_once()
