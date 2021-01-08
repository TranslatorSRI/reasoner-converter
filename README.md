# Reasoner Converter

[![github actions](https://github.com/translatorsri/reasoner-converter/workflows/tests/badge.svg)](https://github.com/TranslatorSRI/reasoner-converter/actions?query=workflow%3Atests)
[![codecov](https://codecov.io/gh/TranslatorSRI/reasoner-converter/branch/main/graph/badge.svg?token=tVG6HrqIvD)](https://codecov.io/gh/TranslatorSRI/reasoner-converter)

Reasoner Converter provides conversion between TRAPI versions [0.9.2](https://github.com/NCATSTranslator/ReasonerAPI/tree/v0.9.2) and [1.0.0](https://github.com/NCATSTranslator/ReasonerAPI/tree/v1.0.0-beta).

Jump to:

* [Python API](#python-api)
* [backwards compatibility](#backwards-compatibility)
* [0.9.2 → 1.0.0 changes](#092--100-changes)

---

## Python API

```python
from reasoner_converter.upgrading import upgrade_Node
from reasoner_converter.downgrading import downgrade_Node

knode0 = {
    "id": "MONDO:0005737",
    "type": ["disease"],
}
knode1 = upgrade_Node(knode0)
knode0 == downgrade_Node(knode1)
```

---

## Backwards compatibility

The following are required to downgrade 1.0.0 → 0.9.2:

* QNode.category is a string or a list of length 1
* QEdge.predicate is a string or a list of length 1

---

## 0.9.2 → 1.0.0 changes

* `/query` returns: `Message` → `Response`
  * `Response` has required property `message`

### Message

* additional properties are: allowed → not allowed

### KnowledgeGraph

* `.nodes` is: an array of objects with required prop `id` → a map with keys equivalent to `id`
* `.edges` is: an array of objects with required prop `id` → a map with keys equivalent to `id`

### Node

* `.type` → `.category`
* `.category` is: an array of strings → a string or an array of strings
* additional properties are: allowed → not allowed

### Edge

* `.type` → `.predicate`
* `.source_id` → `.subject`
* `.target_id` → `.object`
* additional properties are: allowed → not allowed

### QueryGraph

* `.nodes` is: an array of objects with required prop `id` → a map with keys equivalent to `id`
* `.edges` is: an array of objects with required prop `id` → a map with keys equivalent to `id`

### QNode

* `.type` → `.category`
* `.category` is: a string → a string or an array of strings
* `.curie` → `.id`

### QEdge

* `.type` → `.predicate`
* `.predicate` is: a `BiolinkRelation` → a `BiolinkPredicate` or an array of `BiolinkPredicate`s
* `.source_id` → `.subject`
* `.target_id` → `.object`

### Result

* `.node_bindings` is: an array of objects with required prop `qg_id` → a map with keys equivalent to `qg_id` and array values
* `.edge_bindings` is: an array of objects with required prop `qg_id` → a map with keys equivalent to `qg_id` and array values

### NodeBinding

* `.kg_id` → `.id`
* `.id` can be: a string or an array of strings → a string

### EdgeBinding

* `.kg_id` → `.id`
* `.id` can be: a string or an array of strings → a string

### BiolinkEntity

* string → "biolink:PascalCase"

### Biolink~~Relation~~Predicate

* string → "biolink:snake_case"
