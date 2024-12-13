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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.group_matching_mode_enum import GroupMatchingModeEnum
from authentik_client.models.kadmin_type_enum import KadminTypeEnum
from authentik_client.models.policy_engine_mode import PolicyEngineMode
from authentik_client.models.user_matching_mode_enum import UserMatchingModeEnum
from typing import Optional, Set
from typing_extensions import Self

class KerberosSourceRequest(BaseModel):
    """
    Kerberos Source Serializer
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)] = Field(description="Source's display Name.")
    slug: Annotated[str, Field(min_length=1, strict=True, max_length=50)] = Field(description="Internal source name, used in URLs.")
    enabled: Optional[StrictBool] = None
    authentication_flow: Optional[StrictStr] = Field(default=None, description="Flow to use when authenticating existing users.")
    enrollment_flow: Optional[StrictStr] = Field(default=None, description="Flow to use when enrolling new users.")
    user_property_mappings: Optional[List[StrictStr]] = None
    group_property_mappings: Optional[List[StrictStr]] = None
    policy_engine_mode: Optional[PolicyEngineMode] = None
    user_matching_mode: Optional[UserMatchingModeEnum] = Field(default=None, description="How the source determines if an existing user should be authenticated or a new user enrolled.")
    user_path_template: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    group_matching_mode: Optional[GroupMatchingModeEnum] = Field(default=None, description="How the source determines if an existing group should be used or a new group created.")
    realm: Annotated[str, Field(min_length=1, strict=True)] = Field(description="Kerberos realm")
    krb5_conf: Optional[StrictStr] = Field(default=None, description="Custom krb5.conf to use. Uses the system one by default")
    kadmin_type: Optional[KadminTypeEnum] = Field(default=None, description="KAdmin server type")
    sync_users: Optional[StrictBool] = Field(default=None, description="Sync users from Kerberos into authentik")
    sync_users_password: Optional[StrictBool] = Field(default=None, description="When a user changes their password, sync it back to Kerberos")
    sync_principal: Optional[StrictStr] = Field(default=None, description="Principal to authenticate to kadmin for sync.")
    sync_password: Optional[StrictStr] = Field(default=None, description="Password to authenticate to kadmin for sync")
    sync_keytab: Optional[StrictStr] = Field(default=None, description="Keytab to authenticate to kadmin for sync. Must be base64-encoded or in the form TYPE:residual")
    sync_ccache: Optional[StrictStr] = Field(default=None, description="Credentials cache to authenticate to kadmin for sync. Must be in the form TYPE:residual")
    spnego_server_name: Optional[StrictStr] = Field(default=None, description="Force the use of a specific server name for SPNEGO. Must be in the form HTTP@hostname")
    spnego_keytab: Optional[StrictStr] = Field(default=None, description="SPNEGO keytab base64-encoded or path to keytab in the form FILE:path")
    spnego_ccache: Optional[StrictStr] = Field(default=None, description="Credential cache to use for SPNEGO in form type:residual")
    password_login_update_internal_password: Optional[StrictBool] = Field(default=None, description="If enabled, the authentik-stored password will be updated upon login with the Kerberos password backend")
    __properties: ClassVar[List[str]] = ["name", "slug", "enabled", "authentication_flow", "enrollment_flow", "user_property_mappings", "group_property_mappings", "policy_engine_mode", "user_matching_mode", "user_path_template", "group_matching_mode", "realm", "krb5_conf", "kadmin_type", "sync_users", "sync_users_password", "sync_principal", "sync_password", "sync_keytab", "sync_ccache", "spnego_server_name", "spnego_keytab", "spnego_ccache", "password_login_update_internal_password"]

    @field_validator('slug')
    def slug_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[-a-zA-Z0-9_]+$", value):
            raise ValueError(r"must validate the regular expression /^[-a-zA-Z0-9_]+$/")
        return value

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
        """Create an instance of KerberosSourceRequest from a JSON string"""
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
        # set to None if authentication_flow (nullable) is None
        # and model_fields_set contains the field
        if self.authentication_flow is None and "authentication_flow" in self.model_fields_set:
            _dict['authentication_flow'] = None

        # set to None if enrollment_flow (nullable) is None
        # and model_fields_set contains the field
        if self.enrollment_flow is None and "enrollment_flow" in self.model_fields_set:
            _dict['enrollment_flow'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KerberosSourceRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "slug": obj.get("slug"),
            "enabled": obj.get("enabled"),
            "authentication_flow": obj.get("authentication_flow"),
            "enrollment_flow": obj.get("enrollment_flow"),
            "user_property_mappings": obj.get("user_property_mappings"),
            "group_property_mappings": obj.get("group_property_mappings"),
            "policy_engine_mode": obj.get("policy_engine_mode"),
            "user_matching_mode": obj.get("user_matching_mode"),
            "user_path_template": obj.get("user_path_template"),
            "group_matching_mode": obj.get("group_matching_mode"),
            "realm": obj.get("realm"),
            "krb5_conf": obj.get("krb5_conf"),
            "kadmin_type": obj.get("kadmin_type"),
            "sync_users": obj.get("sync_users"),
            "sync_users_password": obj.get("sync_users_password"),
            "sync_principal": obj.get("sync_principal"),
            "sync_password": obj.get("sync_password"),
            "sync_keytab": obj.get("sync_keytab"),
            "sync_ccache": obj.get("sync_ccache"),
            "spnego_server_name": obj.get("spnego_server_name"),
            "spnego_keytab": obj.get("spnego_keytab"),
            "spnego_ccache": obj.get("spnego_ccache"),
            "password_login_update_internal_password": obj.get("password_login_update_internal_password")
        })
        return _obj


