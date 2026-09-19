# Enterprise Knowledge Search

An AI-powered enterprise knowledge retrieval and question-answering system built using **FastAPI, Retrieval-Augmented Generation (RAG), Sentence Transformers, ChromaDB, MySQL, and Gemini**.

The system allows users to upload enterprise documents, process their content into searchable chunks, perform semantic search, and generate answers using the most relevant retrieved information.

---

## 📌 Overview

Enterprise organizations often store important information in documents such as company policies, security guidelines, and internal documentation.

Finding specific information from these documents using traditional keyword search can be difficult.

**Enterprise Knowledge Search** solves this problem by combining:

* PDF document processing
* Text chunking
* AI-based embeddings
* Vector similarity search
* Retrieval-Augmented Generation (RAG)
* User authentication

Users can ask questions in natural language, and the system retrieves relevant document content before generating an answer.

---

## 🎯 Problem Statement

Traditional document search mainly depends on matching keywords.

For example, a user may ask:

> "How many annual leave days does an employee receive?"

Even if the document contains the relevant information using different wording, a keyword-based approach may not retrieve the correct content.

This project uses **semantic search** so that queries can be matched based on meaning rather than exact words.

---

## 💡 Solution

The system follows a Retrieval-Augmented Generation pipeline.

```text
                 User
                   │
                   ▼
              FastAPI API
                   │
          ┌────────┴────────┐
          │                 │
     Authentication     Document Upload
          │                 │
        JWT             PDF Processing
                            │
                            ▼
                       Text Extraction
                            │
                            ▼
                       Text Chunking
                            │
                            ▼
                    Sentence Embeddings
                            │
                            ▼
                         ChromaDB
                            │
                            │
                    User Search Query
                            │
                            ▼
                    Query Embedding
                            │
                            ▼
                    Semantic Search
                            │
                            ▼
                    Relevant Chunks
                            │
                            ▼
                       Gemini LLM
                            │
                            ▼
                    RAG Generated Answer
                            │
                            ▼
                     Answer + Sources
```

---

## ✨ Key Features

### 🔐 User Authentication

* User registration
* Password hashing using bcrypt
* User login
* JWT-based authentication
* Protected profile endpoint
* User roles

### 📄 Document Processing

* PDF upload
* PDF text extraction using PyMuPDF
* Text chunking
* Embedding generation

### 🔎 Semantic Search

* Converts documents into vector embeddings
* Stores embeddings in ChromaDB
* Converts user queries into embeddings
* Performs similarity search
* Retrieves relevant document chunks

### 🤖 RAG Question Answering

* Retrieves relevant document content
* Builds context from retrieved chunks
* Sends the context and user question to Gemini
* Generates an answer based only on the retrieved context
* Returns the retrieved sources with the answer

---

## 🧠 RAG Pipeline

The project implements the following RAG workflow:

### 1. Upload Document

A user uploads a PDF through the `/upload` endpoint.

### 2. Extract Text

The application uses **PyMuPDF** to extract text from the PDF.

### 3. Split Text into Chunks

The extracted text is divided into smaller chunks.

The current implementation uses a chunk size of **500 characters**.

### 4. Generate Embeddings

Each chunk is converted into a vector representation using:

```text
all-MiniLM-L6-v2
```

through the `sentence-transformers` library.

### 5. Store in ChromaDB

The chunks, embeddings, filename, and chunk index are stored in a ChromaDB collection named:

```text
enterprise_documents
```

### 6. Search

When a user enters a question, the query is converted into an embedding.

ChromaDB performs similarity search and retrieves the most relevant document chunks.

### 7. Retrieve Relevant Context

The application filters the retrieved results using a distance threshold and keeps relevant results.

### 8. Generate Answer

The retrieved document content is passed to the Gemini model together with the user's question.

The prompt instructs the model to answer using only the retrieved context and not invent information.

---

## 🏗️ Technology Stack

| Category             | Technology                 |
| -------------------- | -------------------------- |
| Backend              | FastAPI                    |
| Programming Language | Python                     |
| Database             | MySQL                      |
| ORM                  | SQLAlchemy                 |
| Authentication       | JWT + OAuth2               |
| Password Hashing     | bcrypt                     |
| PDF Processing       | PyMuPDF                    |
| Text Embeddings      | Sentence Transformers      |
| Embedding Model      | all-MiniLM-L6-v2           |
| Vector Database      | ChromaDB                   |
| Generative AI        | Gemini                     |
| API Testing          | FastAPI Swagger / REST API |
| Version Control      | Git & GitHub               |

---

