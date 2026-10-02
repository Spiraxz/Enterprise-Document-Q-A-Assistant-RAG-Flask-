# Enterprise Document Q&A Assistant

An internal knowledge-base chatbot that helps employees ask questions about company policy, HR, and technical documents in natural language. The assistant uses a Retrieval-Augmented Generation (RAG) workflow to find relevant document context and return concise, document-grounded chatbot responses through a Flask API and React chat widget.

## Overview

This project provides a document-aware Q&A assistant for enterprise teams. Employees can submit questions through a lightweight React frontend, while the Flask backend handles retrieval, conversation memory, and response generation using LangChain.

The system stores document embeddings in a Chroma vector database, retrieves the most relevant context for each query, and passes that context to the language model so answers stay grounded in the internal knowledge base.

## Features

- Natural-language Q&A over internal policy, HR, and technical documents
- Document upload (.txt, .md, .pdf, .docx) from the chat widget — answers are grounded in uploaded files
- RAG pipeline built with LangChain
- Chroma vector store for semantic search and document retrieval
- Flask REST API for chatbot requests
- React chat-widget frontend
- Conversation memory for more contextual follow-up answers
- Environment-based API key configuration
- Local development setup for backend and frontend

## Tech Stack

- Backend: Flask, Flask-CORS
- Frontend: React, Axios, styled-components
- RAG / LLM Orchestration: LangChain
- Vector Database: Chroma
- Embeddings: Google Gemini (`gemini-embedding-2-preview`)
- Language Model API: Google Gemini (configurable via `GEMINI_MODEL`, default `gemini-3.5-flash-lite`)
- Deployment: Gunicorn-ready Flask API

## Project Structure

```text
.
├── app.py                  # Flask app + API routes (/, /data, /upload)
├── requirements.txt
├── setup.py
├── tests.py                # API test suite
├── .env                    # GOOGLE_API_KEY / GEMINI_MODEL (you create this)
├── sample_docs/            # sample .txt/.pdf/.docx files to try the upload feature
├── database/               # Chroma vector store (created automatically)
├── src
│   ├── components
│   │   └── chatbot.py      # Gemini chatbot + conversation chain
│   ├── exception.py
│   ├── logger.py
│   └── utils.py            # embeddings, retrieval, document ingestion
└── frontend
    ├── public
    └── src
        ├── App.js
        ├── index.js
        └── components
            └── chatbot.js  # chat widget with the 📎 upload button
```

## How It Works

1. (Optional) A user uploads a document with the 📎 button; the backend extracts its text, chunks it, and stores the embeddings in Chroma.
2. A user submits a question from the React chat widget.
3. The frontend sends the query to the Flask `/data` endpoint.
4. The backend refines the query using the conversation history.
5. Relevant text is retrieved from the Chroma vector store.
6. LangChain builds a prompt with the retrieved context and user query.
7. The language model generates a response for the user.
8. The frontend displays the chatbot response in the chat window.

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

`GEMINI_API_KEY` is also accepted as a fallback variable name. You can get a key from Google AI Studio. `GEMINI_MODEL` is optional and defaults to `gemini-3.5-flash-lite` (free-tier daily quotas are tracked per model, so you can switch models here if you hit one).

### 5. Run the Flask Backend

```bash
python app.py
```

The backend runs on:

```text
http://localhost:5000
```

### 6. Run the React Frontend

```bash
cd frontend
npm install
npm start
```

The frontend runs on:

```text
http://localhost:3000
```

### 7. Run the Tests

With the backend dependencies installed (these call the Gemini API):

```bash
python -m unittest tests
```

## API Endpoints

### Health / Idle Prompt

```http
GET /
```

Returns an automated chatbot response when the user is idle.

### Chat Query

```http
POST /data
```

Request body:

```json
{
  "data": "What is the company's leave policy?"
}
```

Response body:

```json
{
  "response": true,
  "message": "Generated chatbot answer"
}
```

### Document Upload

```http
POST /upload
```

Multipart form body with a `file` field. Supported types: `.txt`, `.md`, `.pdf`, `.docx`. The file is text-extracted, chunked, and stored in the Chroma knowledge base so the chatbot can answer questions about it.

Response body:

```json
{
  "response": true,
  "message": "Added 'leave_policy.pdf' (4 chunks) to the knowledge base. Ask me anything about it!"
}
```

## Example Use Cases

- Employees asking about HR policies and benefits
- Technical teams searching engineering documentation
- Internal support teams answering repeated policy questions
- Company-wide document search with conversational follow-ups

## Future Improvements

- Improve source citation formatting in the response payload
- Add authentication for internal users
- Support role-based document access
- Add streaming responses for a smoother chat experience
- Add production deployment configuration

## License

This project is intended for internal enterprise document Q&A use.
