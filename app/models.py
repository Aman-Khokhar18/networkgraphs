from pydantic import BaseModel
from typing import Any, Dict, List

class Node(BaseModel):
    id: str
    label: str
    type: str
    props: Dict[str, Any] = {}

class Edge(BaseModel):
    source: str
    target: str
    label: str

class GraphResponse(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
