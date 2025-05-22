from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    FAB = "fab"
    SUPPLIER = "supplier"
    DISTRIBUTOR = "distributor"
    CUSTOMER = "customer"
    LOGISTICS = "logistics"


class ChipType(str, Enum):
    LOGIC = "logic"
    MEMORY = "memory"
    ANALOG = "analog"
    POWER = "power"
    SENSOR = "sensor"
    DISCRETE = "discrete"


class ProcessNode(str, Enum):
    NODE_3NM = "3nm"
    NODE_5NM = "5nm"
    NODE_7NM = "7nm"
    NODE_10NM = "10nm"
    NODE_14NM = "14nm"
    NODE_28NM = "28nm"
    NODE_40NM = "40nm"
    NODE_65NM = "65nm"
    NODE_90NM = "90nm"
    NODE_130NM = "130nm"
    NODE_180NM = "180nm"
    NODE_250NM = "250nm"


class Location(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    risk_score: float = Field(ge=0.0, le=1.0)


class SupplyChainNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    type: NodeType
    location: Location
    capacity: float  # Units per month
    utilization: float = Field(ge=0.0, le=1.0)
    process_nodes: List[ProcessNode]
    chip_types: List[ChipType]
    risk_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SupplyChainEdge(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    target_id: UUID
    lead_time_days: int
    reliability_score: float = Field(ge=0.0, le=1.0)
    capacity: float
    cost_per_unit: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DisruptionScenario(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    probability: float = Field(ge=0.0, le=1.0)
    duration_days: int
    affected_nodes: List[UUID]
    affected_edges: List[UUID]
    impact_severity: float = Field(ge=0.0, le=1.0)
    affected_regions: List[str]
    affected_process_nodes: List[str]
    mitigation_strategies: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RiskAssessment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    node_id: UUID
    scenario_id: UUID
    risk_score: float = Field(ge=0.0, le=1.0)
    impact_score: float = Field(ge=0.0, le=1.0)
    mitigation_cost: float
    recovery_time_days: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SupplyChainMetrics(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime
    node_id: UUID
    throughput: float
    inventory_level: float
    lead_time: float
    cost_per_unit: float
    quality_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 