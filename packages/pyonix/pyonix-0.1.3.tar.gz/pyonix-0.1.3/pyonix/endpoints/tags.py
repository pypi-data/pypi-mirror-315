# ionix_api/endpoints/tags.py
from typing import List, Dict, Any
from pyonix.client import IonixClient

class Tags:
    """
    Handles interaction with the Ionix Tags API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def post(self, ids: List[str], tags: List[str]) -> Dict[str, Any]:
        """
        Add tags to organizational assets.
        
        Args:
            ids: List of asset IDs to tag
            tags: List of tags to apply
            
        Returns:
            Updated asset information including:
            - id
            - risk_score
            - asset name
            - type
            - importance
            - hosting provider
            - technologies
            - first seen date
            - service information
            - tags
            - groups
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        payload = {
            "ids": ids,
            "tags": tags
        }
        return self.client.post(
            "discovery/org-assets/tags/?fields=id,risk_score,asset,type,importance,hosting_provider,technologies,first_seen,service_type,service,tags,groups",
            data=payload
        )

    async def post_async(self, ids: List[str], tags: List[str]) -> Dict[str, Any]:
        """
        Add tags to organizational assets asynchronously.
        
        Args:
            ids: List of asset IDs to tag
            tags: List of tags to apply
            
        Returns:
            Updated asset information including:
            - id
            - risk_score
            - asset name
            - type
            - importance
            - hosting provider
            - technologies
            - first seen date
            - service information
            - tags
            - groups
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        payload = {
            "ids": ids,
            "tags": tags
        }
        return await self.client.post_async(
            "discovery/org-assets/tags/?fields=id,risk_score,asset,type,importance,hosting_provider,technologies,first_seen,service_type,service,tags,groups",
            data=payload
        )
