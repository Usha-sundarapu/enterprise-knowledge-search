from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, User
from schemas import UserCreate, UserLogin,Token
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

from fastapi import Depends
from auth import get_current_user

from fastapi import UploadFile, File
import shutil
import os
import fitz
from text_utils import chunk_text

from chroma_service import store_chunks
from embedding_service import generate_embeddings
from embedding_service import generate_query_embedding
from chroma_service import search_chunks

from rag_service import generate_rag_answer

from fastapi.middleware.cors import CORSMiddleware
 
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Enterprise Knowledge Search API Running"
    }


@app.post("/register")
def register(user: UserCreate):

    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "Email already exists"
        }

    hashed_pw = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "User registered successfully"
    }


 
@app.post("/login", response_model=Token)
def login(user: UserLogin):

    db: Session = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        db.close()
        return {
            "message": "Invalid Email"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):
        db.close()
        return {
            "message": "Invalid Password"
        }

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    upload_folder = "documents"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename
    }

@app.get("/read-pdf/{filename}")
def read_pdf(filename: str):

    file_path = f"documents/{filename}"

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return {
        "filename": filename,
        "content": text
    }

@app.get("/chunks/{filename}")
def get_chunks(filename: str):

    file_path = f"documents/{filename}"

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    store_chunks(
        chunks,
        embeddings,
        filename
    )

    return {
        "message": "Chunks stored successfully",
        "filename": filename,
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0])
    }


@app.get("/search")
def semantic_search(query: str):

    query_embedding = generate_query_embedding(query)

    results = search_chunks(query_embedding, n_results=5)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    search_results = []

    for i in range(len(documents)):

        # Ignore weakly related results
        if distances[i] <= 1.3:

            search_results.append({
                "content": documents[i],
                "source": metadatas[i]["filename"],
                "chunk_index": metadatas[i]["chunk_index"],
                "distance": distances[i]
            })

    # If nothing passes the threshold, use the best result
    if not search_results and documents:

        search_results.append({
            "content": documents[0],
            "source": metadatas[0]["filename"],
            "chunk_index": metadatas[0]["chunk_index"],
            "distance": distances[0]
        })

    answer = generate_rag_answer(
        query,
        search_results
    )

    return {
        "query": query,
        "answer": answer,
        "sources": search_results
    }