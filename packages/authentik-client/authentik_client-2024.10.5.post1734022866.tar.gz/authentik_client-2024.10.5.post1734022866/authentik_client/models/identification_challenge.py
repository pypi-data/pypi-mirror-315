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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.captcha_challenge import CaptchaChallenge
from authentik_client.models.contextual_flow_info import ContextualFlowInfo
from authentik_client.models.error_detail import ErrorDetail
from authentik_client.models.flow_designation_enum import FlowDesignationEnum
from authentik_client.models.login_source import LoginSource
from typing import Optional, Set
from typing_extensions import Self

class IdentificationChallenge(BaseModel):
    """
    Identification challenges with all UI elements
    """ # noqa: E501
    flow_info: Optional[ContextualFlowInfo] = None
    component: Optional[StrictStr] = 'ak-stage-identification'
    response_errors: Optional[Dict[str, List[ErrorDetail]]] = None
    user_fields: Optional[List[StrictStr]]
    password_fields: StrictBool
    allow_show_password: Optional[StrictBool] = False
    application_pre: Optional[StrictStr] = None
    flow_designation: FlowDesignationEnum
    captcha_stage: Optional[CaptchaChallenge] = None
    enroll_url: Optional[StrictStr] = None
    recovery_url: Optional[StrictStr] = None
    passwordless_url: Optional[StrictStr] = None
    primary_action: StrictStr
    sources: Optional[List[LoginSource]] = None
    show_source_labels: StrictBool
    __properties: ClassVar[List[str]] = ["flow_info", "component", "response_errors", "user_fields", "password_fields", "allow_show_password", "application_pre", "flow_designation", "captcha_stage", "enroll_url", "recovery_url", "passwordless_url", "primary_action", "sources", "show_source_labels"]

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
        """Create an instance of IdentificationChallenge from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of flow_info
        if self.flow_info:
            _dict['flow_info'] = self.flow_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in response_errors (dict of array)
        _field_dict_of_array = {}
        if self.response_errors:
            for _key in self.response_errors:
                if self.response_errors[_key] is not None:
                    _field_dict_of_array[_key] = [
                        _item.to_dict() for _item in self.response_errors[_key]
                    ]
            _dict['response_errors'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of captcha_stage
        if self.captcha_stage:
            _dict['captcha_stage'] = self.captcha_stage.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in sources (list)
        _items = []
        if self.sources:
            for _item in self.sources:
                if _item:
                    _items.append(_item.to_dict())
            _dict['sources'] = _items
        # set to None if user_fields (nullable) is None
        # and model_fields_set contains the field
        if self.user_fields is None and "user_fields" in self.model_fields_set:
            _dict['user_fields'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IdentificationChallenge from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "flow_info": ContextualFlowInfo.from_dict(obj["flow_info"]) if obj.get("flow_info") is not None else None,
            "component": obj.get("component") if obj.get("component") is not None else 'ak-stage-identification',
            "response_errors": dict(
                (_k,
                        [ErrorDetail.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("response_errors", {}).items()
            ),
            "user_fields": obj.get("user_fields"),
            "password_fields": obj.get("password_fields"),
            "allow_show_password": obj.get("allow_show_password") if obj.get("allow_show_password") is not None else False,
            "application_pre": obj.get("application_pre"),
            "flow_designation": obj.get("flow_designation"),
            "captcha_stage": CaptchaChallenge.from_dict(obj["captcha_stage"]) if obj.get("captcha_stage") is not None else None,
            "enroll_url": obj.get("enroll_url"),
            "recovery_url": obj.get("recovery_url"),
            "passwordless_url": obj.get("passwordless_url"),
            "primary_action": obj.get("primary_action"),
            "sources": [LoginSource.from_dict(_item) for _item in obj["sources"]] if obj.get("sources") is not None else None,
            "show_source_labels": obj.get("show_source_labels")
        })
        return _obj


