from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..core.data_generator import SupplyChainDataGenerator
from ..core.simulation import SupplyChainSimulator
from ..data.models import (
    DisruptionScenario,
    SupplyChainEdge,
    SupplyChainMetrics,
    SupplyChainNode,
)

app = FastAPI(
    title="Global Semiconductor Crisis Resilience Platform",
    description="A comprehensive digital twin platform for semiconductor supply chain resilience",
    version="1.0.0",
)

# Initialize simulation components
simulator = SupplyChainSimulator()
data_generator = SupplyChainDataGenerator()


class SimulationResponse(BaseModel):
    nodes: List[SupplyChainNode]
    edges: List[SupplyChainEdge]
    metrics: Dict[str, List[SupplyChainMetrics]]
    health: Dict[str, float]


@app.post("/simulation/initialize", response_model=SimulationResponse)
async def initialize_simulation(
    num_fabs: int = 5,
    num_suppliers: int = 10,
    num_customers: int = 8,
) -> SimulationResponse:
    """Initialize a new supply chain simulation with the specified number of nodes."""
    nodes, edges = data_generator.generate_supply_chain(
        num_fabs=num_fabs,
        num_suppliers=num_suppliers,
        num_customers=num_customers,
    )
    
    # Add nodes and edges to simulator
    for node in nodes:
        simulator.add_node(node)
    for edge in edges:
        simulator.add_edge(edge)
    
    # Run initial simulation step
    metrics = simulator.simulate_step()
    
    return SimulationResponse(
        nodes=nodes,
        edges=edges,
        metrics={str(node.id): [m for m in metrics if m.node_id == node.id] for node in nodes},
        health=simulator.get_supply_chain_health(),
    )


@app.post("/simulation/step", response_model=SimulationResponse)
async def simulation_step(duration_days: int = 1) -> SimulationResponse:
    """Advance the simulation by the specified number of days."""
    if not simulator.state.nodes:
        raise HTTPException(
            status_code=400,
            detail="Simulation not initialized. Call /simulation/initialize first.",
        )
    
    metrics = simulator.simulate_step(duration_days=duration_days)
    
    return SimulationResponse(
        nodes=list(simulator.state.nodes.values()),
        edges=list(simulator.state.edges.values()),
        metrics={str(node_id): node_metrics for node_id, node_metrics in simulator.state.metrics.items()},
        health=simulator.get_supply_chain_health(),
    )


@app.post("/simulation/disruption", response_model=SimulationResponse)
async def apply_disruption(scenario: DisruptionScenario) -> SimulationResponse:
    """Apply a disruption scenario to the supply chain."""
    if not simulator.state.nodes:
        raise HTTPException(
            status_code=400,
            detail="Simulation not initialized. Call /simulation/initialize first.",
        )
    
    simulator.apply_disruption(scenario)
    metrics = simulator.simulate_step()
    
    return SimulationResponse(
        nodes=list(simulator.state.nodes.values()),
        edges=list(simulator.state.edges.values()),
        metrics={str(node_id): node_metrics for node_id, node_metrics in simulator.state.metrics.items()},
        health=simulator.get_supply_chain_health(),
    )


@app.get("/simulation/health")
async def get_health() -> Dict[str, float]:
    """Get the current health metrics of the supply chain."""
    if not simulator.state.nodes:
        raise HTTPException(
            status_code=400,
            detail="Simulation not initialized. Call /simulation/initialize first.",
        )
    
    return simulator.get_supply_chain_health()


@app.get("/simulation/scenarios")
async def get_scenarios() -> List[DisruptionScenario]:
    """Get a list of predefined disruption scenarios."""
    return [
        data_generator.generate_disruption_scenario()
        for _ in range(5)  # Generate 5 random scenarios
    ]


@app.get("/simulation/node/{node_id}/metrics")
async def get_node_metrics(
    node_id: UUID,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> List[SupplyChainMetrics]:
    """Get metrics for a specific node within a time range."""
    if not simulator.state.nodes:
        raise HTTPException(
            status_code=400,
            detail="Simulation not initialized. Call /simulation/initialize first.",
        )
    
    if str(node_id) not in simulator.state.metrics:
        raise HTTPException(
            status_code=404,
            detail=f"Node {node_id} not found in simulation.",
        )
    
    metrics = simulator.state.metrics[str(node_id)]
    
    if start_time:
        metrics = [m for m in metrics if m.timestamp >= start_time]
    if end_time:
        metrics = [m for m in metrics if m.timestamp <= end_time]
    
    return metrics 