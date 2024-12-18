import json
from .RequestManager import RequestManager
from .UrlBuilder import UrlBuilder

class WebmapPermissionsCalculator:
    """Calculate webmap permissions"""
    def __init__(self):
        self._request_manager = RequestManager()
        self._url_builder = UrlBuilder()

    def calculate_webmap_permissions(self, item_id):
        """
        :param item_id: id of the webmap
        """
        payload = {
            "value" : json.dumps({"itemId": item_id})
        }
        try:
            response = self._request_manager.post(
                    self._url_builder.calculate_permissions_from_webmap_item_url(), payload
            )
            print(response.json())
        except Exception as e:
            print(e)
