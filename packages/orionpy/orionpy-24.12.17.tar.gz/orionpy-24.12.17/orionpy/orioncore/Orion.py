# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from enum import Enum
from getpass import getpass
from orionpy.orioncore.OrionBase import OrionBase
from orionpy.orioncore.resources.IMCs import IMCs
from orionpy.orioncore.Exceptions import OrionAuthorizeError

from . import cfg_global
from .features.Geonotes import Geonotes
from .features.Projects import Projects
from .Filters import Filters
from .Groups import Groups
from .RequestManager import RequestManager
from .resources.Businesses import Businesses
from .resources.Services import Services
from .UrlBuilder import UrlBuilder
from .Users import Users
from .WebmapPermissionsCalculator import WebmapPermissionsCalculator

# =============================================================================
# CLASS
# =============================================================================


class Orion(OrionBase):
    # TODO check if Orion should really be a Singleton !
    # TODO get Orion/Portal version (/orion/version)
    """A singleton class. The main class of our project"""

    def __init__(
        self, username, password, url_machine, portal="portal", verify_cert=True
    ):
        super().__init__(username, password, url_machine, portal, verify_cert)
        if not self._is_valid_user():
            raise OrionAuthorizeError('User {} is not authorized to connect on Orion'.format(username))
        
        self._filters = Filters()
        self._groups = Groups()
        self._users = Users()
        self._services = Services()
        self._projects = Projects()
        self._geonotes = Geonotes()
        self._businesses = Businesses()
        self._imcs = IMCs()
        self.webmap_permissions_calculator = WebmapPermissionsCalculator()

    def _is_valid_user(self):
        orion_self_url = self.url_manager.orion_self_url()
        self_struct = self.request.get_in_python(orion_self_url)
        return self_struct.get("isSuperAdmin")
