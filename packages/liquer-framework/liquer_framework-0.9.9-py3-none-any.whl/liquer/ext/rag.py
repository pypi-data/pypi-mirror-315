"""
RAG (Retrieval-Augmented Generation) extension for Liquer
This uses the qdrant via (liquer.ext.lq_qdrant extension) to provide vector database and embeddings.

Dependencies:

    - fastembed
    - qdrant-client - install with pip install qdrant-client[fastembed]
    - langchain
    - langchain_community (CTransformers, e.g. for langchain_community.embeddings.fastembed)
    - CTransformers
    (- llama-cpp-python - requires compilation asof time of writing)
    (- langchain-ollama)
    (- ollama)

"""
