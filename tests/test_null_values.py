"""Test downgrading with null-valued (optional) properties."""
from reasoner_converter.downgrading import (
    downgrade_Node, downgrade_Edge,
    downgrade_QNode, downgrade_QEdge,
    downgrade_Message,
)

from .util.validators import validate1


def test_node_nulls():
    """Test Node with null category/id"""
    x1 = {
        "category": None,
        "name": None,
        "attributes": None,
    }
    validate1(x1, "Node")
    x0 = downgrade_Node(x1, "XXX:YYY")
    assert x0 == {
        "id": "XXX:YYY"
    }


def test_edge_nulls():
    """Test Edge with null predicate/relation."""
    x1 = {
        "subject": "XXX:YYY",
        "object": "XXX:ZZZ",
        "predicate": None,
        "relation": None,
    }
    validate1(x1, "Edge")
    x0 = downgrade_Edge(x1, "xxx")
    assert x0 == {
        "id": "xxx",
        "source_id": "XXX:YYY",
        "target_id": "XXX:ZZZ",
    }


def test_qnode_nulls():
    """Test QNode with null category/id"""
    x1 = {
        "category": None,
        "id": None,
    }
    validate1(x1, "QNode")
    x0 = downgrade_QNode(x1, "n0")
    assert x0 == {
        "id": "n0"
    }


def test_qedge_nulls():
    """Test QEdge with null predicate/relation"""
    x1 = {
        "subject": "n0",
        "object": "n1",
        "predicate": None,
        "relation": None,
    }
    validate1(x1, "QEdge")
    x0 = downgrade_QEdge(x1, "e0")
    assert x0 == {
        "id": "e0",
        "source_id": "n0",
        "target_id": "n1",
    }


def test_message_nulls():
    """Test Message with null query_graph/knowledge_graph/results."""
    x1 = {
        "query_graph": None,
        "knowledge_graph": None,
        "results": None,
    }
    validate1(x1, "Message")
    x0 = downgrade_Message(x1)
    assert x0 == {}
