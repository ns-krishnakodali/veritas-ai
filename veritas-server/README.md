# Veritas AI Server

Backend server for Veritas AI, built with FastAPI. It handles API requests from the Veritas chat system, manages language model interactions, user requests, and streams responses back in real time.

---

## Server Setup

You can run the server either using Docker or a local Python environment.
Ensure that a .env file exists in the project root. This file contains configuration such as your OpenAI credentials, which are required to access the language model APIs.

---

### Option 1: Using Docker

Use the following commands to build and run the server with Docker:

```bash
# Build the Docker image
docker build -t veritas-server .

# Run the container with environment variables
docker run --env-file .env -p 8000:8000 veritas-server
```

---

### Option 2: Local Python Environment

```bash
# Setup virtual environment
python -m venv venv

# Unix/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Start the Server

If using Docker, run the container as mentioned above.

If using a local Python environment:

```bash
# Activate the virtual environment first
uvicorn main:app --reload --port 8000
```
