"""Tests for ZoteroGet REST API endpoint, controlpanels, and package imports."""

import unittest
from unittest.mock import patch, MagicMock

from eea.zotero.restapi.get import ZoteroGet
from eea.zotero.interfaces import IZoteroClientSettings, IEeaZoteroLayer
from eea.zotero import EEAMessageFactory


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
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(
                name, default
            )
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
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(
                name, default
            )
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
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(
                name, default
            )
        )
        self.service.reply()
        for call in mock_registry.call_args_list:
            args, kwargs = call
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
            lambda name, interface=None, default=None: self.MOCK_REGISTRY.get(
                name, default
            )
        )
        self.service.reply()
        self.assertEqual(mock_registry.call_count, 4)


class TestZoteroRestapiControlpanel(unittest.TestCase):
    """Test ZoteroControlpanel REST API controlpanel."""

    def test_schema_is_izoterosettings(self):
        """Test that controlpanel schema is IZoteroClientSettings."""
        from eea.zotero.restapi.controlpanel import ZoteroControlpanel

        self.assertEqual(ZoteroControlpanel.schema, IZoteroClientSettings)

    def test_configlet_id(self):
        """Test that configlet_id is zotero."""
        from eea.zotero.restapi.controlpanel import ZoteroControlpanel

        self.assertEqual(ZoteroControlpanel.configlet_id, "zotero")

    def test_configlet_category_id(self):
        """Test that configlet_category_id is Products."""
        from eea.zotero.restapi.controlpanel import ZoteroControlpanel

        self.assertEqual(ZoteroControlpanel.configlet_category_id, "Products")

    def test_schema_prefix_is_none(self):
        """Test that schema_prefix is None."""
        from eea.zotero.restapi.controlpanel import ZoteroControlpanel

        self.assertIsNone(ZoteroControlpanel.schema_prefix)


class TestZoteroBrowserControlpanel(unittest.TestCase):
    """Test Zotero browser controlpanel."""

    def test_form_id(self):
        """Test that form id is zotero."""
        from eea.zotero.browser.controlpanel import ZoteroControlPanelForm

        self.assertEqual(ZoteroControlPanelForm.id, "zotero")

    def test_form_schema(self):
        """Test that form schema is IZoteroClientSettings."""
        from eea.zotero.browser.controlpanel import ZoteroControlPanelForm

        self.assertEqual(ZoteroControlPanelForm.schema, IZoteroClientSettings)

    def test_view_form_is_set(self):
        """Test that view form is ZoteroControlPanelForm."""
        from eea.zotero.browser.controlpanel import (
            ZoteroControlPanelView,
            ZoteroControlPanelForm,
        )

        self.assertEqual(ZoteroControlPanelView.form, ZoteroControlPanelForm)


class TestZoteroPackageInit(unittest.TestCase):
    """Test eea.zotero package initialization."""

    def test_message_factory(self):
        """Test that EEAMessageFactory is defined."""
        self.assertIsNotNone(EEAMessageFactory)

    def test_message_factory_domain(self):
        """Test that EEAMessageFactory domain is eea."""
        self.assertEqual(EEAMessageFactory._domain, "eea")

    def test_initialize_is_callable(self):
        """Test that initialize function exists and is callable."""
        from eea.zotero import initialize

        self.assertTrue(callable(initialize))


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

    def test_browser_layer_exists(self):
        """Test that IEeaZoteroLayer interface exists."""
        self.assertIsNotNone(IEeaZoteroLayer)


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
