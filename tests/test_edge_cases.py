"""Test edge cases."""
import pytest

from reasoner_converter.upgrading import (
    upgrade_Query, upgrade_Message,
    upgrade_Node, upgrade_Edge,
    upgrade_QNode, upgrade_QEdge,
    upgrade_Result,
)
from reasoner_converter.downgrading import (
    downgrade_Query,
    downgrade_QNode, downgrade_QEdge,
    downgrade_Result,
)

from .util.validators import validate0, validate1


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


def test_missing_message_props():
    """Test missing Message properties."""
    x0 = {}
    validate0(x0, "Message")
    x1 = upgrade_Message(x0)
    validate1(x1, "Message")


def test_addl_query_props():
    """Test additional Query properties."""
    x0a = {
        "message": {},
        "a": 1,
        "b": 2,
        "c": 3,
    }
    validate0(x0a, "Query")
    x1 = upgrade_Query(x0a)
    validate1(x1, "Query")
    x0b = downgrade_Query(x1)
    assert x0a == x0b


def test_addl_binding_props():
    """Test additional Node/EdgeBinding properties."""
    x0 = {
        "node_bindings": [{
            "qg_id": "n0",
            "kg_id": "XXX:YYY",
            "a": 1,
        }],
        "edge_bindings": [{
            "qg_id": "e01",
            "kg_id": "xxx",
            "b": 2,
        }],
    }
    validate0(x0, "Result")
    x1 = upgrade_Result(x0)
    assert x1 == {
        "node_bindings": {
            "n0": [{
                "id": "XXX:YYY",
                "a": 1,
            }],
        },
        "edge_bindings": {
            "e01": [{
                "id": "xxx",
                "b": 2,
            }],
        }
    }


def test_addl_result_props():
    """Test additional Result properties."""
    x0 = {
        "node_bindings": [{
            "qg_id": "n0",
            "kg_id": "XXX:YYY",
        }],
        "edge_bindings": [{
            "qg_id": "e01",
            "kg_id": "xxx",
        }],
        "a": 1,
        "b": 2,
    }
    validate0(x0, "Result")
    x1 = upgrade_Result(x0)
    validate1(x1, "Result")
    x0b = downgrade_Result(x1)
    assert x0 == x0b


def test_addl_qnode_props():
    """Test additional QNode properties."""
    x0a = {
        "id": "n0",
        "a": 1,
        "b": 2,
    }
    validate0(x0a, "QNode")
    x1 = upgrade_QNode(x0a)
    validate1(x1, "QNode")
    x0b = downgrade_QNode(x1, "n0")
    assert x0a == x0b


def test_addl_qedge_props():
    """Test additional QEdge properties."""
    x0a = {
        "id": "e01",
        "source_id": "n0",
        "target_id": "n1",
        "a": 1,
        "b": 2,
    }
    validate0(x0a, "QEdge")
    x1 = upgrade_QEdge(x0a)
    validate1(x1, "QEdge")
    x0b = downgrade_QEdge(x1, "e01")
    assert x0a == x0b
