# ionix_api/endpoints/assessments.py
from typing import List, Optional, Dict, Any
from pyonix.client import IonixClient
from pyonix.models import PaginatedResponse, Assessment

class Assessments:
    """
    Handles interaction with the Ionix Assessments API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def get_digital_supply_chain(self,
                               asset: Optional[str] = None,
                               limit: Optional[int] = None,
                               offset: Optional[int] = None,
                               **kwargs) -> PaginatedResponse:
        """
        Get digital supply chain assessments synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing assessment results
            
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
        response = self.client.get("assessments/digital-supply-chain/", params=params)
        return PaginatedResponse(**response)

    async def get_digital_supply_chain_async(self,
                                           asset: Optional[str] = None,
                                           limit: Optional[int] = None,
                                           offset: Optional[int] = None,
                                           **kwargs) -> PaginatedResponse:
        """
        Get digital supply chain assessments asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing assessment results
            
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
        response = await self.client.get_async("assessments/digital-supply-chain/", params=params)
        return PaginatedResponse(**response)

    def get_all_digital_supply_chain(self,
                                   asset: Optional[str] = None,
                                   limit: Optional[int] = None,
                                   offset: Optional[int] = None,
                                   **kwargs) -> List[Dict[str, Any]]:
        """
        Get all digital supply chain assessments synchronously (handles pagination).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all assessment results across pages
            
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
        return self.client.paginate("assessments/digital-supply-chain/", params=params)

    async def get_all_digital_supply_chain_async(self,
                                               asset: Optional[str] = None,
                                               limit: Optional[int] = None,
                                               offset: Optional[int] = None,
                                               **kwargs) -> List[Dict[str, Any]]:
        """
        Get all digital supply chain assessments asynchronously (handles pagination).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all assessment results across pages
            
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
        return await self.client.paginate_async("assessments/digital-supply-chain/", params=params)

    def get(self,
            asset: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs) -> PaginatedResponse:
        """
        Get organizational asset assessments synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing assessment results
            
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
        response = self.client.get("assessments/org-assets/", params=params)
        return PaginatedResponse(**response)

    async def get_async(self,
                       asset: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None,
                       **kwargs) -> PaginatedResponse:
        """
        Get organizational asset assessments asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing assessment results
            
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
        response = await self.client.get_async("assessments/org-assets/", params=params)
        return PaginatedResponse(**response)

    def get_all(self,
                asset: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                **kwargs) -> List[Dict[str, Any]]:
        """
        Get all organizational asset assessments synchronously (handles pagination).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all assessment results across pages
            
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
        return self.client.paginate("assessments/org-assets/", params=params)

    async def get_all_async(self,
                          asset: Optional[str] = None,
                          limit: Optional[int] = None,
                          offset: Optional[int] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Get all organizational asset assessments asynchronously (handles pagination).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all assessment results across pages
            
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
        return await self.client.paginate_async("assessments/org-assets/", params=params)
