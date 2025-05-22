import random
from datetime import datetime
from typing import List, Tuple
from uuid import UUID

import numpy as np

from ..data.models import (
    ChipType,
    DisruptionScenario,
    Location,
    NodeType,
    ProcessNode,
    SupplyChainEdge,
    SupplyChainNode,
)


class SupplyChainDataGenerator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        
        # Define realistic semiconductor industry parameters
        self.fab_capacities = {
            ProcessNode.NODE_3NM: (50000, 100000),  # (min, max) wafers per month
            ProcessNode.NODE_5NM: (40000, 80000),
            ProcessNode.NODE_7NM: (30000, 60000),
            ProcessNode.NODE_10NM: (20000, 40000),
            ProcessNode.NODE_14NM: (15000, 30000),
            ProcessNode.NODE_28NM: (10000, 20000),
            ProcessNode.NODE_40NM: (8000, 15000),
            ProcessNode.NODE_65NM: (5000, 10000),
            ProcessNode.NODE_90NM: (3000, 6000),
            ProcessNode.NODE_130NM: (2000, 4000),
            ProcessNode.NODE_180NM: (1000, 2000),
            ProcessNode.NODE_250NM: (500, 1000),
        }
        
        # Define major semiconductor manufacturing locations
        self.locations = {
            "TSMC": [
                ("Taiwan", "Hsinchu", "Hsinchu Science Park", 24.8138, 121.0000),
                ("Taiwan", "Tainan", "Southern Taiwan Science Park", 23.0000, 120.2000),
            ],
            "Samsung": [
                ("South Korea", "Gyeonggi", "Hwaseong", 37.2000, 126.8000),
                ("South Korea", "Gyeonggi", "Pyeongtaek", 37.0000, 126.9000),
            ],
            "Intel": [
                ("USA", "Arizona", "Chandler", 33.3000, -111.8000),
                ("USA", "Oregon", "Hillsboro", 45.5000, -122.9000),
            ],
            "GlobalFoundries": [
                ("USA", "New York", "Malta", 42.9000, -73.8000),
                ("Singapore", "Singapore", "Woodlands", 1.4000, 103.8000),
            ],
            "UMC": [
                ("Taiwan", "Hsinchu", "Hsinchu Science Park", 24.8138, 121.0000),
                ("Singapore", "Singapore", "Pasir Ris", 1.3700, 103.9500),
            ],
        }
        
        # Define realistic disruption scenarios
        self.disruption_scenarios = [
            {
                "name": "Taiwan Strait Crisis",
                "description": "Military tensions in Taiwan Strait affecting shipping and production",
                "probability": 0.45,
                "duration_days": 90,
                "impact_severity": 0.8,
                "affected_regions": ["Taiwan", "China"],
                "affected_process_nodes": ["3nm", "5nm", "7nm"],
                "mitigation_strategies": [
                    "Diversify manufacturing locations",
                    "Increase inventory buffers",
                    "Develop alternative suppliers"
                ]
            },
            {
                "name": "ASML Export Controls",
                "description": "Strict export controls on EUV lithography equipment",
                "probability": 0.3,
                "duration_days": 180,
                "impact_severity": 0.6,
                "affected_regions": ["Global"],
                "affected_process_nodes": ["3nm", "5nm"],
                "mitigation_strategies": [
                    "Accelerate domestic EUV development",
                    "Optimize existing equipment utilization",
                    "Develop alternative lithography technologies"
                ]
            },
            {
                "name": "Natural Disaster - Taiwan Earthquake",
                "description": "Major earthquake affecting Taiwan semiconductor production",
                "probability": 0.2,
                "duration_days": 30,
                "impact_severity": 0.7,
                "affected_regions": ["Taiwan"],
                "affected_process_nodes": ["3nm", "5nm", "7nm", "10nm"],
                "mitigation_strategies": [
                    "Implement earthquake-resistant facility designs",
                    "Establish backup power systems",
                    "Develop rapid recovery protocols"
                ]
            },
            {
                "name": "Rare Earth Embargo",
                "description": "Chinese restrictions on rare earth element exports",
                "probability": 0.35,
                "duration_days": 120,
                "impact_severity": 0.5,
                "affected_regions": ["Global"],
                "affected_process_nodes": ["All"],
                "mitigation_strategies": [
                    "Develop alternative rare earth sources",
                    "Implement recycling programs",
                    "Optimize material usage efficiency"
                ]
            },
            {
                "name": "Global Chip Shortage",
                "description": "Prolonged semiconductor shortage affecting multiple industries",
                "probability": 0.4,
                "duration_days": 365,
                "impact_severity": 0.6,
                "affected_regions": ["Global"],
                "affected_process_nodes": ["All"],
                "mitigation_strategies": [
                    "Increase manufacturing capacity",
                    "Implement allocation strategies",
                    "Develop alternative technologies"
                ]
            },
            {
                "name": "Cybersecurity Breach",
                "description": "Major cyber attack on semiconductor manufacturing facilities",
                "probability": 0.25,
                "duration_days": 45,
                "impact_severity": 0.7,
                "affected_regions": ["Global"],
                "affected_process_nodes": ["All"],
                "mitigation_strategies": [
                    "Enhance cybersecurity measures",
                    "Implement air-gapped systems",
                    "Develop rapid recovery protocols"
                ]
            },
            {
                "name": "Trade War Escalation",
                "description": "Intensified trade restrictions between major economies",
                "probability": 0.3,
                "duration_days": 180,
                "impact_severity": 0.6,
                "affected_regions": ["Global"],
                "affected_process_nodes": ["All"],
                "mitigation_strategies": [
                    "Diversify supply chain",
                    "Localize critical manufacturing",
                    "Develop alternative trade routes"
                ]
            }
        ]

    def generate_location(self, company: str) -> Location:
        """Generate a realistic location for a semiconductor company."""
        if company in self.locations:
            country, region, city, lat, lon = random.choice(self.locations[company])
        else:
            # Generate a random location if company not in predefined list
            country = random.choice(["USA", "Japan", "Germany", "France", "UK"])
            region = f"Region_{random.randint(1, 5)}"
            city = f"City_{random.randint(1, 10)}"
            lat = random.uniform(-90, 90)
            lon = random.uniform(-180, 180)
        
        return Location(
            country=country,
            region=region,
            city=city,
            latitude=lat,
            longitude=lon,
            risk_score=random.uniform(0.1, 0.9),
        )

    def generate_fab_node(self, company: str) -> SupplyChainNode:
        """Generate a realistic semiconductor fab node."""
        # Select process nodes based on company capabilities
        if company == "TSMC":
            process_nodes = [
                ProcessNode.NODE_3NM,
                ProcessNode.NODE_5NM,
                ProcessNode.NODE_7NM,
                ProcessNode.NODE_10NM,
            ]
        elif company == "Samsung":
            process_nodes = [
                ProcessNode.NODE_5NM,
                ProcessNode.NODE_7NM,
                ProcessNode.NODE_10NM,
                ProcessNode.NODE_14NM,
            ]
        else:
            process_nodes = random.sample(list(ProcessNode), k=random.randint(1, 4))
        
        # Calculate capacity based on process nodes
        capacity = sum(
            random.uniform(*self.fab_capacities[node])
            for node in process_nodes
        )
        
        return SupplyChainNode(
            name=f"{company}_Fab_{random.randint(1, 5)}",
            type=NodeType.FAB,
            location=self.generate_location(company),
            capacity=capacity,
            utilization=random.uniform(0.7, 0.95),
            process_nodes=process_nodes,
            chip_types=random.sample(list(ChipType), k=random.randint(1, 3)),
            risk_score=random.uniform(0.1, 0.9),
        )

    def generate_supplier_node(self) -> SupplyChainNode:
        """Generate a realistic supplier node."""
        company = random.choice([
            "ASML", "Applied Materials", "Lam Research", "Tokyo Electron",
            "KLA Corporation", "Teradyne", "Advantest",
        ])
        
        return SupplyChainNode(
            name=f"{company}_Supplier_{random.randint(1, 3)}",
            type=NodeType.SUPPLIER,
            location=self.generate_location(company),
            capacity=random.uniform(1000, 5000),
            utilization=random.uniform(0.6, 0.9),
            process_nodes=random.sample(list(ProcessNode), k=random.randint(1, 3)),
            chip_types=random.sample(list(ChipType), k=random.randint(1, 2)),
            risk_score=random.uniform(0.1, 0.9),
        )

    def generate_edge(
        self, source_id: UUID, target_id: UUID, source_type: NodeType, target_type: NodeType
    ) -> SupplyChainEdge:
        """Generate a realistic supply chain edge."""
        # Adjust lead time and reliability based on node types
        if source_type == NodeType.FAB and target_type == NodeType.CUSTOMER:
            lead_time = random.randint(30, 90)  # Longer lead time for fab to customer
            reliability = random.uniform(0.8, 0.95)
        elif source_type == NodeType.SUPPLIER and target_type == NodeType.FAB:
            lead_time = random.randint(15, 45)  # Medium lead time for supplier to fab
            reliability = random.uniform(0.85, 0.98)
        else:
            lead_time = random.randint(5, 20)  # Shorter lead time for other connections
            reliability = random.uniform(0.9, 0.99)
        
        return SupplyChainEdge(
            source_id=source_id,
            target_id=target_id,
            lead_time_days=lead_time,
            reliability_score=reliability,
            capacity=random.uniform(1000, 10000),
            cost_per_unit=random.uniform(100, 1000),
        )

    def generate_disruption_scenario(self) -> DisruptionScenario:
        """Generate a realistic disruption scenario."""
        scenario = random.choice(self.disruption_scenarios)
        return DisruptionScenario(
            name=scenario["name"],
            description=scenario["description"],
            probability=scenario["probability"],
            duration_days=scenario["duration_days"],
            affected_nodes=[],  # To be filled by the simulation
            affected_edges=[],  # To be filled by the simulation
            impact_severity=scenario["impact_severity"],
        )

    def generate_supply_chain(
        self, num_fabs: int = 5, num_suppliers: int = 10, num_customers: int = 8
    ) -> Tuple[List[SupplyChainNode], List[SupplyChainEdge]]:
        """Generate a complete supply chain network."""
        nodes = []
        edges = []
        
        # Generate fab nodes
        companies = ["TSMC", "Samsung", "Intel", "GlobalFoundries", "UMC"]
        for _ in range(num_fabs):
            company = random.choice(companies)
            fab_node = self.generate_fab_node(company)
            nodes.append(fab_node)
        
        # Generate supplier nodes
        for _ in range(num_suppliers):
            supplier_node = self.generate_supplier_node()
            nodes.append(supplier_node)
        
        # Generate customer nodes
        for i in range(num_customers):
            customer_node = SupplyChainNode(
                name=f"Customer_{i+1}",
                type=NodeType.CUSTOMER,
                location=self.generate_location("Customer"),
                capacity=random.uniform(500, 2000),
                utilization=random.uniform(0.5, 0.8),
                process_nodes=random.sample(list(ProcessNode), k=random.randint(1, 2)),
                chip_types=random.sample(list(ChipType), k=random.randint(1, 2)),
                risk_score=random.uniform(0.1, 0.9),
            )
            nodes.append(customer_node)
        
        # Generate edges between nodes
        for i, source in enumerate(nodes):
            # Connect suppliers to fabs
            if source.type == NodeType.SUPPLIER:
                for target in nodes:
                    if target.type == NodeType.FAB:
                        if random.random() < 0.3:  # 30% chance of connection
                            edge = self.generate_edge(
                                source.id, target.id, source.type, target.type
                            )
                            edges.append(edge)
            
            # Connect fabs to customers
            elif source.type == NodeType.FAB:
                for target in nodes:
                    if target.type == NodeType.CUSTOMER:
                        if random.random() < 0.4:  # 40% chance of connection
                            edge = self.generate_edge(
                                source.id, target.id, source.type, target.type
                            )
                            edges.append(edge)
        
        return nodes, edges 