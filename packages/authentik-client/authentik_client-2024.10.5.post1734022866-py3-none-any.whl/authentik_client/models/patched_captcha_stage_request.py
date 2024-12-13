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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from authentik_client.models.flow_set_request import FlowSetRequest
from typing import Optional, Set
from typing_extensions import Self

class PatchedCaptchaStageRequest(BaseModel):
    """
    CaptchaStage Serializer
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    flow_set: Optional[List[FlowSetRequest]] = None
    public_key: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Public key, acquired your captcha Provider.")
    private_key: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Private key, acquired your captcha Provider.")
    js_url: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    api_url: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    interactive: Optional[StrictBool] = None
    score_min_threshold: Optional[Union[StrictFloat, StrictInt]] = None
    score_max_threshold: Optional[Union[StrictFloat, StrictInt]] = None
    error_on_invalid_score: Optional[StrictBool] = Field(default=None, description="When enabled and the received captcha score is outside of the given threshold, the stage will show an error message. When not enabled, the flow will continue, but the data from the captcha will be available in the context for policy decisions")
    __properties: ClassVar[List[str]] = ["name", "flow_set", "public_key", "private_key", "js_url", "api_url", "interactive", "score_min_threshold", "score_max_threshold", "error_on_invalid_score"]

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
        """Create an instance of PatchedCaptchaStageRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedCaptchaStageRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "flow_set": [FlowSetRequest.from_dict(_item) for _item in obj["flow_set"]] if obj.get("flow_set") is not None else None,
            "public_key": obj.get("public_key"),
            "private_key": obj.get("private_key"),
            "js_url": obj.get("js_url"),
            "api_url": obj.get("api_url"),
            "interactive": obj.get("interactive"),
            "score_min_threshold": obj.get("score_min_threshold"),
            "score_max_threshold": obj.get("score_max_threshold"),
            "error_on_invalid_score": obj.get("error_on_invalid_score")
        })
        return _obj


