import json
from datetime import datetime, timedelta
from typing import Dict, List

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
import requests

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# API endpoint
API_URL = "http://localhost:8000"

# Layout components
def create_network_graph(nodes: List[Dict], edges: List[Dict]) -> go.Figure:
    """Create a network graph visualization of the supply chain."""
    G = nx.DiGraph()
    
    # Add nodes
    for node in nodes:
        G.add_node(
            str(node["id"]),
            name=node["name"],
            type=node["type"],
            capacity=node["capacity"],
            utilization=node["utilization"],
        )
    
    # Add edges
    for edge in edges:
        G.add_edge(
            str(edge["source_id"]),
            str(edge["target_id"]),
            capacity=edge["capacity"],
            reliability=edge["reliability_score"],
        )
    
    # Create layout
    pos = nx.spring_layout(G)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_data = G.nodes[node]
        node_text.append(
            f"{node_data['name']}<br>"
            f"Type: {node_data['type']}<br>"
            f"Capacity: {node_data['capacity']:,.0f}<br>"
            f"Utilization: {node_data['utilization']:.1%}"
        )
        node_color.append(node_data["utilization"])
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale="YlOrRd",
            color=node_color,
            size=15,
            colorbar=dict(
                thickness=15,
                title="Utilization",
                xanchor="left",
                titleside="right",
            ),
        ),
    )
    
    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Semiconductor Supply Chain Network",
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    
    return fig


def create_metrics_plot(metrics: Dict[str, List[Dict]]) -> go.Figure:
    """Create a time series plot of supply chain metrics."""
    # Prepare data for plotting
    data = []
    for node_id, node_metrics in metrics.items():
        for metric in node_metrics:
            data.append({
                "timestamp": datetime.fromisoformat(metric["timestamp"]),
                "node_id": node_id,
                "throughput": metric["throughput"],
                "inventory": metric["inventory_level"],
                "lead_time": metric["lead_time"],
                "cost": metric["cost_per_unit"],
                "quality": metric["quality_score"],
            })
    
    # Create figure with subplots
    fig = go.Figure()
    
    # Add throughput trace
    fig.add_trace(
        go.Scatter(
            x=[d["timestamp"] for d in data],
            y=[d["throughput"] for d in data],
            name="Throughput",
            mode="lines",
        )
    )
    
    # Add inventory trace
    fig.add_trace(
        go.Scatter(
            x=[d["timestamp"] for d in data],
            y=[d["inventory"] for d in data],
            name="Inventory",
            mode="lines",
        )
    )
    
    # Add lead time trace
    fig.add_trace(
        go.Scatter(
            x=[d["timestamp"] for d in data],
            y=[d["lead_time"] for d in data],
            name="Lead Time",
            mode="lines",
        )
    )
    
    fig.update_layout(
        title="Supply Chain Metrics Over Time",
        xaxis_title="Time",
        yaxis_title="Value",
        hovermode="x unified",
    )
    
    return fig


def create_scenario_card(scenario):
    """Create a card displaying scenario information."""
    return dbc.Card(
        [
            dbc.CardHeader(scenario["name"]),
            dbc.CardBody(
                [
                    html.P(scenario["description"]),
                    html.Hr(),
                    html.P(f"Probability: {scenario['probability']:.1%}"),
                    html.P(f"Duration: {scenario['duration_days']} days"),
                    html.P(f"Impact Severity: {scenario['impact_severity']:.1%}"),
                    html.Hr(),
                    html.H6("Affected Regions:"),
                    html.Ul([html.Li(region) for region in scenario["affected_regions"]]),
                    html.H6("Affected Process Nodes:"),
                    html.Ul([html.Li(node) for node in scenario["affected_process_nodes"]]),
                    html.H6("Mitigation Strategies:"),
                    html.Ul([html.Li(strategy) for strategy in scenario["mitigation_strategies"]]),
                ]
            ),
        ],
        className="mb-3",
    )


# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Global Semiconductor Crisis Resilience Platform",
                        className="text-center my-4",
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Simulation Controls"),
                                dbc.CardBody(
                                    [
                                        dbc.Button(
                                            "Initialize Simulation",
                                            id="init-sim-button",
                                            color="primary",
                                            className="mb-3",
                                        ),
                                        dbc.Button(
                                            "Step Simulation",
                                            id="step-sim-button",
                                            color="success",
                                            className="mb-3",
                                        ),
                                        dbc.Button(
                                            "Apply Disruption",
                                            id="disrupt-sim-button",
                                            color="danger",
                                            className="mb-3",
                                        ),
                                        dcc.Dropdown(
                                            id="scenario-dropdown",
                                            options=[],
                                            placeholder="Select disruption scenario",
                                        ),
                                    ]
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Supply Chain Health"),
                                dbc.CardBody(id="health-metrics"),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Selected Scenario"),
                                dbc.CardBody(id="scenario-details"),
                            ],
                            className="mb-4",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Supply Chain Network"),
                                dbc.CardBody(
                                    dcc.Graph(id="network-graph"),
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Supply Chain Metrics"),
                                dbc.CardBody(
                                    dcc.Graph(id="metrics-graph"),
                                ),
                            ],
                        ),
                    ],
                    width=9,
                ),
            ]
        ),
        dcc.Store(id="simulation-state"),
    ],
    fluid=True,
)


