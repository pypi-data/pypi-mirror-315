"""FastAPI server for MistralVDB."""

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
from ..vectordb import MistralVDB
from .auth import (
    Token,
    User,
    USERS,
    create_access_token,
    verify_password,
    get_current_user
)

app = FastAPI(title="MistralVDB API")
security = HTTPBearer()

# Store VectorDB instances
vector_dbs: Dict[str, MistralVDB] = {}

class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str

class SearchRequest(BaseModel):
    """Search request model."""
    query: str
    k: Optional[int] = 4
    collection_name: Optional[str] = "default"

class AddTextsRequest(BaseModel):
    """Add texts request model."""
    texts: List[str]
    metadata: Optional[List[Dict[str, Any]]] = None
    collection_name: Optional[str] = "default"

class CollectionRequest(BaseModel):
    """Collection management request model."""
    collection_name: str

@app.post("/token", response_model=Token)
async def login(request: LoginRequest):
    """Login to get access token."""
    user = USERS.get(request.username)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token({"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_db(collection_name: str = "default") -> MistralVDB:
    """Get or create VectorDB instance."""
    if collection_name not in vector_dbs:
        # Initialize with environment variables in production
        vector_dbs[collection_name] = MistralVDB(
            api_key="your-mistral-api-key",  # Use environment variable
            collection_name=collection_name
        )
    return vector_dbs[collection_name]

@app.post("/add_texts")
async def add_texts(
    request: AddTextsRequest,
    current_user: str = Depends(get_current_user)
):
    """Add texts to the database."""
    db = get_db(request.collection_name)
    try:
        ids = db.add_texts(request.texts, request.metadata)
        return {"status": "success", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(
    request: SearchRequest,
    current_user: str = Depends(get_current_user)
):
    """Search for similar documents."""
    db = get_db(request.collection_name)
    try:
        results = db.search(request.query, k=request.k)
        response = []
        for doc_id, score in results:
            response.append({
                "id": doc_id,
                "score": float(score),
                "text": db.get_text(doc_id),
                "metadata": db.get_metadata(doc_id)
            })
        return {"results": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections(
    current_user: str = Depends(get_current_user)
):
    """List all collections."""
    try:
        db = get_db()
        return {"collections": db.list_collections()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collection/{collection_name}")
async def get_collection_info(
    collection_name: str,
    current_user: str = Depends(get_current_user)
):
    """Get collection information."""
    try:
        db = get_db(collection_name)
        return {"info": db.get_collection_info()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/collection/{collection_name}")
async def delete_collection(
    collection_name: str,
    current_user: str = Depends(get_current_user)
):
    """Delete a collection."""
    try:
        db = get_db(collection_name)
        db.delete_collection()
        if collection_name in vector_dbs:
            del vector_dbs[collection_name]
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    mistral_api_key: str = None,
    jwt_secret_key: str = None
):
    """Start the API server."""
    if mistral_api_key:
        # Set Mistral API key for VectorDB instances
        global vector_dbs
        vector_dbs = {}  # Clear existing instances
    
    if jwt_secret_key:
        # Update JWT secret key
        from .auth import AuthConfig
        AuthConfig.SECRET_KEY = jwt_secret_key
    
    uvicorn.run(app, host=host, port=port)
