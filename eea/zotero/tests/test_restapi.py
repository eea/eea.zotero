"""Tests for ZoteroGet REST API endpoint."""

import unittest
from unittest.mock import patch, MagicMock

from eea.zotero.restapi.get import ZoteroGet
from eea.zotero.interfaces import IZoteroClientSettings


class TestZoteroGetReply(unittest.TestCase):
    """Test ZoteroGet.reply()."""

    # Mock data based on volto-slate-zotero cypress fixtures
    MOCK_REGISTRY = {
        "server": "https://api.zotero.org/users/6732",
        "password": "test",
        "default": "NH578GBA",
        "style": "https://www.eea.europa.eu/zotero/eea.csl",
    }

    def setUp(self):
        """Create ZoteroGet instance without full Plone init."""
        self.service = ZoteroGet.__new__(ZoteroGet)
        self.service.context = MagicMock()
        self.service.request = MagicMock()
        self.service.request._rest_cors_preflight = False

    @patch("eea.zotero.restapi.get.api.portal.get_registry_record")
    def test_reply_returns_dict_with_all_keys(self, mock_registry):
        """Test that reply returns dict with server, password, default, style."""
        mock_registry.side_effect = (
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(name, default)
        )
        result = self.service.reply()
        self.assertIsInstance(result, dict)
        self.assertIn("server", result)
        self.assertIn("password", result)
        self.assertIn("default", result)
        self.assertIn("style", result)

    @patch("eea.zotero.restapi.get.api.portal.get_registry_record")
    def test_reply_returns_correct_values(self, mock_registry):
        """Test that reply returns correct values from registry."""
        mock_registry.side_effect = (
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(name, default)
        )
        result = self.service.reply()
        self.assertEqual(result["server"], "https://api.zotero.org/users/6732")
        self.assertEqual(result["password"], "test")
        self.assertEqual(result["default"], "NH578GBA")
        self.assertEqual(result["style"], "https://www.eea.europa.eu/zotero/eea.csl")

    @patch("eea.zotero.restapi.get.api.portal.get_registry_record")
    def test_reply_uses_izoterosettings_interface(self, mock_registry):
        """Test that reply queries registry with IZoteroClientSettings interface."""
        mock_registry.side_effect = (
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(name, default)
        )
        self.service.reply()
        for call in mock_registry.call_args_list:
            args, kwargs = call
            # interface should be IZoteroClientSettings (positional or kwarg)
            iface = kwargs.get("interface") or (args[1] if len(args) > 1 else None)
            self.assertEqual(iface, IZoteroClientSettings)

    @patch("eea.zotero.restapi.get.api.portal.get_registry_record")
    def test_reply_with_empty_registry(self, mock_registry):
        """Test reply with empty registry returns empty strings."""
        mock_registry.side_effect = (
            lambda name, interface=None, default=None: default or ""
        )
        result = self.service.reply()
        self.assertEqual(result["server"], "")
        self.assertEqual(result["password"], "")
        self.assertEqual(result["default"], "")
        self.assertEqual(result["style"], "")

    @patch("eea.zotero.restapi.get.api.portal.get_registry_record")
    def test_reply_calls_registry_four_times(self, mock_registry):
        """Test that reply calls get_registry_record exactly 4 times."""
        mock_registry.side_effect = (
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(name, default)
        )
        self.service.reply()
        self.assertEqual(mock_registry.call_count, 4)


class TestZoteroInterfaces(unittest.TestCase):
    """Test IZoteroClientSettings interface fields."""

    def test_interface_has_server_field(self):
        """Test that server field exists."""
        self.assertIn("server", list(IZoteroClientSettings.names()))

    def test_interface_has_password_field(self):
        """Test that password field exists."""
        self.assertIn("password", list(IZoteroClientSettings.names()))

    def test_interface_has_default_field(self):
        """Test that default field exists."""
        self.assertIn("default", list(IZoteroClientSettings.names()))

    def test_interface_has_style_field(self):
        """Test that style field exists."""
        self.assertIn("style", list(IZoteroClientSettings.names()))

    def test_server_default_value(self):
        """Test server field default."""
        self.assertEqual(
            IZoteroClientSettings["server"].default,
            "https://api.zotero.org/users/12345",
        )

    def test_style_default_value(self):
        """Test style field default."""
        self.assertEqual(
            IZoteroClientSettings["style"].default,
            "https://www.eea.europa.eu/zotero/eea.csl",
        )

    def test_password_default_empty(self):
        """Test password field default is empty."""
        self.assertEqual(IZoteroClientSettings["password"].default, "")

    def test_default_field_default_empty(self):
        """Test default field default is empty."""
        self.assertEqual(IZoteroClientSettings["default"].default, "")


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)