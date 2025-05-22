# Global Semiconductor Crisis Resilience Platform

A comprehensive digital twin platform that models, simulates, and optimizes global semiconductor supply chain resilience against catastrophic disruption scenarios.

## Project Overview

This platform addresses critical chokepoints in modern technology:
- Taiwan's dominance in advanced chip manufacturing (92% of chips ≤10nm)
- ASML's EUV lithography monopoly
- Automotive chip dependencies
- Rare earth elements concentration (90% Chinese processing)

## Core Features

1. Digital Twin Infrastructure
   - Real-time supply chain simulation
   - Multi-scenario crisis modeling
   - Predictive analytics
   - Interactive visualization

2. Risk Analytics
   - Early warning systems
   - Cascade impact modeling
   - Optimization algorithms
   - Strategic decision support

3. Data Integration
   - Manufacturing data
   - Shipping intelligence
   - Geopolitical risk monitoring
   - Economic indicators

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

## Project Structure

```
semiconductor_resilience/
├── api/                    # FastAPI backend
├── core/                   # Core business logic
├── data/                   # Data models and schemas
├── models/                 # ML models and simulations
├── services/              # External service integrations
├── tests/                 # Test suite
└── web/                   # Frontend dashboard
```

## Development

1. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. Run development server:
   ```bash
   uvicorn api.main:app --reload
   ```

3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests. 