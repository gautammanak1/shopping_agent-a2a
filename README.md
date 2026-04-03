# Shopping Partner Agent (A2A)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-000000)](https://fetch.ai/)
[![A2A](https://img.shields.io/badge/A2A-Protocol-purple)](https://github.com/google/A2A)

AI-powered product recommendation agent that searches trusted e-commerce platforms and provides detailed product comparisons. Built with Google Gemini, Exa Search, and the Agent-to-Agent (A2A) protocol integrated with Fetch.ai uAgents.

## Features

- **Smart Product Search** — Finds products matching user preferences across Amazon, Flipkart, Myntra, Nike, and more
- **Detailed Recommendations** — Up to 10 products with name, price, rating, features, pros/cons, and direct links
- **Comparative Analysis** — Side-by-side comparison of top recommendations
- **Stock Verification** — Ensures recommended products are available for purchase
- **A2A + uAgents** — Combines Google's A2A protocol with Fetch.ai's agent framework

## Architecture

```
User Query
    │
    ▼
┌────────────────┐     ┌──────────────────┐
│ uAgent         │────▶│ A2A Server       │
│ Coordinator    │     │ (FastAPI)        │
│ (port 8200)    │     │ (port 10020)     │
└────────────────┘     └────────┬─────────┘
                                │
                       ┌────────▼─────────┐
                       │ Shopping Agent   │
                       │ (Gemini + Exa)   │
                       └──────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Google Gemini 2.0 Flash |
| Search | Exa Tools |
| Agent Framework | Fetch.ai uAgents |
| Communication | A2A Protocol (Google) |
| API Server | FastAPI + Uvicorn |
| Data Validation | Pydantic |

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Exa API key

### Installation

```bash
git clone https://github.com/GAUTAMMANAK1/shopping_agent-a2a.git
cd shopping_agent-a2a
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=your-openai-key
EXA_API_KEY=your-exa-key
```

## Usage

```bash
python main.py
```

This starts:
- FastAPI health check server on port 8000
- A2A agent server on port 10020
- uAgent coordinator on port 8200

### Docker

```bash
docker build -t shopping-agent .
docker compose up -d
```

### Example Query

> "Find me a durable, waterproof backpack suitable for hiking under $150"

## Project Structure

```
shopping_agent-a2a/
├── main.py              # System startup and coordination
├── shopping_agent.py    # Product recommendation logic (Gemini + Exa)
├── adpter.py            # A2A ↔ uAgent adapter
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-service setup
└── requirements.txt     # Python dependencies
```

## License

MIT
