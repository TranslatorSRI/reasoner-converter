"""Test edge cases."""
import pytest

from reasoner_converter.upgrading import upgrade_Node, upgrade_Edge
from reasoner_converter.downgrading import downgrade_QNode, downgrade_QEdge


def test_092_node_type_curie():
    """Test upgrading a 0.9.2 node type that's already a CURIE."""
    knode0 = {
        "id": "MONDO:0005737",
        "type": ["biolink:Disease"],
    }
    knode1 = upgrade_Node(knode0)
    assert knode1 == {
        "category": ["biolink:Disease"],
    }


def test_092_edge_type_curie():
    """Test upgrading a 0.9.2 edge type that's already a CURIE."""
    kedge0 = {
        "id": "xxx",
        "type": "biolink:related_to",
        "source_id": "MONDO:0005737",
        "target_id": "HGNC:4897",
    }
    kedge1 = upgrade_Edge(kedge0)
    assert kedge1 == {
        "predicate": "biolink:related_to",
        "subject": "MONDO:0005737",
        "object": "HGNC:4897",
    }

def test_no_edge_type():
    """Test upgrading a 0.9.2 edge without a type."""
    kedge0 = {
        "id": "xxx",
        "source_id": "MONDO:0005737",
        "target_id": "HGNC:4897",
    }
    kedge1 = upgrade_Edge(kedge0)
    assert kedge1 == {
        "subject": "MONDO:0005737",
        "object": "HGNC:4897",
    }

def test_none_edge_type():
    """Test upgrading a 0.9.2 edge without an edge that has type:None."""
    kedge0 = {
        "id": "xxx",
        "type": None,
        "source_id": "MONDO:0005737",
        "target_id": "HGNC:4897",
    }
    kedge1 = upgrade_Edge(kedge0)
    assert kedge1 == {
        "predicate": None,
        "subject": "MONDO:0005737",
        "object": "HGNC:4897",
    }

def test_100_qnode_category_list():
    """Test downgrading a 1.0.0 qnode category that's a list."""
    qnode1 = {
        "category": ["biolink:Disease"],
    }
    qnode0 = downgrade_QNode(qnode1, "n0")
    assert qnode0 == {
        "id": "n0",
        "type": "disease",
    }

    qnode1 = {
        "category": ["biolink:Disease", "biolink:NamedThing"],
    }
    with pytest.raises(ValueError):
        qnode0 = downgrade_QNode(qnode1, "n0")


def test_100_qedge_predicate_list():
    """Test downgrading a 1.0.0 qedge predicate that's a list."""
    qedge1 = {
        "predicate": ["biolink:affects"],
        "subject": "n0",
        "object": "n1",
    }
    qedge0 = downgrade_QEdge(qedge1, "e01")
    assert qedge0 == {
        "id": "e01",
        "type": "affects",
        "source_id": "n0",
        "target_id": "n1",
    }

    qedge1 = {
        "predicate": ["biolink:affects", "biolink:related_to"],
        "subject": "n0",
        "object": "n1",
    }
    with pytest.raises(ValueError):
        qedge0 = downgrade_QEdge(qedge1, "n0")
