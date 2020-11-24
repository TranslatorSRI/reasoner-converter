"""Test interface conversions."""
from reasoner_converter.interfaces import downgrade_reasoner, upgrade_reasoner


def test_downgrade():
    """Test downgrading interface."""

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
    fcn = lambda x: x
    output = downgrade_reasoner(fcn)(query0)


def test_upgrade():
    """Test upgrading interface."""
    query1 = {
        "message": {
            "query_graph": {
                "nodes": {
                    "n0": {
                        "category": "biolink:Disease"
                    }
                },
                "edges": {
                    "e01": {
                        "subject": "n0",
                        "object": "n1",
                        "predicate": "biolink:related_to"
                    }
                }
            },
            "knowledge_graph": {
                "nodes": {
                    "MONDO:0005737": {
                        "category": [
                            "biolink:Disease"
                        ]
                    }
                },
                "edges": {
                    "xxx": {
                        "predicate": "biolink:related_to",
                        "subject": "yyy:123",
                        "object": "zzz:456"
                    }
                }
            },
            "results": [
                {
                    "node_bindings": {
                        "n0": [
                            {
                                "id": "MONDO:0005737"
                            }
                        ]
                    },
                    "edge_bindings": {
                        "e01": [
                            {
                                "id": "xxx",
                                "kg_id": "xxx"
                            }
                        ]
                    }
                }
            ]
        }
    }
    fcn = lambda x: x["message"]
    output = upgrade_reasoner(fcn)(query1)