## 📂 Project Structure

```text
enterprise-knowledge-search/
│
├── backend/
│   │
│   ├── auth.py
│   ├── chroma_service.py
│   ├── database.py
│   ├── embedding_service.py
│   ├── main.py
│   ├── models.py
│   ├── rag_service.py
│   ├── schemas.py
│   ├── text_utils.py
│   │
│   ├── documents/
│   │   ├── Company_IT_Security_Policy.txt
│   │   └── Company_Leave_Policy.txt
│   │
│   └── chroma_db/
│
├── .gitignore
│
└── README.md
```

---

## 🔐 Authentication Flow

The application uses JWT-based authentication.

### Registration

```text
POST /register
```

The user provides:

* Name
* Email
* Password
* Role

The password is hashed before being stored in the database.

### Login

```text
POST /login
```

The user's credentials are verified and an access token is generated.

### Protected Profile

```text
GET /profile
```

The JWT token is verified before returning the authenticated user's profile.

---

## 📡 API Endpoints

| Method | Endpoint               | Purpose                                           |
| ------ | ---------------------- | ------------------------------------------------- |
| GET    | `/`                    | Check whether the API is running                  |
| POST   | `/register`            | Register a new user                               |
| POST   | `/login`               | Authenticate a user and receive JWT               |
| GET    | `/profile`             | Retrieve authenticated user information           |
| POST   | `/upload`              | Upload a PDF document                             |
| GET    | `/read-pdf/{filename}` | Extract text from a PDF                           |
| GET    | `/chunks/{filename}`   | Chunk, embed and store document content           |
| GET    | `/search`              | Perform semantic search and generate a RAG answer |

---

## 🔎 Semantic Search Example

A user can send a query such as:

```text
What is the company's annual leave policy?
```

The system:

```text
Question
   ↓
Query Embedding
   ↓
ChromaDB Similarity Search
   ↓
Relevant Document Chunks
   ↓
Distance Filtering
   ↓
Retrieved Context
   ↓
Gemini
   ↓
Generated Answer
```

The search response includes:

* User query
* Generated answer
* Source document
* Chunk index
* Distance information

---

## 📚 Knowledge Base

The current project includes example enterprise documents such as:

* `Company_IT_Security_Policy.txt`
* `Company_Leave_Policy.txt`

These documents provide the knowledge used by the semantic search and RAG pipeline.

---

## 🔒 Security

The application includes:

* Password hashing
* JWT authentication
* Protected user profile access
* Environment-variable support for sensitive configuration

**Important:** API keys, JWT secrets, database passwords, and other credentials should be stored in environment variables and must not be committed to GitHub.

Example:

```env
GEMINI_API_KEY=your_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Usha-sundarapu/enterprise-knowledge-search.git
```

### 2. Open the backend

```bash
cd enterprise-knowledge-search/backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install dependencies

If a `requirements.txt` file is added:

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file and add the required configuration values.

### 7. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 8. Open API documentation

```text
http://127.0.0.1:8000/docs
```

FastAPI's Swagger UI can then be used to test the available endpoints.

---

## 🧪 Example Use Case

### Question

```text
How many days of annual leave does an employee receive?
```

### System Process

```text
User Question
     ↓
Generate Query Embedding
     ↓
Search ChromaDB
     ↓
Retrieve Relevant Leave Policy Chunk
     ↓
Pass Context to Gemini
     ↓
Generate Answer
```

The answer is generated using the retrieved enterprise document context.

---

## 🧩 Challenges

Some of the key implementation challenges include:

* Extracting useful text from PDF documents
* Choosing an appropriate chunk size
* Generating meaningful embeddings
* Storing and retrieving vectors efficiently
* Filtering irrelevant search results
* Passing retrieved context correctly to the LLM
* Preventing the LLM from generating information outside the retrieved documents
* Implementing authentication for protected resources

---

## 🔮 Future Improvements

Possible improvements include:

* Frontend integration
* Role-based document access
* Document-level permissions
* Support for additional document formats
* Improved chunking strategies
* Hybrid keyword + semantic search
* Conversation history
* Better retrieval evaluation
* Source citations in the user interface
* Cloud deployment
* Monitoring and logging
* Improved authentication and authorization

---

## 👥 Project

**Enterprise Knowledge Search** is a team project focused on applying modern AI techniques to enterprise document retrieval and question answering.

The project combines **FastAPI, MySQL, JWT authentication, PDF processing, semantic embeddings, ChromaDB, and RAG-based generation** into a single backend system.

---

## 📄 License

This project is developed for educational and project purposes.
