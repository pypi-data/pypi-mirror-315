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
from authentik_client.models.binding_type_enum import BindingTypeEnum
from authentik_client.models.digest_algorithm_enum import DigestAlgorithmEnum
from authentik_client.models.group_matching_mode_enum import GroupMatchingModeEnum
from authentik_client.models.name_id_policy_enum import NameIdPolicyEnum
from authentik_client.models.policy_engine_mode import PolicyEngineMode
from authentik_client.models.signature_algorithm_enum import SignatureAlgorithmEnum
from authentik_client.models.user_matching_mode_enum import UserMatchingModeEnum
from typing import Optional, Set
from typing_extensions import Self

class SAMLSourceRequest(BaseModel):
    """
    SAMLSource Serializer
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
    pre_authentication_flow: StrictStr = Field(description="Flow used before authentication.")
    issuer: Optional[StrictStr] = Field(default=None, description="Also known as Entity ID. Defaults the Metadata URL.")
    sso_url: Annotated[str, Field(min_length=1, strict=True, max_length=200)] = Field(description="URL that the initial Login request is sent to.")
    slo_url: Optional[Annotated[str, Field(strict=True, max_length=200)]] = Field(default=None, description="Optional URL if your IDP supports Single-Logout.")
    allow_idp_initiated: Optional[StrictBool] = Field(default=None, description="Allows authentication flows initiated by the IdP. This can be a security risk, as no validation of the request ID is done.")
    name_id_policy: Optional[NameIdPolicyEnum] = Field(default=None, description="NameID Policy sent to the IdP. Can be unset, in which case no Policy is sent.")
    binding_type: Optional[BindingTypeEnum] = None
    verification_kp: Optional[StrictStr] = Field(default=None, description="When selected, incoming assertion's Signatures will be validated against this certificate. To allow unsigned Requests, leave on default.")
    signing_kp: Optional[StrictStr] = Field(default=None, description="Keypair used to sign outgoing Responses going to the Identity Provider.")
    digest_algorithm: Optional[DigestAlgorithmEnum] = None
    signature_algorithm: Optional[SignatureAlgorithmEnum] = None
    temporary_user_delete_after: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Time offset when temporary users should be deleted. This only applies if your IDP uses the NameID Format 'transient', and the user doesn't log out manually. (Format: hours=1;minutes=2;seconds=3).")
    encryption_kp: Optional[StrictStr] = Field(default=None, description="When selected, incoming assertions are encrypted by the IdP using the public key of the encryption keypair. The assertion is decrypted by the SP using the the private key.")
    __properties: ClassVar[List[str]] = ["name", "slug", "enabled", "authentication_flow", "enrollment_flow", "user_property_mappings", "group_property_mappings", "policy_engine_mode", "user_matching_mode", "user_path_template", "group_matching_mode", "pre_authentication_flow", "issuer", "sso_url", "slo_url", "allow_idp_initiated", "name_id_policy", "binding_type", "verification_kp", "signing_kp", "digest_algorithm", "signature_algorithm", "temporary_user_delete_after", "encryption_kp"]

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
        """Create an instance of SAMLSourceRequest from a JSON string"""
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

        # set to None if slo_url (nullable) is None
        # and model_fields_set contains the field
        if self.slo_url is None and "slo_url" in self.model_fields_set:
            _dict['slo_url'] = None

        # set to None if verification_kp (nullable) is None
        # and model_fields_set contains the field
        if self.verification_kp is None and "verification_kp" in self.model_fields_set:
            _dict['verification_kp'] = None

        # set to None if signing_kp (nullable) is None
        # and model_fields_set contains the field
        if self.signing_kp is None and "signing_kp" in self.model_fields_set:
            _dict['signing_kp'] = None

        # set to None if encryption_kp (nullable) is None
        # and model_fields_set contains the field
        if self.encryption_kp is None and "encryption_kp" in self.model_fields_set:
            _dict['encryption_kp'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SAMLSourceRequest from a dict"""
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
            "pre_authentication_flow": obj.get("pre_authentication_flow"),
            "issuer": obj.get("issuer"),
            "sso_url": obj.get("sso_url"),
            "slo_url": obj.get("slo_url"),
            "allow_idp_initiated": obj.get("allow_idp_initiated"),
            "name_id_policy": obj.get("name_id_policy"),
            "binding_type": obj.get("binding_type"),
            "verification_kp": obj.get("verification_kp"),
            "signing_kp": obj.get("signing_kp"),
            "digest_algorithm": obj.get("digest_algorithm"),
            "signature_algorithm": obj.get("signature_algorithm"),
            "temporary_user_delete_after": obj.get("temporary_user_delete_after"),
            "encryption_kp": obj.get("encryption_kp")
        })
        return _obj


