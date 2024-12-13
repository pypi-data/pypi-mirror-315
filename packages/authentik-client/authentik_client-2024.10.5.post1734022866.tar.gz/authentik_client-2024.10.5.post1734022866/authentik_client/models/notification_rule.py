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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.group import Group
from authentik_client.models.severity_enum import SeverityEnum
from typing import Optional, Set
from typing_extensions import Self

class NotificationRule(BaseModel):
    """
    NotificationRule Serializer
    """ # noqa: E501
    pk: StrictStr
    name: StrictStr
    transports: Optional[List[StrictStr]] = Field(default=None, description="Select which transports should be used to notify the user. If none are selected, the notification will only be shown in the authentik UI.")
    severity: Optional[SeverityEnum] = Field(default=None, description="Controls which severity level the created notifications will have.")
    group: Optional[StrictStr] = Field(default=None, description="Define which group of users this notification should be sent and shown to. If left empty, Notification won't ben sent.")
    group_obj: Group
    __properties: ClassVar[List[str]] = ["pk", "name", "transports", "severity", "group", "group_obj"]

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
        """Create an instance of NotificationRule from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "pk",
            "group_obj",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of group_obj
        if self.group_obj:
            _dict['group_obj'] = self.group_obj.to_dict()
        # set to None if group (nullable) is None
        # and model_fields_set contains the field
        if self.group is None and "group" in self.model_fields_set:
            _dict['group'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of NotificationRule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "name": obj.get("name"),
            "transports": obj.get("transports"),
            "severity": obj.get("severity"),
            "group": obj.get("group"),
            "group_obj": Group.from_dict(obj["group_obj"]) if obj.get("group_obj") is not None else None
        })
        return _obj