# Callbacks
@app.callback(
    [
        Output("simulation-state", "data"),
        Output("network-graph", "figure"),
        Output("metrics-graph", "figure"),
        Output("health-metrics", "children"),
        Output("scenario-dropdown", "options"),
    ],
    [Input("init-sim-button", "n_clicks")],
    [State("simulation-state", "data")],
)
def initialize_simulation(n_clicks, current_state):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    # Initialize simulation
    response = requests.post(f"{API_URL}/simulation/initialize")
    data = response.json()
    
    # Create visualizations
    network_fig = create_network_graph(data["nodes"], data["edges"])
    metrics_fig = create_metrics_plot(data["metrics"])
    
    # Create health metrics display
    health_metrics = [
        html.H5(f"Average Utilization: {data['health']['average_utilization']:.1%}"),
        html.H5(f"Average Risk Score: {data['health']['average_risk_score']:.1%}"),
        html.H5(f"Average Reliability: {data['health']['average_reliability']:.1%}"),
        html.H5(f"Active Disruptions: {data['health']['active_disruptions']}"),
    ]
    
    # Get available scenarios
    scenarios_response = requests.get(f"{API_URL}/simulation/scenarios")
    scenarios = scenarios_response.json()
    scenario_options = [
        {"label": s["name"], "value": json.dumps(s)}
        for s in scenarios
    ]
    
    return data, network_fig, metrics_fig, health_metrics, scenario_options


@app.callback(
    [
        Output("simulation-state", "data", allow_duplicate=True),
        Output("network-graph", "figure", allow_duplicate=True),
        Output("metrics-graph", "figure", allow_duplicate=True),
        Output("health-metrics", "children", allow_duplicate=True),
    ],
    [Input("step-sim-button", "n_clicks")],
    [State("simulation-state", "data")],
    prevent_initial_call=True,
)
def step_simulation(n_clicks, current_state):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    # Step simulation
    response = requests.post(f"{API_URL}/simulation/step")
    data = response.json()
    
    # Create visualizations
    network_fig = create_network_graph(data["nodes"], data["edges"])
    metrics_fig = create_metrics_plot(data["metrics"])
    
    # Create health metrics display
    health_metrics = [
        html.H5(f"Average Utilization: {data['health']['average_utilization']:.1%}"),
        html.H5(f"Average Risk Score: {data['health']['average_risk_score']:.1%}"),
        html.H5(f"Average Reliability: {data['health']['average_reliability']:.1%}"),
        html.H5(f"Active Disruptions: {data['health']['active_disruptions']}"),
    ]
    
    return data, network_fig, metrics_fig, health_metrics


@app.callback(
    [
        Output("simulation-state", "data", allow_duplicate=True),
        Output("network-graph", "figure", allow_duplicate=True),
        Output("metrics-graph", "figure", allow_duplicate=True),
        Output("health-metrics", "children", allow_duplicate=True),
    ],
    [Input("disrupt-sim-button", "n_clicks")],
    [State("scenario-dropdown", "value"), State("simulation-state", "data")],
    prevent_initial_call=True,
)
def apply_disruption(n_clicks, scenario_value, current_state):
    if n_clicks is None or not scenario_value:
        raise dash.exceptions.PreventUpdate
    
    # Apply disruption
    scenario = json.loads(scenario_value)
    response = requests.post(f"{API_URL}/simulation/disruption", json=scenario)
    data = response.json()
    
    # Create visualizations
    network_fig = create_network_graph(data["nodes"], data["edges"])
    metrics_fig = create_metrics_plot(data["metrics"])
    
    # Create health metrics display
    health_metrics = [
        html.H5(f"Average Utilization: {data['health']['average_utilization']:.1%}"),
        html.H5(f"Average Risk Score: {data['health']['average_risk_score']:.1%}"),
        html.H5(f"Average Reliability: {data['health']['average_reliability']:.1%}"),
        html.H5(f"Active Disruptions: {data['health']['active_disruptions']}"),
    ]
    
    return data, network_fig, metrics_fig, health_metrics


@app.callback(
    Output("scenario-details", "children"),
    [Input("scenario-dropdown", "value")],
    prevent_initial_call=True,
)
def update_scenario_details(scenario_value):
    if not scenario_value:
        return "No scenario selected"
    
    scenario = json.loads(scenario_value)
    return create_scenario_card(scenario)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050) 