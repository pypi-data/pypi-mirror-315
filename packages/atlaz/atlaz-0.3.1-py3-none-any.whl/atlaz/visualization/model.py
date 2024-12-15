from typing import List, Optional
from pydantic import BaseModel, Field # type: ignore

class Node(BaseModel):
    id: str = Field(..., description="Unique identifier of the node.")
    label: str = Field(..., description="Human-readable label of the node.")
    color: str = Field(..., description="Color used to represent the node.")
    shape: str = Field(..., description="Shape used to represent the node, e.g., 'ellipse', 'box', etc.")

class Edge(BaseModel):
    source: str = Field(..., description="ID of the source node.")
    target: str = Field(..., description="ID of the target node.")
    type: Optional[str] = Field(None, description="Type of relationship, e.g., 'subtype' or 'dependency'.")
    color: str = Field(..., description="Color used to represent the edge.")
    arrowhead: str = Field(..., description="Shape of the arrowhead, e.g., 'normal', 'diamond'.")
    label: Optional[str] = Field(None, description="Optional label for the edge relationship.")

class Cluster(BaseModel):
    name: str = Field(..., description="Name of the cluster.")
    color: str = Field(..., description="Color used to represent the cluster.")
    nodes: List[str] = Field(..., description="List of node IDs that belong to this cluster.")

class Graph(BaseModel):
    nodes: List[Node] = Field(..., description="List of nodes in the graph.")
    edges: List[Edge] = Field(..., description="List of edges in the graph.")
    clusters: List[Cluster] = Field(..., description="List of clusters grouping nodes.")