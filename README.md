# langchain_mongodb_atlas_management
Easily manage MongoDB Atlas vector search with LangChain using OpenAI or HuggingFace embeddings.

## install

```bash
git clone https://github.com/BWKBH/langchain_mongodb_atlas_management.git
cd langchain_mongodb_atlas_management
pip install -e .
pip install -r requirements.txt
```

# 🧰 Project Structure
```
langchain_mongodb_atlas_management/src
  ├── __init__.py
  ├── vector_index_manager.py   # VectorIndexManager
  └── mongodb_model.py          # MongoDBModel
```
  
## 🧩 Core Classes

### 1. VectorIndexManager
**Role**: Create or drop vector indexes in MongoDB Atlas.

```python
from mongodb_atlas import VectorIndexManager

manager = VectorIndexManager(
    db_name="ragdb",
    collection_name="docs",
    uri_name="MONGODB_ATLAS_URI"
)

# Create vector index
manager.create_hnsw_index(
    index_name="hnsw_index",
    dimensions=1536,
    attribute_name="embedding",
    similarity="cosine",
    filter_attribute_names=["source", "tags"]
)

# Drop vector index
manager.drop_hnsw_index("hnsw_index")
```

### 2. MongoDBModel
**Role**: Manage documents and configure the vector store.

```python
from mongodb_atlas import MongoDBModel

db = MongoDBModel(DB_name="ragdb", collection_name="docs", uri_name="MONGODB_ATLAS_URI")

# Delete all documents
db.delete_all_documents()

# Count documents
print(db.count_number_of_documents())

# Retrieve documents
print(db.get_all_documents())

# Set up vector store (OpenAI embeddings)
vector_store = db.set_vector_store(
    relevance_scores="cosine",
    index_name="hnsw_index",
    embedding_model="text-embedding-3-small",
    api_key_name="OPENAI_API_KEY"
)```
