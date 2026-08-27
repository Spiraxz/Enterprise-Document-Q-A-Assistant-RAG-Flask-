# Enterprise Document Q&A Assistant

An internal knowledge-base chatbot that helps employees ask questions about company policy, HR, and technical documents in natural language. The assistant uses a Retrieval-Augmented Generation (RAG) workflow to find relevant document context and return concise, document-grounded chatbot responses through a Flask API and React chat widget.

## Overview

This project provides a document-aware Q&A assistant for enterprise teams. Employees can submit questions through a lightweight React frontend, while the Flask backend handles retrieval, conversation memory, and response generation using LangChain.

The system stores document embeddings in a Chroma vector database, retrieves the most relevant context for each query, and passes that context to the language model so answers stay grounded in the internal knowledge base.

## Features

- Natural-language Q&A over internal policy, HR, and technical documents
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
- Embeddings: OpenAI embeddings
- Language Model API: Provider-configurable setup for OpenAI, Gemini, or Claude
- Deployment: Gunicorn-ready Flask API

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── setup.py
├── src
│   ├── components
│   │   └── chatbot.py
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
└── frontend
    ├── public
    └── src
        ├── App.js
        ├── index.js
        └── components
            └── chatbot.js
```

## How It Works

1. A user submits a question from the React chat widget.
2. The frontend sends the query to the Flask `/data` endpoint.
3. The backend refines the query using the conversation history.
4. Relevant text is retrieved from the Chroma vector store.
5. LangChain builds a prompt with the retrieved context and user query.
6. The language model generates a response for the user.
7. The frontend displays the chatbot response in the chat window.

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd chatbot-langchain-flask-main
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
OPENAI_API_KEY=your_api_key_here
```

If using Gemini or Claude instead of OpenAI, update the model initialization in the LangChain chatbot component and set the matching provider key in the environment.

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

## Example Use Cases

- Employees asking about HR policies and benefits
- Technical teams searching engineering documentation
- Internal support teams answering repeated policy questions
- Company-wide document search with conversational follow-ups

## Future Improvements

- Improve source citation formatting in the response payload
- Add authentication for internal users
- Support file upload and document ingestion from the UI
- Add role-based document access
- Add streaming responses for a smoother chat experience
- Add production deployment configuration

## License

This project is intended for internal enterprise document Q&A use.
