"""Validators."""
import copy

import httpx
import jsonschema
import yaml
from yaml import Loader

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
