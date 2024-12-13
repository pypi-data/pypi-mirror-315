# ionix_api/models.py
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PaginatedResponse:
    """Base class for paginated API responses"""
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Dict[str, Any]]

@dataclass
class RiskRank:
    """Risk ranking information"""
    risk_score: int
    type: str

@dataclass
class ActionItem:
    """Action item details"""
    id: str
    title: str
    type: str
    asset: str
    summary: str
    urgency: str
    cves: List[str]
    first_opened_at: datetime
    last_opened_at: datetime
    description: Optional[str] = None

@dataclass
class Assessment:
    """Assessment details"""
    risk_score: int
    asset: str
    cloud_services: List[str]
    cloud_risk_grade: int
    cves: List[str]
    connections_types: List[str]
    ips: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    groups: Optional[List[str]] = None

@dataclass
class Connection:
    """Connection details"""
    id: int
    risk: RiskRank
    source: str
    target: str
    connected_asset_type: str
    type: str
    is_redirected: bool = False
    remarks: Optional[str] = None
    source_groups: Optional[List[str]] = None
    details: Optional[Dict[str, Any]] = None
