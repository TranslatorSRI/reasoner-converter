"""TRAPI 1.0.0 to 0.9.2."""
from .util import ensure_list, snake_case

def downgrade_BiolinkEntity(biolink_entity):
    """Downgrade BiolinkEntity from 1.0.0 to 0.9.2."""
    return snake_case(biolink_entity[8:])


def downgrade_BiolinkPredicate(biolink_predicate):
    """Downgrade BiolinkPredicate (1.0.0) to BiolinkRelation (0.9.2)."""
    return biolink_predicate[8:]


def downgrade_Node(node, id_):
    """Downgrade Node from 1.0.0 to 0.9.2."""
    new = {"id": id_}
    if node.get("category", None) is not None:
        new["type"] = [
            downgrade_BiolinkEntity(node_type)
            for node_type in ensure_list(node["category"])
        ]
    if node.get("name", None) is not None:
        new["name"] = node["name"]
    if node.get("attributes", None) is not None:
        new = {
            **new,
            **{
                attribute.get("name", f"attribute{idx:02d}"): attribute["value"]
                for idx, attribute in enumerate(node["attributes"])
            }
        }
    return new


def downgrade_Edge(edge, id_):
    """Downgrade Edge from 1.0.0 to 0.9.2."""
    new = {
        "id": id_,
        "source_id": edge["subject"],
        "target_id": edge["object"],
    }
    if edge.get("predicate", None) is not None:
        new["type"] = downgrade_BiolinkPredicate(edge["predicate"])
    if edge.get("relation", None) is not None:
        new["relation"] = edge["relation"]
    if edge.get("attributes", None) is not None:
        new = {
            **new,
            **{
                attribute.get("name", f"attribute{idx:02d}"): attribute["value"]
                for idx, attribute in enumerate(edge.get("attributes", []))
            }
        }
    return new


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
    qnode = {**qnode}
    new = {"id": id_}
    category = qnode.pop("category", None)
    if category is not None:
        if isinstance(category, list):
            if len(category) > 1:
                raise ValueError("QNode with multiple categories is not backwards-compatible")
            new["type"] = downgrade_BiolinkEntity(category[0])
        else:
            new["type"] = downgrade_BiolinkEntity(category)
    curie = qnode.pop("id", None)
    if curie is not None:
        new["curie"] = curie
    new = {
        **new,
        **qnode,
    }
    return new


def downgrade_QEdge(qedge, id_):
    """Downgrade QEdge from 1.0.0 to 0.9.2."""
    qedge = {**qedge}
    new = {
        "id": id_,
        "source_id": qedge.pop("subject"),
        "target_id": qedge.pop("object"),
    }
    predicate = qedge.pop("predicate", None)
    if predicate is not None:
        if isinstance(predicate, list):
            if len(predicate) > 1:
                raise ValueError("QEdge with multiple predicates is not backwards-compatible")
            new["type"] = downgrade_BiolinkPredicate(predicate[0])
        else:
            new["type"] = downgrade_BiolinkPredicate(predicate)
    relation = qedge.pop("relation", None)
    if relation is not None:
        new["relation"] = relation
    new = {
        **new,
        **qedge,
    }
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
    result = {**result}
    new = {
        "node_bindings": [],
        "edge_bindings": [],
    }
    for qg_id, nbs in result.pop("node_bindings").items():
        new["node_bindings"].extend(
            downgrade_NodeBinding(nb, qg_id)
            for nb in nbs
        )
    for qg_id, ebs in result.pop("edge_bindings").items():
        new["edge_bindings"].extend(
            downgrade_EdgeBinding(eb, qg_id)
            for eb in ebs
        )
    new = {
        **new,
        **result,
    }
    return new


def downgrade_Message(message):
    """Downgrade Message from 1.0.0 to 0.9.2."""
    new = dict()
    if message.get("query_graph", None) is not None:
        new["query_graph"] = downgrade_QueryGraph(message["query_graph"])
    if message.get("knowledge_graph", None) is not None:
        new["knowledge_graph"] = downgrade_KnowledgeGraph(message["knowledge_graph"])
    if message.get("results", None) is not None:
        new["results"] = [
            downgrade_Result(result)
            for result in message["results"]
        ]
    return new


def downgrade_Query(query):
    """Downgrade Query from 1.0.0 to 0.9.2."""
    query = {**query}
    return {
        "message": downgrade_Message(query.pop("message")),
        **query,
    }
