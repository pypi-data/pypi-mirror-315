# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from bceinternalsdk.client.paging import PagingRequest


class ListDeviceRequest(BaseModel, PagingRequest):
    """
    Request for listing devices.
    """

    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_group_name: Optional[str] = Field(
        default=None, alias="deviceGroupName")
    status: Optional[str] = Field(default=None, alias="status")
    kind: Optional[str] = Field(default=None, alias="kind")
    dept_id: Optional[str] = Field(default=None, alias="deptID")
    filter: Optional[str] = Field(default=None, alias="filter")
    local_names: Optional[list] = Field(default=None, alias="localNames")


class UpdateDeviceRequest(BaseModel):
    """
    Request for updating a device.
    """

    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_name: str = Field(alias="deviceName")
    display_name: Optional[str] = Field(default=None, alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    tags: Optional[dict] = Field(default=None, alias="tags")
    status: Optional[str] = Field(default=None, alias="status")
    device_group_name: Optional[str] = Field(
        default=None, alias="deviceGroupName")
    category: Optional[str] = Field(default=None, alias="category")
    dept_id: Optional[str] = Field(default=None, alias="deptID")


class InvokeMethodHTTPRequest(BaseModel):
    """
    Request for invoking a method via HTTP.
    """

    class Config(ConfigDict):
        """
        Configuration for the request model.
        """

        arbitrary_types_allowed = True

    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_name: str = Field(alias="deviceName")
    uri: str = Field(alias="uri")
    body: Optional[Any] = Field(default=None, alias="body")
    params: Optional[dict] = Field(default=None, alias="params")
    raw_query: Optional[str] = Field(default=None, alias="rawQuery")
