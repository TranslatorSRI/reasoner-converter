"""TRAPI 0.9.2 to 1.0.0."""
from collections import defaultdict

from .util import ensure_list, pascal_case, snake_case


def upgrade_BiolinkEntity(biolink_entity):
    """Upgrade BiolinkEntity from 0.9.2 to 1.0.0."""
    if biolink_entity.startswith("biolink:"):
        return biolink_entity
    return "biolink:" + pascal_case(biolink_entity)


def upgrade_BiolinkRelation(biolink_relation):
    """Upgrade BiolinkRelation from 0.9.2 to 1.0.0."""
    if biolink_relation.startswith("biolink:"):
        return biolink_relation
    return "biolink:" + snake_case(biolink_relation)


def upgrade_Node(node):
    """Upgrade Node from 0.9.2 to 1.0.0."""
    new = dict()
    if "type" in node:
        new["category"] = [
            upgrade_BiolinkEntity(node_type)  # node.type is a list[str]
            for node_type in node["type"]
        ]
    if "name" in node:
        new["name"] = node["name"]
    return new


def upgrade_Edge(edge):
    """Upgrade Edge from 0.9.2 to 1.0.0."""
    return {
        "predicate": upgrade_BiolinkRelation(edge["type"]),
        "subject": edge["source_id"],
        "object": edge["target_id"],
    }


def upgrade_KnowledgeGraph(kgraph):
    """Upgrade KnowledgeGraph from 0.9.2 to 1.0.0."""
    return {
        "nodes": {
            knode["id"]: upgrade_Node(knode)
            for knode in kgraph["nodes"]
        },
        "edges": {
            kedge["id"]: upgrade_Edge(kedge)
            for kedge in kgraph["edges"]
        },
    }


def upgrade_QNode(qnode):
    """Upgrade QNode from 0.9.2 to 1.0.0."""
    new = dict()
    if "type" in qnode:
        new["category"] = upgrade_BiolinkEntity(qnode["type"])
    if "curie" in qnode:
        new["id"] = qnode["curie"]
    return new


def upgrade_QEdge(qedge):
    """Upgrade QEdge from 0.9.2 to 1.0.0."""
    new = {
        "subject": qedge["source_id"],
        "object": qedge["target_id"],
    }
    if "type" in qedge:
        new["predicate"] = upgrade_BiolinkRelation(qedge["type"])
    return new


def upgrade_QueryGraph(qgraph):
    """Upgrade QueryGraph from 0.9.2 to 1.0.0."""
    return {
        "nodes": {
            qnode["id"]: upgrade_QNode(qnode)
            for qnode in qgraph["nodes"]
        },
        "edges": {
            qedge["id"]: upgrade_QEdge(qedge)
            for qedge in qgraph["edges"]
        },
    }


def upgrade_NodeBinding(node_binding):
    """Upgrade NodeBinding from 0.9.2 to 1.0.0."""
    for kg_id in ensure_list(node_binding["kg_id"]):
        new = {
            "id": kg_id,
        }
        for key, value in node_binding.items():
            if key in ("qg_id", "kg_id"):
                continue
            new[key] = value
        yield new


def upgrade_EdgeBinding(edge_binding):
    """Upgrade EdgeBinding from 0.9.2 to 1.0.0."""
    for kg_id in ensure_list(edge_binding["kg_id"]):
        new = {
            "id": kg_id,
        }
        for key, value in edge_binding.items():
            if key == "qg_id":
                continue
            new[key] = value
        yield new


def upgrade_Result(result):
    """Upgrade Result from 0.9.2 to 1.0.0."""
    new = {
        "node_bindings": defaultdict(list),
        "edge_bindings": defaultdict(list),
    }
    for node_binding in result["node_bindings"]:
        new["node_bindings"][node_binding["qg_id"]].extend(
            upgrade_NodeBinding(node_binding)
        )
    for edge_binding in result["edge_bindings"]:
        new["edge_bindings"][edge_binding["qg_id"]].extend(
            upgrade_EdgeBinding(edge_binding)
        ) 
    return new


def upgrade_Message(message):
    """Upgrade Message from 0.9.2 to 1.0.0."""
    return {
        "query_graph": upgrade_QueryGraph(message["query_graph"]),
        "knowledge_graph": upgrade_KnowledgeGraph(message["knowledge_graph"]),
        "results": [
            upgrade_Result(result)
            for result in message["results"]
        ],
    }


def upgrade_Query(query):
    """Upgrade Query from 0.9.2 to 1.0.0."""
    return {
        "message": upgrade_Message(query["message"]),
    }
