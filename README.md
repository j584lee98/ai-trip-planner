# AI Trip Planner

An AI-powered trip planning application built with Streamlit and LangGraph. The app validates trip details and fetches travel information using the Amadeus API.

## Features

- Trip details validation using LLM
- Flight and accommodation search via Amadeus API
- Interactive Streamlit interface

## Requirements

- Python 3.11+
- OpenAI API key
- Amadeus API credentials (optional, for flight data)

## Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/j584lee98/ai-trip-planner.git
   cd ai-trip-planner
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (see [Environment Variables](#environment-variables))

5. Run the app:
   ```bash
   streamlit run app.py
   ```

### Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Or build and run manually:
   ```bash
   docker build -t ai-trip-planner .
   docker run -p 8501:8501 --env-file .env ai-trip-planner
   ```

The app will be available at `http://localhost:8501`

## Environment Variables

Create a `.streamlit/secrets.toml` file or set environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `MODEL_NAME` | OpenAI model name (e.g., `gpt-4o`) | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `AMADEUS_CLIENT_ID` | Amadeus API client ID | No |
| `AMADEUS_CLIENT_SECRET` | Amadeus API client secret | No |

### Using `.streamlit/secrets.toml`

```toml
MODEL_NAME = "gpt-4o"
OPENAI_API_KEY = "sk-..."
AMADEUS_CLIENT_ID = "your-client-id"
AMADEUS_CLIENT_SECRET = "your-client-secret"
```

### Using `.env` file (for Docker)

```env
MODEL_NAME=gpt-4o
OPENAI_API_KEY=sk-...
AMADEUS_CLIENT_ID=your-client-id
AMADEUS_CLIENT_SECRET=your-client-secret
```

## Project Structure

```
ai-trip-planner/
├── app.py                 # Streamlit application
├── backend/
│   ├── agents/
│   │   ├── validator.py   # Trip details validation agent
│   │   └── data_fetcher.py # Travel data fetcher agent
│   ├── config/
│   │   ├── graph.py       # LangGraph workflow definition
│   │   ├── runtime.py     # Graph invocation utilities
│   │   └── state.py       # State schema
│   ├── core/
│   │   └── llm.py         # LLM factory
│   └── tools/
│       └── amadeus.py     # Amadeus API tools
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```
