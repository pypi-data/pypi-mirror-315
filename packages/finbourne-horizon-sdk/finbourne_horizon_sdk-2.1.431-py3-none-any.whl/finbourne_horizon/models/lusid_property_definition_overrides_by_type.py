# coding: utf-8

"""
    FINBOURNE Horizon API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist

class LusidPropertyDefinitionOverridesByType(BaseModel):
    """
    LusidPropertyDefinitionOverridesByType
    """
    display_name_override: Optional[StrictStr] = Field(None, alias="displayNameOverride")
    description_override: Optional[StrictStr] = Field(None, alias="descriptionOverride")
    entity_type: Optional[StrictStr] = Field(None, alias="entityType")
    entity_sub_type: Optional[conlist(StrictStr)] = Field(None, alias="entitySubType")
    vendor_package: Optional[conlist(StrictStr)] = Field(None, alias="vendorPackage")
    __properties = ["displayNameOverride", "descriptionOverride", "entityType", "entitySubType", "vendorPackage"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LusidPropertyDefinitionOverridesByType:
        """Create an instance of LusidPropertyDefinitionOverridesByType from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if display_name_override (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name_override is None and "display_name_override" in self.__fields_set__:
            _dict['displayNameOverride'] = None

        # set to None if description_override (nullable) is None
        # and __fields_set__ contains the field
        if self.description_override is None and "description_override" in self.__fields_set__:
            _dict['descriptionOverride'] = None

        # set to None if entity_type (nullable) is None
        # and __fields_set__ contains the field
        if self.entity_type is None and "entity_type" in self.__fields_set__:
            _dict['entityType'] = None

        # set to None if entity_sub_type (nullable) is None
        # and __fields_set__ contains the field
        if self.entity_sub_type is None and "entity_sub_type" in self.__fields_set__:
            _dict['entitySubType'] = None

        # set to None if vendor_package (nullable) is None
        # and __fields_set__ contains the field
        if self.vendor_package is None and "vendor_package" in self.__fields_set__:
            _dict['vendorPackage'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LusidPropertyDefinitionOverridesByType:
        """Create an instance of LusidPropertyDefinitionOverridesByType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LusidPropertyDefinitionOverridesByType.parse_obj(obj)

        _obj = LusidPropertyDefinitionOverridesByType.parse_obj({
            "display_name_override": obj.get("displayNameOverride"),
            "description_override": obj.get("descriptionOverride"),
            "entity_type": obj.get("entityType"),
            "entity_sub_type": obj.get("entitySubType"),
            "vendor_package": obj.get("vendorPackage")
        })
        return _obj
