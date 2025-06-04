# Veritas AI

**Veritas AI** is a modular Retrieval-Augmented Generation (RAG) based personal assistant system designed to answer questions using relevant contextual information. This repository uses a monorepo architecture that includes both the UI frontend and backend server components.

## Overview

The core idea of **Veritas AI** is to augment user queries with relevant context chunks from ingested raw data, enabling a Large Language Model (LLM) to generate more accurate and relevant responses.

This monorepo setup is organized into two main components:

- [`veritas-chat`](./veritas-chat): Frontend UI for interacting with the RAG system.
- [`veritas-server`](./veritas-server): Backend server for data ingestion, context retrieval, prompt construction, and LLM interaction.

## Architecture

The RAG pipeline is split into two primary workflows:

### 1. Context Workflow

This stage processes raw data and prepares contexts for query-time retrieval.

![Context Workflow](./resources/context-workflow.png)

- **Data Collection**: Supports `.txt` and `.json` file formats. Please refer to the README in `veritas-server` to prepare and run the RAG context.
- **Chunking**: Breaks documents into manageable chunks.
- **Embedding**: Each chunk is transformed into a vector using OpenAI's `text-embedding-3-small` model.
- **Vector Storage**: The embeddings are stored in a `FAISS` vector database for fast similarity search.
- **Context Storage**: The raw text and metadata of the chunk are stored along with the embeddings.

The embedding model is easily configurable, so you can switch to another one if needed.

### 2. Query Handling and Context Retrieval

This stage retrieves relevant chunks and uses them to generate LLM prompts.

![User Query Workflow](./resources/user-query-workflow.png)

- **User Query**: Received via the `/conversation` API.
- **Query Embedding**: The user’s question is embedded using `text-embedding-3-small` and compared with stored vectors in FAISS.
- **Context Retrieval**: Top-k (=5) similar chunks are fetched using cosine similarity.
- **Prompt Construction**: The retrieved context is combined with the query to construct the prompt.
- **LLM Generation**: The prompt is passed to the `gpt-4.1-mini` model to generate a response. Like the embedding model, this can also be configured as needed.

---

## Getting Started

To run the full application, you can do it in one of two ways: locally or using Docker.

### Local Development

1. **Start the backend server**:
   See [`veritas-server`](./veritas-server/README.md) for details.

2. **Run the frontend application**:
   See [`veritas-chat`](./veritas-chat/README.md) for setup and launch instructions.

### Docker Setup

You can also run the entire stack using Docker Compose.

Make sure Docker and Docker Compose are installed on your system.

From the root of the repository:

```bash
docker-compose up --build
```

This will start the following services:

- **veritas-server** on port `8080`
- **veritas-chat** on port `3000` (depends on the backend)

To stop the services:

```bash
docker-compose down
```
