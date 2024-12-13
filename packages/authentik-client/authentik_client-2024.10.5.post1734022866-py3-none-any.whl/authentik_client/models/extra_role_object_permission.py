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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ExtraRoleObjectPermission(BaseModel):
    """
    User permission with additional object-related data
    """ # noqa: E501
    id: StrictInt
    codename: StrictStr
    model: StrictStr
    app_label: StrictStr
    object_pk: StrictStr
    name: StrictStr
    app_label_verbose: StrictStr = Field(description="Get app label from permission's model")
    model_verbose: StrictStr = Field(description="Get model label from permission's model")
    object_description: Optional[StrictStr] = Field(description="Get model description from attached model. This operation takes at least one additional query, and the description is only shown if the user/role has the view_ permission on the object")
    __properties: ClassVar[List[str]] = ["id", "codename", "model", "app_label", "object_pk", "name", "app_label_verbose", "model_verbose", "object_description"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ExtraRoleObjectPermission from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "codename",
            "model",
            "app_label",
            "name",
            "app_label_verbose",
            "model_verbose",
            "object_description",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if object_description (nullable) is None
        # and model_fields_set contains the field
        if self.object_description is None and "object_description" in self.model_fields_set:
            _dict['object_description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ExtraRoleObjectPermission from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "codename": obj.get("codename"),
            "model": obj.get("model"),
            "app_label": obj.get("app_label"),
            "object_pk": obj.get("object_pk"),
            "name": obj.get("name"),
            "app_label_verbose": obj.get("app_label_verbose"),
            "model_verbose": obj.get("model_verbose"),
            "object_description": obj.get("object_description")
        })
        return _obj


