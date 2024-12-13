# ionix_api/endpoints/connections.py
from typing import List, Optional, Dict, Any
from pyonix.client import IonixClient
from pyonix.models import PaginatedResponse, Connection

class Connections:
    """
    Handles interaction with the Ionix Connections API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def get_all(self,
                asset: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                **kwargs) -> List[Dict[str, Any]]:
        """
        Get all connections synchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all connections across pages
            
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
        return self.client.paginate("discovery/connections/", params=params)

    async def get_all_async(self,
                          asset: Optional[str] = None,
                          limit: Optional[int] = None,
                          offset: Optional[int] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Get all connections asynchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all connections across pages
            
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
        return await self.client.paginate_async("discovery/connections/", params=params)

    def get(self,
            asset: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs) -> PaginatedResponse:
        """
        Get paginated connections synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing connections
            
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
        response = self.client.get("discovery/connections/", params=params)
        return PaginatedResponse(**response)

    async def get_async(self,
                       asset: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None,
                       **kwargs) -> PaginatedResponse:
        """
        Get paginated connections asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing connections
            
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
        response = await self.client.get_async("discovery/connections/", params=params)
        return PaginatedResponse(**response)
