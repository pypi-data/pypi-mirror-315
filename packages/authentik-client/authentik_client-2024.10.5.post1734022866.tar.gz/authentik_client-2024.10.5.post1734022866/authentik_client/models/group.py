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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.group_member import GroupMember
from authentik_client.models.role import Role
from typing import Optional, Set
from typing_extensions import Self

class Group(BaseModel):
    """
    Group Serializer
    """ # noqa: E501
    pk: StrictStr
    num_pk: StrictInt
    name: StrictStr
    is_superuser: Optional[StrictBool] = Field(default=None, description="Users added to this group will be superusers.")
    parent: Optional[StrictStr] = None
    parent_name: Optional[StrictStr]
    users: Optional[List[StrictInt]] = None
    users_obj: Optional[List[GroupMember]]
    attributes: Optional[Dict[str, Any]] = None
    roles: Optional[List[StrictStr]] = None
    roles_obj: List[Role]
    __properties: ClassVar[List[str]] = ["pk", "num_pk", "name", "is_superuser", "parent", "parent_name", "users", "users_obj", "attributes", "roles", "roles_obj"]

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
        """Create an instance of Group from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "pk",
            "num_pk",
            "parent_name",
            "users_obj",
            "roles_obj",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in users_obj (list)
        _items = []
        if self.users_obj:
            for _item in self.users_obj:
                if _item:
                    _items.append(_item.to_dict())
            _dict['users_obj'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in roles_obj (list)
        _items = []
        if self.roles_obj:
            for _item in self.roles_obj:
                if _item:
                    _items.append(_item.to_dict())
            _dict['roles_obj'] = _items
        # set to None if parent (nullable) is None
        # and model_fields_set contains the field
        if self.parent is None and "parent" in self.model_fields_set:
            _dict['parent'] = None

        # set to None if parent_name (nullable) is None
        # and model_fields_set contains the field
        if self.parent_name is None and "parent_name" in self.model_fields_set:
            _dict['parent_name'] = None

        # set to None if users_obj (nullable) is None
        # and model_fields_set contains the field
        if self.users_obj is None and "users_obj" in self.model_fields_set:
            _dict['users_obj'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Group from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "num_pk": obj.get("num_pk"),
            "name": obj.get("name"),
            "is_superuser": obj.get("is_superuser"),
            "parent": obj.get("parent"),
            "parent_name": obj.get("parent_name"),
            "users": obj.get("users"),
            "users_obj": [GroupMember.from_dict(_item) for _item in obj["users_obj"]] if obj.get("users_obj") is not None else None,
            "attributes": obj.get("attributes"),
            "roles": obj.get("roles"),
            "roles_obj": [Role.from_dict(_item) for _item in obj["roles_obj"]] if obj.get("roles_obj") is not None else None
        })
        return _obj


