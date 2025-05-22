from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import networkx as nx
import numpy as np
from pydantic import BaseModel

from ..data.models import (
    DisruptionScenario,
    ProcessNode,
    RiskAssessment,
    SupplyChainEdge,
    SupplyChainMetrics,
    SupplyChainNode,
)


class SimulationState(BaseModel):
    timestamp: datetime
    nodes: Dict[str, SupplyChainNode]
    edges: Dict[str, SupplyChainEdge]
    metrics: Dict[str, List[SupplyChainMetrics]]
    active_scenarios: List[DisruptionScenario]


class SupplyChainSimulator:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.state = SimulationState(
            timestamp=datetime.utcnow(),
            nodes={},
            edges={},
            metrics={},
            active_scenarios=[],
        )

    def add_node(self, node: SupplyChainNode) -> None:
        """Add a node to the supply chain network."""
        self.state.nodes[str(node.id)] = node
        self.graph.add_node(
            str(node.id),
            **node.dict(exclude={"id"}),
        )

    def add_edge(self, edge: SupplyChainEdge) -> None:
        """Add an edge to the supply chain network."""
        self.state.edges[str(edge.id)] = edge
        self.graph.add_edge(
            str(edge.source_id),
            str(edge.target_id),
            id=str(edge.id),
            **edge.dict(exclude={"id", "source_id", "target_id"}),
        )

    def apply_disruption(self, scenario: DisruptionScenario) -> None:
        """Apply a disruption scenario to the supply chain."""
        self.state.active_scenarios.append(scenario)
        
        # Apply impact to nodes based on region and process node
        for node_id, node in self.state.nodes.items():
            should_affect = False
            
            # Check if node is in affected region
            if node.location.country in scenario.affected_regions or "Global" in scenario.affected_regions:
                should_affect = True
            
            # Check if node's process nodes are affected
            if any(process_node in scenario.affected_process_nodes for process_node in node.process_nodes) or "All" in scenario.affected_process_nodes:
                should_affect = True
            
            if should_affect:
                # Calculate impact based on node's vulnerability and scenario severity
                impact_factor = scenario.impact_severity * (1 + node.risk_score) / 2
                
                # Apply impact to node metrics
                node.utilization *= (1 - impact_factor)
                node.risk_score = min(1.0, node.risk_score + impact_factor)
                self.state.nodes[node_id] = node
                
                # Add node to affected nodes list if not already present
                if node.id not in scenario.affected_nodes:
                    scenario.affected_nodes.append(node.id)

        # Apply impact to edges connected to affected nodes
        for edge_id, edge in self.state.edges.items():
            if (edge.source_id in scenario.affected_nodes or 
                edge.target_id in scenario.affected_nodes):
                # Calculate impact based on edge's vulnerability and scenario severity
                impact_factor = scenario.impact_severity * (1 + edge.reliability_score) / 2
                
                # Apply impact to edge metrics
                edge.reliability_score *= (1 - impact_factor)
                edge.capacity *= (1 - impact_factor)
                self.state.edges[edge_id] = edge
                
                # Add edge to affected edges list if not already present
                if edge.id not in scenario.affected_edges:
                    scenario.affected_edges.append(edge.id)

    def simulate_step(self, duration_days: int = 1) -> List[SupplyChainMetrics]:
        """Simulate one step of the supply chain."""
        new_metrics = []
        
        for node_id, node in self.state.nodes.items():
            # Calculate throughput based on capacity and utilization
            throughput = node.capacity * node.utilization
            
            # Calculate inventory changes
            incoming_edges = self.graph.in_edges(node_id, data=True)
            outgoing_edges = self.graph.out_edges(node_id, data=True)
            
            incoming_flow = sum(
                self.state.edges[edge_data['id']].capacity
                for _, _, edge_data in incoming_edges
            )
            outgoing_flow = sum(
                self.state.edges[edge_data['id']].capacity
                for _, _, edge_data in outgoing_edges
            )
            
            # Calculate lead time as average of incoming edge lead times
            lead_time = np.mean([
                self.state.edges[edge_data['id']].lead_time_days
                for _, _, edge_data in incoming_edges
            ]) if incoming_edges else 0
            
            # Calculate quality score based on node reliability and incoming material quality
            quality_score = node.risk_score * np.mean([
                self.state.edges[edge_data['id']].reliability_score
                for _, _, edge_data in incoming_edges
            ]) if incoming_edges else node.risk_score
            
            # Create metrics for this node
            metrics = SupplyChainMetrics(
                timestamp=self.state.timestamp,
                node_id=node.id,
                throughput=throughput,
                inventory_level=incoming_flow - outgoing_flow,
                lead_time=lead_time,
                cost_per_unit=sum(
                    self.state.edges[edge_data['id']].cost_per_unit
                    for _, _, edge_data in incoming_edges
                ) / len(incoming_edges) if incoming_edges else 0,
                quality_score=quality_score,
            )
            
            new_metrics.append(metrics)
            
            # Update node metrics history
            if node_id not in self.state.metrics:
                self.state.metrics[node_id] = []
            self.state.metrics[node_id].append(metrics)
        
        # Update simulation timestamp
        self.state.timestamp += timedelta(days=duration_days)
        
        return new_metrics

    def calculate_risk_assessment(
        self, node_id: str, scenario: DisruptionScenario
    ) -> RiskAssessment:
        """Calculate risk assessment for a node under a specific scenario."""
        node = self.state.nodes[node_id]
        
        # Calculate risk score based on node vulnerability and scenario impact
        risk_score = node.risk_score * scenario.impact_severity
        
        # Calculate impact score based on node importance and scenario severity
        impact_score = (
            node.utilization * node.capacity * scenario.impact_severity
        ) / max(1, len(self.state.nodes))
        
        # Estimate recovery time based on scenario duration and node complexity
        recovery_time_days = int(
            scenario.duration_days * (1 + len(self.graph.edges(node_id)) / 10)
        )
        
        # Estimate mitigation cost based on node capacity and scenario impact
        mitigation_cost = node.capacity * scenario.impact_severity * 1000000  # Example cost factor
        
        return RiskAssessment(
            node_id=node.id,
            scenario_id=scenario.id,
            risk_score=risk_score,
            impact_score=impact_score,
            mitigation_cost=mitigation_cost,
            recovery_time_days=recovery_time_days,
        )

    def get_supply_chain_health(self) -> Dict[str, float]:
        """Calculate overall supply chain health metrics."""
        return {
            "average_utilization": np.mean([node.utilization for node in self.state.nodes.values()]),
            "average_risk_score": np.mean([node.risk_score for node in self.state.nodes.values()]),
            "average_reliability": np.mean([edge.reliability_score for edge in self.state.edges.values()]),
            "active_disruptions": len(self.state.active_scenarios),
        } 