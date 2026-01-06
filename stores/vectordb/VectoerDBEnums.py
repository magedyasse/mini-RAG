from enum   import Enum


class VectoerDBEnums(Enum):

    PINECONE    = "Pinecone"
    WEAVIATE    = "Weaviate"
    CHROMA      = "Chroma"
    QDRANT      = "Qdrant"
    MILVUS      = "Milvus"
    VESPA       = "Vespa"
    OPENSEARCH  = "OpenSearch"
    ELASTICSEARCH = "Elasticsearch"

class DistanceMethodEnums(Enum):

    COSINE        = "cosine"
    EUCLIDEAN     = "euclidean" # L2
    MANHATTAN    = "manhattan" # L1
    HAMMING      = "hamming" 
    DOT   = "dot_product"
    L2_SQUARED   = "l2_squared" 
    CHEBYSHEV   = "chebyshev"
    JACCARD      = "jaccard"
