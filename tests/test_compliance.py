"""Test compliance of converted results with TRAPI specifications."""
import copy

import httpx
import jsonschema
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from reasoner_converter.upgrading import (
    upgrade_BiolinkEntity, upgrade_BiolinkRelation,
    upgrade_Node, upgrade_Edge, upgrade_KnowledgeGraph,
    upgrade_QNode, upgrade_QEdge, upgrade_QueryGraph,
    upgrade_NodeBinding, upgrade_EdgeBinding, upgrade_Result,
    upgrade_Message, upgrade_Query,
)
from reasoner_converter.downgrading import (
    downgrade_BiolinkEntity, downgrade_BiolinkRelation,
    downgrade_Node, downgrade_Edge, downgrade_KnowledgeGraph,
    downgrade_QNode, downgrade_QEdge, downgrade_QueryGraph,
    downgrade_NodeBinding, downgrade_EdgeBinding, downgrade_Result,
    downgrade_Message, downgrade_Query,
)

response = httpx.get("https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/v0.9.2/API/TranslatorReasonersAPI.yaml")
response.raise_for_status()
schema0 = response.text

response = httpx.get("https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/v1.0.0-beta/TranslatorReasonerAPI.yaml")
response.raise_for_status()
schema1 = response.text

spec = yaml.load(schema0, Loader=Loader)
components0 = spec['components']['schemas']

spec = yaml.load(schema1, Loader=Loader)
components1 = spec['components']['schemas']

def validate1(obj, component_name):
    """Validate object against schema."""
    # build json schema against which we validate
    other_components = copy.deepcopy(components1)
    schema = other_components.pop(component_name)
    schema['components'] = {'schemas': other_components}

    jsonschema.validate(obj, schema)


def validate0(obj, component_name):
    """Validate object against schema."""
    # build json schema against which we validate
    other_components = copy.deepcopy(components0)
    schema = other_components.pop(component_name)
    schema['components'] = {'schemas': other_components}

    jsonschema.validate(obj, schema)


def test_biolink_entity():
    """Test biolink_entity 0.9.2 -> 1.0.0."""
    bent0 = "disease"
    validate0(bent0, "BiolinkEntity")
    bent1 = upgrade_BiolinkEntity(bent0)
    validate1(bent1, "BiolinkEntity")
    bent0b = downgrade_BiolinkEntity(bent1)
    assert bent0 == bent0b


def test_biolink_relation():
    """Test biolink_relation 0.9.2 -> 1.0.0."""
    brel0 = "related_to"
    validate0(brel0, "BiolinkRelation")
    brel1 = upgrade_BiolinkRelation(brel0)
    validate1(brel1, "BiolinkRelation")
    brel0b = downgrade_BiolinkRelation(brel1)
    assert brel0 == brel0b


def test_knode():
    """Test knode 0.9.2 -> 1.0.0."""
    knode0 = {
        "id": "MONDO:0005737",
        "type": ["disease"],
        "name": "Ebola hemorrhagic fever",
    }
    validate0(knode0, "Node")
    knode1 = upgrade_Node(knode0)
    validate1(knode1, "Node")
    knode0b = downgrade_Node(knode1, "MONDO:0005737")
    assert knode0 == knode0b


def test_kedge():
    """Test kedge 0.9.2 -> 1.0.0."""
    kedge0 = {
        "id": "xxx",
        "type": "related_to",
        "source_id": "yyy:123",
        "target_id": "zzz:456",
    }
    validate0(kedge0, "Edge")
    kedge1 = upgrade_Edge(kedge0)
    validate1(kedge1, "Edge")
    kedge0b = downgrade_Edge(kedge1, "xxx")
    assert kedge0 == kedge0b


def test_kgraph():
    """Test kgraph 0.9.2 -> 1.0.0."""
    kgraph0 = {
        "nodes": [
            {
                "id": "MONDO:0005737",
                "type": ["disease"],
            }
        ],
        "edges": [
            {
                "id": "xxx",
                "type": "related_to",
                "source_id": "yyy:123",
                "target_id": "zzz:456",
            }
        ]
    }
    validate0(kgraph0, "KnowledgeGraph")
    kgraph1 = upgrade_KnowledgeGraph(kgraph0)
    validate1(kgraph1, "KnowledgeGraph")
    kgraph0b = downgrade_KnowledgeGraph(kgraph1)
    assert kgraph0 == kgraph0b


def test_qnode():
    """Test qnode 0.9.2 -> 1.0.0."""
    qnode0 = {
        "id": "n0",
        "type": "disease",
        "curie": "MONDO:0005737",
    }
    validate0(qnode0, "QNode")
    qnode1 = upgrade_QNode(qnode0)
    validate1(qnode1, "QNode")
    qnode0b = downgrade_QNode(qnode1, "n0")
    assert qnode0 == qnode0b


