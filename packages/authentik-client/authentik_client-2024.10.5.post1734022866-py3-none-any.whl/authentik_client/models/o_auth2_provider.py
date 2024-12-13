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
from typing_extensions import Annotated
from authentik_client.models.client_type_enum import ClientTypeEnum
from authentik_client.models.issuer_mode_enum import IssuerModeEnum
from authentik_client.models.redirect_uri import RedirectURI
from authentik_client.models.sub_mode_enum import SubModeEnum
from typing import Optional, Set
from typing_extensions import Self

class OAuth2Provider(BaseModel):
    """
    OAuth2Provider Serializer
    """ # noqa: E501
    pk: StrictInt
    name: StrictStr
    authentication_flow: Optional[StrictStr] = Field(default=None, description="Flow used for authentication when the associated application is accessed by an un-authenticated user.")
    authorization_flow: StrictStr = Field(description="Flow used when authorizing this provider.")
    invalidation_flow: StrictStr = Field(description="Flow used ending the session from a provider.")
    property_mappings: Optional[List[StrictStr]] = None
    component: StrictStr = Field(description="Get object component so that we know how to edit the object")
    assigned_application_slug: StrictStr = Field(description="Internal application name, used in URLs.")
    assigned_application_name: StrictStr = Field(description="Application's display Name.")
    assigned_backchannel_application_slug: StrictStr = Field(description="Internal application name, used in URLs.")
    assigned_backchannel_application_name: StrictStr = Field(description="Application's display Name.")
    verbose_name: StrictStr = Field(description="Return object's verbose_name")
    verbose_name_plural: StrictStr = Field(description="Return object's plural verbose_name")
    meta_model_name: StrictStr = Field(description="Return internal model name")
    client_type: Optional[ClientTypeEnum] = Field(default=None, description="Confidential clients are capable of maintaining the confidentiality of their credentials. Public clients are incapable")
    client_id: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    client_secret: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    access_code_validity: Optional[StrictStr] = Field(default=None, description="Access codes not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).")
    access_token_validity: Optional[StrictStr] = Field(default=None, description="Tokens not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).")
    refresh_token_validity: Optional[StrictStr] = Field(default=None, description="Tokens not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).")
    include_claims_in_id_token: Optional[StrictBool] = Field(default=None, description="Include User claims from scopes in the id_token, for applications that don't access the userinfo endpoint.")
    signing_key: Optional[StrictStr] = Field(default=None, description="Key used to sign the tokens.")
    encryption_key: Optional[StrictStr] = Field(default=None, description="Key used to encrypt the tokens. When set, tokens will be encrypted and returned as JWEs.")
    redirect_uris: List[RedirectURI]
    sub_mode: Optional[SubModeEnum] = Field(default=None, description="Configure what data should be used as unique User Identifier. For most cases, the default should be fine.")
    issuer_mode: Optional[IssuerModeEnum] = Field(default=None, description="Configure how the issuer field of the ID Token should be filled.")
    jwt_federation_sources: Optional[List[StrictStr]] = None
    jwt_federation_providers: Optional[List[StrictInt]] = None
    __properties: ClassVar[List[str]] = ["pk", "name", "authentication_flow", "authorization_flow", "invalidation_flow", "property_mappings", "component", "assigned_application_slug", "assigned_application_name", "assigned_backchannel_application_slug", "assigned_backchannel_application_name", "verbose_name", "verbose_name_plural", "meta_model_name", "client_type", "client_id", "client_secret", "access_code_validity", "access_token_validity", "refresh_token_validity", "include_claims_in_id_token", "signing_key", "encryption_key", "redirect_uris", "sub_mode", "issuer_mode", "jwt_federation_sources", "jwt_federation_providers"]

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
        """Create an instance of OAuth2Provider from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "pk",
            "component",
            "assigned_application_slug",
            "assigned_application_name",
            "assigned_backchannel_application_slug",
            "assigned_backchannel_application_name",
            "verbose_name",
            "verbose_name_plural",
            "meta_model_name",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in redirect_uris (list)
        _items = []
        if self.redirect_uris:
            for _item in self.redirect_uris:
                if _item:
                    _items.append(_item.to_dict())
            _dict['redirect_uris'] = _items
        # set to None if authentication_flow (nullable) is None
        # and model_fields_set contains the field
        if self.authentication_flow is None and "authentication_flow" in self.model_fields_set:
            _dict['authentication_flow'] = None

        # set to None if signing_key (nullable) is None
        # and model_fields_set contains the field
        if self.signing_key is None and "signing_key" in self.model_fields_set:
            _dict['signing_key'] = None

        # set to None if encryption_key (nullable) is None
        # and model_fields_set contains the field
        if self.encryption_key is None and "encryption_key" in self.model_fields_set:
            _dict['encryption_key'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OAuth2Provider from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "name": obj.get("name"),
            "authentication_flow": obj.get("authentication_flow"),
            "authorization_flow": obj.get("authorization_flow"),
            "invalidation_flow": obj.get("invalidation_flow"),
            "property_mappings": obj.get("property_mappings"),
            "component": obj.get("component"),
            "assigned_application_slug": obj.get("assigned_application_slug"),
            "assigned_application_name": obj.get("assigned_application_name"),
            "assigned_backchannel_application_slug": obj.get("assigned_backchannel_application_slug"),
            "assigned_backchannel_application_name": obj.get("assigned_backchannel_application_name"),
            "verbose_name": obj.get("verbose_name"),
            "verbose_name_plural": obj.get("verbose_name_plural"),
            "meta_model_name": obj.get("meta_model_name"),
            "client_type": obj.get("client_type"),
            "client_id": obj.get("client_id"),
            "client_secret": obj.get("client_secret"),
            "access_code_validity": obj.get("access_code_validity"),
            "access_token_validity": obj.get("access_token_validity"),
            "refresh_token_validity": obj.get("refresh_token_validity"),
            "include_claims_in_id_token": obj.get("include_claims_in_id_token"),
            "signing_key": obj.get("signing_key"),
            "encryption_key": obj.get("encryption_key"),
            "redirect_uris": [RedirectURI.from_dict(_item) for _item in obj["redirect_uris"]] if obj.get("redirect_uris") is not None else None,
            "sub_mode": obj.get("sub_mode"),
            "issuer_mode": obj.get("issuer_mode"),
            "jwt_federation_sources": obj.get("jwt_federation_sources"),
            "jwt_federation_providers": obj.get("jwt_federation_providers")
        })
        return _obj


