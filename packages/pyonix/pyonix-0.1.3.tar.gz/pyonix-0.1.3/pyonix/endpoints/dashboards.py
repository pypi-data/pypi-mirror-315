# ionix_api/endpoints/dashboards.py
from typing import Optional, Dict, Any
from pyonix.client import IonixClient

class Dashboards:
    """
    Handles interaction with the Ionix Dashboards API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def get(self, 
            asset: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs) -> Dict[str, Any]:
        """
        Get dashboard summary synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            Dashboard summary data
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return self.client.get("dashboard/summary/", params=params)

    async def get_async(self,
                       asset: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Get dashboard summary asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            Dashboard summary data
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return await self.client.get_async("dashboard/summary/", params=params)
