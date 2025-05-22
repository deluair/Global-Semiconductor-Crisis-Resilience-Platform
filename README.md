# Global Semiconductor Crisis Resilience Platform

A comprehensive digital twin platform that models, simulates, and optimizes global semiconductor supply chain resilience against catastrophic disruption scenarios.

## Project Overview

This platform addresses critical chokepoints in modern technology:
- Taiwan's dominance in advanced chip manufacturing (92% of chips ≤10nm)
- ASML's EUV lithography monopoly
- Automotive chip dependencies
- Rare earth elements concentration (90% Chinese processing)

## Core Features

1. **Digital Twin Infrastructure**
   - Real-time supply chain simulation
   - Multi-scenario crisis modeling
   - Predictive analytics
   - Interactive visualization

2. **Risk Analytics**
   - Early warning systems
   - Cascade impact modeling
   - Optimization algorithms
   - Strategic decision support

3. **Data Integration**
   - Manufacturing data
   - Shipping intelligence
   - Geopolitical risk monitoring
   - Economic indicators

4. **Disruption Scenario Modeling**
   - Taiwan Strait Crisis
   - ASML Export Controls
   - Natural Disaster (e.g., Taiwan Earthquake)
   - Rare Earth Embargo
   - Global Chip Shortage
   - Cybersecurity Breach
   - Trade War Escalation
   - Each scenario includes: affected regions, process nodes, mitigation strategies, and severity

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Platform

To launch both the FastAPI backend and Dash frontend together:

```bash
python run.py
```

- The backend API will be available at: http://localhost:8000
- The frontend dashboard will be available at: http://localhost:8050

**Note:**
- Ensure all dependencies are installed, including `dash-bootstrap-components`.
- If you encounter a `ModuleNotFoundError`, install the missing package with `pip install <package-name>`.
- For Dash v3+, the platform uses `app.run()` instead of `app.run_server()`.

## Project Structure

```
semiconductor_resilience/
├── api/        # FastAPI backend
├── core/       # Core simulation and data generation
├── data/       # Data models and schemas
├── web/        # Dash frontend dashboard
├── models/     # ML models and simulations (future)
├── services/   # External service integrations (future)
├── tests/      # Test suite
└── run.py      # Script to run both backend and frontend
```

## Usage

### Web Dashboard
- Open [http://localhost:8050](http://localhost:8050) in your browser.
- **Simulation Controls:**
  - Initialize Simulation: Generates a new supply chain network.
  - Step Simulation: Advances the simulation by one step (day).
  - Apply Disruption: Select and apply a disruption scenario to see its impact.
- **Scenario Details:**
  - View affected regions, process nodes, and recommended mitigation strategies for each scenario.
- **Network Graph:**
  - Visualizes the supply chain as a directed network.
  - Node color indicates utilization; hover for details.
- **Metrics Graph:**
  - Time series of throughput, inventory, and lead time across the network.
- **Health Metrics:**
  - Displays average utilization, risk score, reliability, and active disruptions.

### API Endpoints
- The FastAPI backend exposes endpoints for simulation control, scenario management, and metrics retrieval.
- Example: `POST /simulation/initialize`, `POST /simulation/step`, `POST /simulation/disruption`, `GET /simulation/health`, etc.
- See the OpenAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Troubleshooting
- If the frontend fails to start, ensure you are using Dash v3+ and have all required packages installed.
- If ports 8000 or 8050 are in use, stop other services or change the ports in `run.py` and `app.py`.
- For Windows users, use the provided commands in PowerShell or CMD.

## Development

1. Set up environment variables (if needed):
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
2. Run tests:
   ```bash
   pytest
   ```
3. Code formatting:
   ```bash
   black .
   isort .
   mypy .
   ```

## License

MIT License

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests. 