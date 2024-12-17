import pytest
from mkdocs_drawio_converter.plugin import DrawioConverterPlugin

def test_plugin_initialization():
    plugin = DrawioConverterPlugin()
    assert plugin is not None