"""TRAPI 1.0.0 to 0.9.2."""
from .util import ensure_list, snake_case

def downgrade_BiolinkEntity(biolink_entity):
    """Downgrade BiolinkEntity from 1.0.0 to 0.9.2."""
    return snake_case(biolink_entity[8:])


def downgrade_BiolinkRelation(biolink_relation):
    """Downgrade BiolinkRelation from 1.0.0 to 0.9.2."""
    return biolink_relation[8:]


def downgrade_Node(node, id_):
    """Downgrade Node from 1.0.0 to 0.9.2."""
    new = {"id": id_}
    if "category" in node:
        new["type"] = [
            downgrade_BiolinkEntity(node_type)
            for node_type in ensure_list(node["category"])
        ]
    if "name" in node:
        new["name"] = node["name"]
    return new


def downgrade_Edge(edge, id_):
    """Downgrade Edge from 1.0.0 to 0.9.2."""
    return {
        "id": id_,
        "type": downgrade_BiolinkRelation(edge["predicate"]),
        "source_id": edge["subject"],
        "target_id": edge["object"],
    }


def downgrade_KnowledgeGraph(kgraph):
    """Downgrade KnowledgeGraph from 1.0.0 to 0.9.2."""
    return {
        "nodes": [
            downgrade_Node(knode, id_)
            for id_, knode in kgraph["nodes"].items()
        ],
        "edges": [
            downgrade_Edge(kedge, id_)
            for id_, kedge in kgraph["edges"].items()
        ],
    }


def downgrade_QNode(qnode, id_):
    """Downgrade QNode from 1.0.0 to 0.9.2."""
    new = {"id": id_}
    if "category" in qnode:
        if isinstance(qnode["category"], list):
            if len(qnode["category"]) > 1:
                raise ValueError("QNode with multiple categories is not backwards-compatible")
            new["type"] = downgrade_BiolinkEntity(qnode["category"][0])
        else:
            new["type"] = downgrade_BiolinkEntity(qnode["category"])
    if "id" in qnode:
        new["curie"] = qnode["id"]
    return new


def downgrade_QEdge(qedge, id_):
    """Downgrade QEdge from 1.0.0 to 0.9.2."""
    new = {
        "id": id_,
        "source_id": qedge["subject"],
        "target_id": qedge["object"],
    }
    if "predicate" in qedge:
        if isinstance(qedge["predicate"], list):
            if len(qedge["predicate"]) > 1:
                raise ValueError("QEdge with multiple predicates is not backwards-compatible")
            new["type"] = downgrade_BiolinkRelation(qedge["predicate"][0])
        else:
            new["type"] = downgrade_BiolinkRelation(qedge["predicate"])
    return new


def downgrade_QueryGraph(qgraph):
    """Downgrade QueryGraph from 1.0.0 to 0.9.2."""
    return {
        "nodes": [
            downgrade_QNode(qnode, id_)
            for id_, qnode in qgraph["nodes"].items()
        ],
        "edges": [
            downgrade_QEdge(qedge, id_)
            for id_, qedge in qgraph["edges"].items()
        ],
    }


def downgrade_NodeBinding(node_binding, qg_id):
    """Downgrade NodeBinding from 1.0.0 to 0.9.2."""
    new = {
        "qg_id": qg_id,
        "kg_id": node_binding["id"],
    }
    for key, value in node_binding.items():
        if key == "id":
            continue
        new[key] = value
    return new


def downgrade_EdgeBinding(edge_binding, qg_id):
    """Downgrade EdgeBinding from 1.0.0 to 0.9.2."""
    new = {
        "qg_id": qg_id,
        "kg_id": edge_binding["id"],
    }
    for key, value in edge_binding.items():
        if key == "id":
            continue
        new[key] = value
    return new


def downgrade_Result(result):
    """Downgrade Result from 1.0.0 to 0.9.2."""
    new = {
        "node_bindings": [],
        "edge_bindings": [],
    }
    for qg_id, nbs in result["node_bindings"].items():
        new["node_bindings"].extend(
            downgrade_NodeBinding(nb, qg_id)
            for nb in nbs
        )
    for qg_id, ebs in result["edge_bindings"].items():
        new["edge_bindings"].extend(
            downgrade_EdgeBinding(eb, qg_id)
            for eb in ebs
        ) 
    return new


def downgrade_Message(message):
    """Downgrade Message from 1.0.0 to 0.9.2."""
    return {
        "query_graph": downgrade_QueryGraph(message["query_graph"]),
        "knowledge_graph": downgrade_KnowledgeGraph(message["knowledge_graph"]),
        "results": [
            downgrade_Result(result)
            for result in message["results"]
        ],
    }


def downgrade_Query(query):
    """Downgrade Query from 1.0.0 to 0.9.2."""
    return {
        "message": downgrade_Message(query["message"]),
    }
