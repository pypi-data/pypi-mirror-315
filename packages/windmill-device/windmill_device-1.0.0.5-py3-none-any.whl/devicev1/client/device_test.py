# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import unittest
import json
from device_api import InvokeMethodHTTPRequest, UpdateDeviceRequest, ListDeviceRequest


class TestDevice(unittest.TestCase):
    """
    Test Device
    """

    def test_list_request(self):
        """
        Test list request
        """

        req = ListDeviceRequest(
            workspaceID="ws01",
            deviceHubName="dh01",
            deviceGroupName="dg01",
            status="online",
            kind="thing",
            localNames=["local"],
            pageNo=1,
            pageSize=3,
            orderBy="createAt",
            order="desc")
        print(req.model_dump_json(by_alias=True))

    def test_device_invoke_request(self):
        """
        Test invoke request
        """
        req = InvokeMethodHTTPRequest(
            workspaceID="ws01",
            deviceHubName="dh01",
            deviceName="dev01",
            uri="/test",
            body={"hello": "world"})
        print(req.model_dump_json(by_alias=True))

    def test_device_request(self):
        """
        Test update request
        """
        req = UpdateDeviceRequest(
            workspaceID="ws01",
            deviceHubName="dh01",
            deviceName="dev01",
            properties={"key": "value"},
            tags={"tag1": 12},
            metadata={},
            attributes={})
        print(req.model_dump_json(by_alias=True))


if __name__ == '__main__':
    unittest.main()