def test_qedge():
    """Test qedge 0.9.2 -> 1.0.0."""
    qedge0 = {
        "id": "e01",
        "type": "related_to",
        "source_id": "n0",
        "target_id": "n1",
    }
    validate0(qedge0, "QEdge")
    qedge1 = upgrade_QEdge(qedge0)
    validate1(qedge1, "QEdge")
    qedge0b = downgrade_QEdge(qedge1, "e01")
    assert qedge0 == qedge0b


def test_qgraph():
    """Test qgraph 0.9.2 -> 1.0.0."""
    qgraph0 = {
        "nodes": [
            {
                "id": "n0",
                "type": "disease",
            }
        ],
        "edges": [
            {
                "id": "e01",
                "type": "related_to",
                "source_id": "n0",
                "target_id": "n1",
            }
        ]
    }
    validate0(qgraph0, "QueryGraph")
    qgraph1 = upgrade_QueryGraph(qgraph0)
    validate1(qgraph1, "QueryGraph")
    qgraph0b = downgrade_QueryGraph(qgraph1)
    assert qgraph0 == qgraph0b


def test_node_binding():
    """Test node_binding 0.9.2 -> 1.0.0."""
    nb0 = {
        "qg_id": "n0",
        "kg_id": "MONDO:0005737",
        "score": 5.0,
    }
    validate0(nb0, "NodeBinding")
    nb1 = list(upgrade_NodeBinding(nb0))[0]
    validate1(nb1, "NodeBinding")
    nb0b = downgrade_NodeBinding(nb1, "n0")
    assert nb0 == nb0b


def test_edge_binding():
    """Test edge_binding 0.9.2 -> 1.0.0."""
    eb0 = {
        "qg_id": "e01",
        "kg_id": "xxx",
    }
    validate0(eb0, "EdgeBinding")
    eb1 = list(upgrade_EdgeBinding(eb0))[0]
    validate1(eb1, "EdgeBinding")
    eb0b = downgrade_EdgeBinding(eb1, "e01")
    assert eb0 == eb0b


def test_result():
    """Test result 0.9.2 -> 1.0.0."""
    result0 = {
        "node_bindings": [
            {
                "qg_id": "n0",
                "kg_id": "MONDO:0005737",
            },
        ],
        "edge_bindings": [
            {
                "qg_id": "e01",
                "kg_id": "xxx",
            },
        ],
    }
    validate0(result0, "Result")
    result1 = upgrade_Result(result0)
    validate1(result1, "Result")
    result0b = downgrade_Result(result1)
    assert result0 == result0b


def test_message():
    """Test message 0.9.2 -> 1.0.0."""
    message0 = {
        "query_graph": {
            "nodes": [
                {
                    "id": "n0",
                    "type": "disease",
                }
            ],
            "edges": [
                {
                    "id": "e01",
                    "type": "related_to",
                    "source_id": "n0",
                    "target_id": "n1",
                }
            ]
        },
        "knowledge_graph": {
            "nodes": [
                {
                    "id": "MONDO:0005737",
                    "type": ["disease"],
                }
            ],
            "edges": [
                {
                    "id": "xxx",
                    "type": "related_to",
                    "source_id": "yyy:123",
                    "target_id": "zzz:456",
                }
            ]
        },
        "results": [
            {
                "node_bindings": [
                    {
                        "qg_id": "n0",
                        "kg_id": "MONDO:0005737",
                    },
                ],
                "edge_bindings": [
                    {
                        "qg_id": "e01",
                        "kg_id": "xxx",
                    },
                ],
            }
        ]
    }
    validate0(message0, "Message")
    message1 = upgrade_Message(message0)
    validate1(message1, "Message")
    message0b = downgrade_Message(message1)
    assert message0 == message0b


def test_query():
    """Test query 0.9.2 -> 1.0.0."""
    query0 = {
        "message": {
            "query_graph": {
                "nodes": [
                    {
                        "id": "n0",
                        "type": "disease",
                    }
                ],
                "edges": [
                    {
                        "id": "e01",
                        "type": "related_to",
                        "source_id": "n0",
                        "target_id": "n1",
                    }
                ]
            },
            "knowledge_graph": {
                "nodes": [
                    {
                        "id": "MONDO:0005737",
                        "type": ["disease"],
                    }
                ],
                "edges": [
                    {
                        "id": "xxx",
                        "type": "related_to",
                        "source_id": "yyy:123",
                        "target_id": "zzz:456",
                    }
                ]
            },
            "results": [
                {
                    "node_bindings": [
                        {
                            "qg_id": "n0",
                            "kg_id": "MONDO:0005737",
                        },
                    ],
                    "edge_bindings": [
                        {
                            "qg_id": "e01",
                            "kg_id": "xxx",
                        },
                    ],
                }
            ]
        }
    }
    validate0(query0, "Query")
    query1 = upgrade_Query(query0)
    validate1(query1, "Query")
    query0b = downgrade_Query(query1)
    assert query0 == query0b
