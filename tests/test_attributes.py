"""Test handling additional properties and `attributes`."""
from reasoner_converter.downgrading import (
    downgrade_Node, downgrade_Edge,
)
from reasoner_converter.upgrading import (
    upgrade_Node, upgrade_Edge,
)

from .util.validators import validate0, validate1


def test_node_attributes():
    """Test node attribute handling."""
    x0a = {
        "id": "XXX:YYY",
        "a": 1,
        "b": 2,
        "c": 3,
    }
    validate0(x0a, "Node")
    x1 = upgrade_Node(x0a)
    validate1(x1, "Node")
    x0b = downgrade_Node(x1, x0a["id"])
    assert x0a == x0b


def test_edge_attributes():
    """Test edge attribute handling."""
    x0a = {
        "id": "xxx",
        "source_id": "XXX:YYY",
        "target_id": "XXX:ZZZ",
        "a": 1,
        "b": 2,
        "c": 3,
    }
    validate0(x0a, "Edge")
    x1 = upgrade_Edge(x0a)
    validate1(x1, "Edge")
    x0b = downgrade_Edge(x1, x0a["id"])
    assert x0a == x0b
