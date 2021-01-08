"""Validators."""
import copy

import httpx
import jsonschema
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def fix_nullable(schema):
    """Replace nullable: true with json schema-compliant alternative."""
    if "$ref" in schema:
        return schema
    if "oneOf" in schema:
        if schema.pop("nullable", False):
            schema["oneOf"].append({"type": "null"})
    elif "allOf" in schema:
        if schema.pop("nullable", False):
            if len(schema["allOf"]) == 1:
                schema["oneOf"] = [
                    schema.pop("allOf")[0],
                    {"type": "null"},
                ]
            else:
                schema["oneOf"] = [
                    schema.pop("allOf"),
                    {"type": "null"},
                ]
    elif "type" in schema:
        if schema["type"] == "object":
            if "properties" in schema:
                schema["properties"] = {
                    pname: fix_nullable(property)
                    for pname, property in schema["properties"].items()
                }
            if "additionalProperties" in schema and isinstance(schema["additionalProperties"], dict):
                schema["additionalProperties"] = fix_nullable(schema["additionalProperties"])
        if schema.pop("nullable", False):
            schema = {
                "oneOf": [
                    schema,
                    {"type": "null"}
                ]
            }
    return schema


response = httpx.get("https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/v0.9.2/API/TranslatorReasonersAPI.yaml")
response.raise_for_status()
schema0 = response.text

response = httpx.get("https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/fix-nullable-$ref/TranslatorReasonerAPI.yaml")
response.raise_for_status()
schema1 = response.text

spec = yaml.load(schema0, Loader=Loader)
components0 = spec['components']['schemas']

spec = yaml.load(schema1, Loader=Loader)
components1 = spec['components']['schemas']
components1 = {
    cname: fix_nullable(component)
    for cname, component in components1.items()
}


def validate0(obj, component_name):
    """Validate object against schema."""
    # build json schema against which we validate
    other_components = copy.deepcopy(components0)
    schema = other_components.pop(component_name)
    schema['components'] = {'schemas': other_components}

    jsonschema.validate(obj, schema)


def validate1(obj, component_name):
    """Validate object against schema."""
    # build json schema against which we validate
    other_components = copy.deepcopy(components1)
    schema = other_components.pop(component_name)
    schema['components'] = {'schemas': other_components}

    jsonschema.validate(obj, schema)
