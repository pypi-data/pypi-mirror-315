# coding: utf-8

"""
    authentik

    Making authentication simple.

    The version of the OpenAPI document: 2024.10.5
    Contact: hello@goauthentik.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class ResidentKeyRequirementEnum(str, Enum):
    """
    ResidentKeyRequirementEnum
    """

    """
    allowed enum values
    """
    DISCOURAGED = 'discouraged'
    PREFERRED = 'preferred'
    REQUIRED = 'required'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ResidentKeyRequirementEnum from a JSON string"""
        return cls(json.loads(json_str))


