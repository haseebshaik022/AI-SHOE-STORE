# AI Shoe Store Backend

An AI-powered e-commerce backend built with FastAPI that combines
traditional backend APIs with RAG, vector search, Redis, and an LLM
to provide an intelligent shoe-store assistant.

The project is backend-only and is designed to demonstrate
real-world backend, database, AI integration, authentication,
caching, and deployment concepts.

---

## 🚀 Features

- User registration and login
- JWT-based authentication
- Secure password hashing with bcrypt
- Shoe catalogue management
- Order creation and order history
- AI-powered conversational assistant
- Retrieval-Augmented Generation (RAG)
- Semantic policy search using pgvector
- Hugging Face embeddings
- Groq LLM integration
- Redis-based conversation history
- Async PostgreSQL operations
- SQLAlchemy ORM
- Dockerized deployment
- Interactive Swagger API documentation

---

## 🤖 AI Assistant

The chatbot understands natural-language questions and uses
different data sources depending on the user's request.

### Policy Questions

Company policies are stored as text, split into chunks, and
converted into embeddings.

```text
User Question
      ↓
Hugging Face Embedding
      ↓
pgvector Similarity Search
      ↓
Relevant Policy Chunks
      ↓
Groq LLM
      ↓
Answer
