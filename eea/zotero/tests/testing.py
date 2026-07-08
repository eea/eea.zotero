"""Test layer for eea.zotero."""

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import eea.zotero


class EeaZoteroLayer(PloneSandboxLayer):
    """Test layer for eea.zotero."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=eea.zotero)

    def setUpPloneSite(self, portal):
        """Set up Plone site."""
        applyProfile(portal, "eea.zotero:default")


EEA_ZOTERO_FIXTURE = EeaZoteroLayer()

EEA_ZOTERO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_ZOTERO_FIXTURE,),
    name="EeaZoteroLayer:IntegrationTesting",
)
