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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.backends_enum import BackendsEnum
from authentik_client.models.flow_set_request import FlowSetRequest
from typing import Optional, Set
from typing_extensions import Self

class PasswordStageRequest(BaseModel):
    """
    PasswordStage Serializer
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)]
    flow_set: Optional[List[FlowSetRequest]] = None
    backends: List[BackendsEnum] = Field(description="Selection of backends to test the password against.")
    configure_flow: Optional[StrictStr] = Field(default=None, description="Flow used by an authenticated user to configure this Stage. If empty, user will not be able to configure this stage.")
    failed_attempts_before_cancel: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]] = Field(default=None, description="How many attempts a user has before the flow is canceled. To lock the user out, use a reputation policy and a user_write stage.")
    allow_show_password: Optional[StrictBool] = Field(default=None, description="When enabled, provides a 'show password' button with the password input field.")
    __properties: ClassVar[List[str]] = ["name", "flow_set", "backends", "configure_flow", "failed_attempts_before_cancel", "allow_show_password"]

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
        """Create an instance of PasswordStageRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in flow_set (list)
        _items = []
        if self.flow_set:
            for _item in self.flow_set:
                if _item:
                    _items.append(_item.to_dict())
            _dict['flow_set'] = _items
        # set to None if configure_flow (nullable) is None
        # and model_fields_set contains the field
        if self.configure_flow is None and "configure_flow" in self.model_fields_set:
            _dict['configure_flow'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PasswordStageRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "flow_set": [FlowSetRequest.from_dict(_item) for _item in obj["flow_set"]] if obj.get("flow_set") is not None else None,
            "backends": obj.get("backends"),
            "configure_flow": obj.get("configure_flow"),
            "failed_attempts_before_cancel": obj.get("failed_attempts_before_cancel"),
            "allow_show_password": obj.get("allow_show_password")
        })
        return _obj


