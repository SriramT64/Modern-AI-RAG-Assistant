# 🤖 Modern-AI-RAG-Assistant
End-to-end local Retrieval-Augmented Generation (RAG) AI assistant using FastAPI, ChromaDB, Ollama, Qwen, and Streamlit.

An end-to-end Retrieval-Augmented Generation (RAG) AI assistant that answers questions using information retrieved from a private document knowledge base.

The application runs locally using Ollama and provides both a REST API and a web-based Streamlit interface.

## 🚀 Features

- Multi-document knowledge base
- Document chunking and ingestion
- Semantic search using embeddings
- ChromaDB vector database
- Top-K retrieval
- Retrieval reranking
- Relevance filtering
- Local LLM inference with Ollama
- Conversation memory
- FastAPI REST API
- Streamlit web interface
- RAG evaluation
- Source retrieval
- Docker configuration

## 🛠️ Tech Stack

### Programming & Development
- Python 3.13
- VS Code
- Git
- GitHub

### Generative AI
- Generative AI
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering

### LLM & Embeddings
- Qwen 2.5 Coder 3B
- Ollama
- Nomic Embed Text

### Retrieval & Vector Database
- ChromaDB
- Vector Embeddings
- Semantic Search
- Top-K Retrieval
- Hybrid Chunking
- Keyword Overlap
- Custom Reranking
- Relevance Filtering

### Backend
- FastAPI
- Uvicorn
- REST API
- JSON
- Swagger UI / OpenAPI

### Frontend
- Streamlit
- Chat-based UI
- Source Document Display

### Evaluation
- Custom RAG Evaluation Pipeline
- Retrieval Testing
- Question-Answer Evaluation
- `evaluation_results.json`

### Deployment & DevOps
- Docker
- Docker Compose
- Dockerfile
- `.dockerignore`

### Storage
- ChromaDB Persistent Storage
- Local Document Storage

### Architecture
- End-to-End RAG Architecture
- API-based Backend
- Local LLM Inference
- Conversation Memory
- Source-aware Responses
## 🏗️ Architecture

```text
                         User
                           │
                           ▼
                    ┌─────────────┐
                    │  Streamlit  │
                    │  Frontend   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │   Backend   │
                    └──────┬──────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Query Embedding  │
                  │ Nomic Embeddings  │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  ChromaDB   │
                    │ Vector DB   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Reranking  │
                    └──────┬──────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Relevance Filter │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Qwen LLM  │
                    │   Ollama    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Answer   │
                    └─────────────┘
