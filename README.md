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
