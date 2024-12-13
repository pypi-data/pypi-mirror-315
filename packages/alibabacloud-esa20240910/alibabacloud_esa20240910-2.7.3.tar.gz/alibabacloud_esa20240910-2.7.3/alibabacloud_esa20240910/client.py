# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_esa20240910 import models as esa20240910_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_openplatform20191219.client import Client as OpenPlatformClient
from alibabacloud_openplatform20191219 import models as open_platform_models
from alibabacloud_oss_sdk import models as oss_models
from alibabacloud_oss_sdk.client import Client as OSSClient
from alibabacloud_tea_fileform import models as file_form_models
from alibabacloud_oss_util import models as ossutil_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('esa', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def activate_client_certificate_with_options(
        self,
        request: esa20240910_models.ActivateClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ActivateClientCertificateResponse:
        """
        @summary Activates a client certificate.
        
        @param request: ActivateClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ActivateClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ActivateClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ActivateClientCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def activate_client_certificate_with_options_async(
        self,
        request: esa20240910_models.ActivateClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ActivateClientCertificateResponse:
        """
        @summary Activates a client certificate.
        
        @param request: ActivateClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ActivateClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ActivateClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ActivateClientCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def activate_client_certificate(
        self,
        request: esa20240910_models.ActivateClientCertificateRequest,
    ) -> esa20240910_models.ActivateClientCertificateResponse:
        """
        @summary Activates a client certificate.
        
        @param request: ActivateClientCertificateRequest
        @return: ActivateClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.activate_client_certificate_with_options(request, runtime)

    async def activate_client_certificate_async(
        self,
        request: esa20240910_models.ActivateClientCertificateRequest,
    ) -> esa20240910_models.ActivateClientCertificateResponse:
        """
        @summary Activates a client certificate.
        
        @param request: ActivateClientCertificateRequest
        @return: ActivateClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.activate_client_certificate_with_options_async(request, runtime)

    def batch_create_records_with_options(
        self,
        tmp_req: esa20240910_models.BatchCreateRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchCreateRecordsResponse:
        """
        @summary Adds DNS records of different record types at a time..
        
        @description This operation allows you to create or update multiple DNS records at a time. It is suitable for managing a large number of DNS configurations. Supported record types include but are not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. The operation allows you to configure the priority, flag, tag, and weight for DNS records. In addition, for specific types of records, such as CERT, SSHFP, SMIMEA, and TLSA, advanced settings such as certificate information and encryption algorithms are also supported.
        Successful and failed records along with error messages are listed in the response.
        
        @param tmp_req: BatchCreateRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchCreateRecordsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchCreateRecordsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.record_list):
            request.record_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.record_list, 'RecordList', 'json')
        query = {}
        if not UtilClient.is_unset(request.record_list_shrink):
            query['RecordList'] = request.record_list_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchCreateRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchCreateRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_create_records_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchCreateRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchCreateRecordsResponse:
        """
        @summary Adds DNS records of different record types at a time..
        
        @description This operation allows you to create or update multiple DNS records at a time. It is suitable for managing a large number of DNS configurations. Supported record types include but are not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. The operation allows you to configure the priority, flag, tag, and weight for DNS records. In addition, for specific types of records, such as CERT, SSHFP, SMIMEA, and TLSA, advanced settings such as certificate information and encryption algorithms are also supported.
        Successful and failed records along with error messages are listed in the response.
        
        @param tmp_req: BatchCreateRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchCreateRecordsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchCreateRecordsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.record_list):
            request.record_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.record_list, 'RecordList', 'json')
        query = {}
        if not UtilClient.is_unset(request.record_list_shrink):
            query['RecordList'] = request.record_list_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchCreateRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchCreateRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_create_records(
        self,
        request: esa20240910_models.BatchCreateRecordsRequest,
    ) -> esa20240910_models.BatchCreateRecordsResponse:
        """
        @summary Adds DNS records of different record types at a time..
        
        @description This operation allows you to create or update multiple DNS records at a time. It is suitable for managing a large number of DNS configurations. Supported record types include but are not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. The operation allows you to configure the priority, flag, tag, and weight for DNS records. In addition, for specific types of records, such as CERT, SSHFP, SMIMEA, and TLSA, advanced settings such as certificate information and encryption algorithms are also supported.
        Successful and failed records along with error messages are listed in the response.
        
        @param request: BatchCreateRecordsRequest
        @return: BatchCreateRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_create_records_with_options(request, runtime)

    async def batch_create_records_async(
        self,
        request: esa20240910_models.BatchCreateRecordsRequest,
    ) -> esa20240910_models.BatchCreateRecordsResponse:
        """
        @summary Adds DNS records of different record types at a time..
        
        @description This operation allows you to create or update multiple DNS records at a time. It is suitable for managing a large number of DNS configurations. Supported record types include but are not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. The operation allows you to configure the priority, flag, tag, and weight for DNS records. In addition, for specific types of records, such as CERT, SSHFP, SMIMEA, and TLSA, advanced settings such as certificate information and encryption algorithms are also supported.
        Successful and failed records along with error messages are listed in the response.
        
        @param request: BatchCreateRecordsRequest
        @return: BatchCreateRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_create_records_with_options_async(request, runtime)

    def batch_create_waf_rules_with_options(
        self,
        tmp_req: esa20240910_models.BatchCreateWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchCreateWafRulesResponse:
        """
        @summary Creates multiple rules of a specific Web Application Firewall (WAF) rule category at a time. You can also configure shared settings for the rules.
        
        @param tmp_req: BatchCreateWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchCreateWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchCreateWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.configs):
            request.configs_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.configs, 'Configs', 'json')
        if not UtilClient.is_unset(tmp_req.shared):
            request.shared_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shared, 'Shared', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.configs_shrink):
            body['Configs'] = request.configs_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        if not UtilClient.is_unset(request.shared_shrink):
            body['Shared'] = request.shared_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchCreateWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchCreateWafRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_create_waf_rules_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchCreateWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchCreateWafRulesResponse:
        """
        @summary Creates multiple rules of a specific Web Application Firewall (WAF) rule category at a time. You can also configure shared settings for the rules.
        
        @param tmp_req: BatchCreateWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchCreateWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchCreateWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.configs):
            request.configs_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.configs, 'Configs', 'json')
        if not UtilClient.is_unset(tmp_req.shared):
            request.shared_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shared, 'Shared', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.configs_shrink):
            body['Configs'] = request.configs_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        if not UtilClient.is_unset(request.shared_shrink):
            body['Shared'] = request.shared_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchCreateWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchCreateWafRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_create_waf_rules(
        self,
        request: esa20240910_models.BatchCreateWafRulesRequest,
    ) -> esa20240910_models.BatchCreateWafRulesResponse:
        """
        @summary Creates multiple rules of a specific Web Application Firewall (WAF) rule category at a time. You can also configure shared settings for the rules.
        
        @param request: BatchCreateWafRulesRequest
        @return: BatchCreateWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_create_waf_rules_with_options(request, runtime)

    async def batch_create_waf_rules_async(
        self,
        request: esa20240910_models.BatchCreateWafRulesRequest,
    ) -> esa20240910_models.BatchCreateWafRulesResponse:
        """
        @summary Creates multiple rules of a specific Web Application Firewall (WAF) rule category at a time. You can also configure shared settings for the rules.
        
        @param request: BatchCreateWafRulesRequest
        @return: BatchCreateWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_create_waf_rules_with_options_async(request, runtime)

    def batch_delete_kv_with_options(
        self,
        tmp_req: esa20240910_models.BatchDeleteKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvResponse:
        """
        @summary Deletes key-value pairs from a namespace at a time based on keys.
        
        @param tmp_req: BatchDeleteKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchDeleteKvResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchDeleteKvShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.keys):
            request.keys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.keys, 'Keys', 'json')
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.keys_shrink):
            body['Keys'] = request.keys_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchDeleteKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchDeleteKvResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_delete_kv_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchDeleteKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvResponse:
        """
        @summary Deletes key-value pairs from a namespace at a time based on keys.
        
        @param tmp_req: BatchDeleteKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchDeleteKvResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchDeleteKvShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.keys):
            request.keys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.keys, 'Keys', 'json')
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.keys_shrink):
            body['Keys'] = request.keys_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchDeleteKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchDeleteKvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_delete_kv(
        self,
        request: esa20240910_models.BatchDeleteKvRequest,
    ) -> esa20240910_models.BatchDeleteKvResponse:
        """
        @summary Deletes key-value pairs from a namespace at a time based on keys.
        
        @param request: BatchDeleteKvRequest
        @return: BatchDeleteKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_delete_kv_with_options(request, runtime)

    async def batch_delete_kv_async(
        self,
        request: esa20240910_models.BatchDeleteKvRequest,
    ) -> esa20240910_models.BatchDeleteKvResponse:
        """
        @summary Deletes key-value pairs from a namespace at a time based on keys.
        
        @param request: BatchDeleteKvRequest
        @return: BatchDeleteKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_delete_kv_with_options_async(request, runtime)

    def batch_delete_kv_with_high_capacity_with_options(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        """
        @summary Deletes multiple key-value pairs from a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html). For small request bodies, we recommend that you use [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchDeleteKvWithHighCapacityAdvance to call the operation.
        func TestBatchDeleteWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for deleting key-value pairs at a time.
        namespace := "test_batch_put"
        rawReq := BatchDeleteKvRequest{
        Namespace: &namespace,
        }
        for i := 0; i < 10000; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        rawReq.Keys = append(rawReq.Keys, &key)
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchDeleteKvWithHighCapacity operation for deletion.
        reqHighCapacity := BatchDeleteKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchDeleteKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchDeleteKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchDeleteKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchDeleteKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchDeleteKvWithHighCapacityResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_delete_kv_with_high_capacity_with_options_async(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        """
        @summary Deletes multiple key-value pairs from a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html). For small request bodies, we recommend that you use [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchDeleteKvWithHighCapacityAdvance to call the operation.
        func TestBatchDeleteWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for deleting key-value pairs at a time.
        namespace := "test_batch_put"
        rawReq := BatchDeleteKvRequest{
        Namespace: &namespace,
        }
        for i := 0; i < 10000; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        rawReq.Keys = append(rawReq.Keys, &key)
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchDeleteKvWithHighCapacity operation for deletion.
        reqHighCapacity := BatchDeleteKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchDeleteKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchDeleteKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchDeleteKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchDeleteKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchDeleteKvWithHighCapacityResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_delete_kv_with_high_capacity(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityRequest,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        """
        @summary Deletes multiple key-value pairs from a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html). For small request bodies, we recommend that you use [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchDeleteKvWithHighCapacityAdvance to call the operation.
        func TestBatchDeleteWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for deleting key-value pairs at a time.
        namespace := "test_batch_put"
        rawReq := BatchDeleteKvRequest{
        Namespace: &namespace,
        }
        for i := 0; i < 10000; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        rawReq.Keys = append(rawReq.Keys, &key)
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchDeleteKvWithHighCapacity operation for deletion.
        reqHighCapacity := BatchDeleteKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchDeleteKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchDeleteKvWithHighCapacityRequest
        @return: BatchDeleteKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_delete_kv_with_high_capacity_with_options(request, runtime)

    async def batch_delete_kv_with_high_capacity_async(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityRequest,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        """
        @summary Deletes multiple key-value pairs from a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html). For small request bodies, we recommend that you use [BatchDeleteKv](https://help.aliyun.com/document_detail/2850204.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchDeleteKvWithHighCapacityAdvance to call the operation.
        func TestBatchDeleteWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for deleting key-value pairs at a time.
        namespace := "test_batch_put"
        rawReq := BatchDeleteKvRequest{
        Namespace: &namespace,
        }
        for i := 0; i < 10000; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        rawReq.Keys = append(rawReq.Keys, &key)
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchDeleteKvWithHighCapacity operation for deletion.
        reqHighCapacity := BatchDeleteKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchDeleteKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchDeleteKvWithHighCapacityRequest
        @return: BatchDeleteKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_delete_kv_with_high_capacity_with_options_async(request, runtime)

    def batch_delete_kv_with_high_capacity_advance(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        batch_delete_kv_with_high_capacity_req = esa20240910_models.BatchDeleteKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, batch_delete_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            batch_delete_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        batch_delete_kv_with_high_capacity_resp = self.batch_delete_kv_with_high_capacity_with_options(batch_delete_kv_with_high_capacity_req, runtime)
        return batch_delete_kv_with_high_capacity_resp

    async def batch_delete_kv_with_high_capacity_advance_async(
        self,
        request: esa20240910_models.BatchDeleteKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchDeleteKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        batch_delete_kv_with_high_capacity_req = esa20240910_models.BatchDeleteKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, batch_delete_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            batch_delete_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        batch_delete_kv_with_high_capacity_resp = await self.batch_delete_kv_with_high_capacity_with_options_async(batch_delete_kv_with_high_capacity_req, runtime)
        return batch_delete_kv_with_high_capacity_resp

    def batch_get_expression_fields_with_options(
        self,
        tmp_req: esa20240910_models.BatchGetExpressionFieldsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchGetExpressionFieldsResponse:
        """
        @summary Batch queries the objects that match specific expressions.
        
        @param tmp_req: BatchGetExpressionFieldsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchGetExpressionFieldsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchGetExpressionFieldsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.expressions):
            request.expressions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.expressions, 'Expressions', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.expressions_shrink):
            body['Expressions'] = request.expressions_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchGetExpressionFields',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchGetExpressionFieldsResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_get_expression_fields_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchGetExpressionFieldsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchGetExpressionFieldsResponse:
        """
        @summary Batch queries the objects that match specific expressions.
        
        @param tmp_req: BatchGetExpressionFieldsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchGetExpressionFieldsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchGetExpressionFieldsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.expressions):
            request.expressions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.expressions, 'Expressions', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.expressions_shrink):
            body['Expressions'] = request.expressions_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchGetExpressionFields',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchGetExpressionFieldsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_get_expression_fields(
        self,
        request: esa20240910_models.BatchGetExpressionFieldsRequest,
    ) -> esa20240910_models.BatchGetExpressionFieldsResponse:
        """
        @summary Batch queries the objects that match specific expressions.
        
        @param request: BatchGetExpressionFieldsRequest
        @return: BatchGetExpressionFieldsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_get_expression_fields_with_options(request, runtime)

    async def batch_get_expression_fields_async(
        self,
        request: esa20240910_models.BatchGetExpressionFieldsRequest,
    ) -> esa20240910_models.BatchGetExpressionFieldsResponse:
        """
        @summary Batch queries the objects that match specific expressions.
        
        @param request: BatchGetExpressionFieldsRequest
        @return: BatchGetExpressionFieldsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_get_expression_fields_with_options_async(request, runtime)

    def batch_put_kv_with_options(
        self,
        tmp_req: esa20240910_models.BatchPutKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys.
        
        @param tmp_req: BatchPutKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchPutKvResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchPutKvShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.kv_list):
            request.kv_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kv_list, 'KvList', 'json')
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.kv_list_shrink):
            body['KvList'] = request.kv_list_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchPutKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchPutKvResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_put_kv_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchPutKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys.
        
        @param tmp_req: BatchPutKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchPutKvResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchPutKvShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.kv_list):
            request.kv_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kv_list, 'KvList', 'json')
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.kv_list_shrink):
            body['KvList'] = request.kv_list_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchPutKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchPutKvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_put_kv(
        self,
        request: esa20240910_models.BatchPutKvRequest,
    ) -> esa20240910_models.BatchPutKvResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys.
        
        @param request: BatchPutKvRequest
        @return: BatchPutKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_put_kv_with_options(request, runtime)

    async def batch_put_kv_async(
        self,
        request: esa20240910_models.BatchPutKvRequest,
    ) -> esa20240910_models.BatchPutKvResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys.
        
        @param request: BatchPutKvRequest
        @return: BatchPutKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_put_kv_with_options_async(request, runtime)

    def batch_put_kv_with_high_capacity_with_options(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html). For small request bodies, we recommend that you use [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchPutKvWithHighCapacityAdvance to call the operation.
        func TestBatchPutKvWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs at a time.
        namespace := "test_batch_put"
        numKv := 10000
        kvList := make([]BatchPutKvRequestKvList, numKv)
        test_value := strings.Repeat("a", 101024)
        for i := 0; i < numKv; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        value := test_value
        kvList[i] = &BatchPutKvRequestKvList{
        Key:   &key,
        Value: &value,
        }
        }
        rawReq := BatchPutKvRequest{
        Namespace: &namespace,
        KvList:    kvList,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchPutKvWithHighCapacity operation for upload.
        reqHighCapacity := BatchPutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchPutKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchPutKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchPutKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchPutKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchPutKvWithHighCapacityResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_put_kv_with_high_capacity_with_options_async(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html). For small request bodies, we recommend that you use [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchPutKvWithHighCapacityAdvance to call the operation.
        func TestBatchPutKvWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs at a time.
        namespace := "test_batch_put"
        numKv := 10000
        kvList := make([]BatchPutKvRequestKvList, numKv)
        test_value := strings.Repeat("a", 101024)
        for i := 0; i < numKv; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        value := test_value
        kvList[i] = &BatchPutKvRequestKvList{
        Key:   &key,
        Value: &value,
        }
        }
        rawReq := BatchPutKvRequest{
        Namespace: &namespace,
        KvList:    kvList,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchPutKvWithHighCapacity operation for upload.
        reqHighCapacity := BatchPutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchPutKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchPutKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchPutKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchPutKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchPutKvWithHighCapacityResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_put_kv_with_high_capacity(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityRequest,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html). For small request bodies, we recommend that you use [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchPutKvWithHighCapacityAdvance to call the operation.
        func TestBatchPutKvWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs at a time.
        namespace := "test_batch_put"
        numKv := 10000
        kvList := make([]BatchPutKvRequestKvList, numKv)
        test_value := strings.Repeat("a", 101024)
        for i := 0; i < numKv; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        value := test_value
        kvList[i] = &BatchPutKvRequestKvList{
        Key:   &key,
        Value: &value,
        }
        }
        rawReq := BatchPutKvRequest{
        Namespace: &namespace,
        KvList:    kvList,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchPutKvWithHighCapacity operation for upload.
        reqHighCapacity := BatchPutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchPutKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchPutKvWithHighCapacityRequest
        @return: BatchPutKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_put_kv_with_high_capacity_with_options(request, runtime)

    async def batch_put_kv_with_high_capacity_async(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityRequest,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        """
        @summary Configures key-value pairs for a namespace at a time based on specified keys. The request body can be up to 100 MB.
        
        @description This operation allows you to upload a larger request body than by using [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html). For small request bodies, we recommend that you use [BatchPutKv](https://help.aliyun.com/document_detail/2850203.html) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and BatchPutKvWithHighCapacityAdvance to call the operation.
        func TestBatchPutKvWithHighCapacity() error {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs at a time.
        namespace := "test_batch_put"
        numKv := 10000
        kvList := make([]BatchPutKvRequestKvList, numKv)
        test_value := strings.Repeat("a", 101024)
        for i := 0; i < numKv; i++ {
        key := fmt.Sprintf("test_key_%d", i)
        value := test_value
        kvList[i] = &BatchPutKvRequestKvList{
        Key:   &key,
        Value: &value,
        }
        }
        rawReq := BatchPutKvRequest{
        Namespace: &namespace,
        KvList:    kvList,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the BatchPutKvWithHighCapacity operation for upload.
        reqHighCapacity := BatchPutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        UrlObject: bytes.NewReader(payload),
        }
        resp, err := cli.BatchPutKvWithHighCapacityAdvance(&reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: BatchPutKvWithHighCapacityRequest
        @return: BatchPutKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_put_kv_with_high_capacity_with_options_async(request, runtime)

    def batch_put_kv_with_high_capacity_advance(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        batch_put_kv_with_high_capacity_req = esa20240910_models.BatchPutKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, batch_put_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            batch_put_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        batch_put_kv_with_high_capacity_resp = self.batch_put_kv_with_high_capacity_with_options(batch_put_kv_with_high_capacity_req, runtime)
        return batch_put_kv_with_high_capacity_resp

    async def batch_put_kv_with_high_capacity_advance_async(
        self,
        request: esa20240910_models.BatchPutKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchPutKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        batch_put_kv_with_high_capacity_req = esa20240910_models.BatchPutKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, batch_put_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            batch_put_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        batch_put_kv_with_high_capacity_resp = await self.batch_put_kv_with_high_capacity_with_options_async(batch_put_kv_with_high_capacity_req, runtime)
        return batch_put_kv_with_high_capacity_resp

    def batch_update_waf_rules_with_options(
        self,
        tmp_req: esa20240910_models.BatchUpdateWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchUpdateWafRulesResponse:
        """
        @summary Modifies multiple rules in a specific Web Application Firewall (WAF) ruleset at a time.
        
        @param tmp_req: BatchUpdateWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchUpdateWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchUpdateWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.configs):
            request.configs_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.configs, 'Configs', 'json')
        if not UtilClient.is_unset(tmp_req.shared):
            request.shared_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shared, 'Shared', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.configs_shrink):
            body['Configs'] = request.configs_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        if not UtilClient.is_unset(request.ruleset_id):
            body['RulesetId'] = request.ruleset_id
        if not UtilClient.is_unset(request.shared_shrink):
            body['Shared'] = request.shared_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchUpdateWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchUpdateWafRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def batch_update_waf_rules_with_options_async(
        self,
        tmp_req: esa20240910_models.BatchUpdateWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BatchUpdateWafRulesResponse:
        """
        @summary Modifies multiple rules in a specific Web Application Firewall (WAF) ruleset at a time.
        
        @param tmp_req: BatchUpdateWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BatchUpdateWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BatchUpdateWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.configs):
            request.configs_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.configs, 'Configs', 'json')
        if not UtilClient.is_unset(tmp_req.shared):
            request.shared_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shared, 'Shared', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.configs_shrink):
            body['Configs'] = request.configs_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        if not UtilClient.is_unset(request.ruleset_id):
            body['RulesetId'] = request.ruleset_id
        if not UtilClient.is_unset(request.shared_shrink):
            body['Shared'] = request.shared_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchUpdateWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BatchUpdateWafRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def batch_update_waf_rules(
        self,
        request: esa20240910_models.BatchUpdateWafRulesRequest,
    ) -> esa20240910_models.BatchUpdateWafRulesResponse:
        """
        @summary Modifies multiple rules in a specific Web Application Firewall (WAF) ruleset at a time.
        
        @param request: BatchUpdateWafRulesRequest
        @return: BatchUpdateWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_update_waf_rules_with_options(request, runtime)

    async def batch_update_waf_rules_async(
        self,
        request: esa20240910_models.BatchUpdateWafRulesRequest,
    ) -> esa20240910_models.BatchUpdateWafRulesResponse:
        """
        @summary Modifies multiple rules in a specific Web Application Firewall (WAF) ruleset at a time.
        
        @param request: BatchUpdateWafRulesRequest
        @return: BatchUpdateWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.batch_update_waf_rules_with_options_async(request, runtime)

    def block_object_with_options(
        self,
        tmp_req: esa20240910_models.BlockObjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BlockObjectResponse:
        """
        @summary Blocks URLs.
        
        @param tmp_req: BlockObjectRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BlockObjectResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BlockObjectShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.extension):
            query['Extension'] = request.extension
        if not UtilClient.is_unset(request.maxage):
            query['Maxage'] = request.maxage
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BlockObject',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BlockObjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def block_object_with_options_async(
        self,
        tmp_req: esa20240910_models.BlockObjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.BlockObjectResponse:
        """
        @summary Blocks URLs.
        
        @param tmp_req: BlockObjectRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: BlockObjectResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.BlockObjectShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.extension):
            query['Extension'] = request.extension
        if not UtilClient.is_unset(request.maxage):
            query['Maxage'] = request.maxage
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BlockObject',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.BlockObjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def block_object(
        self,
        request: esa20240910_models.BlockObjectRequest,
    ) -> esa20240910_models.BlockObjectResponse:
        """
        @summary Blocks URLs.
        
        @param request: BlockObjectRequest
        @return: BlockObjectResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.block_object_with_options(request, runtime)

    async def block_object_async(
        self,
        request: esa20240910_models.BlockObjectRequest,
    ) -> esa20240910_models.BlockObjectResponse:
        """
        @summary Blocks URLs.
        
        @param request: BlockObjectRequest
        @return: BlockObjectResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.block_object_with_options_async(request, runtime)

    def change_resource_group_with_options(
        self,
        request: esa20240910_models.ChangeResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ChangeResourceGroupResponse:
        """
        @summary Moves a website from one resource group to another.
        
        @param request: ChangeResourceGroupRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeResourceGroupResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ChangeResourceGroup',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ChangeResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def change_resource_group_with_options_async(
        self,
        request: esa20240910_models.ChangeResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ChangeResourceGroupResponse:
        """
        @summary Moves a website from one resource group to another.
        
        @param request: ChangeResourceGroupRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeResourceGroupResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ChangeResourceGroup',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ChangeResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def change_resource_group(
        self,
        request: esa20240910_models.ChangeResourceGroupRequest,
    ) -> esa20240910_models.ChangeResourceGroupResponse:
        """
        @summary Moves a website from one resource group to another.
        
        @param request: ChangeResourceGroupRequest
        @return: ChangeResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.change_resource_group_with_options(request, runtime)

    async def change_resource_group_async(
        self,
        request: esa20240910_models.ChangeResourceGroupRequest,
    ) -> esa20240910_models.ChangeResourceGroupResponse:
        """
        @summary Moves a website from one resource group to another.
        
        @param request: ChangeResourceGroupRequest
        @return: ChangeResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.change_resource_group_with_options_async(request, runtime)

    def check_site_name_with_options(
        self,
        request: esa20240910_models.CheckSiteNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckSiteNameResponse:
        """
        @summary Checks whether a specified website name is available.
        
        @param request: CheckSiteNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckSiteNameResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_name):
            query['SiteName'] = request.site_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckSiteName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckSiteNameResponse(),
            self.call_api(params, req, runtime)
        )

    async def check_site_name_with_options_async(
        self,
        request: esa20240910_models.CheckSiteNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckSiteNameResponse:
        """
        @summary Checks whether a specified website name is available.
        
        @param request: CheckSiteNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckSiteNameResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_name):
            query['SiteName'] = request.site_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckSiteName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckSiteNameResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def check_site_name(
        self,
        request: esa20240910_models.CheckSiteNameRequest,
    ) -> esa20240910_models.CheckSiteNameResponse:
        """
        @summary Checks whether a specified website name is available.
        
        @param request: CheckSiteNameRequest
        @return: CheckSiteNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.check_site_name_with_options(request, runtime)

    async def check_site_name_async(
        self,
        request: esa20240910_models.CheckSiteNameRequest,
    ) -> esa20240910_models.CheckSiteNameResponse:
        """
        @summary Checks whether a specified website name is available.
        
        @param request: CheckSiteNameRequest
        @return: CheckSiteNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.check_site_name_with_options_async(request, runtime)

    def check_site_project_name_with_options(
        self,
        request: esa20240910_models.CheckSiteProjectNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckSiteProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task.
        
        @param request: CheckSiteProjectNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckSiteProjectNameResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckSiteProjectName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckSiteProjectNameResponse(),
            self.call_api(params, req, runtime)
        )

    async def check_site_project_name_with_options_async(
        self,
        request: esa20240910_models.CheckSiteProjectNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckSiteProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task.
        
        @param request: CheckSiteProjectNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckSiteProjectNameResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckSiteProjectName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckSiteProjectNameResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def check_site_project_name(
        self,
        request: esa20240910_models.CheckSiteProjectNameRequest,
    ) -> esa20240910_models.CheckSiteProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task.
        
        @param request: CheckSiteProjectNameRequest
        @return: CheckSiteProjectNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.check_site_project_name_with_options(request, runtime)

    async def check_site_project_name_async(
        self,
        request: esa20240910_models.CheckSiteProjectNameRequest,
    ) -> esa20240910_models.CheckSiteProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task.
        
        @param request: CheckSiteProjectNameRequest
        @return: CheckSiteProjectNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.check_site_project_name_with_options_async(request, runtime)

    def check_user_project_name_with_options(
        self,
        request: esa20240910_models.CheckUserProjectNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckUserProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task by account.
        
        @param request: CheckUserProjectNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckUserProjectNameResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckUserProjectName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckUserProjectNameResponse(),
            self.call_api(params, req, runtime)
        )

    async def check_user_project_name_with_options_async(
        self,
        request: esa20240910_models.CheckUserProjectNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CheckUserProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task by account.
        
        @param request: CheckUserProjectNameRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckUserProjectNameResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CheckUserProjectName',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CheckUserProjectNameResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def check_user_project_name(
        self,
        request: esa20240910_models.CheckUserProjectNameRequest,
    ) -> esa20240910_models.CheckUserProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task by account.
        
        @param request: CheckUserProjectNameRequest
        @return: CheckUserProjectNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.check_user_project_name_with_options(request, runtime)

    async def check_user_project_name_async(
        self,
        request: esa20240910_models.CheckUserProjectNameRequest,
    ) -> esa20240910_models.CheckUserProjectNameResponse:
        """
        @summary Checks the name of a real-time log delivery task by account.
        
        @param request: CheckUserProjectNameRequest
        @return: CheckUserProjectNameResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.check_user_project_name_with_options_async(request, runtime)

    def commit_routine_staging_code_with_options(
        self,
        request: esa20240910_models.CommitRoutineStagingCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CommitRoutineStagingCodeResponse:
        """
        @summary Commits the unstable code in the staging environment to generate an official code version.
        
        @param request: CommitRoutineStagingCodeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommitRoutineStagingCodeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_description):
            body['CodeDescription'] = request.code_description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CommitRoutineStagingCode',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CommitRoutineStagingCodeResponse(),
            self.call_api(params, req, runtime)
        )

    async def commit_routine_staging_code_with_options_async(
        self,
        request: esa20240910_models.CommitRoutineStagingCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CommitRoutineStagingCodeResponse:
        """
        @summary Commits the unstable code in the staging environment to generate an official code version.
        
        @param request: CommitRoutineStagingCodeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommitRoutineStagingCodeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_description):
            body['CodeDescription'] = request.code_description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CommitRoutineStagingCode',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CommitRoutineStagingCodeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def commit_routine_staging_code(
        self,
        request: esa20240910_models.CommitRoutineStagingCodeRequest,
    ) -> esa20240910_models.CommitRoutineStagingCodeResponse:
        """
        @summary Commits the unstable code in the staging environment to generate an official code version.
        
        @param request: CommitRoutineStagingCodeRequest
        @return: CommitRoutineStagingCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.commit_routine_staging_code_with_options(request, runtime)

    async def commit_routine_staging_code_async(
        self,
        request: esa20240910_models.CommitRoutineStagingCodeRequest,
    ) -> esa20240910_models.CommitRoutineStagingCodeResponse:
        """
        @summary Commits the unstable code in the staging environment to generate an official code version.
        
        @param request: CommitRoutineStagingCodeRequest
        @return: CommitRoutineStagingCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.commit_routine_staging_code_with_options_async(request, runtime)

    def create_client_certificate_with_options(
        self,
        request: esa20240910_models.CreateClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateClientCertificateResponse:
        """
        @summary 创建客户端证书
        
        @param request: CreateClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.csr):
            body['CSR'] = request.csr
        if not UtilClient.is_unset(request.pkey_type):
            body['PkeyType'] = request.pkey_type
        if not UtilClient.is_unset(request.validity_days):
            body['ValidityDays'] = request.validity_days
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateClientCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_client_certificate_with_options_async(
        self,
        request: esa20240910_models.CreateClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateClientCertificateResponse:
        """
        @summary 创建客户端证书
        
        @param request: CreateClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.csr):
            body['CSR'] = request.csr
        if not UtilClient.is_unset(request.pkey_type):
            body['PkeyType'] = request.pkey_type
        if not UtilClient.is_unset(request.validity_days):
            body['ValidityDays'] = request.validity_days
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateClientCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_client_certificate(
        self,
        request: esa20240910_models.CreateClientCertificateRequest,
    ) -> esa20240910_models.CreateClientCertificateResponse:
        """
        @summary 创建客户端证书
        
        @param request: CreateClientCertificateRequest
        @return: CreateClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_client_certificate_with_options(request, runtime)

    async def create_client_certificate_async(
        self,
        request: esa20240910_models.CreateClientCertificateRequest,
    ) -> esa20240910_models.CreateClientCertificateResponse:
        """
        @summary 创建客户端证书
        
        @param request: CreateClientCertificateRequest
        @return: CreateClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_client_certificate_with_options_async(request, runtime)

    def create_custom_scene_policy_with_options(
        self,
        request: esa20240910_models.CreateCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateCustomScenePolicyResponse:
        """
        @summary Creates an account-level custom scenario policy. You can execute a policy after you associate the policy with a website.
        
        @param request: CreateCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.objects):
            query['Objects'] = request.objects
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.template):
            query['Template'] = request.template
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateCustomScenePolicyResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_custom_scene_policy_with_options_async(
        self,
        request: esa20240910_models.CreateCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateCustomScenePolicyResponse:
        """
        @summary Creates an account-level custom scenario policy. You can execute a policy after you associate the policy with a website.
        
        @param request: CreateCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.objects):
            query['Objects'] = request.objects
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.template):
            query['Template'] = request.template
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateCustomScenePolicyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_custom_scene_policy(
        self,
        request: esa20240910_models.CreateCustomScenePolicyRequest,
    ) -> esa20240910_models.CreateCustomScenePolicyResponse:
        """
        @summary Creates an account-level custom scenario policy. You can execute a policy after you associate the policy with a website.
        
        @param request: CreateCustomScenePolicyRequest
        @return: CreateCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_custom_scene_policy_with_options(request, runtime)

    async def create_custom_scene_policy_async(
        self,
        request: esa20240910_models.CreateCustomScenePolicyRequest,
    ) -> esa20240910_models.CreateCustomScenePolicyResponse:
        """
        @summary Creates an account-level custom scenario policy. You can execute a policy after you associate the policy with a website.
        
        @param request: CreateCustomScenePolicyRequest
        @return: CreateCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_custom_scene_policy_with_options_async(request, runtime)

    def create_edge_container_app_with_options(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppResponse:
        """
        @summary Creates a containerized application. You can deploy and release a version of the application across points of presence (POPs).
        
        @param request: CreateEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.health_check_fail_times):
            body['HealthCheckFailTimes'] = request.health_check_fail_times
        if not UtilClient.is_unset(request.health_check_host):
            body['HealthCheckHost'] = request.health_check_host
        if not UtilClient.is_unset(request.health_check_http_code):
            body['HealthCheckHttpCode'] = request.health_check_http_code
        if not UtilClient.is_unset(request.health_check_interval):
            body['HealthCheckInterval'] = request.health_check_interval
        if not UtilClient.is_unset(request.health_check_method):
            body['HealthCheckMethod'] = request.health_check_method
        if not UtilClient.is_unset(request.health_check_port):
            body['HealthCheckPort'] = request.health_check_port
        if not UtilClient.is_unset(request.health_check_succ_times):
            body['HealthCheckSuccTimes'] = request.health_check_succ_times
        if not UtilClient.is_unset(request.health_check_timeout):
            body['HealthCheckTimeout'] = request.health_check_timeout
        if not UtilClient.is_unset(request.health_check_type):
            body['HealthCheckType'] = request.health_check_type
        if not UtilClient.is_unset(request.health_check_uri):
            body['HealthCheckURI'] = request.health_check_uri
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        if not UtilClient.is_unset(request.service_port):
            body['ServicePort'] = request.service_port
        if not UtilClient.is_unset(request.target_port):
            body['TargetPort'] = request.target_port
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_edge_container_app_with_options_async(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppResponse:
        """
        @summary Creates a containerized application. You can deploy and release a version of the application across points of presence (POPs).
        
        @param request: CreateEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.health_check_fail_times):
            body['HealthCheckFailTimes'] = request.health_check_fail_times
        if not UtilClient.is_unset(request.health_check_host):
            body['HealthCheckHost'] = request.health_check_host
        if not UtilClient.is_unset(request.health_check_http_code):
            body['HealthCheckHttpCode'] = request.health_check_http_code
        if not UtilClient.is_unset(request.health_check_interval):
            body['HealthCheckInterval'] = request.health_check_interval
        if not UtilClient.is_unset(request.health_check_method):
            body['HealthCheckMethod'] = request.health_check_method
        if not UtilClient.is_unset(request.health_check_port):
            body['HealthCheckPort'] = request.health_check_port
        if not UtilClient.is_unset(request.health_check_succ_times):
            body['HealthCheckSuccTimes'] = request.health_check_succ_times
        if not UtilClient.is_unset(request.health_check_timeout):
            body['HealthCheckTimeout'] = request.health_check_timeout
        if not UtilClient.is_unset(request.health_check_type):
            body['HealthCheckType'] = request.health_check_type
        if not UtilClient.is_unset(request.health_check_uri):
            body['HealthCheckURI'] = request.health_check_uri
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        if not UtilClient.is_unset(request.service_port):
            body['ServicePort'] = request.service_port
        if not UtilClient.is_unset(request.target_port):
            body['TargetPort'] = request.target_port
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_edge_container_app(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppResponse:
        """
        @summary Creates a containerized application. You can deploy and release a version of the application across points of presence (POPs).
        
        @param request: CreateEdgeContainerAppRequest
        @return: CreateEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_edge_container_app_with_options(request, runtime)

    async def create_edge_container_app_async(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppResponse:
        """
        @summary Creates a containerized application. You can deploy and release a version of the application across points of presence (POPs).
        
        @param request: CreateEdgeContainerAppRequest
        @return: CreateEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_edge_container_app_with_options_async(request, runtime)

    def create_edge_container_app_record_with_options(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppRecordResponse:
        """
        @summary Associates a domain name with a containerized application. This way, requests destined for the associated domain name are forwarded to the application.
        
        @param request: CreateEdgeContainerAppRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerAppRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_edge_container_app_record_with_options_async(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppRecordResponse:
        """
        @summary Associates a domain name with a containerized application. This way, requests destined for the associated domain name are forwarded to the application.
        
        @param request: CreateEdgeContainerAppRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerAppRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_edge_container_app_record(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRecordRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppRecordResponse:
        """
        @summary Associates a domain name with a containerized application. This way, requests destined for the associated domain name are forwarded to the application.
        
        @param request: CreateEdgeContainerAppRecordRequest
        @return: CreateEdgeContainerAppRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_edge_container_app_record_with_options(request, runtime)

    async def create_edge_container_app_record_async(
        self,
        request: esa20240910_models.CreateEdgeContainerAppRecordRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppRecordResponse:
        """
        @summary Associates a domain name with a containerized application. This way, requests destined for the associated domain name are forwarded to the application.
        
        @param request: CreateEdgeContainerAppRecordRequest
        @return: CreateEdgeContainerAppRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_edge_container_app_record_with_options_async(request, runtime)

    def create_edge_container_app_version_with_options(
        self,
        tmp_req: esa20240910_models.CreateEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppVersionResponse:
        """
        @summary Creates a version for a containerized application. You can iterate the application based on the version.
        
        @param tmp_req: CreateEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateEdgeContainerAppVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.containers):
            request.containers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.containers, 'Containers', 'json')
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.containers_shrink):
            body['Containers'] = request.containers_shrink
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_edge_container_app_version_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateEdgeContainerAppVersionResponse:
        """
        @summary Creates a version for a containerized application. You can iterate the application based on the version.
        
        @param tmp_req: CreateEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateEdgeContainerAppVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.containers):
            request.containers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.containers, 'Containers', 'json')
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.containers_shrink):
            body['Containers'] = request.containers_shrink
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateEdgeContainerAppVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_edge_container_app_version(
        self,
        request: esa20240910_models.CreateEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppVersionResponse:
        """
        @summary Creates a version for a containerized application. You can iterate the application based on the version.
        
        @param request: CreateEdgeContainerAppVersionRequest
        @return: CreateEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_edge_container_app_version_with_options(request, runtime)

    async def create_edge_container_app_version_async(
        self,
        request: esa20240910_models.CreateEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.CreateEdgeContainerAppVersionResponse:
        """
        @summary Creates a version for a containerized application. You can iterate the application based on the version.
        
        @param request: CreateEdgeContainerAppVersionRequest
        @return: CreateEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_edge_container_app_version_with_options_async(request, runtime)

    def create_kv_namespace_with_options(
        self,
        request: esa20240910_models.CreateKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateKvNamespaceResponse:
        """
        @summary Create a namespace in your Alibaba Cloud account.
        
        @param request: CreateKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.namespace):
            body['Namespace'] = request.namespace
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateKvNamespaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_kv_namespace_with_options_async(
        self,
        request: esa20240910_models.CreateKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateKvNamespaceResponse:
        """
        @summary Create a namespace in your Alibaba Cloud account.
        
        @param request: CreateKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.namespace):
            body['Namespace'] = request.namespace
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateKvNamespaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_kv_namespace(
        self,
        request: esa20240910_models.CreateKvNamespaceRequest,
    ) -> esa20240910_models.CreateKvNamespaceResponse:
        """
        @summary Create a namespace in your Alibaba Cloud account.
        
        @param request: CreateKvNamespaceRequest
        @return: CreateKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_kv_namespace_with_options(request, runtime)

    async def create_kv_namespace_async(
        self,
        request: esa20240910_models.CreateKvNamespaceRequest,
    ) -> esa20240910_models.CreateKvNamespaceResponse:
        """
        @summary Create a namespace in your Alibaba Cloud account.
        
        @param request: CreateKvNamespaceRequest
        @return: CreateKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_kv_namespace_with_options_async(request, runtime)

    def create_list_with_options(
        self,
        tmp_req: esa20240910_models.CreateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateListResponse:
        """
        @summary Creates a list. Lists are used for the referencing of values in the rules engine to implement complex logic and control in security policies.
        
        @param tmp_req: CreateListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.items):
            request.items_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.items, 'Items', 'json')
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.items_shrink):
            body['Items'] = request.items_shrink
        if not UtilClient.is_unset(request.kind):
            body['Kind'] = request.kind
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateListResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_list_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateListResponse:
        """
        @summary Creates a list. Lists are used for the referencing of values in the rules engine to implement complex logic and control in security policies.
        
        @param tmp_req: CreateListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.items):
            request.items_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.items, 'Items', 'json')
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.items_shrink):
            body['Items'] = request.items_shrink
        if not UtilClient.is_unset(request.kind):
            body['Kind'] = request.kind
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_list(
        self,
        request: esa20240910_models.CreateListRequest,
    ) -> esa20240910_models.CreateListResponse:
        """
        @summary Creates a list. Lists are used for the referencing of values in the rules engine to implement complex logic and control in security policies.
        
        @param request: CreateListRequest
        @return: CreateListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_list_with_options(request, runtime)

    async def create_list_async(
        self,
        request: esa20240910_models.CreateListRequest,
    ) -> esa20240910_models.CreateListResponse:
        """
        @summary Creates a list. Lists are used for the referencing of values in the rules engine to implement complex logic and control in security policies.
        
        @param request: CreateListRequest
        @return: CreateListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_list_with_options_async(request, runtime)

    def create_origin_protection_with_options(
        self,
        request: esa20240910_models.CreateOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateOriginProtectionResponse:
        """
        @summary Enables origin protection.
        
        @param request: CreateOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateOriginProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_origin_protection_with_options_async(
        self,
        request: esa20240910_models.CreateOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateOriginProtectionResponse:
        """
        @summary Enables origin protection.
        
        @param request: CreateOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateOriginProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_origin_protection(
        self,
        request: esa20240910_models.CreateOriginProtectionRequest,
    ) -> esa20240910_models.CreateOriginProtectionResponse:
        """
        @summary Enables origin protection.
        
        @param request: CreateOriginProtectionRequest
        @return: CreateOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_origin_protection_with_options(request, runtime)

    async def create_origin_protection_async(
        self,
        request: esa20240910_models.CreateOriginProtectionRequest,
    ) -> esa20240910_models.CreateOriginProtectionResponse:
        """
        @summary Enables origin protection.
        
        @param request: CreateOriginProtectionRequest
        @return: CreateOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_origin_protection_with_options_async(request, runtime)

    def create_page_with_options(
        self,
        request: esa20240910_models.CreatePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreatePageResponse:
        """
        @summary Creates a custom error page, which is displayed when a request is blocked by Web Application Firewall (WAF). You can configure the HTML content, page type, and description, and submit the Base64-encoded page content.
        
        @param request: CreatePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreatePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.content_type):
            body['ContentType'] = request.content_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreatePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreatePageResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_page_with_options_async(
        self,
        request: esa20240910_models.CreatePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreatePageResponse:
        """
        @summary Creates a custom error page, which is displayed when a request is blocked by Web Application Firewall (WAF). You can configure the HTML content, page type, and description, and submit the Base64-encoded page content.
        
        @param request: CreatePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreatePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.content_type):
            body['ContentType'] = request.content_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreatePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreatePageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_page(
        self,
        request: esa20240910_models.CreatePageRequest,
    ) -> esa20240910_models.CreatePageResponse:
        """
        @summary Creates a custom error page, which is displayed when a request is blocked by Web Application Firewall (WAF). You can configure the HTML content, page type, and description, and submit the Base64-encoded page content.
        
        @param request: CreatePageRequest
        @return: CreatePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_page_with_options(request, runtime)

    async def create_page_async(
        self,
        request: esa20240910_models.CreatePageRequest,
    ) -> esa20240910_models.CreatePageResponse:
        """
        @summary Creates a custom error page, which is displayed when a request is blocked by Web Application Firewall (WAF). You can configure the HTML content, page type, and description, and submit the Base64-encoded page content.
        
        @param request: CreatePageRequest
        @return: CreatePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_page_with_options_async(request, runtime)

    def create_record_with_options(
        self,
        tmp_req: esa20240910_models.CreateRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRecordResponse:
        """
        @summary Creates a DNS record for a specific website.
        
        @param tmp_req: CreateRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRecordResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateRecordShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.auth_conf):
            request.auth_conf_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.auth_conf, 'AuthConf', 'json')
        if not UtilClient.is_unset(tmp_req.data):
            request.data_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.data, 'Data', 'json')
        query = {}
        if not UtilClient.is_unset(request.auth_conf_shrink):
            query['AuthConf'] = request.auth_conf_shrink
        if not UtilClient.is_unset(request.biz_name):
            query['BizName'] = request.biz_name
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.data_shrink):
            query['Data'] = request.data_shrink
        if not UtilClient.is_unset(request.host_policy):
            query['HostPolicy'] = request.host_policy
        if not UtilClient.is_unset(request.proxied):
            query['Proxied'] = request.proxied
        if not UtilClient.is_unset(request.record_name):
            query['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.ttl):
            query['Ttl'] = request.ttl
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_record_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRecordResponse:
        """
        @summary Creates a DNS record for a specific website.
        
        @param tmp_req: CreateRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRecordResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateRecordShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.auth_conf):
            request.auth_conf_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.auth_conf, 'AuthConf', 'json')
        if not UtilClient.is_unset(tmp_req.data):
            request.data_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.data, 'Data', 'json')
        query = {}
        if not UtilClient.is_unset(request.auth_conf_shrink):
            query['AuthConf'] = request.auth_conf_shrink
        if not UtilClient.is_unset(request.biz_name):
            query['BizName'] = request.biz_name
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.data_shrink):
            query['Data'] = request.data_shrink
        if not UtilClient.is_unset(request.host_policy):
            query['HostPolicy'] = request.host_policy
        if not UtilClient.is_unset(request.proxied):
            query['Proxied'] = request.proxied
        if not UtilClient.is_unset(request.record_name):
            query['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.ttl):
            query['Ttl'] = request.ttl
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_record(
        self,
        request: esa20240910_models.CreateRecordRequest,
    ) -> esa20240910_models.CreateRecordResponse:
        """
        @summary Creates a DNS record for a specific website.
        
        @param request: CreateRecordRequest
        @return: CreateRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_record_with_options(request, runtime)

    async def create_record_async(
        self,
        request: esa20240910_models.CreateRecordRequest,
    ) -> esa20240910_models.CreateRecordResponse:
        """
        @summary Creates a DNS record for a specific website.
        
        @param request: CreateRecordRequest
        @return: CreateRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_record_with_options_async(request, runtime)

    def create_routine_with_options(
        self,
        request: esa20240910_models.CreateRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineResponse:
        """
        @summary Creates a routine.
        
        @param request: CreateRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.spec_name):
            body['SpecName'] = request.spec_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_routine_with_options_async(
        self,
        request: esa20240910_models.CreateRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineResponse:
        """
        @summary Creates a routine.
        
        @param request: CreateRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.spec_name):
            body['SpecName'] = request.spec_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_routine(
        self,
        request: esa20240910_models.CreateRoutineRequest,
    ) -> esa20240910_models.CreateRoutineResponse:
        """
        @summary Creates a routine.
        
        @param request: CreateRoutineRequest
        @return: CreateRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_routine_with_options(request, runtime)

    async def create_routine_async(
        self,
        request: esa20240910_models.CreateRoutineRequest,
    ) -> esa20240910_models.CreateRoutineResponse:
        """
        @summary Creates a routine.
        
        @param request: CreateRoutineRequest
        @return: CreateRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_routine_with_options_async(request, runtime)

    def create_routine_related_record_with_options(
        self,
        request: esa20240910_models.CreateRoutineRelatedRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineRelatedRecordResponse:
        """
        @summary Adds a record to map a domain that is associated with a routine. This record is used to trigger the associated routine code.
        
        @param request: CreateRoutineRelatedRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineRelatedRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutineRelatedRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineRelatedRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_routine_related_record_with_options_async(
        self,
        request: esa20240910_models.CreateRoutineRelatedRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineRelatedRecordResponse:
        """
        @summary Adds a record to map a domain that is associated with a routine. This record is used to trigger the associated routine code.
        
        @param request: CreateRoutineRelatedRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineRelatedRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutineRelatedRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineRelatedRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_routine_related_record(
        self,
        request: esa20240910_models.CreateRoutineRelatedRecordRequest,
    ) -> esa20240910_models.CreateRoutineRelatedRecordResponse:
        """
        @summary Adds a record to map a domain that is associated with a routine. This record is used to trigger the associated routine code.
        
        @param request: CreateRoutineRelatedRecordRequest
        @return: CreateRoutineRelatedRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_routine_related_record_with_options(request, runtime)

    async def create_routine_related_record_async(
        self,
        request: esa20240910_models.CreateRoutineRelatedRecordRequest,
    ) -> esa20240910_models.CreateRoutineRelatedRecordResponse:
        """
        @summary Adds a record to map a domain that is associated with a routine. This record is used to trigger the associated routine code.
        
        @param request: CreateRoutineRelatedRecordRequest
        @return: CreateRoutineRelatedRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_routine_related_record_with_options_async(request, runtime)

    def create_routine_related_route_with_options(
        self,
        request: esa20240910_models.CreateRoutineRelatedRouteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineRelatedRouteResponse:
        """
        @summary Adds a route to map a URL to a routine so that the routine can be triggered to respond to requests destined for the URL.
        
        @param request: CreateRoutineRelatedRouteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineRelatedRouteResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.by_pass):
            body['ByPass'] = request.by_pass
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.route):
            body['Route'] = request.route
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutineRelatedRoute',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineRelatedRouteResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_routine_related_route_with_options_async(
        self,
        request: esa20240910_models.CreateRoutineRelatedRouteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateRoutineRelatedRouteResponse:
        """
        @summary Adds a route to map a URL to a routine so that the routine can be triggered to respond to requests destined for the URL.
        
        @param request: CreateRoutineRelatedRouteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateRoutineRelatedRouteResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.by_pass):
            body['ByPass'] = request.by_pass
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.route):
            body['Route'] = request.route
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateRoutineRelatedRoute',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateRoutineRelatedRouteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_routine_related_route(
        self,
        request: esa20240910_models.CreateRoutineRelatedRouteRequest,
    ) -> esa20240910_models.CreateRoutineRelatedRouteResponse:
        """
        @summary Adds a route to map a URL to a routine so that the routine can be triggered to respond to requests destined for the URL.
        
        @param request: CreateRoutineRelatedRouteRequest
        @return: CreateRoutineRelatedRouteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_routine_related_route_with_options(request, runtime)

    async def create_routine_related_route_async(
        self,
        request: esa20240910_models.CreateRoutineRelatedRouteRequest,
    ) -> esa20240910_models.CreateRoutineRelatedRouteResponse:
        """
        @summary Adds a route to map a URL to a routine so that the routine can be triggered to respond to requests destined for the URL.
        
        @param request: CreateRoutineRelatedRouteRequest
        @return: CreateRoutineRelatedRouteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_routine_related_route_with_options_async(request, runtime)

    def create_scheduled_preload_executions_with_options(
        self,
        tmp_req: esa20240910_models.CreateScheduledPreloadExecutionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateScheduledPreloadExecutionsResponse:
        """
        @summary Creates scheduled prefetch plans.
        
        @param tmp_req: CreateScheduledPreloadExecutionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateScheduledPreloadExecutionsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateScheduledPreloadExecutionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.executions):
            request.executions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.executions, 'Executions', 'json')
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        body = {}
        if not UtilClient.is_unset(request.executions_shrink):
            body['Executions'] = request.executions_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateScheduledPreloadExecutions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateScheduledPreloadExecutionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_scheduled_preload_executions_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateScheduledPreloadExecutionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateScheduledPreloadExecutionsResponse:
        """
        @summary Creates scheduled prefetch plans.
        
        @param tmp_req: CreateScheduledPreloadExecutionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateScheduledPreloadExecutionsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateScheduledPreloadExecutionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.executions):
            request.executions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.executions, 'Executions', 'json')
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        body = {}
        if not UtilClient.is_unset(request.executions_shrink):
            body['Executions'] = request.executions_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateScheduledPreloadExecutions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateScheduledPreloadExecutionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_scheduled_preload_executions(
        self,
        request: esa20240910_models.CreateScheduledPreloadExecutionsRequest,
    ) -> esa20240910_models.CreateScheduledPreloadExecutionsResponse:
        """
        @summary Creates scheduled prefetch plans.
        
        @param request: CreateScheduledPreloadExecutionsRequest
        @return: CreateScheduledPreloadExecutionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_scheduled_preload_executions_with_options(request, runtime)

    async def create_scheduled_preload_executions_async(
        self,
        request: esa20240910_models.CreateScheduledPreloadExecutionsRequest,
    ) -> esa20240910_models.CreateScheduledPreloadExecutionsResponse:
        """
        @summary Creates scheduled prefetch plans.
        
        @param request: CreateScheduledPreloadExecutionsRequest
        @return: CreateScheduledPreloadExecutionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_scheduled_preload_executions_with_options_async(request, runtime)

    def create_scheduled_preload_job_with_options(
        self,
        request: esa20240910_models.CreateScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateScheduledPreloadJobResponse:
        """
        @summary Adds a scheduled prefetch task.
        
        @param request: CreateScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.insert_way):
            body['InsertWay'] = request.insert_way
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.oss_url):
            body['OssUrl'] = request.oss_url
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.url_list):
            body['UrlList'] = request.url_list
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateScheduledPreloadJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_scheduled_preload_job_with_options_async(
        self,
        request: esa20240910_models.CreateScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateScheduledPreloadJobResponse:
        """
        @summary Adds a scheduled prefetch task.
        
        @param request: CreateScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.insert_way):
            body['InsertWay'] = request.insert_way
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.oss_url):
            body['OssUrl'] = request.oss_url
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.url_list):
            body['UrlList'] = request.url_list
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateScheduledPreloadJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_scheduled_preload_job(
        self,
        request: esa20240910_models.CreateScheduledPreloadJobRequest,
    ) -> esa20240910_models.CreateScheduledPreloadJobResponse:
        """
        @summary Adds a scheduled prefetch task.
        
        @param request: CreateScheduledPreloadJobRequest
        @return: CreateScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_scheduled_preload_job_with_options(request, runtime)

    async def create_scheduled_preload_job_async(
        self,
        request: esa20240910_models.CreateScheduledPreloadJobRequest,
    ) -> esa20240910_models.CreateScheduledPreloadJobResponse:
        """
        @summary Adds a scheduled prefetch task.
        
        @param request: CreateScheduledPreloadJobRequest
        @return: CreateScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_scheduled_preload_job_with_options_async(request, runtime)

    def create_site_with_options(
        self,
        request: esa20240910_models.CreateSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteResponse:
        """
        @summary Adds a website.
        
        @description    Make sure that you have an available plan before you add a website.
        Make sure that your website domain name has an ICP filing if the location you want to specify covers the Chinese mainland.
        
        @param request: CreateSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_type):
            query['AccessType'] = request.access_type
        if not UtilClient.is_unset(request.coverage):
            query['Coverage'] = request.coverage
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.site_name):
            query['SiteName'] = request.site_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_site_with_options_async(
        self,
        request: esa20240910_models.CreateSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteResponse:
        """
        @summary Adds a website.
        
        @description    Make sure that you have an available plan before you add a website.
        Make sure that your website domain name has an ICP filing if the location you want to specify covers the Chinese mainland.
        
        @param request: CreateSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_type):
            query['AccessType'] = request.access_type
        if not UtilClient.is_unset(request.coverage):
            query['Coverage'] = request.coverage
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.site_name):
            query['SiteName'] = request.site_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_site(
        self,
        request: esa20240910_models.CreateSiteRequest,
    ) -> esa20240910_models.CreateSiteResponse:
        """
        @summary Adds a website.
        
        @description    Make sure that you have an available plan before you add a website.
        Make sure that your website domain name has an ICP filing if the location you want to specify covers the Chinese mainland.
        
        @param request: CreateSiteRequest
        @return: CreateSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_site_with_options(request, runtime)

    async def create_site_async(
        self,
        request: esa20240910_models.CreateSiteRequest,
    ) -> esa20240910_models.CreateSiteResponse:
        """
        @summary Adds a website.
        
        @description    Make sure that you have an available plan before you add a website.
        Make sure that your website domain name has an ICP filing if the location you want to specify covers the Chinese mainland.
        
        @param request: CreateSiteRequest
        @return: CreateSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_site_with_options_async(request, runtime)

    def create_site_custom_log_with_options(
        self,
        tmp_req: esa20240910_models.CreateSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteCustomLogResponse:
        """
        @summary Adds the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @description    **Custom field limits**: The key name of a custom field can contain only letters, digits, underscores (_), and spaces. The key name cannot contain other characters. Otherwise, errors may occur.
        **Parameter passing**: Submit `SiteId`, `RequestHeaders`, `ResponseHeaders`, and `Cookies` by using `formData`. Each array element matches a custom field name.
        **(Required) SiteId**: Although `SiteId` is not marked as required in the Required column, you must specify a website ID by using this parameter when you can call this API operation.
        
        @param tmp_req: CreateSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteCustomLogResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateSiteCustomLogShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cookies):
            request.cookies_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cookies, 'Cookies', 'json')
        if not UtilClient.is_unset(tmp_req.request_headers):
            request.request_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.request_headers, 'RequestHeaders', 'json')
        if not UtilClient.is_unset(tmp_req.response_headers):
            request.response_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.response_headers, 'ResponseHeaders', 'json')
        body = {}
        if not UtilClient.is_unset(request.cookies_shrink):
            body['Cookies'] = request.cookies_shrink
        if not UtilClient.is_unset(request.request_headers_shrink):
            body['RequestHeaders'] = request.request_headers_shrink
        if not UtilClient.is_unset(request.response_headers_shrink):
            body['ResponseHeaders'] = request.response_headers_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteCustomLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_site_custom_log_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteCustomLogResponse:
        """
        @summary Adds the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @description    **Custom field limits**: The key name of a custom field can contain only letters, digits, underscores (_), and spaces. The key name cannot contain other characters. Otherwise, errors may occur.
        **Parameter passing**: Submit `SiteId`, `RequestHeaders`, `ResponseHeaders`, and `Cookies` by using `formData`. Each array element matches a custom field name.
        **(Required) SiteId**: Although `SiteId` is not marked as required in the Required column, you must specify a website ID by using this parameter when you can call this API operation.
        
        @param tmp_req: CreateSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteCustomLogResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateSiteCustomLogShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cookies):
            request.cookies_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cookies, 'Cookies', 'json')
        if not UtilClient.is_unset(tmp_req.request_headers):
            request.request_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.request_headers, 'RequestHeaders', 'json')
        if not UtilClient.is_unset(tmp_req.response_headers):
            request.response_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.response_headers, 'ResponseHeaders', 'json')
        body = {}
        if not UtilClient.is_unset(request.cookies_shrink):
            body['Cookies'] = request.cookies_shrink
        if not UtilClient.is_unset(request.request_headers_shrink):
            body['RequestHeaders'] = request.request_headers_shrink
        if not UtilClient.is_unset(request.response_headers_shrink):
            body['ResponseHeaders'] = request.response_headers_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteCustomLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_site_custom_log(
        self,
        request: esa20240910_models.CreateSiteCustomLogRequest,
    ) -> esa20240910_models.CreateSiteCustomLogResponse:
        """
        @summary Adds the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @description    **Custom field limits**: The key name of a custom field can contain only letters, digits, underscores (_), and spaces. The key name cannot contain other characters. Otherwise, errors may occur.
        **Parameter passing**: Submit `SiteId`, `RequestHeaders`, `ResponseHeaders`, and `Cookies` by using `formData`. Each array element matches a custom field name.
        **(Required) SiteId**: Although `SiteId` is not marked as required in the Required column, you must specify a website ID by using this parameter when you can call this API operation.
        
        @param request: CreateSiteCustomLogRequest
        @return: CreateSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_site_custom_log_with_options(request, runtime)

    async def create_site_custom_log_async(
        self,
        request: esa20240910_models.CreateSiteCustomLogRequest,
    ) -> esa20240910_models.CreateSiteCustomLogResponse:
        """
        @summary Adds the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @description    **Custom field limits**: The key name of a custom field can contain only letters, digits, underscores (_), and spaces. The key name cannot contain other characters. Otherwise, errors may occur.
        **Parameter passing**: Submit `SiteId`, `RequestHeaders`, `ResponseHeaders`, and `Cookies` by using `formData`. Each array element matches a custom field name.
        **(Required) SiteId**: Although `SiteId` is not marked as required in the Required column, you must specify a website ID by using this parameter when you can call this API operation.
        
        @param request: CreateSiteCustomLogRequest
        @return: CreateSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_site_custom_log_with_options_async(request, runtime)

    def create_site_delivery_task_with_options(
        self,
        tmp_req: esa20240910_models.CreateSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteDeliveryTaskResponse:
        """
        @summary Creates a real-time log delivery task.
        
        @param tmp_req: CreateSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateSiteDeliveryTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.http_delivery):
            request.http_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.http_delivery, 'HttpDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.kafka_delivery):
            request.kafka_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kafka_delivery, 'KafkaDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.oss_delivery):
            request.oss_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.oss_delivery, 'OssDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.s_3delivery):
            request.s_3delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.s_3delivery, 'S3Delivery', 'json')
        if not UtilClient.is_unset(tmp_req.sls_delivery):
            request.sls_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sls_delivery, 'SlsDelivery', 'json')
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.data_center):
            body['DataCenter'] = request.data_center
        if not UtilClient.is_unset(request.delivery_type):
            body['DeliveryType'] = request.delivery_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.http_delivery_shrink):
            body['HttpDelivery'] = request.http_delivery_shrink
        if not UtilClient.is_unset(request.kafka_delivery_shrink):
            body['KafkaDelivery'] = request.kafka_delivery_shrink
        if not UtilClient.is_unset(request.oss_delivery_shrink):
            body['OssDelivery'] = request.oss_delivery_shrink
        if not UtilClient.is_unset(request.s_3delivery_shrink):
            body['S3Delivery'] = request.s_3delivery_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.sls_delivery_shrink):
            body['SlsDelivery'] = request.sls_delivery_shrink
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_site_delivery_task_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateSiteDeliveryTaskResponse:
        """
        @summary Creates a real-time log delivery task.
        
        @param tmp_req: CreateSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateSiteDeliveryTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.http_delivery):
            request.http_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.http_delivery, 'HttpDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.kafka_delivery):
            request.kafka_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kafka_delivery, 'KafkaDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.oss_delivery):
            request.oss_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.oss_delivery, 'OssDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.s_3delivery):
            request.s_3delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.s_3delivery, 'S3Delivery', 'json')
        if not UtilClient.is_unset(tmp_req.sls_delivery):
            request.sls_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sls_delivery, 'SlsDelivery', 'json')
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.data_center):
            body['DataCenter'] = request.data_center
        if not UtilClient.is_unset(request.delivery_type):
            body['DeliveryType'] = request.delivery_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.http_delivery_shrink):
            body['HttpDelivery'] = request.http_delivery_shrink
        if not UtilClient.is_unset(request.kafka_delivery_shrink):
            body['KafkaDelivery'] = request.kafka_delivery_shrink
        if not UtilClient.is_unset(request.oss_delivery_shrink):
            body['OssDelivery'] = request.oss_delivery_shrink
        if not UtilClient.is_unset(request.s_3delivery_shrink):
            body['S3Delivery'] = request.s_3delivery_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.sls_delivery_shrink):
            body['SlsDelivery'] = request.sls_delivery_shrink
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateSiteDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_site_delivery_task(
        self,
        request: esa20240910_models.CreateSiteDeliveryTaskRequest,
    ) -> esa20240910_models.CreateSiteDeliveryTaskResponse:
        """
        @summary Creates a real-time log delivery task.
        
        @param request: CreateSiteDeliveryTaskRequest
        @return: CreateSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_site_delivery_task_with_options(request, runtime)

    async def create_site_delivery_task_async(
        self,
        request: esa20240910_models.CreateSiteDeliveryTaskRequest,
    ) -> esa20240910_models.CreateSiteDeliveryTaskResponse:
        """
        @summary Creates a real-time log delivery task.
        
        @param request: CreateSiteDeliveryTaskRequest
        @return: CreateSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_site_delivery_task_with_options_async(request, runtime)

    def create_user_delivery_task_with_options(
        self,
        tmp_req: esa20240910_models.CreateUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateUserDeliveryTaskResponse:
        """
        @summary Creates a log delivery task to ship logs to the specified destination.
        
        @description This API operation allows you to deliver logs to destinations such as Simple Log Service (SLS), HTTP servers, Object Storage Service (OSS), Amazon Simple Storage Service (S3), and Kafka. You can specify the task name, log fields to deliver, data center, discard rate, delivery type, and delivery details.
        **Field filtering**: Use the `FieldName` parameter to specify log fields to deliver.
        **Filtering rules**: Use the `FilterRules` parameter to pre-process and filter log data.
        **Diverse delivery destinations**: Logs can be delivered to different destinations. Configuration parameters vary with delivery destinations.
        ## [](#)Precautions
        Make sure that you have sufficient permissions to perform delivery tasks.
        If you enable encryption or authentication, properly configure corresponding parameters.
        Verify the syntax of `FilterRules` to make sure that filtering logic works as expected.
        Specify advanced settings such as the number of retries and timeout period based on your needs to have optimal delivery efficiency and stability.
        
        @param tmp_req: CreateUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateUserDeliveryTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateUserDeliveryTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.http_delivery):
            request.http_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.http_delivery, 'HttpDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.kafka_delivery):
            request.kafka_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kafka_delivery, 'KafkaDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.oss_delivery):
            request.oss_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.oss_delivery, 'OssDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.s_3delivery):
            request.s_3delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.s_3delivery, 'S3Delivery', 'json')
        if not UtilClient.is_unset(tmp_req.sls_delivery):
            request.sls_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sls_delivery, 'SlsDelivery', 'json')
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.data_center):
            body['DataCenter'] = request.data_center
        if not UtilClient.is_unset(request.delivery_type):
            body['DeliveryType'] = request.delivery_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.http_delivery_shrink):
            body['HttpDelivery'] = request.http_delivery_shrink
        if not UtilClient.is_unset(request.kafka_delivery_shrink):
            body['KafkaDelivery'] = request.kafka_delivery_shrink
        if not UtilClient.is_unset(request.oss_delivery_shrink):
            body['OssDelivery'] = request.oss_delivery_shrink
        if not UtilClient.is_unset(request.s_3delivery_shrink):
            body['S3Delivery'] = request.s_3delivery_shrink
        if not UtilClient.is_unset(request.sls_delivery_shrink):
            body['SlsDelivery'] = request.sls_delivery_shrink
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateUserDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_user_delivery_task_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateUserDeliveryTaskResponse:
        """
        @summary Creates a log delivery task to ship logs to the specified destination.
        
        @description This API operation allows you to deliver logs to destinations such as Simple Log Service (SLS), HTTP servers, Object Storage Service (OSS), Amazon Simple Storage Service (S3), and Kafka. You can specify the task name, log fields to deliver, data center, discard rate, delivery type, and delivery details.
        **Field filtering**: Use the `FieldName` parameter to specify log fields to deliver.
        **Filtering rules**: Use the `FilterRules` parameter to pre-process and filter log data.
        **Diverse delivery destinations**: Logs can be delivered to different destinations. Configuration parameters vary with delivery destinations.
        ## [](#)Precautions
        Make sure that you have sufficient permissions to perform delivery tasks.
        If you enable encryption or authentication, properly configure corresponding parameters.
        Verify the syntax of `FilterRules` to make sure that filtering logic works as expected.
        Specify advanced settings such as the number of retries and timeout period based on your needs to have optimal delivery efficiency and stability.
        
        @param tmp_req: CreateUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateUserDeliveryTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateUserDeliveryTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.http_delivery):
            request.http_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.http_delivery, 'HttpDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.kafka_delivery):
            request.kafka_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.kafka_delivery, 'KafkaDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.oss_delivery):
            request.oss_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.oss_delivery, 'OssDelivery', 'json')
        if not UtilClient.is_unset(tmp_req.s_3delivery):
            request.s_3delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.s_3delivery, 'S3Delivery', 'json')
        if not UtilClient.is_unset(tmp_req.sls_delivery):
            request.sls_delivery_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sls_delivery, 'SlsDelivery', 'json')
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.data_center):
            body['DataCenter'] = request.data_center
        if not UtilClient.is_unset(request.delivery_type):
            body['DeliveryType'] = request.delivery_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.http_delivery_shrink):
            body['HttpDelivery'] = request.http_delivery_shrink
        if not UtilClient.is_unset(request.kafka_delivery_shrink):
            body['KafkaDelivery'] = request.kafka_delivery_shrink
        if not UtilClient.is_unset(request.oss_delivery_shrink):
            body['OssDelivery'] = request.oss_delivery_shrink
        if not UtilClient.is_unset(request.s_3delivery_shrink):
            body['S3Delivery'] = request.s_3delivery_shrink
        if not UtilClient.is_unset(request.sls_delivery_shrink):
            body['SlsDelivery'] = request.sls_delivery_shrink
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateUserDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_user_delivery_task(
        self,
        request: esa20240910_models.CreateUserDeliveryTaskRequest,
    ) -> esa20240910_models.CreateUserDeliveryTaskResponse:
        """
        @summary Creates a log delivery task to ship logs to the specified destination.
        
        @description This API operation allows you to deliver logs to destinations such as Simple Log Service (SLS), HTTP servers, Object Storage Service (OSS), Amazon Simple Storage Service (S3), and Kafka. You can specify the task name, log fields to deliver, data center, discard rate, delivery type, and delivery details.
        **Field filtering**: Use the `FieldName` parameter to specify log fields to deliver.
        **Filtering rules**: Use the `FilterRules` parameter to pre-process and filter log data.
        **Diverse delivery destinations**: Logs can be delivered to different destinations. Configuration parameters vary with delivery destinations.
        ## [](#)Precautions
        Make sure that you have sufficient permissions to perform delivery tasks.
        If you enable encryption or authentication, properly configure corresponding parameters.
        Verify the syntax of `FilterRules` to make sure that filtering logic works as expected.
        Specify advanced settings such as the number of retries and timeout period based on your needs to have optimal delivery efficiency and stability.
        
        @param request: CreateUserDeliveryTaskRequest
        @return: CreateUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_user_delivery_task_with_options(request, runtime)

    async def create_user_delivery_task_async(
        self,
        request: esa20240910_models.CreateUserDeliveryTaskRequest,
    ) -> esa20240910_models.CreateUserDeliveryTaskResponse:
        """
        @summary Creates a log delivery task to ship logs to the specified destination.
        
        @description This API operation allows you to deliver logs to destinations such as Simple Log Service (SLS), HTTP servers, Object Storage Service (OSS), Amazon Simple Storage Service (S3), and Kafka. You can specify the task name, log fields to deliver, data center, discard rate, delivery type, and delivery details.
        **Field filtering**: Use the `FieldName` parameter to specify log fields to deliver.
        **Filtering rules**: Use the `FilterRules` parameter to pre-process and filter log data.
        **Diverse delivery destinations**: Logs can be delivered to different destinations. Configuration parameters vary with delivery destinations.
        ## [](#)Precautions
        Make sure that you have sufficient permissions to perform delivery tasks.
        If you enable encryption or authentication, properly configure corresponding parameters.
        Verify the syntax of `FilterRules` to make sure that filtering logic works as expected.
        Specify advanced settings such as the number of retries and timeout period based on your needs to have optimal delivery efficiency and stability.
        
        @param request: CreateUserDeliveryTaskRequest
        @return: CreateUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_user_delivery_task_with_options_async(request, runtime)

    def create_waf_rule_with_options(
        self,
        tmp_req: esa20240910_models.CreateWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWafRuleResponse:
        """
        @summary Creates a Web Application Firewall (WAF) rule. This allows you to configure fine-grained WAF settings to improve the security of your website or application.
        
        @param tmp_req: CreateWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWafRuleResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateWafRuleShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.config):
            request.config_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.config, 'Config', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.config_shrink):
            body['Config'] = request.config_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWafRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_waf_rule_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWafRuleResponse:
        """
        @summary Creates a Web Application Firewall (WAF) rule. This allows you to configure fine-grained WAF settings to improve the security of your website or application.
        
        @param tmp_req: CreateWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWafRuleResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateWafRuleShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.config):
            request.config_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.config, 'Config', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.config_shrink):
            body['Config'] = request.config_shrink
        if not UtilClient.is_unset(request.phase):
            body['Phase'] = request.phase
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWafRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_waf_rule(
        self,
        request: esa20240910_models.CreateWafRuleRequest,
    ) -> esa20240910_models.CreateWafRuleResponse:
        """
        @summary Creates a Web Application Firewall (WAF) rule. This allows you to configure fine-grained WAF settings to improve the security of your website or application.
        
        @param request: CreateWafRuleRequest
        @return: CreateWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_waf_rule_with_options(request, runtime)

    async def create_waf_rule_async(
        self,
        request: esa20240910_models.CreateWafRuleRequest,
    ) -> esa20240910_models.CreateWafRuleResponse:
        """
        @summary Creates a Web Application Firewall (WAF) rule. This allows you to configure fine-grained WAF settings to improve the security of your website or application.
        
        @param request: CreateWafRuleRequest
        @return: CreateWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_waf_rule_with_options_async(request, runtime)

    def create_waiting_room_with_options(
        self,
        tmp_req: esa20240910_models.CreateWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomResponse:
        """
        @summary Creates a waiting room for a website.
        
        @param tmp_req: CreateWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateWaitingRoomShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.host_name_and_path):
            request.host_name_and_path_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.host_name_and_path, 'HostNameAndPath', 'json')
        query = {}
        if not UtilClient.is_unset(request.cookie_name):
            query['CookieName'] = request.cookie_name
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.host_name_and_path_shrink):
            query['HostNameAndPath'] = request.host_name_and_path_shrink
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.queue_all_enable):
            query['QueueAllEnable'] = request.queue_all_enable
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_waiting_room_with_options_async(
        self,
        tmp_req: esa20240910_models.CreateWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomResponse:
        """
        @summary Creates a waiting room for a website.
        
        @param tmp_req: CreateWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.CreateWaitingRoomShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.host_name_and_path):
            request.host_name_and_path_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.host_name_and_path, 'HostNameAndPath', 'json')
        query = {}
        if not UtilClient.is_unset(request.cookie_name):
            query['CookieName'] = request.cookie_name
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.host_name_and_path_shrink):
            query['HostNameAndPath'] = request.host_name_and_path_shrink
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.queue_all_enable):
            query['QueueAllEnable'] = request.queue_all_enable
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_waiting_room(
        self,
        request: esa20240910_models.CreateWaitingRoomRequest,
    ) -> esa20240910_models.CreateWaitingRoomResponse:
        """
        @summary Creates a waiting room for a website.
        
        @param request: CreateWaitingRoomRequest
        @return: CreateWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_waiting_room_with_options(request, runtime)

    async def create_waiting_room_async(
        self,
        request: esa20240910_models.CreateWaitingRoomRequest,
    ) -> esa20240910_models.CreateWaitingRoomResponse:
        """
        @summary Creates a waiting room for a website.
        
        @param request: CreateWaitingRoomRequest
        @return: CreateWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_waiting_room_with_options_async(request, runtime)

    def create_waiting_room_event_with_options(
        self,
        request: esa20240910_models.CreateWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomEventResponse:
        """
        @summary Creates a waiting room event.
        
        @param request: CreateWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.pre_queue_enable):
            query['PreQueueEnable'] = request.pre_queue_enable
        if not UtilClient.is_unset(request.pre_queue_start_time):
            query['PreQueueStartTime'] = request.pre_queue_start_time
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.random_pre_queue_enable):
            query['RandomPreQueueEnable'] = request.random_pre_queue_enable
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomEventResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_waiting_room_event_with_options_async(
        self,
        request: esa20240910_models.CreateWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomEventResponse:
        """
        @summary Creates a waiting room event.
        
        @param request: CreateWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.pre_queue_enable):
            query['PreQueueEnable'] = request.pre_queue_enable
        if not UtilClient.is_unset(request.pre_queue_start_time):
            query['PreQueueStartTime'] = request.pre_queue_start_time
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.random_pre_queue_enable):
            query['RandomPreQueueEnable'] = request.random_pre_queue_enable
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomEventResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_waiting_room_event(
        self,
        request: esa20240910_models.CreateWaitingRoomEventRequest,
    ) -> esa20240910_models.CreateWaitingRoomEventResponse:
        """
        @summary Creates a waiting room event.
        
        @param request: CreateWaitingRoomEventRequest
        @return: CreateWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_waiting_room_event_with_options(request, runtime)

    async def create_waiting_room_event_async(
        self,
        request: esa20240910_models.CreateWaitingRoomEventRequest,
    ) -> esa20240910_models.CreateWaitingRoomEventResponse:
        """
        @summary Creates a waiting room event.
        
        @param request: CreateWaitingRoomEventRequest
        @return: CreateWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_waiting_room_event_with_options_async(request, runtime)

    def create_waiting_room_rule_with_options(
        self,
        request: esa20240910_models.CreateWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomRuleResponse:
        """
        @summary Creates a waiting room bypass rule.
        
        @param request: CreateWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.rule):
            query['Rule'] = request.rule
        if not UtilClient.is_unset(request.rule_enable):
            query['RuleEnable'] = request.rule_enable
        if not UtilClient.is_unset(request.rule_name):
            query['RuleName'] = request.rule_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_waiting_room_rule_with_options_async(
        self,
        request: esa20240910_models.CreateWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.CreateWaitingRoomRuleResponse:
        """
        @summary Creates a waiting room bypass rule.
        
        @param request: CreateWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.rule):
            query['Rule'] = request.rule
        if not UtilClient.is_unset(request.rule_enable):
            query['RuleEnable'] = request.rule_enable
        if not UtilClient.is_unset(request.rule_name):
            query['RuleName'] = request.rule_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.CreateWaitingRoomRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_waiting_room_rule(
        self,
        request: esa20240910_models.CreateWaitingRoomRuleRequest,
    ) -> esa20240910_models.CreateWaitingRoomRuleResponse:
        """
        @summary Creates a waiting room bypass rule.
        
        @param request: CreateWaitingRoomRuleRequest
        @return: CreateWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_waiting_room_rule_with_options(request, runtime)

    async def create_waiting_room_rule_async(
        self,
        request: esa20240910_models.CreateWaitingRoomRuleRequest,
    ) -> esa20240910_models.CreateWaitingRoomRuleResponse:
        """
        @summary Creates a waiting room bypass rule.
        
        @param request: CreateWaitingRoomRuleRequest
        @return: CreateWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_waiting_room_rule_with_options_async(request, runtime)

    def delete_certificate_with_options(
        self,
        request: esa20240910_models.DeleteCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteCertificateResponse:
        """
        @summary Deletes a certificate for a website.
        
        @param request: DeleteCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_certificate_with_options_async(
        self,
        request: esa20240910_models.DeleteCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteCertificateResponse:
        """
        @summary Deletes a certificate for a website.
        
        @param request: DeleteCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_certificate(
        self,
        request: esa20240910_models.DeleteCertificateRequest,
    ) -> esa20240910_models.DeleteCertificateResponse:
        """
        @summary Deletes a certificate for a website.
        
        @param request: DeleteCertificateRequest
        @return: DeleteCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_certificate_with_options(request, runtime)

    async def delete_certificate_async(
        self,
        request: esa20240910_models.DeleteCertificateRequest,
    ) -> esa20240910_models.DeleteCertificateResponse:
        """
        @summary Deletes a certificate for a website.
        
        @param request: DeleteCertificateRequest
        @return: DeleteCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_certificate_with_options_async(request, runtime)

    def delete_client_ca_certificate_with_options(
        self,
        request: esa20240910_models.DeleteClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteClientCaCertificateResponse:
        """
        @summary Deletes a client CA certificate.
        
        @param request: DeleteClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteClientCaCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_client_ca_certificate_with_options_async(
        self,
        request: esa20240910_models.DeleteClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteClientCaCertificateResponse:
        """
        @summary Deletes a client CA certificate.
        
        @param request: DeleteClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteClientCaCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_client_ca_certificate(
        self,
        request: esa20240910_models.DeleteClientCaCertificateRequest,
    ) -> esa20240910_models.DeleteClientCaCertificateResponse:
        """
        @summary Deletes a client CA certificate.
        
        @param request: DeleteClientCaCertificateRequest
        @return: DeleteClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_client_ca_certificate_with_options(request, runtime)

    async def delete_client_ca_certificate_async(
        self,
        request: esa20240910_models.DeleteClientCaCertificateRequest,
    ) -> esa20240910_models.DeleteClientCaCertificateResponse:
        """
        @summary Deletes a client CA certificate.
        
        @param request: DeleteClientCaCertificateRequest
        @return: DeleteClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_client_ca_certificate_with_options_async(request, runtime)

    def delete_client_certificate_with_options(
        self,
        request: esa20240910_models.DeleteClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteClientCertificateResponse:
        """
        @summary 删除客户端证书
        
        @param request: DeleteClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteClientCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_client_certificate_with_options_async(
        self,
        request: esa20240910_models.DeleteClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteClientCertificateResponse:
        """
        @summary 删除客户端证书
        
        @param request: DeleteClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteClientCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_client_certificate(
        self,
        request: esa20240910_models.DeleteClientCertificateRequest,
    ) -> esa20240910_models.DeleteClientCertificateResponse:
        """
        @summary 删除客户端证书
        
        @param request: DeleteClientCertificateRequest
        @return: DeleteClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_client_certificate_with_options(request, runtime)

    async def delete_client_certificate_async(
        self,
        request: esa20240910_models.DeleteClientCertificateRequest,
    ) -> esa20240910_models.DeleteClientCertificateResponse:
        """
        @summary 删除客户端证书
        
        @param request: DeleteClientCertificateRequest
        @return: DeleteClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_client_certificate_with_options_async(request, runtime)

    def delete_custom_scene_policy_with_options(
        self,
        request: esa20240910_models.DeleteCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteCustomScenePolicyResponse:
        """
        @summary Deletes a scenario-specific custom policy.
        
        @param request: DeleteCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteCustomScenePolicyResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_custom_scene_policy_with_options_async(
        self,
        request: esa20240910_models.DeleteCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteCustomScenePolicyResponse:
        """
        @summary Deletes a scenario-specific custom policy.
        
        @param request: DeleteCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteCustomScenePolicyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_custom_scene_policy(
        self,
        request: esa20240910_models.DeleteCustomScenePolicyRequest,
    ) -> esa20240910_models.DeleteCustomScenePolicyResponse:
        """
        @summary Deletes a scenario-specific custom policy.
        
        @param request: DeleteCustomScenePolicyRequest
        @return: DeleteCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_custom_scene_policy_with_options(request, runtime)

    async def delete_custom_scene_policy_async(
        self,
        request: esa20240910_models.DeleteCustomScenePolicyRequest,
    ) -> esa20240910_models.DeleteCustomScenePolicyResponse:
        """
        @summary Deletes a scenario-specific custom policy.
        
        @param request: DeleteCustomScenePolicyRequest
        @return: DeleteCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_custom_scene_policy_with_options_async(request, runtime)

    def delete_edge_container_app_with_options(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppResponse:
        """
        @summary Deletes a containerized application.
        
        @param request: DeleteEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_edge_container_app_with_options_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppResponse:
        """
        @summary Deletes a containerized application.
        
        @param request: DeleteEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_edge_container_app(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppResponse:
        """
        @summary Deletes a containerized application.
        
        @param request: DeleteEdgeContainerAppRequest
        @return: DeleteEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_edge_container_app_with_options(request, runtime)

    async def delete_edge_container_app_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppResponse:
        """
        @summary Deletes a containerized application.
        
        @param request: DeleteEdgeContainerAppRequest
        @return: DeleteEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_edge_container_app_with_options_async(request, runtime)

    def delete_edge_container_app_record_with_options(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppRecordResponse:
        """
        @summary Disassociates a domain name from a containerized application. After the dissociation, you can no longer use the domain name to access the containerized application.
        
        @param request: DeleteEdgeContainerAppRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerAppRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_edge_container_app_record_with_options_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppRecordResponse:
        """
        @summary Disassociates a domain name from a containerized application. After the dissociation, you can no longer use the domain name to access the containerized application.
        
        @param request: DeleteEdgeContainerAppRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppRecordResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerAppRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_edge_container_app_record(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRecordRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppRecordResponse:
        """
        @summary Disassociates a domain name from a containerized application. After the dissociation, you can no longer use the domain name to access the containerized application.
        
        @param request: DeleteEdgeContainerAppRecordRequest
        @return: DeleteEdgeContainerAppRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_edge_container_app_record_with_options(request, runtime)

    async def delete_edge_container_app_record_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppRecordRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppRecordResponse:
        """
        @summary Disassociates a domain name from a containerized application. After the dissociation, you can no longer use the domain name to access the containerized application.
        
        @param request: DeleteEdgeContainerAppRecordRequest
        @return: DeleteEdgeContainerAppRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_edge_container_app_record_with_options_async(request, runtime)

    def delete_edge_container_app_version_with_options(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppVersionResponse:
        """
        @summary Deletes a version of a containerized application.
        
        @param request: DeleteEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_edge_container_app_version_with_options_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteEdgeContainerAppVersionResponse:
        """
        @summary Deletes a version of a containerized application.
        
        @param request: DeleteEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteEdgeContainerAppVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_edge_container_app_version(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppVersionResponse:
        """
        @summary Deletes a version of a containerized application.
        
        @param request: DeleteEdgeContainerAppVersionRequest
        @return: DeleteEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_edge_container_app_version_with_options(request, runtime)

    async def delete_edge_container_app_version_async(
        self,
        request: esa20240910_models.DeleteEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.DeleteEdgeContainerAppVersionResponse:
        """
        @summary Deletes a version of a containerized application.
        
        @param request: DeleteEdgeContainerAppVersionRequest
        @return: DeleteEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_edge_container_app_version_with_options_async(request, runtime)

    def delete_kv_with_options(
        self,
        request: esa20240910_models.DeleteKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteKvResponse:
        """
        @summary Deletes a key-value pair from a namespace.
        
        @param request: DeleteKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteKvResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteKvResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_kv_with_options_async(
        self,
        request: esa20240910_models.DeleteKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteKvResponse:
        """
        @summary Deletes a key-value pair from a namespace.
        
        @param request: DeleteKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteKvResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteKvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_kv(
        self,
        request: esa20240910_models.DeleteKvRequest,
    ) -> esa20240910_models.DeleteKvResponse:
        """
        @summary Deletes a key-value pair from a namespace.
        
        @param request: DeleteKvRequest
        @return: DeleteKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_kv_with_options(request, runtime)

    async def delete_kv_async(
        self,
        request: esa20240910_models.DeleteKvRequest,
    ) -> esa20240910_models.DeleteKvResponse:
        """
        @summary Deletes a key-value pair from a namespace.
        
        @param request: DeleteKvRequest
        @return: DeleteKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_kv_with_options_async(request, runtime)

    def delete_kv_namespace_with_options(
        self,
        request: esa20240910_models.DeleteKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteKvNamespaceResponse:
        """
        @summary Deletes a namespace from an Alibaba Cloud account.
        
        @param request: DeleteKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteKvNamespaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_kv_namespace_with_options_async(
        self,
        request: esa20240910_models.DeleteKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteKvNamespaceResponse:
        """
        @summary Deletes a namespace from an Alibaba Cloud account.
        
        @param request: DeleteKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteKvNamespaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_kv_namespace(
        self,
        request: esa20240910_models.DeleteKvNamespaceRequest,
    ) -> esa20240910_models.DeleteKvNamespaceResponse:
        """
        @summary Deletes a namespace from an Alibaba Cloud account.
        
        @param request: DeleteKvNamespaceRequest
        @return: DeleteKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_kv_namespace_with_options(request, runtime)

    async def delete_kv_namespace_async(
        self,
        request: esa20240910_models.DeleteKvNamespaceRequest,
    ) -> esa20240910_models.DeleteKvNamespaceResponse:
        """
        @summary Deletes a namespace from an Alibaba Cloud account.
        
        @param request: DeleteKvNamespaceRequest
        @return: DeleteKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_kv_namespace_with_options_async(request, runtime)

    def delete_list_with_options(
        self,
        request: esa20240910_models.DeleteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteListResponse:
        """
        @summary Deletes a custom list that is no longer needed.
        
        @param request: DeleteListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteListResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteListResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_list_with_options_async(
        self,
        request: esa20240910_models.DeleteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteListResponse:
        """
        @summary Deletes a custom list that is no longer needed.
        
        @param request: DeleteListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteListResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_list(
        self,
        request: esa20240910_models.DeleteListRequest,
    ) -> esa20240910_models.DeleteListResponse:
        """
        @summary Deletes a custom list that is no longer needed.
        
        @param request: DeleteListRequest
        @return: DeleteListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_list_with_options(request, runtime)

    async def delete_list_async(
        self,
        request: esa20240910_models.DeleteListRequest,
    ) -> esa20240910_models.DeleteListResponse:
        """
        @summary Deletes a custom list that is no longer needed.
        
        @param request: DeleteListRequest
        @return: DeleteListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_list_with_options_async(request, runtime)

    def delete_origin_protection_with_options(
        self,
        request: esa20240910_models.DeleteOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteOriginProtectionResponse:
        """
        @summary Disables origin protection.
        
        @param request: DeleteOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteOriginProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_origin_protection_with_options_async(
        self,
        request: esa20240910_models.DeleteOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteOriginProtectionResponse:
        """
        @summary Disables origin protection.
        
        @param request: DeleteOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteOriginProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_origin_protection(
        self,
        request: esa20240910_models.DeleteOriginProtectionRequest,
    ) -> esa20240910_models.DeleteOriginProtectionResponse:
        """
        @summary Disables origin protection.
        
        @param request: DeleteOriginProtectionRequest
        @return: DeleteOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_origin_protection_with_options(request, runtime)

    async def delete_origin_protection_async(
        self,
        request: esa20240910_models.DeleteOriginProtectionRequest,
    ) -> esa20240910_models.DeleteOriginProtectionResponse:
        """
        @summary Disables origin protection.
        
        @param request: DeleteOriginProtectionRequest
        @return: DeleteOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_origin_protection_with_options_async(request, runtime)

    def delete_page_with_options(
        self,
        request: esa20240910_models.DeletePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeletePageResponse:
        """
        @summary Deletes a custom error page that is no longer needed.
        
        @param request: DeletePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeletePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeletePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeletePageResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_page_with_options_async(
        self,
        request: esa20240910_models.DeletePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeletePageResponse:
        """
        @summary Deletes a custom error page that is no longer needed.
        
        @param request: DeletePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeletePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeletePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeletePageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_page(
        self,
        request: esa20240910_models.DeletePageRequest,
    ) -> esa20240910_models.DeletePageResponse:
        """
        @summary Deletes a custom error page that is no longer needed.
        
        @param request: DeletePageRequest
        @return: DeletePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_page_with_options(request, runtime)

    async def delete_page_async(
        self,
        request: esa20240910_models.DeletePageRequest,
    ) -> esa20240910_models.DeletePageResponse:
        """
        @summary Deletes a custom error page that is no longer needed.
        
        @param request: DeletePageRequest
        @return: DeletePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_page_with_options_async(request, runtime)

    def delete_record_with_options(
        self,
        request: esa20240910_models.DeleteRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRecordResponse:
        """
        @summary Deletes a DNS record of a website based on the specified RecordId.
        
        @param request: DeleteRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRecordResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.record_id):
            query['RecordId'] = request.record_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_record_with_options_async(
        self,
        request: esa20240910_models.DeleteRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRecordResponse:
        """
        @summary Deletes a DNS record of a website based on the specified RecordId.
        
        @param request: DeleteRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRecordResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.record_id):
            query['RecordId'] = request.record_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_record(
        self,
        request: esa20240910_models.DeleteRecordRequest,
    ) -> esa20240910_models.DeleteRecordResponse:
        """
        @summary Deletes a DNS record of a website based on the specified RecordId.
        
        @param request: DeleteRecordRequest
        @return: DeleteRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_record_with_options(request, runtime)

    async def delete_record_async(
        self,
        request: esa20240910_models.DeleteRecordRequest,
    ) -> esa20240910_models.DeleteRecordResponse:
        """
        @summary Deletes a DNS record of a website based on the specified RecordId.
        
        @param request: DeleteRecordRequest
        @return: DeleteRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_record_with_options_async(request, runtime)

    def delete_routine_with_options(
        self,
        request: esa20240910_models.DeleteRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineResponse:
        """
        @summary Deletes a routine in Edge Routine.
        
        @param request: DeleteRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_routine_with_options_async(
        self,
        request: esa20240910_models.DeleteRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineResponse:
        """
        @summary Deletes a routine in Edge Routine.
        
        @param request: DeleteRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_routine(
        self,
        request: esa20240910_models.DeleteRoutineRequest,
    ) -> esa20240910_models.DeleteRoutineResponse:
        """
        @summary Deletes a routine in Edge Routine.
        
        @param request: DeleteRoutineRequest
        @return: DeleteRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_routine_with_options(request, runtime)

    async def delete_routine_async(
        self,
        request: esa20240910_models.DeleteRoutineRequest,
    ) -> esa20240910_models.DeleteRoutineResponse:
        """
        @summary Deletes a routine in Edge Routine.
        
        @param request: DeleteRoutineRequest
        @return: DeleteRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_routine_with_options_async(request, runtime)

    def delete_routine_code_version_with_options(
        self,
        request: esa20240910_models.DeleteRoutineCodeVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineCodeVersionResponse:
        """
        @summary Deletes a code version of a routine.
        
        @param request: DeleteRoutineCodeVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineCodeVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_version):
            body['CodeVersion'] = request.code_version
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineCodeVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineCodeVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_routine_code_version_with_options_async(
        self,
        request: esa20240910_models.DeleteRoutineCodeVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineCodeVersionResponse:
        """
        @summary Deletes a code version of a routine.
        
        @param request: DeleteRoutineCodeVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineCodeVersionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_version):
            body['CodeVersion'] = request.code_version
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineCodeVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineCodeVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_routine_code_version(
        self,
        request: esa20240910_models.DeleteRoutineCodeVersionRequest,
    ) -> esa20240910_models.DeleteRoutineCodeVersionResponse:
        """
        @summary Deletes a code version of a routine.
        
        @param request: DeleteRoutineCodeVersionRequest
        @return: DeleteRoutineCodeVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_routine_code_version_with_options(request, runtime)

    async def delete_routine_code_version_async(
        self,
        request: esa20240910_models.DeleteRoutineCodeVersionRequest,
    ) -> esa20240910_models.DeleteRoutineCodeVersionResponse:
        """
        @summary Deletes a code version of a routine.
        
        @param request: DeleteRoutineCodeVersionRequest
        @return: DeleteRoutineCodeVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_routine_code_version_with_options_async(request, runtime)

    def delete_routine_related_record_with_options(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineRelatedRecordResponse:
        """
        @summary Deletes a record that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineRelatedRecordResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.record_id):
            body['RecordId'] = request.record_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineRelatedRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineRelatedRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_routine_related_record_with_options_async(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineRelatedRecordResponse:
        """
        @summary Deletes a record that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineRelatedRecordResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.record_id):
            body['RecordId'] = request.record_id
        if not UtilClient.is_unset(request.record_name):
            body['RecordName'] = request.record_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineRelatedRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineRelatedRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_routine_related_record(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRecordRequest,
    ) -> esa20240910_models.DeleteRoutineRelatedRecordResponse:
        """
        @summary Deletes a record that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRecordRequest
        @return: DeleteRoutineRelatedRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_routine_related_record_with_options(request, runtime)

    async def delete_routine_related_record_async(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRecordRequest,
    ) -> esa20240910_models.DeleteRoutineRelatedRecordResponse:
        """
        @summary Deletes a record that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRecordRequest
        @return: DeleteRoutineRelatedRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_routine_related_record_with_options_async(request, runtime)

    def delete_routine_related_route_with_options(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRouteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineRelatedRouteResponse:
        """
        @summary Deletes a route that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRouteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineRelatedRouteResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.route):
            body['Route'] = request.route
        if not UtilClient.is_unset(request.route_id):
            body['RouteId'] = request.route_id
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineRelatedRoute',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineRelatedRouteResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_routine_related_route_with_options_async(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRouteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteRoutineRelatedRouteResponse:
        """
        @summary Deletes a route that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRouteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteRoutineRelatedRouteResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.route):
            body['Route'] = request.route
        if not UtilClient.is_unset(request.route_id):
            body['RouteId'] = request.route_id
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteRoutineRelatedRoute',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteRoutineRelatedRouteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_routine_related_route(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRouteRequest,
    ) -> esa20240910_models.DeleteRoutineRelatedRouteResponse:
        """
        @summary Deletes a route that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRouteRequest
        @return: DeleteRoutineRelatedRouteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_routine_related_route_with_options(request, runtime)

    async def delete_routine_related_route_async(
        self,
        request: esa20240910_models.DeleteRoutineRelatedRouteRequest,
    ) -> esa20240910_models.DeleteRoutineRelatedRouteResponse:
        """
        @summary Deletes a route that is associated with a routine.
        
        @param request: DeleteRoutineRelatedRouteRequest
        @return: DeleteRoutineRelatedRouteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_routine_related_route_with_options_async(request, runtime)

    def delete_scheduled_preload_execution_with_options(
        self,
        request: esa20240910_models.DeleteScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteScheduledPreloadExecutionResponse:
        """
        @summary Deletes a scheduled prefetch plan based on the plan ID.
        
        @param request: DeleteScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteScheduledPreloadExecutionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_scheduled_preload_execution_with_options_async(
        self,
        request: esa20240910_models.DeleteScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteScheduledPreloadExecutionResponse:
        """
        @summary Deletes a scheduled prefetch plan based on the plan ID.
        
        @param request: DeleteScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteScheduledPreloadExecutionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_scheduled_preload_execution(
        self,
        request: esa20240910_models.DeleteScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.DeleteScheduledPreloadExecutionResponse:
        """
        @summary Deletes a scheduled prefetch plan based on the plan ID.
        
        @param request: DeleteScheduledPreloadExecutionRequest
        @return: DeleteScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_scheduled_preload_execution_with_options(request, runtime)

    async def delete_scheduled_preload_execution_async(
        self,
        request: esa20240910_models.DeleteScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.DeleteScheduledPreloadExecutionResponse:
        """
        @summary Deletes a scheduled prefetch plan based on the plan ID.
        
        @param request: DeleteScheduledPreloadExecutionRequest
        @return: DeleteScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_scheduled_preload_execution_with_options_async(request, runtime)

    def delete_scheduled_preload_job_with_options(
        self,
        request: esa20240910_models.DeleteScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteScheduledPreloadJobResponse:
        """
        @summary Deletes a specified scheduled prefetch task based on the task ID.
        
        @param request: DeleteScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteScheduledPreloadJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_scheduled_preload_job_with_options_async(
        self,
        request: esa20240910_models.DeleteScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteScheduledPreloadJobResponse:
        """
        @summary Deletes a specified scheduled prefetch task based on the task ID.
        
        @param request: DeleteScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteScheduledPreloadJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_scheduled_preload_job(
        self,
        request: esa20240910_models.DeleteScheduledPreloadJobRequest,
    ) -> esa20240910_models.DeleteScheduledPreloadJobResponse:
        """
        @summary Deletes a specified scheduled prefetch task based on the task ID.
        
        @param request: DeleteScheduledPreloadJobRequest
        @return: DeleteScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_scheduled_preload_job_with_options(request, runtime)

    async def delete_scheduled_preload_job_async(
        self,
        request: esa20240910_models.DeleteScheduledPreloadJobRequest,
    ) -> esa20240910_models.DeleteScheduledPreloadJobResponse:
        """
        @summary Deletes a specified scheduled prefetch task based on the task ID.
        
        @param request: DeleteScheduledPreloadJobRequest
        @return: DeleteScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_scheduled_preload_job_with_options_async(request, runtime)

    def delete_site_with_options(
        self,
        request: esa20240910_models.DeleteSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteSiteResponse:
        """
        @summary Deletes a website based on the specified website ID.
        
        @param request: DeleteSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteSiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteSiteResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_site_with_options_async(
        self,
        request: esa20240910_models.DeleteSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteSiteResponse:
        """
        @summary Deletes a website based on the specified website ID.
        
        @param request: DeleteSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteSiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteSiteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_site(
        self,
        request: esa20240910_models.DeleteSiteRequest,
    ) -> esa20240910_models.DeleteSiteResponse:
        """
        @summary Deletes a website based on the specified website ID.
        
        @param request: DeleteSiteRequest
        @return: DeleteSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_site_with_options(request, runtime)

    async def delete_site_async(
        self,
        request: esa20240910_models.DeleteSiteRequest,
    ) -> esa20240910_models.DeleteSiteResponse:
        """
        @summary Deletes a website based on the specified website ID.
        
        @param request: DeleteSiteRequest
        @return: DeleteSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_site_with_options_async(request, runtime)

    def delete_site_delivery_task_with_options(
        self,
        request: esa20240910_models.DeleteSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteSiteDeliveryTaskResponse:
        """
        @summary Deletes a real-time log delivery task.
        
        @param request: DeleteSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteSiteDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_site_delivery_task_with_options_async(
        self,
        request: esa20240910_models.DeleteSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteSiteDeliveryTaskResponse:
        """
        @summary Deletes a real-time log delivery task.
        
        @param request: DeleteSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteSiteDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_site_delivery_task(
        self,
        request: esa20240910_models.DeleteSiteDeliveryTaskRequest,
    ) -> esa20240910_models.DeleteSiteDeliveryTaskResponse:
        """
        @summary Deletes a real-time log delivery task.
        
        @param request: DeleteSiteDeliveryTaskRequest
        @return: DeleteSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_site_delivery_task_with_options(request, runtime)

    async def delete_site_delivery_task_async(
        self,
        request: esa20240910_models.DeleteSiteDeliveryTaskRequest,
    ) -> esa20240910_models.DeleteSiteDeliveryTaskResponse:
        """
        @summary Deletes a real-time log delivery task.
        
        @param request: DeleteSiteDeliveryTaskRequest
        @return: DeleteSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_site_delivery_task_with_options_async(request, runtime)

    def delete_user_delivery_task_with_options(
        self,
        request: esa20240910_models.DeleteUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteUserDeliveryTaskResponse:
        """
        @summary Deletes a log delivery task from your Alibaba Cloud account.
        
        @description *****>
        Deleted tasks cannot be restored. Proceed with caution.
        To call this operation, you must have an account that has the required permissions.
        The returned `RequestId` value can be used to track the request processing progress and troubleshoot issues.
        
        @param request: DeleteUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteUserDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_user_delivery_task_with_options_async(
        self,
        request: esa20240910_models.DeleteUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteUserDeliveryTaskResponse:
        """
        @summary Deletes a log delivery task from your Alibaba Cloud account.
        
        @description *****>
        Deleted tasks cannot be restored. Proceed with caution.
        To call this operation, you must have an account that has the required permissions.
        The returned `RequestId` value can be used to track the request processing progress and troubleshoot issues.
        
        @param request: DeleteUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteUserDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_user_delivery_task(
        self,
        request: esa20240910_models.DeleteUserDeliveryTaskRequest,
    ) -> esa20240910_models.DeleteUserDeliveryTaskResponse:
        """
        @summary Deletes a log delivery task from your Alibaba Cloud account.
        
        @description *****>
        Deleted tasks cannot be restored. Proceed with caution.
        To call this operation, you must have an account that has the required permissions.
        The returned `RequestId` value can be used to track the request processing progress and troubleshoot issues.
        
        @param request: DeleteUserDeliveryTaskRequest
        @return: DeleteUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_user_delivery_task_with_options(request, runtime)

    async def delete_user_delivery_task_async(
        self,
        request: esa20240910_models.DeleteUserDeliveryTaskRequest,
    ) -> esa20240910_models.DeleteUserDeliveryTaskResponse:
        """
        @summary Deletes a log delivery task from your Alibaba Cloud account.
        
        @description *****>
        Deleted tasks cannot be restored. Proceed with caution.
        To call this operation, you must have an account that has the required permissions.
        The returned `RequestId` value can be used to track the request processing progress and troubleshoot issues.
        
        @param request: DeleteUserDeliveryTaskRequest
        @return: DeleteUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_user_delivery_task_with_options_async(request, runtime)

    def delete_waf_rule_with_options(
        self,
        request: esa20240910_models.DeleteWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWafRuleResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) rule, including its configurations and match conditions.
        
        @param request: DeleteWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWafRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWafRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_waf_rule_with_options_async(
        self,
        request: esa20240910_models.DeleteWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWafRuleResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) rule, including its configurations and match conditions.
        
        @param request: DeleteWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWafRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWafRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_waf_rule(
        self,
        request: esa20240910_models.DeleteWafRuleRequest,
    ) -> esa20240910_models.DeleteWafRuleResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) rule, including its configurations and match conditions.
        
        @param request: DeleteWafRuleRequest
        @return: DeleteWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_waf_rule_with_options(request, runtime)

    async def delete_waf_rule_async(
        self,
        request: esa20240910_models.DeleteWafRuleRequest,
    ) -> esa20240910_models.DeleteWafRuleResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) rule, including its configurations and match conditions.
        
        @param request: DeleteWafRuleRequest
        @return: DeleteWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_waf_rule_with_options_async(request, runtime)

    def delete_waf_ruleset_with_options(
        self,
        request: esa20240910_models.DeleteWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWafRulesetResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) ruleset that is no longer needed.
        
        @param request: DeleteWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWafRulesetResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_waf_ruleset_with_options_async(
        self,
        request: esa20240910_models.DeleteWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWafRulesetResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) ruleset that is no longer needed.
        
        @param request: DeleteWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWafRulesetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_waf_ruleset(
        self,
        request: esa20240910_models.DeleteWafRulesetRequest,
    ) -> esa20240910_models.DeleteWafRulesetResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) ruleset that is no longer needed.
        
        @param request: DeleteWafRulesetRequest
        @return: DeleteWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_waf_ruleset_with_options(request, runtime)

    async def delete_waf_ruleset_async(
        self,
        request: esa20240910_models.DeleteWafRulesetRequest,
    ) -> esa20240910_models.DeleteWafRulesetResponse:
        """
        @summary Deletes a Web Application Firewall (WAF) ruleset that is no longer needed.
        
        @param request: DeleteWafRulesetRequest
        @return: DeleteWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_waf_ruleset_with_options_async(request, runtime)

    def delete_waiting_room_with_options(
        self,
        request: esa20240910_models.DeleteWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomResponse:
        """
        @summary Deletes a waiting room.
        
        @param request: DeleteWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_waiting_room_with_options_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomResponse:
        """
        @summary Deletes a waiting room.
        
        @param request: DeleteWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_waiting_room(
        self,
        request: esa20240910_models.DeleteWaitingRoomRequest,
    ) -> esa20240910_models.DeleteWaitingRoomResponse:
        """
        @summary Deletes a waiting room.
        
        @param request: DeleteWaitingRoomRequest
        @return: DeleteWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_waiting_room_with_options(request, runtime)

    async def delete_waiting_room_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomRequest,
    ) -> esa20240910_models.DeleteWaitingRoomResponse:
        """
        @summary Deletes a waiting room.
        
        @param request: DeleteWaitingRoomRequest
        @return: DeleteWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_waiting_room_with_options_async(request, runtime)

    def delete_waiting_room_event_with_options(
        self,
        request: esa20240910_models.DeleteWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomEventResponse:
        """
        @summary Deletes a waiting room event.
        
        @param request: DeleteWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_event_id):
            query['WaitingRoomEventId'] = request.waiting_room_event_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomEventResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_waiting_room_event_with_options_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomEventResponse:
        """
        @summary Deletes a waiting room event.
        
        @param request: DeleteWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_event_id):
            query['WaitingRoomEventId'] = request.waiting_room_event_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomEventResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_waiting_room_event(
        self,
        request: esa20240910_models.DeleteWaitingRoomEventRequest,
    ) -> esa20240910_models.DeleteWaitingRoomEventResponse:
        """
        @summary Deletes a waiting room event.
        
        @param request: DeleteWaitingRoomEventRequest
        @return: DeleteWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_waiting_room_event_with_options(request, runtime)

    async def delete_waiting_room_event_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomEventRequest,
    ) -> esa20240910_models.DeleteWaitingRoomEventResponse:
        """
        @summary Deletes a waiting room event.
        
        @param request: DeleteWaitingRoomEventRequest
        @return: DeleteWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_waiting_room_event_with_options_async(request, runtime)

    def delete_waiting_room_rule_with_options(
        self,
        request: esa20240910_models.DeleteWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomRuleResponse:
        """
        @summary Deletes a waiting room bypass rule.
        
        @param request: DeleteWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_rule_id):
            query['WaitingRoomRuleId'] = request.waiting_room_rule_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_waiting_room_rule_with_options_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DeleteWaitingRoomRuleResponse:
        """
        @summary Deletes a waiting room bypass rule.
        
        @param request: DeleteWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_rule_id):
            query['WaitingRoomRuleId'] = request.waiting_room_rule_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DeleteWaitingRoomRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_waiting_room_rule(
        self,
        request: esa20240910_models.DeleteWaitingRoomRuleRequest,
    ) -> esa20240910_models.DeleteWaitingRoomRuleResponse:
        """
        @summary Deletes a waiting room bypass rule.
        
        @param request: DeleteWaitingRoomRuleRequest
        @return: DeleteWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_waiting_room_rule_with_options(request, runtime)

    async def delete_waiting_room_rule_async(
        self,
        request: esa20240910_models.DeleteWaitingRoomRuleRequest,
    ) -> esa20240910_models.DeleteWaitingRoomRuleResponse:
        """
        @summary Deletes a waiting room bypass rule.
        
        @param request: DeleteWaitingRoomRuleRequest
        @return: DeleteWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_waiting_room_rule_with_options_async(request, runtime)

    def describe_custom_scene_policies_with_options(
        self,
        request: esa20240910_models.DescribeCustomScenePoliciesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeCustomScenePoliciesResponse:
        """
        @summary Queries the configurations of a scenario-specific policy.
        
        @param request: DescribeCustomScenePoliciesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeCustomScenePoliciesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeCustomScenePolicies',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeCustomScenePoliciesResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_custom_scene_policies_with_options_async(
        self,
        request: esa20240910_models.DescribeCustomScenePoliciesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeCustomScenePoliciesResponse:
        """
        @summary Queries the configurations of a scenario-specific policy.
        
        @param request: DescribeCustomScenePoliciesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeCustomScenePoliciesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeCustomScenePolicies',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeCustomScenePoliciesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_custom_scene_policies(
        self,
        request: esa20240910_models.DescribeCustomScenePoliciesRequest,
    ) -> esa20240910_models.DescribeCustomScenePoliciesResponse:
        """
        @summary Queries the configurations of a scenario-specific policy.
        
        @param request: DescribeCustomScenePoliciesRequest
        @return: DescribeCustomScenePoliciesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_custom_scene_policies_with_options(request, runtime)

    async def describe_custom_scene_policies_async(
        self,
        request: esa20240910_models.DescribeCustomScenePoliciesRequest,
    ) -> esa20240910_models.DescribeCustomScenePoliciesResponse:
        """
        @summary Queries the configurations of a scenario-specific policy.
        
        @param request: DescribeCustomScenePoliciesRequest
        @return: DescribeCustomScenePoliciesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_custom_scene_policies_with_options_async(request, runtime)

    def describe_ddo_sall_event_list_with_options(
        self,
        request: esa20240910_models.DescribeDDoSAllEventListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeDDoSAllEventListResponse:
        """
        @summary Queries DDoS attack events.
        
        @param request: DescribeDDoSAllEventListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeDDoSAllEventListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.event_type):
            query['EventType'] = request.event_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeDDoSAllEventList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeDDoSAllEventListResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_ddo_sall_event_list_with_options_async(
        self,
        request: esa20240910_models.DescribeDDoSAllEventListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeDDoSAllEventListResponse:
        """
        @summary Queries DDoS attack events.
        
        @param request: DescribeDDoSAllEventListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeDDoSAllEventListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.event_type):
            query['EventType'] = request.event_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeDDoSAllEventList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeDDoSAllEventListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_ddo_sall_event_list(
        self,
        request: esa20240910_models.DescribeDDoSAllEventListRequest,
    ) -> esa20240910_models.DescribeDDoSAllEventListResponse:
        """
        @summary Queries DDoS attack events.
        
        @param request: DescribeDDoSAllEventListRequest
        @return: DescribeDDoSAllEventListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_ddo_sall_event_list_with_options(request, runtime)

    async def describe_ddo_sall_event_list_async(
        self,
        request: esa20240910_models.DescribeDDoSAllEventListRequest,
    ) -> esa20240910_models.DescribeDDoSAllEventListResponse:
        """
        @summary Queries DDoS attack events.
        
        @param request: DescribeDDoSAllEventListRequest
        @return: DescribeDDoSAllEventListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_ddo_sall_event_list_with_options_async(request, runtime)

    def describe_http_ddo_sattack_intelligent_protection_with_options(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Queries the configuration of smart HTTP DDoS protection for a website.
        
        @param request: DescribeHttpDDoSAttackIntelligentProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeHttpDDoSAttackIntelligentProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHttpDDoSAttackIntelligentProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_http_ddo_sattack_intelligent_protection_with_options_async(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Queries the configuration of smart HTTP DDoS protection for a website.
        
        @param request: DescribeHttpDDoSAttackIntelligentProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeHttpDDoSAttackIntelligentProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHttpDDoSAttackIntelligentProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_http_ddo_sattack_intelligent_protection(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionRequest,
    ) -> esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Queries the configuration of smart HTTP DDoS protection for a website.
        
        @param request: DescribeHttpDDoSAttackIntelligentProtectionRequest
        @return: DescribeHttpDDoSAttackIntelligentProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_http_ddo_sattack_intelligent_protection_with_options(request, runtime)

    async def describe_http_ddo_sattack_intelligent_protection_async(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionRequest,
    ) -> esa20240910_models.DescribeHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Queries the configuration of smart HTTP DDoS protection for a website.
        
        @param request: DescribeHttpDDoSAttackIntelligentProtectionRequest
        @return: DescribeHttpDDoSAttackIntelligentProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_http_ddo_sattack_intelligent_protection_with_options_async(request, runtime)

    def describe_http_ddo_sattack_protection_with_options(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeHttpDDoSAttackProtectionResponse:
        """
        @summary Queries the configurations of HTTP DDoS attack protection.
        
        @param request: DescribeHttpDDoSAttackProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeHttpDDoSAttackProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHttpDDoSAttackProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeHttpDDoSAttackProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_http_ddo_sattack_protection_with_options_async(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeHttpDDoSAttackProtectionResponse:
        """
        @summary Queries the configurations of HTTP DDoS attack protection.
        
        @param request: DescribeHttpDDoSAttackProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeHttpDDoSAttackProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHttpDDoSAttackProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeHttpDDoSAttackProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_http_ddo_sattack_protection(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackProtectionRequest,
    ) -> esa20240910_models.DescribeHttpDDoSAttackProtectionResponse:
        """
        @summary Queries the configurations of HTTP DDoS attack protection.
        
        @param request: DescribeHttpDDoSAttackProtectionRequest
        @return: DescribeHttpDDoSAttackProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_http_ddo_sattack_protection_with_options(request, runtime)

    async def describe_http_ddo_sattack_protection_async(
        self,
        request: esa20240910_models.DescribeHttpDDoSAttackProtectionRequest,
    ) -> esa20240910_models.DescribeHttpDDoSAttackProtectionResponse:
        """
        @summary Queries the configurations of HTTP DDoS attack protection.
        
        @param request: DescribeHttpDDoSAttackProtectionRequest
        @return: DescribeHttpDDoSAttackProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_http_ddo_sattack_protection_with_options_async(request, runtime)

    def describe_kv_account_status_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeKvAccountStatusResponse:
        """
        @summary Queries whether Edge KV is activated in your Alibaba Cloud account.
        
        @param request: DescribeKvAccountStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeKvAccountStatusResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='DescribeKvAccountStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeKvAccountStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_kv_account_status_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribeKvAccountStatusResponse:
        """
        @summary Queries whether Edge KV is activated in your Alibaba Cloud account.
        
        @param request: DescribeKvAccountStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeKvAccountStatusResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='DescribeKvAccountStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribeKvAccountStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_kv_account_status(self) -> esa20240910_models.DescribeKvAccountStatusResponse:
        """
        @summary Queries whether Edge KV is activated in your Alibaba Cloud account.
        
        @return: DescribeKvAccountStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_kv_account_status_with_options(runtime)

    async def describe_kv_account_status_async(self) -> esa20240910_models.DescribeKvAccountStatusResponse:
        """
        @summary Queries whether Edge KV is activated in your Alibaba Cloud account.
        
        @return: DescribeKvAccountStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_kv_account_status_with_options_async(runtime)

    def describe_preload_tasks_with_options(
        self,
        request: esa20240910_models.DescribePreloadTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribePreloadTasksResponse:
        """
        @summary Queries the details of prefetch tasks by time, task status, or prefetch URL.
        
        @param request: DescribePreloadTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePreloadTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePreloadTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribePreloadTasksResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_preload_tasks_with_options_async(
        self,
        request: esa20240910_models.DescribePreloadTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribePreloadTasksResponse:
        """
        @summary Queries the details of prefetch tasks by time, task status, or prefetch URL.
        
        @param request: DescribePreloadTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePreloadTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePreloadTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribePreloadTasksResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_preload_tasks(
        self,
        request: esa20240910_models.DescribePreloadTasksRequest,
    ) -> esa20240910_models.DescribePreloadTasksResponse:
        """
        @summary Queries the details of prefetch tasks by time, task status, or prefetch URL.
        
        @param request: DescribePreloadTasksRequest
        @return: DescribePreloadTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_preload_tasks_with_options(request, runtime)

    async def describe_preload_tasks_async(
        self,
        request: esa20240910_models.DescribePreloadTasksRequest,
    ) -> esa20240910_models.DescribePreloadTasksResponse:
        """
        @summary Queries the details of prefetch tasks by time, task status, or prefetch URL.
        
        @param request: DescribePreloadTasksRequest
        @return: DescribePreloadTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_preload_tasks_with_options_async(request, runtime)

    def describe_purge_tasks_with_options(
        self,
        request: esa20240910_models.DescribePurgeTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribePurgeTasksResponse:
        """
        @summary Queries the details of purge tasks.
        
        @param request: DescribePurgeTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePurgeTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePurgeTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribePurgeTasksResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_purge_tasks_with_options_async(
        self,
        request: esa20240910_models.DescribePurgeTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DescribePurgeTasksResponse:
        """
        @summary Queries the details of purge tasks.
        
        @param request: DescribePurgeTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePurgeTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePurgeTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DescribePurgeTasksResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_purge_tasks(
        self,
        request: esa20240910_models.DescribePurgeTasksRequest,
    ) -> esa20240910_models.DescribePurgeTasksResponse:
        """
        @summary Queries the details of purge tasks.
        
        @param request: DescribePurgeTasksRequest
        @return: DescribePurgeTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_purge_tasks_with_options(request, runtime)

    async def describe_purge_tasks_async(
        self,
        request: esa20240910_models.DescribePurgeTasksRequest,
    ) -> esa20240910_models.DescribePurgeTasksResponse:
        """
        @summary Queries the details of purge tasks.
        
        @param request: DescribePurgeTasksRequest
        @return: DescribePurgeTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_purge_tasks_with_options_async(request, runtime)

    def disable_custom_scene_policy_with_options(
        self,
        request: esa20240910_models.DisableCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DisableCustomScenePolicyResponse:
        """
        @summary Disables a scenario-specific policy.
        
        @param request: DisableCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DisableCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DisableCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DisableCustomScenePolicyResponse(),
            self.call_api(params, req, runtime)
        )

    async def disable_custom_scene_policy_with_options_async(
        self,
        request: esa20240910_models.DisableCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.DisableCustomScenePolicyResponse:
        """
        @summary Disables a scenario-specific policy.
        
        @param request: DisableCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DisableCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DisableCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.DisableCustomScenePolicyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def disable_custom_scene_policy(
        self,
        request: esa20240910_models.DisableCustomScenePolicyRequest,
    ) -> esa20240910_models.DisableCustomScenePolicyResponse:
        """
        @summary Disables a scenario-specific policy.
        
        @param request: DisableCustomScenePolicyRequest
        @return: DisableCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.disable_custom_scene_policy_with_options(request, runtime)

    async def disable_custom_scene_policy_async(
        self,
        request: esa20240910_models.DisableCustomScenePolicyRequest,
    ) -> esa20240910_models.DisableCustomScenePolicyResponse:
        """
        @summary Disables a scenario-specific policy.
        
        @param request: DisableCustomScenePolicyRequest
        @return: DisableCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.disable_custom_scene_policy_with_options_async(request, runtime)

    def edit_site_waf_settings_with_options(
        self,
        tmp_req: esa20240910_models.EditSiteWafSettingsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.EditSiteWafSettingsResponse:
        """
        @summary Modifies the Web Application Firewall (WAF) configuration of a website, such as the client IP address that is identified by WAF.
        
        @param tmp_req: EditSiteWafSettingsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EditSiteWafSettingsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.EditSiteWafSettingsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.settings):
            request.settings_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.settings, 'Settings', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.settings_shrink):
            body['Settings'] = request.settings_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EditSiteWafSettings',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.EditSiteWafSettingsResponse(),
            self.call_api(params, req, runtime)
        )

    async def edit_site_waf_settings_with_options_async(
        self,
        tmp_req: esa20240910_models.EditSiteWafSettingsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.EditSiteWafSettingsResponse:
        """
        @summary Modifies the Web Application Firewall (WAF) configuration of a website, such as the client IP address that is identified by WAF.
        
        @param tmp_req: EditSiteWafSettingsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EditSiteWafSettingsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.EditSiteWafSettingsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.settings):
            request.settings_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.settings, 'Settings', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.settings_shrink):
            body['Settings'] = request.settings_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EditSiteWafSettings',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.EditSiteWafSettingsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def edit_site_waf_settings(
        self,
        request: esa20240910_models.EditSiteWafSettingsRequest,
    ) -> esa20240910_models.EditSiteWafSettingsResponse:
        """
        @summary Modifies the Web Application Firewall (WAF) configuration of a website, such as the client IP address that is identified by WAF.
        
        @param request: EditSiteWafSettingsRequest
        @return: EditSiteWafSettingsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.edit_site_waf_settings_with_options(request, runtime)

    async def edit_site_waf_settings_async(
        self,
        request: esa20240910_models.EditSiteWafSettingsRequest,
    ) -> esa20240910_models.EditSiteWafSettingsResponse:
        """
        @summary Modifies the Web Application Firewall (WAF) configuration of a website, such as the client IP address that is identified by WAF.
        
        @param request: EditSiteWafSettingsRequest
        @return: EditSiteWafSettingsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.edit_site_waf_settings_with_options_async(request, runtime)

    def enable_custom_scene_policy_with_options(
        self,
        request: esa20240910_models.EnableCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.EnableCustomScenePolicyResponse:
        """
        @summary Enables a scenario-specific policy.
        
        @param request: EnableCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EnableCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='EnableCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.EnableCustomScenePolicyResponse(),
            self.call_api(params, req, runtime)
        )

    async def enable_custom_scene_policy_with_options_async(
        self,
        request: esa20240910_models.EnableCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.EnableCustomScenePolicyResponse:
        """
        @summary Enables a scenario-specific policy.
        
        @param request: EnableCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EnableCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='EnableCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.EnableCustomScenePolicyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def enable_custom_scene_policy(
        self,
        request: esa20240910_models.EnableCustomScenePolicyRequest,
    ) -> esa20240910_models.EnableCustomScenePolicyResponse:
        """
        @summary Enables a scenario-specific policy.
        
        @param request: EnableCustomScenePolicyRequest
        @return: EnableCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.enable_custom_scene_policy_with_options(request, runtime)

    async def enable_custom_scene_policy_async(
        self,
        request: esa20240910_models.EnableCustomScenePolicyRequest,
    ) -> esa20240910_models.EnableCustomScenePolicyResponse:
        """
        @summary Enables a scenario-specific policy.
        
        @param request: EnableCustomScenePolicyRequest
        @return: EnableCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.enable_custom_scene_policy_with_options_async(request, runtime)

    def export_records_with_options(
        self,
        request: esa20240910_models.ExportRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ExportRecordsResponse:
        """
        @summary Exports all DNS records of a website domain as a TXT file.
        
        @param request: ExportRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ExportRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ExportRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ExportRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def export_records_with_options_async(
        self,
        request: esa20240910_models.ExportRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ExportRecordsResponse:
        """
        @summary Exports all DNS records of a website domain as a TXT file.
        
        @param request: ExportRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ExportRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ExportRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ExportRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def export_records(
        self,
        request: esa20240910_models.ExportRecordsRequest,
    ) -> esa20240910_models.ExportRecordsResponse:
        """
        @summary Exports all DNS records of a website domain as a TXT file.
        
        @param request: ExportRecordsRequest
        @return: ExportRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.export_records_with_options(request, runtime)

    async def export_records_async(
        self,
        request: esa20240910_models.ExportRecordsRequest,
    ) -> esa20240910_models.ExportRecordsResponse:
        """
        @summary Exports all DNS records of a website domain as a TXT file.
        
        @param request: ExportRecordsRequest
        @return: ExportRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.export_records_with_options_async(request, runtime)

    def get_cache_reserve_specification_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetCacheReserveSpecificationResponse:
        """
        @summary Queries the available specifications of cache reserve instances.
        
        @param request: GetCacheReserveSpecificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCacheReserveSpecificationResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetCacheReserveSpecification',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetCacheReserveSpecificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_cache_reserve_specification_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetCacheReserveSpecificationResponse:
        """
        @summary Queries the available specifications of cache reserve instances.
        
        @param request: GetCacheReserveSpecificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCacheReserveSpecificationResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetCacheReserveSpecification',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetCacheReserveSpecificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_cache_reserve_specification(self) -> esa20240910_models.GetCacheReserveSpecificationResponse:
        """
        @summary Queries the available specifications of cache reserve instances.
        
        @return: GetCacheReserveSpecificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_cache_reserve_specification_with_options(runtime)

    async def get_cache_reserve_specification_async(self) -> esa20240910_models.GetCacheReserveSpecificationResponse:
        """
        @summary Queries the available specifications of cache reserve instances.
        
        @return: GetCacheReserveSpecificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_cache_reserve_specification_with_options_async(runtime)

    def get_certificate_quota_with_options(
        self,
        request: esa20240910_models.GetCertificateQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetCertificateQuotaResponse:
        """
        @summary 查询证书quota及用量
        
        @param request: GetCertificateQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCertificateQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCertificateQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetCertificateQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_certificate_quota_with_options_async(
        self,
        request: esa20240910_models.GetCertificateQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetCertificateQuotaResponse:
        """
        @summary 查询证书quota及用量
        
        @param request: GetCertificateQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetCertificateQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCertificateQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetCertificateQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_certificate_quota(
        self,
        request: esa20240910_models.GetCertificateQuotaRequest,
    ) -> esa20240910_models.GetCertificateQuotaResponse:
        """
        @summary 查询证书quota及用量
        
        @param request: GetCertificateQuotaRequest
        @return: GetCertificateQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_certificate_quota_with_options(request, runtime)

    async def get_certificate_quota_async(
        self,
        request: esa20240910_models.GetCertificateQuotaRequest,
    ) -> esa20240910_models.GetCertificateQuotaResponse:
        """
        @summary 查询证书quota及用量
        
        @param request: GetCertificateQuotaRequest
        @return: GetCertificateQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_certificate_quota_with_options_async(request, runtime)

    def get_client_ca_certificate_with_options(
        self,
        request: esa20240910_models.GetClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCaCertificateResponse:
        """
        @summary 获取客户端CA证书信息
        
        @param request: GetClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCaCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_client_ca_certificate_with_options_async(
        self,
        request: esa20240910_models.GetClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCaCertificateResponse:
        """
        @summary 获取客户端CA证书信息
        
        @param request: GetClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCaCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_client_ca_certificate(
        self,
        request: esa20240910_models.GetClientCaCertificateRequest,
    ) -> esa20240910_models.GetClientCaCertificateResponse:
        """
        @summary 获取客户端CA证书信息
        
        @param request: GetClientCaCertificateRequest
        @return: GetClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_client_ca_certificate_with_options(request, runtime)

    async def get_client_ca_certificate_async(
        self,
        request: esa20240910_models.GetClientCaCertificateRequest,
    ) -> esa20240910_models.GetClientCaCertificateResponse:
        """
        @summary 获取客户端CA证书信息
        
        @param request: GetClientCaCertificateRequest
        @return: GetClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_client_ca_certificate_with_options_async(request, runtime)

    def get_client_certificate_with_options(
        self,
        request: esa20240910_models.GetClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCertificateResponse:
        """
        @summary Queries information about a client certificate.
        
        @param request: GetClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_client_certificate_with_options_async(
        self,
        request: esa20240910_models.GetClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCertificateResponse:
        """
        @summary Queries information about a client certificate.
        
        @param request: GetClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_client_certificate(
        self,
        request: esa20240910_models.GetClientCertificateRequest,
    ) -> esa20240910_models.GetClientCertificateResponse:
        """
        @summary Queries information about a client certificate.
        
        @param request: GetClientCertificateRequest
        @return: GetClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_client_certificate_with_options(request, runtime)

    async def get_client_certificate_async(
        self,
        request: esa20240910_models.GetClientCertificateRequest,
    ) -> esa20240910_models.GetClientCertificateResponse:
        """
        @summary Queries information about a client certificate.
        
        @param request: GetClientCertificateRequest
        @return: GetClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_client_certificate_with_options_async(request, runtime)

    def get_client_certificate_hostnames_with_options(
        self,
        request: esa20240910_models.GetClientCertificateHostnamesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCertificateHostnamesResponse:
        """
        @summary 获取客户端证书绑定的域名列表
        
        @param request: GetClientCertificateHostnamesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCertificateHostnamesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCertificateHostnames',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCertificateHostnamesResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_client_certificate_hostnames_with_options_async(
        self,
        request: esa20240910_models.GetClientCertificateHostnamesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetClientCertificateHostnamesResponse:
        """
        @summary 获取客户端证书绑定的域名列表
        
        @param request: GetClientCertificateHostnamesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetClientCertificateHostnamesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientCertificateHostnames',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetClientCertificateHostnamesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_client_certificate_hostnames(
        self,
        request: esa20240910_models.GetClientCertificateHostnamesRequest,
    ) -> esa20240910_models.GetClientCertificateHostnamesResponse:
        """
        @summary 获取客户端证书绑定的域名列表
        
        @param request: GetClientCertificateHostnamesRequest
        @return: GetClientCertificateHostnamesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_client_certificate_hostnames_with_options(request, runtime)

    async def get_client_certificate_hostnames_async(
        self,
        request: esa20240910_models.GetClientCertificateHostnamesRequest,
    ) -> esa20240910_models.GetClientCertificateHostnamesResponse:
        """
        @summary 获取客户端证书绑定的域名列表
        
        @param request: GetClientCertificateHostnamesRequest
        @return: GetClientCertificateHostnamesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_client_certificate_hostnames_with_options_async(request, runtime)

    def get_edge_container_app_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppResponse:
        """
        @summary Queries the information about a containerized application, including basic application configurations and health check configurations.
        
        @param request: GetEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_app_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppResponse:
        """
        @summary Queries the information about a containerized application, including basic application configurations and health check configurations.
        
        @param request: GetEdgeContainerAppRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerApp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_app(
        self,
        request: esa20240910_models.GetEdgeContainerAppRequest,
    ) -> esa20240910_models.GetEdgeContainerAppResponse:
        """
        @summary Queries the information about a containerized application, including basic application configurations and health check configurations.
        
        @param request: GetEdgeContainerAppRequest
        @return: GetEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_app_with_options(request, runtime)

    async def get_edge_container_app_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppRequest,
    ) -> esa20240910_models.GetEdgeContainerAppResponse:
        """
        @summary Queries the information about a containerized application, including basic application configurations and health check configurations.
        
        @param request: GetEdgeContainerAppRequest
        @return: GetEdgeContainerAppResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_app_with_options_async(request, runtime)

    def get_edge_container_app_status_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerAppStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppStatusResponse:
        """
        @summary Queries the status information about a containerized application, including the deployment, release, and rollback of the application.
        
        @param request: GetEdgeContainerAppStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.publish_env):
            query['PublishEnv'] = request.publish_env
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerAppStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_app_status_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppStatusResponse:
        """
        @summary Queries the status information about a containerized application, including the deployment, release, and rollback of the application.
        
        @param request: GetEdgeContainerAppStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.publish_env):
            query['PublishEnv'] = request.publish_env
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerAppStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_app_status(
        self,
        request: esa20240910_models.GetEdgeContainerAppStatusRequest,
    ) -> esa20240910_models.GetEdgeContainerAppStatusResponse:
        """
        @summary Queries the status information about a containerized application, including the deployment, release, and rollback of the application.
        
        @param request: GetEdgeContainerAppStatusRequest
        @return: GetEdgeContainerAppStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_app_status_with_options(request, runtime)

    async def get_edge_container_app_status_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppStatusRequest,
    ) -> esa20240910_models.GetEdgeContainerAppStatusResponse:
        """
        @summary Queries the status information about a containerized application, including the deployment, release, and rollback of the application.
        
        @param request: GetEdgeContainerAppStatusRequest
        @return: GetEdgeContainerAppStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_app_status_with_options_async(request, runtime)

    def get_edge_container_app_version_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppVersionResponse:
        """
        @summary Queries the information about a version of a containerized application. You can select an application version to release based on the version information.
        
        @param request: GetEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_app_version_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerAppVersionResponse:
        """
        @summary Queries the information about a version of a containerized application. You can select an application version to release based on the version information.
        
        @param request: GetEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerAppVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_app_version(
        self,
        request: esa20240910_models.GetEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.GetEdgeContainerAppVersionResponse:
        """
        @summary Queries the information about a version of a containerized application. You can select an application version to release based on the version information.
        
        @param request: GetEdgeContainerAppVersionRequest
        @return: GetEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_app_version_with_options(request, runtime)

    async def get_edge_container_app_version_async(
        self,
        request: esa20240910_models.GetEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.GetEdgeContainerAppVersionResponse:
        """
        @summary Queries the information about a version of a containerized application. You can select an application version to release based on the version information.
        
        @param request: GetEdgeContainerAppVersionRequest
        @return: GetEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_app_version_with_options_async(request, runtime)

    def get_edge_container_deploy_regions_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerDeployRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerDeployRegionsResponse:
        """
        @summary Queries regions where a containerized application is deployed based on the application ID.
        
        @param request: GetEdgeContainerDeployRegionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerDeployRegionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerDeployRegions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerDeployRegionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_deploy_regions_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerDeployRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerDeployRegionsResponse:
        """
        @summary Queries regions where a containerized application is deployed based on the application ID.
        
        @param request: GetEdgeContainerDeployRegionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerDeployRegionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerDeployRegions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerDeployRegionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_deploy_regions(
        self,
        request: esa20240910_models.GetEdgeContainerDeployRegionsRequest,
    ) -> esa20240910_models.GetEdgeContainerDeployRegionsResponse:
        """
        @summary Queries regions where a containerized application is deployed based on the application ID.
        
        @param request: GetEdgeContainerDeployRegionsRequest
        @return: GetEdgeContainerDeployRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_deploy_regions_with_options(request, runtime)

    async def get_edge_container_deploy_regions_async(
        self,
        request: esa20240910_models.GetEdgeContainerDeployRegionsRequest,
    ) -> esa20240910_models.GetEdgeContainerDeployRegionsResponse:
        """
        @summary Queries regions where a containerized application is deployed based on the application ID.
        
        @param request: GetEdgeContainerDeployRegionsRequest
        @return: GetEdgeContainerDeployRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_deploy_regions_with_options_async(request, runtime)

    def get_edge_container_logs_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerLogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerLogsResponse:
        """
        @summary Queries Edge Container logs.
        
        @param request: GetEdgeContainerLogsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerLogsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerLogs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerLogsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_logs_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerLogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerLogsResponse:
        """
        @summary Queries Edge Container logs.
        
        @param request: GetEdgeContainerLogsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerLogsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerLogs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerLogsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_logs(
        self,
        request: esa20240910_models.GetEdgeContainerLogsRequest,
    ) -> esa20240910_models.GetEdgeContainerLogsResponse:
        """
        @summary Queries Edge Container logs.
        
        @param request: GetEdgeContainerLogsRequest
        @return: GetEdgeContainerLogsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_logs_with_options(request, runtime)

    async def get_edge_container_logs_async(
        self,
        request: esa20240910_models.GetEdgeContainerLogsRequest,
    ) -> esa20240910_models.GetEdgeContainerLogsResponse:
        """
        @summary Queries Edge Container logs.
        
        @param request: GetEdgeContainerLogsRequest
        @return: GetEdgeContainerLogsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_logs_with_options_async(request, runtime)

    def get_edge_container_staging_deploy_status_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerStagingDeployStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerStagingDeployStatusResponse:
        """
        @summary Queries the deployment status of an application in the staging environment by using the application ID.
        
        @param request: GetEdgeContainerStagingDeployStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerStagingDeployStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerStagingDeployStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerStagingDeployStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_staging_deploy_status_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerStagingDeployStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerStagingDeployStatusResponse:
        """
        @summary Queries the deployment status of an application in the staging environment by using the application ID.
        
        @param request: GetEdgeContainerStagingDeployStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerStagingDeployStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerStagingDeployStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerStagingDeployStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_staging_deploy_status(
        self,
        request: esa20240910_models.GetEdgeContainerStagingDeployStatusRequest,
    ) -> esa20240910_models.GetEdgeContainerStagingDeployStatusResponse:
        """
        @summary Queries the deployment status of an application in the staging environment by using the application ID.
        
        @param request: GetEdgeContainerStagingDeployStatusRequest
        @return: GetEdgeContainerStagingDeployStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_staging_deploy_status_with_options(request, runtime)

    async def get_edge_container_staging_deploy_status_async(
        self,
        request: esa20240910_models.GetEdgeContainerStagingDeployStatusRequest,
    ) -> esa20240910_models.GetEdgeContainerStagingDeployStatusResponse:
        """
        @summary Queries the deployment status of an application in the staging environment by using the application ID.
        
        @param request: GetEdgeContainerStagingDeployStatusRequest
        @return: GetEdgeContainerStagingDeployStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_staging_deploy_status_with_options_async(request, runtime)

    def get_edge_container_terminal_with_options(
        self,
        request: esa20240910_models.GetEdgeContainerTerminalRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerTerminalResponse:
        """
        @summary Queries the terminal information of a containerized application.
        
        @param request: GetEdgeContainerTerminalRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerTerminalResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerTerminal',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerTerminalResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_edge_container_terminal_with_options_async(
        self,
        request: esa20240910_models.GetEdgeContainerTerminalRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetEdgeContainerTerminalResponse:
        """
        @summary Queries the terminal information of a containerized application.
        
        @param request: GetEdgeContainerTerminalRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetEdgeContainerTerminalResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEdgeContainerTerminal',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetEdgeContainerTerminalResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_edge_container_terminal(
        self,
        request: esa20240910_models.GetEdgeContainerTerminalRequest,
    ) -> esa20240910_models.GetEdgeContainerTerminalResponse:
        """
        @summary Queries the terminal information of a containerized application.
        
        @param request: GetEdgeContainerTerminalRequest
        @return: GetEdgeContainerTerminalResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_edge_container_terminal_with_options(request, runtime)

    async def get_edge_container_terminal_async(
        self,
        request: esa20240910_models.GetEdgeContainerTerminalRequest,
    ) -> esa20240910_models.GetEdgeContainerTerminalResponse:
        """
        @summary Queries the terminal information of a containerized application.
        
        @param request: GetEdgeContainerTerminalRequest
        @return: GetEdgeContainerTerminalResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_edge_container_terminal_with_options_async(request, runtime)

    def get_er_service_with_options(
        self,
        request: esa20240910_models.GetErServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetErServiceResponse:
        """
        @summary Checks the status of Edge Routine.
        
        @param request: GetErServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetErServiceResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetErService',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetErServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_er_service_with_options_async(
        self,
        request: esa20240910_models.GetErServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetErServiceResponse:
        """
        @summary Checks the status of Edge Routine.
        
        @param request: GetErServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetErServiceResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetErService',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetErServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_er_service(
        self,
        request: esa20240910_models.GetErServiceRequest,
    ) -> esa20240910_models.GetErServiceResponse:
        """
        @summary Checks the status of Edge Routine.
        
        @param request: GetErServiceRequest
        @return: GetErServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_er_service_with_options(request, runtime)

    async def get_er_service_async(
        self,
        request: esa20240910_models.GetErServiceRequest,
    ) -> esa20240910_models.GetErServiceResponse:
        """
        @summary Checks the status of Edge Routine.
        
        @param request: GetErServiceRequest
        @return: GetErServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_er_service_with_options_async(request, runtime)

    def get_kv_with_options(
        self,
        request: esa20240910_models.GetKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvResponse:
        """
        @summary Queries the value of a key in a key-value pair.
        
        @param request: GetKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_kv_with_options_async(
        self,
        request: esa20240910_models.GetKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvResponse:
        """
        @summary Queries the value of a key in a key-value pair.
        
        @param request: GetKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_kv(
        self,
        request: esa20240910_models.GetKvRequest,
    ) -> esa20240910_models.GetKvResponse:
        """
        @summary Queries the value of a key in a key-value pair.
        
        @param request: GetKvRequest
        @return: GetKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_kv_with_options(request, runtime)

    async def get_kv_async(
        self,
        request: esa20240910_models.GetKvRequest,
    ) -> esa20240910_models.GetKvResponse:
        """
        @summary Queries the value of a key in a key-value pair.
        
        @param request: GetKvRequest
        @return: GetKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_kv_with_options_async(request, runtime)

    def get_kv_account_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvAccountResponse:
        """
        @summary Queries the Edge KV usage in your Alibaba Cloud account, including the information about all namespaces.
        
        @param request: GetKvAccountRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvAccountResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetKvAccount',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvAccountResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_kv_account_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvAccountResponse:
        """
        @summary Queries the Edge KV usage in your Alibaba Cloud account, including the information about all namespaces.
        
        @param request: GetKvAccountRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvAccountResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetKvAccount',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvAccountResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_kv_account(self) -> esa20240910_models.GetKvAccountResponse:
        """
        @summary Queries the Edge KV usage in your Alibaba Cloud account, including the information about all namespaces.
        
        @return: GetKvAccountResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_kv_account_with_options(runtime)

    async def get_kv_account_async(self) -> esa20240910_models.GetKvAccountResponse:
        """
        @summary Queries the Edge KV usage in your Alibaba Cloud account, including the information about all namespaces.
        
        @return: GetKvAccountResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_kv_account_with_options_async(runtime)

    def get_kv_namespace_with_options(
        self,
        request: esa20240910_models.GetKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvNamespaceResponse:
        """
        @summary Queries the information about a namespace in your Alibaba Cloud account.
        
        @param request: GetKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvNamespaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_kv_namespace_with_options_async(
        self,
        request: esa20240910_models.GetKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetKvNamespaceResponse:
        """
        @summary Queries the information about a namespace in your Alibaba Cloud account.
        
        @param request: GetKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetKvNamespaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_kv_namespace(
        self,
        request: esa20240910_models.GetKvNamespaceRequest,
    ) -> esa20240910_models.GetKvNamespaceResponse:
        """
        @summary Queries the information about a namespace in your Alibaba Cloud account.
        
        @param request: GetKvNamespaceRequest
        @return: GetKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_kv_namespace_with_options(request, runtime)

    async def get_kv_namespace_async(
        self,
        request: esa20240910_models.GetKvNamespaceRequest,
    ) -> esa20240910_models.GetKvNamespaceResponse:
        """
        @summary Queries the information about a namespace in your Alibaba Cloud account.
        
        @param request: GetKvNamespaceRequest
        @return: GetKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_kv_namespace_with_options_async(request, runtime)

    def get_list_with_options(
        self,
        request: esa20240910_models.GetListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetListResponse:
        """
        @summary Queries the details of a custom list, such as the name, description, type, and content.
        
        @param request: GetListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetListResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_list_with_options_async(
        self,
        request: esa20240910_models.GetListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetListResponse:
        """
        @summary Queries the details of a custom list, such as the name, description, type, and content.
        
        @param request: GetListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_list(
        self,
        request: esa20240910_models.GetListRequest,
    ) -> esa20240910_models.GetListResponse:
        """
        @summary Queries the details of a custom list, such as the name, description, type, and content.
        
        @param request: GetListRequest
        @return: GetListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_list_with_options(request, runtime)

    async def get_list_async(
        self,
        request: esa20240910_models.GetListRequest,
    ) -> esa20240910_models.GetListResponse:
        """
        @summary Queries the details of a custom list, such as the name, description, type, and content.
        
        @param request: GetListRequest
        @return: GetListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_list_with_options_async(request, runtime)

    def get_origin_protection_with_options(
        self,
        request: esa20240910_models.GetOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetOriginProtectionResponse:
        """
        @summary Queries the origin protection configurations of a website, including the origin protection, IP convergence, and the status and details of the IP whitelist for origin protection. The details includes the IP whitelist used by the website, the latest IP whitelist, and the differences between them.
        
        @param request: GetOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetOriginProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_origin_protection_with_options_async(
        self,
        request: esa20240910_models.GetOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetOriginProtectionResponse:
        """
        @summary Queries the origin protection configurations of a website, including the origin protection, IP convergence, and the status and details of the IP whitelist for origin protection. The details includes the IP whitelist used by the website, the latest IP whitelist, and the differences between them.
        
        @param request: GetOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetOriginProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_origin_protection(
        self,
        request: esa20240910_models.GetOriginProtectionRequest,
    ) -> esa20240910_models.GetOriginProtectionResponse:
        """
        @summary Queries the origin protection configurations of a website, including the origin protection, IP convergence, and the status and details of the IP whitelist for origin protection. The details includes the IP whitelist used by the website, the latest IP whitelist, and the differences between them.
        
        @param request: GetOriginProtectionRequest
        @return: GetOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_origin_protection_with_options(request, runtime)

    async def get_origin_protection_async(
        self,
        request: esa20240910_models.GetOriginProtectionRequest,
    ) -> esa20240910_models.GetOriginProtectionResponse:
        """
        @summary Queries the origin protection configurations of a website, including the origin protection, IP convergence, and the status and details of the IP whitelist for origin protection. The details includes the IP whitelist used by the website, the latest IP whitelist, and the differences between them.
        
        @param request: GetOriginProtectionRequest
        @return: GetOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_origin_protection_with_options_async(request, runtime)

    def get_page_with_options(
        self,
        request: esa20240910_models.GetPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetPageResponse:
        """
        @summary Queries the details of a custom error page based on the error page ID.
        
        @param request: GetPageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetPageResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_page_with_options_async(
        self,
        request: esa20240910_models.GetPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetPageResponse:
        """
        @summary Queries the details of a custom error page based on the error page ID.
        
        @param request: GetPageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetPageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_page(
        self,
        request: esa20240910_models.GetPageRequest,
    ) -> esa20240910_models.GetPageResponse:
        """
        @summary Queries the details of a custom error page based on the error page ID.
        
        @param request: GetPageRequest
        @return: GetPageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_page_with_options(request, runtime)

    async def get_page_async(
        self,
        request: esa20240910_models.GetPageRequest,
    ) -> esa20240910_models.GetPageResponse:
        """
        @summary Queries the details of a custom error page based on the error page ID.
        
        @param request: GetPageRequest
        @return: GetPageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_page_with_options_async(request, runtime)

    def get_purge_quota_with_options(
        self,
        request: esa20240910_models.GetPurgeQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetPurgeQuotaResponse:
        """
        @summary Queries the quotas and quota usage for different cache purge options.
        
        @param request: GetPurgeQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPurgeQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPurgeQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetPurgeQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_purge_quota_with_options_async(
        self,
        request: esa20240910_models.GetPurgeQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetPurgeQuotaResponse:
        """
        @summary Queries the quotas and quota usage for different cache purge options.
        
        @param request: GetPurgeQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetPurgeQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetPurgeQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetPurgeQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_purge_quota(
        self,
        request: esa20240910_models.GetPurgeQuotaRequest,
    ) -> esa20240910_models.GetPurgeQuotaResponse:
        """
        @summary Queries the quotas and quota usage for different cache purge options.
        
        @param request: GetPurgeQuotaRequest
        @return: GetPurgeQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_purge_quota_with_options(request, runtime)

    async def get_purge_quota_async(
        self,
        request: esa20240910_models.GetPurgeQuotaRequest,
    ) -> esa20240910_models.GetPurgeQuotaResponse:
        """
        @summary Queries the quotas and quota usage for different cache purge options.
        
        @param request: GetPurgeQuotaRequest
        @return: GetPurgeQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_purge_quota_with_options_async(request, runtime)

    def get_realtime_delivery_field_with_options(
        self,
        request: esa20240910_models.GetRealtimeDeliveryFieldRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRealtimeDeliveryFieldResponse:
        """
        @summary Queries the fields in real-time logs based on the log category.
        
        @param request: GetRealtimeDeliveryFieldRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRealtimeDeliveryFieldResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRealtimeDeliveryField',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRealtimeDeliveryFieldResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_realtime_delivery_field_with_options_async(
        self,
        request: esa20240910_models.GetRealtimeDeliveryFieldRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRealtimeDeliveryFieldResponse:
        """
        @summary Queries the fields in real-time logs based on the log category.
        
        @param request: GetRealtimeDeliveryFieldRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRealtimeDeliveryFieldResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRealtimeDeliveryField',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRealtimeDeliveryFieldResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_realtime_delivery_field(
        self,
        request: esa20240910_models.GetRealtimeDeliveryFieldRequest,
    ) -> esa20240910_models.GetRealtimeDeliveryFieldResponse:
        """
        @summary Queries the fields in real-time logs based on the log category.
        
        @param request: GetRealtimeDeliveryFieldRequest
        @return: GetRealtimeDeliveryFieldResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_realtime_delivery_field_with_options(request, runtime)

    async def get_realtime_delivery_field_async(
        self,
        request: esa20240910_models.GetRealtimeDeliveryFieldRequest,
    ) -> esa20240910_models.GetRealtimeDeliveryFieldResponse:
        """
        @summary Queries the fields in real-time logs based on the log category.
        
        @param request: GetRealtimeDeliveryFieldRequest
        @return: GetRealtimeDeliveryFieldResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_realtime_delivery_field_with_options_async(request, runtime)

    def get_record_with_options(
        self,
        request: esa20240910_models.GetRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRecordResponse:
        """
        @summary Queries the configuration of a single DNS record, such as the record value, priority, and origin authentication setting (exclusive to CNAME records).
        
        @param request: GetRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRecordResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_record_with_options_async(
        self,
        request: esa20240910_models.GetRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRecordResponse:
        """
        @summary Queries the configuration of a single DNS record, such as the record value, priority, and origin authentication setting (exclusive to CNAME records).
        
        @param request: GetRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRecordResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_record(
        self,
        request: esa20240910_models.GetRecordRequest,
    ) -> esa20240910_models.GetRecordResponse:
        """
        @summary Queries the configuration of a single DNS record, such as the record value, priority, and origin authentication setting (exclusive to CNAME records).
        
        @param request: GetRecordRequest
        @return: GetRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_record_with_options(request, runtime)

    async def get_record_async(
        self,
        request: esa20240910_models.GetRecordRequest,
    ) -> esa20240910_models.GetRecordResponse:
        """
        @summary Queries the configuration of a single DNS record, such as the record value, priority, and origin authentication setting (exclusive to CNAME records).
        
        @param request: GetRecordRequest
        @return: GetRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_record_with_options_async(request, runtime)

    def get_routine_with_options(
        self,
        request: esa20240910_models.GetRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineResponse:
        """
        @summary Queries the configurations of a routine, including the code versions and the configurations of the environments, associated domain names, and associated routes.
        
        @param request: GetRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_routine_with_options_async(
        self,
        request: esa20240910_models.GetRoutineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineResponse:
        """
        @summary Queries the configurations of a routine, including the code versions and the configurations of the environments, associated domain names, and associated routes.
        
        @param request: GetRoutineRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetRoutine',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_routine(
        self,
        request: esa20240910_models.GetRoutineRequest,
    ) -> esa20240910_models.GetRoutineResponse:
        """
        @summary Queries the configurations of a routine, including the code versions and the configurations of the environments, associated domain names, and associated routes.
        
        @param request: GetRoutineRequest
        @return: GetRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_routine_with_options(request, runtime)

    async def get_routine_async(
        self,
        request: esa20240910_models.GetRoutineRequest,
    ) -> esa20240910_models.GetRoutineResponse:
        """
        @summary Queries the configurations of a routine, including the code versions and the configurations of the environments, associated domain names, and associated routes.
        
        @param request: GetRoutineRequest
        @return: GetRoutineResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_routine_with_options_async(request, runtime)

    def get_routine_staging_code_upload_info_with_options(
        self,
        request: esa20240910_models.GetRoutineStagingCodeUploadInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineStagingCodeUploadInfoResponse:
        """
        @summary Obtains the release information about the routine code that is released to the staging environment. This information can be used to upload the test code to Object Storage Service (OSS).
        
        @description    Every time the code of a routine is released to the staging environment, a version number is generated. Such code is for tests only.
        A routine can retain a maximum of 10 code versions. If the number of versions reaches the limit, you must call the DeleteRoutineCodeRevision operation to delete unwanted versions.
        
        @param request: GetRoutineStagingCodeUploadInfoRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineStagingCodeUploadInfoResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_description):
            body['CodeDescription'] = request.code_description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetRoutineStagingCodeUploadInfo',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineStagingCodeUploadInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_routine_staging_code_upload_info_with_options_async(
        self,
        request: esa20240910_models.GetRoutineStagingCodeUploadInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineStagingCodeUploadInfoResponse:
        """
        @summary Obtains the release information about the routine code that is released to the staging environment. This information can be used to upload the test code to Object Storage Service (OSS).
        
        @description    Every time the code of a routine is released to the staging environment, a version number is generated. Such code is for tests only.
        A routine can retain a maximum of 10 code versions. If the number of versions reaches the limit, you must call the DeleteRoutineCodeRevision operation to delete unwanted versions.
        
        @param request: GetRoutineStagingCodeUploadInfoRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineStagingCodeUploadInfoResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code_description):
            body['CodeDescription'] = request.code_description
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GetRoutineStagingCodeUploadInfo',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineStagingCodeUploadInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_routine_staging_code_upload_info(
        self,
        request: esa20240910_models.GetRoutineStagingCodeUploadInfoRequest,
    ) -> esa20240910_models.GetRoutineStagingCodeUploadInfoResponse:
        """
        @summary Obtains the release information about the routine code that is released to the staging environment. This information can be used to upload the test code to Object Storage Service (OSS).
        
        @description    Every time the code of a routine is released to the staging environment, a version number is generated. Such code is for tests only.
        A routine can retain a maximum of 10 code versions. If the number of versions reaches the limit, you must call the DeleteRoutineCodeRevision operation to delete unwanted versions.
        
        @param request: GetRoutineStagingCodeUploadInfoRequest
        @return: GetRoutineStagingCodeUploadInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_routine_staging_code_upload_info_with_options(request, runtime)

    async def get_routine_staging_code_upload_info_async(
        self,
        request: esa20240910_models.GetRoutineStagingCodeUploadInfoRequest,
    ) -> esa20240910_models.GetRoutineStagingCodeUploadInfoResponse:
        """
        @summary Obtains the release information about the routine code that is released to the staging environment. This information can be used to upload the test code to Object Storage Service (OSS).
        
        @description    Every time the code of a routine is released to the staging environment, a version number is generated. Such code is for tests only.
        A routine can retain a maximum of 10 code versions. If the number of versions reaches the limit, you must call the DeleteRoutineCodeRevision operation to delete unwanted versions.
        
        @param request: GetRoutineStagingCodeUploadInfoRequest
        @return: GetRoutineStagingCodeUploadInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_routine_staging_code_upload_info_with_options_async(request, runtime)

    def get_routine_staging_env_ip_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineStagingEnvIpResponse:
        """
        @summary Queries the IP addresses of staging environments for Edge Routine.
        
        @param request: GetRoutineStagingEnvIpRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineStagingEnvIpResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetRoutineStagingEnvIp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineStagingEnvIpResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_routine_staging_env_ip_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineStagingEnvIpResponse:
        """
        @summary Queries the IP addresses of staging environments for Edge Routine.
        
        @param request: GetRoutineStagingEnvIpRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineStagingEnvIpResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetRoutineStagingEnvIp',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineStagingEnvIpResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_routine_staging_env_ip(self) -> esa20240910_models.GetRoutineStagingEnvIpResponse:
        """
        @summary Queries the IP addresses of staging environments for Edge Routine.
        
        @return: GetRoutineStagingEnvIpResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_routine_staging_env_ip_with_options(runtime)

    async def get_routine_staging_env_ip_async(self) -> esa20240910_models.GetRoutineStagingEnvIpResponse:
        """
        @summary Queries the IP addresses of staging environments for Edge Routine.
        
        @return: GetRoutineStagingEnvIpResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_routine_staging_env_ip_with_options_async(runtime)

    def get_routine_user_info_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineUserInfoResponse:
        """
        @summary Queries the Edge Routine information in your Alibaba Cloud account, including the associated subdomain and created routines.
        
        @param request: GetRoutineUserInfoRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineUserInfoResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetRoutineUserInfo',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineUserInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_routine_user_info_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetRoutineUserInfoResponse:
        """
        @summary Queries the Edge Routine information in your Alibaba Cloud account, including the associated subdomain and created routines.
        
        @param request: GetRoutineUserInfoRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetRoutineUserInfoResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetRoutineUserInfo',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetRoutineUserInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_routine_user_info(self) -> esa20240910_models.GetRoutineUserInfoResponse:
        """
        @summary Queries the Edge Routine information in your Alibaba Cloud account, including the associated subdomain and created routines.
        
        @return: GetRoutineUserInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_routine_user_info_with_options(runtime)

    async def get_routine_user_info_async(self) -> esa20240910_models.GetRoutineUserInfoResponse:
        """
        @summary Queries the Edge Routine information in your Alibaba Cloud account, including the associated subdomain and created routines.
        
        @return: GetRoutineUserInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_routine_user_info_with_options_async(runtime)

    def get_scheduled_preload_job_with_options(
        self,
        request: esa20240910_models.GetScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetScheduledPreloadJobResponse:
        """
        @summary Queries a specified scheduled prefetch task based on the task ID.
        
        @param request: GetScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetScheduledPreloadJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_scheduled_preload_job_with_options_async(
        self,
        request: esa20240910_models.GetScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetScheduledPreloadJobResponse:
        """
        @summary Queries a specified scheduled prefetch task based on the task ID.
        
        @param request: GetScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetScheduledPreloadJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_scheduled_preload_job(
        self,
        request: esa20240910_models.GetScheduledPreloadJobRequest,
    ) -> esa20240910_models.GetScheduledPreloadJobResponse:
        """
        @summary Queries a specified scheduled prefetch task based on the task ID.
        
        @param request: GetScheduledPreloadJobRequest
        @return: GetScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_scheduled_preload_job_with_options(request, runtime)

    async def get_scheduled_preload_job_async(
        self,
        request: esa20240910_models.GetScheduledPreloadJobRequest,
    ) -> esa20240910_models.GetScheduledPreloadJobResponse:
        """
        @summary Queries a specified scheduled prefetch task based on the task ID.
        
        @param request: GetScheduledPreloadJobRequest
        @return: GetScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_scheduled_preload_job_with_options_async(request, runtime)

    def get_site_with_options(
        self,
        request: esa20240910_models.GetSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteResponse:
        """
        @summary Queries information about a website based on the website ID.
        
        @param request: GetSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_with_options_async(
        self,
        request: esa20240910_models.GetSiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteResponse:
        """
        @summary Queries information about a website based on the website ID.
        
        @param request: GetSiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site(
        self,
        request: esa20240910_models.GetSiteRequest,
    ) -> esa20240910_models.GetSiteResponse:
        """
        @summary Queries information about a website based on the website ID.
        
        @param request: GetSiteRequest
        @return: GetSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_with_options(request, runtime)

    async def get_site_async(
        self,
        request: esa20240910_models.GetSiteRequest,
    ) -> esa20240910_models.GetSiteResponse:
        """
        @summary Queries information about a website based on the website ID.
        
        @param request: GetSiteRequest
        @return: GetSiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_with_options_async(request, runtime)

    def get_site_current_nswith_options(
        self,
        request: esa20240910_models.GetSiteCurrentNSRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteCurrentNSResponse:
        """
        @summary Queries the nameservers configured for a website.
        
        @param request: GetSiteCurrentNSRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteCurrentNSResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteCurrentNS',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteCurrentNSResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_current_nswith_options_async(
        self,
        request: esa20240910_models.GetSiteCurrentNSRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteCurrentNSResponse:
        """
        @summary Queries the nameservers configured for a website.
        
        @param request: GetSiteCurrentNSRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteCurrentNSResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteCurrentNS',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteCurrentNSResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site_current_ns(
        self,
        request: esa20240910_models.GetSiteCurrentNSRequest,
    ) -> esa20240910_models.GetSiteCurrentNSResponse:
        """
        @summary Queries the nameservers configured for a website.
        
        @param request: GetSiteCurrentNSRequest
        @return: GetSiteCurrentNSResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_current_nswith_options(request, runtime)

    async def get_site_current_ns_async(
        self,
        request: esa20240910_models.GetSiteCurrentNSRequest,
    ) -> esa20240910_models.GetSiteCurrentNSResponse:
        """
        @summary Queries the nameservers configured for a website.
        
        @param request: GetSiteCurrentNSRequest
        @return: GetSiteCurrentNSResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_current_nswith_options_async(request, runtime)

    def get_site_custom_log_with_options(
        self,
        request: esa20240910_models.GetSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteCustomLogResponse:
        """
        @summary Queries the configuration of custom log fields for a website.
        
        @description    **Description**: You can call this operation to query the configuration of custom log fields for a website, including custom fields in request headers, response headers, and cookies.
        **Scenarios**: You can call this operation in scenarios where you need to obtain specific HTTP headers or cookie information for log analysis.
        ****\
        
        @param request: GetSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteCustomLogResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteCustomLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_custom_log_with_options_async(
        self,
        request: esa20240910_models.GetSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteCustomLogResponse:
        """
        @summary Queries the configuration of custom log fields for a website.
        
        @description    **Description**: You can call this operation to query the configuration of custom log fields for a website, including custom fields in request headers, response headers, and cookies.
        **Scenarios**: You can call this operation in scenarios where you need to obtain specific HTTP headers or cookie information for log analysis.
        ****\
        
        @param request: GetSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteCustomLogResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteCustomLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site_custom_log(
        self,
        request: esa20240910_models.GetSiteCustomLogRequest,
    ) -> esa20240910_models.GetSiteCustomLogResponse:
        """
        @summary Queries the configuration of custom log fields for a website.
        
        @description    **Description**: You can call this operation to query the configuration of custom log fields for a website, including custom fields in request headers, response headers, and cookies.
        **Scenarios**: You can call this operation in scenarios where you need to obtain specific HTTP headers or cookie information for log analysis.
        ****\
        
        @param request: GetSiteCustomLogRequest
        @return: GetSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_custom_log_with_options(request, runtime)

    async def get_site_custom_log_async(
        self,
        request: esa20240910_models.GetSiteCustomLogRequest,
    ) -> esa20240910_models.GetSiteCustomLogResponse:
        """
        @summary Queries the configuration of custom log fields for a website.
        
        @description    **Description**: You can call this operation to query the configuration of custom log fields for a website, including custom fields in request headers, response headers, and cookies.
        **Scenarios**: You can call this operation in scenarios where you need to obtain specific HTTP headers or cookie information for log analysis.
        ****\
        
        @param request: GetSiteCustomLogRequest
        @return: GetSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_custom_log_with_options_async(request, runtime)

    def get_site_delivery_task_with_options(
        self,
        request: esa20240910_models.GetSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteDeliveryTaskResponse:
        """
        @summary Queries a real-time log delivery task.
        
        @param request: GetSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_delivery_task_with_options_async(
        self,
        request: esa20240910_models.GetSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteDeliveryTaskResponse:
        """
        @summary Queries a real-time log delivery task.
        
        @param request: GetSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site_delivery_task(
        self,
        request: esa20240910_models.GetSiteDeliveryTaskRequest,
    ) -> esa20240910_models.GetSiteDeliveryTaskResponse:
        """
        @summary Queries a real-time log delivery task.
        
        @param request: GetSiteDeliveryTaskRequest
        @return: GetSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_delivery_task_with_options(request, runtime)

    async def get_site_delivery_task_async(
        self,
        request: esa20240910_models.GetSiteDeliveryTaskRequest,
    ) -> esa20240910_models.GetSiteDeliveryTaskResponse:
        """
        @summary Queries a real-time log delivery task.
        
        @param request: GetSiteDeliveryTaskRequest
        @return: GetSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_delivery_task_with_options_async(request, runtime)

    def get_site_log_delivery_quota_with_options(
        self,
        request: esa20240910_models.GetSiteLogDeliveryQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining quota for delivering a specific category of real-time logs in a website.
        
        @description You can call this operation to query the remaining quota for delivering a specific category of real-time logs in a website within an Alibaba Cloud account. This is essential for monitoring and managing your log delivery capacity to ensure that logs can be delivered to the destination and prevent data loss or latency caused by insufficient quota.
        *Take note of the following parameters:**\
        ``
        `BusinessType` is required. You must specify a log category to obtain the corresponding quota information.
        `SiteId` specifies the ID of a website, which must be a valid integer that corresponds to a website that you configured on Alibaba Cloud.
        *Response:**\
        If a request is successful, the system returns the remaining log delivery quota (`FreeQuota`), request ID (`RequestId`), website ID (`SiteId`), and log category (`BusinessType`). You can confirm and record the returned data.
        
        @param request: GetSiteLogDeliveryQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteLogDeliveryQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteLogDeliveryQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteLogDeliveryQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_log_delivery_quota_with_options_async(
        self,
        request: esa20240910_models.GetSiteLogDeliveryQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining quota for delivering a specific category of real-time logs in a website.
        
        @description You can call this operation to query the remaining quota for delivering a specific category of real-time logs in a website within an Alibaba Cloud account. This is essential for monitoring and managing your log delivery capacity to ensure that logs can be delivered to the destination and prevent data loss or latency caused by insufficient quota.
        *Take note of the following parameters:**\
        ``
        `BusinessType` is required. You must specify a log category to obtain the corresponding quota information.
        `SiteId` specifies the ID of a website, which must be a valid integer that corresponds to a website that you configured on Alibaba Cloud.
        *Response:**\
        If a request is successful, the system returns the remaining log delivery quota (`FreeQuota`), request ID (`RequestId`), website ID (`SiteId`), and log category (`BusinessType`). You can confirm and record the returned data.
        
        @param request: GetSiteLogDeliveryQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteLogDeliveryQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteLogDeliveryQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteLogDeliveryQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site_log_delivery_quota(
        self,
        request: esa20240910_models.GetSiteLogDeliveryQuotaRequest,
    ) -> esa20240910_models.GetSiteLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining quota for delivering a specific category of real-time logs in a website.
        
        @description You can call this operation to query the remaining quota for delivering a specific category of real-time logs in a website within an Alibaba Cloud account. This is essential for monitoring and managing your log delivery capacity to ensure that logs can be delivered to the destination and prevent data loss or latency caused by insufficient quota.
        *Take note of the following parameters:**\
        ``
        `BusinessType` is required. You must specify a log category to obtain the corresponding quota information.
        `SiteId` specifies the ID of a website, which must be a valid integer that corresponds to a website that you configured on Alibaba Cloud.
        *Response:**\
        If a request is successful, the system returns the remaining log delivery quota (`FreeQuota`), request ID (`RequestId`), website ID (`SiteId`), and log category (`BusinessType`). You can confirm and record the returned data.
        
        @param request: GetSiteLogDeliveryQuotaRequest
        @return: GetSiteLogDeliveryQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_log_delivery_quota_with_options(request, runtime)

    async def get_site_log_delivery_quota_async(
        self,
        request: esa20240910_models.GetSiteLogDeliveryQuotaRequest,
    ) -> esa20240910_models.GetSiteLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining quota for delivering a specific category of real-time logs in a website.
        
        @description You can call this operation to query the remaining quota for delivering a specific category of real-time logs in a website within an Alibaba Cloud account. This is essential for monitoring and managing your log delivery capacity to ensure that logs can be delivered to the destination and prevent data loss or latency caused by insufficient quota.
        *Take note of the following parameters:**\
        ``
        `BusinessType` is required. You must specify a log category to obtain the corresponding quota information.
        `SiteId` specifies the ID of a website, which must be a valid integer that corresponds to a website that you configured on Alibaba Cloud.
        *Response:**\
        If a request is successful, the system returns the remaining log delivery quota (`FreeQuota`), request ID (`RequestId`), website ID (`SiteId`), and log category (`BusinessType`). You can confirm and record the returned data.
        
        @param request: GetSiteLogDeliveryQuotaRequest
        @return: GetSiteLogDeliveryQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_log_delivery_quota_with_options_async(request, runtime)

    def get_site_waf_settings_with_options(
        self,
        request: esa20240910_models.GetSiteWafSettingsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteWafSettingsResponse:
        """
        @summary Queries the Web Application Firewall (WAF) configurations of a website.
        
        @param request: GetSiteWafSettingsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteWafSettingsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.path):
            query['Path'] = request.path
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteWafSettings',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteWafSettingsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_site_waf_settings_with_options_async(
        self,
        request: esa20240910_models.GetSiteWafSettingsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetSiteWafSettingsResponse:
        """
        @summary Queries the Web Application Firewall (WAF) configurations of a website.
        
        @param request: GetSiteWafSettingsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetSiteWafSettingsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.path):
            query['Path'] = request.path
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetSiteWafSettings',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetSiteWafSettingsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_site_waf_settings(
        self,
        request: esa20240910_models.GetSiteWafSettingsRequest,
    ) -> esa20240910_models.GetSiteWafSettingsResponse:
        """
        @summary Queries the Web Application Firewall (WAF) configurations of a website.
        
        @param request: GetSiteWafSettingsRequest
        @return: GetSiteWafSettingsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_site_waf_settings_with_options(request, runtime)

    async def get_site_waf_settings_async(
        self,
        request: esa20240910_models.GetSiteWafSettingsRequest,
    ) -> esa20240910_models.GetSiteWafSettingsResponse:
        """
        @summary Queries the Web Application Firewall (WAF) configurations of a website.
        
        @param request: GetSiteWafSettingsRequest
        @return: GetSiteWafSettingsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_site_waf_settings_with_options_async(request, runtime)

    def get_upload_task_with_options(
        self,
        request: esa20240910_models.GetUploadTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUploadTaskResponse:
        """
        @summary Queries the execution status and running information of a file upload task based on the task ID.
        
        @param request: GetUploadTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUploadTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUploadTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUploadTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_upload_task_with_options_async(
        self,
        request: esa20240910_models.GetUploadTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUploadTaskResponse:
        """
        @summary Queries the execution status and running information of a file upload task based on the task ID.
        
        @param request: GetUploadTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUploadTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUploadTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUploadTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_upload_task(
        self,
        request: esa20240910_models.GetUploadTaskRequest,
    ) -> esa20240910_models.GetUploadTaskResponse:
        """
        @summary Queries the execution status and running information of a file upload task based on the task ID.
        
        @param request: GetUploadTaskRequest
        @return: GetUploadTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_upload_task_with_options(request, runtime)

    async def get_upload_task_async(
        self,
        request: esa20240910_models.GetUploadTaskRequest,
    ) -> esa20240910_models.GetUploadTaskResponse:
        """
        @summary Queries the execution status and running information of a file upload task based on the task ID.
        
        @param request: GetUploadTaskRequest
        @return: GetUploadTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_upload_task_with_options_async(request, runtime)

    def get_user_delivery_task_with_options(
        self,
        request: esa20240910_models.GetUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUserDeliveryTaskResponse:
        """
        @summary Queries the information about a log delivery task by account.
        
        @description    This API operation queries the details of a delivery task, including the task name, discard rate, region, log category, status, delivery destination, configuration, and filtering rules.****\
        You can call this operation to query detailed information about a log delivery task to analyze log processing efficiency or troubleshoot delivery problems.****\
        ****````
        
        @param request: GetUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUserDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_user_delivery_task_with_options_async(
        self,
        request: esa20240910_models.GetUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUserDeliveryTaskResponse:
        """
        @summary Queries the information about a log delivery task by account.
        
        @description    This API operation queries the details of a delivery task, including the task name, discard rate, region, log category, status, delivery destination, configuration, and filtering rules.****\
        You can call this operation to query detailed information about a log delivery task to analyze log processing efficiency or troubleshoot delivery problems.****\
        ****````
        
        @param request: GetUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUserDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_user_delivery_task(
        self,
        request: esa20240910_models.GetUserDeliveryTaskRequest,
    ) -> esa20240910_models.GetUserDeliveryTaskResponse:
        """
        @summary Queries the information about a log delivery task by account.
        
        @description    This API operation queries the details of a delivery task, including the task name, discard rate, region, log category, status, delivery destination, configuration, and filtering rules.****\
        You can call this operation to query detailed information about a log delivery task to analyze log processing efficiency or troubleshoot delivery problems.****\
        ****````
        
        @param request: GetUserDeliveryTaskRequest
        @return: GetUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_user_delivery_task_with_options(request, runtime)

    async def get_user_delivery_task_async(
        self,
        request: esa20240910_models.GetUserDeliveryTaskRequest,
    ) -> esa20240910_models.GetUserDeliveryTaskResponse:
        """
        @summary Queries the information about a log delivery task by account.
        
        @description    This API operation queries the details of a delivery task, including the task name, discard rate, region, log category, status, delivery destination, configuration, and filtering rules.****\
        You can call this operation to query detailed information about a log delivery task to analyze log processing efficiency or troubleshoot delivery problems.****\
        ****````
        
        @param request: GetUserDeliveryTaskRequest
        @return: GetUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_user_delivery_task_with_options_async(request, runtime)

    def get_user_log_delivery_quota_with_options(
        self,
        request: esa20240910_models.GetUserLogDeliveryQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUserLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining log delivery quota of each log category in your account.
        
        @description This operation allows you to query the remaining real-time log delivery quota of each log category in your Alibaba Cloud account. You must provide your Alibaba Cloud account ID (aliUid) and log category (BusinessType). The system then returns the remaining quota of the log category to help you track the usage.
        
        @param request: GetUserLogDeliveryQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUserLogDeliveryQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserLogDeliveryQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUserLogDeliveryQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_user_log_delivery_quota_with_options_async(
        self,
        request: esa20240910_models.GetUserLogDeliveryQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetUserLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining log delivery quota of each log category in your account.
        
        @description This operation allows you to query the remaining real-time log delivery quota of each log category in your Alibaba Cloud account. You must provide your Alibaba Cloud account ID (aliUid) and log category (BusinessType). The system then returns the remaining quota of the log category to help you track the usage.
        
        @param request: GetUserLogDeliveryQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUserLogDeliveryQuotaResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUserLogDeliveryQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetUserLogDeliveryQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_user_log_delivery_quota(
        self,
        request: esa20240910_models.GetUserLogDeliveryQuotaRequest,
    ) -> esa20240910_models.GetUserLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining log delivery quota of each log category in your account.
        
        @description This operation allows you to query the remaining real-time log delivery quota of each log category in your Alibaba Cloud account. You must provide your Alibaba Cloud account ID (aliUid) and log category (BusinessType). The system then returns the remaining quota of the log category to help you track the usage.
        
        @param request: GetUserLogDeliveryQuotaRequest
        @return: GetUserLogDeliveryQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_user_log_delivery_quota_with_options(request, runtime)

    async def get_user_log_delivery_quota_async(
        self,
        request: esa20240910_models.GetUserLogDeliveryQuotaRequest,
    ) -> esa20240910_models.GetUserLogDeliveryQuotaResponse:
        """
        @summary Queries the remaining log delivery quota of each log category in your account.
        
        @description This operation allows you to query the remaining real-time log delivery quota of each log category in your Alibaba Cloud account. You must provide your Alibaba Cloud account ID (aliUid) and log category (BusinessType). The system then returns the remaining quota of the log category to help you track the usage.
        
        @param request: GetUserLogDeliveryQuotaRequest
        @return: GetUserLogDeliveryQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_user_log_delivery_quota_with_options_async(request, runtime)

    def get_waf_bot_app_key_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafBotAppKeyResponse:
        """
        @summary Queries the application key (AppKey) that is used for authentication and data exchange in bot behavior detection in Web Application Firewall (WAF).
        
        @param request: GetWafBotAppKeyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafBotAppKeyResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetWafBotAppKey',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafBotAppKeyResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_waf_bot_app_key_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafBotAppKeyResponse:
        """
        @summary Queries the application key (AppKey) that is used for authentication and data exchange in bot behavior detection in Web Application Firewall (WAF).
        
        @param request: GetWafBotAppKeyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafBotAppKeyResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetWafBotAppKey',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafBotAppKeyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_waf_bot_app_key(self) -> esa20240910_models.GetWafBotAppKeyResponse:
        """
        @summary Queries the application key (AppKey) that is used for authentication and data exchange in bot behavior detection in Web Application Firewall (WAF).
        
        @return: GetWafBotAppKeyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_waf_bot_app_key_with_options(runtime)

    async def get_waf_bot_app_key_async(self) -> esa20240910_models.GetWafBotAppKeyResponse:
        """
        @summary Queries the application key (AppKey) that is used for authentication and data exchange in bot behavior detection in Web Application Firewall (WAF).
        
        @return: GetWafBotAppKeyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_waf_bot_app_key_with_options_async(runtime)

    def get_waf_filter_with_options(
        self,
        request: esa20240910_models.GetWafFilterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafFilterResponse:
        """
        @summary Queries the conditions for matching incoming requests that are configured in a WAF rule category for a website. These conditions define how WAF detects and processes different types of requests.
        
        @param request: GetWafFilterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafFilterResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.target):
            query['Target'] = request.target
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafFilter',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafFilterResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_waf_filter_with_options_async(
        self,
        request: esa20240910_models.GetWafFilterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafFilterResponse:
        """
        @summary Queries the conditions for matching incoming requests that are configured in a WAF rule category for a website. These conditions define how WAF detects and processes different types of requests.
        
        @param request: GetWafFilterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafFilterResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.target):
            query['Target'] = request.target
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafFilter',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafFilterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_waf_filter(
        self,
        request: esa20240910_models.GetWafFilterRequest,
    ) -> esa20240910_models.GetWafFilterResponse:
        """
        @summary Queries the conditions for matching incoming requests that are configured in a WAF rule category for a website. These conditions define how WAF detects and processes different types of requests.
        
        @param request: GetWafFilterRequest
        @return: GetWafFilterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_waf_filter_with_options(request, runtime)

    async def get_waf_filter_async(
        self,
        request: esa20240910_models.GetWafFilterRequest,
    ) -> esa20240910_models.GetWafFilterResponse:
        """
        @summary Queries the conditions for matching incoming requests that are configured in a WAF rule category for a website. These conditions define how WAF detects and processes different types of requests.
        
        @param request: GetWafFilterRequest
        @return: GetWafFilterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_waf_filter_with_options_async(request, runtime)

    def get_waf_quota_with_options(
        self,
        request: esa20240910_models.GetWafQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafQuotaResponse:
        """
        @summary Queries the quotas of Web Application Firewall (WAF) resources, such as managed rule groups, custom lists, custom error pages, and scenario-specific policies.
        
        @param request: GetWafQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafQuotaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.paths):
            query['Paths'] = request.paths
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_waf_quota_with_options_async(
        self,
        request: esa20240910_models.GetWafQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafQuotaResponse:
        """
        @summary Queries the quotas of Web Application Firewall (WAF) resources, such as managed rule groups, custom lists, custom error pages, and scenario-specific policies.
        
        @param request: GetWafQuotaRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafQuotaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.paths):
            query['Paths'] = request.paths
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafQuota',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_waf_quota(
        self,
        request: esa20240910_models.GetWafQuotaRequest,
    ) -> esa20240910_models.GetWafQuotaResponse:
        """
        @summary Queries the quotas of Web Application Firewall (WAF) resources, such as managed rule groups, custom lists, custom error pages, and scenario-specific policies.
        
        @param request: GetWafQuotaRequest
        @return: GetWafQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_waf_quota_with_options(request, runtime)

    async def get_waf_quota_async(
        self,
        request: esa20240910_models.GetWafQuotaRequest,
    ) -> esa20240910_models.GetWafQuotaResponse:
        """
        @summary Queries the quotas of Web Application Firewall (WAF) resources, such as managed rule groups, custom lists, custom error pages, and scenario-specific policies.
        
        @param request: GetWafQuotaRequest
        @return: GetWafQuotaResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_waf_quota_with_options_async(request, runtime)

    def get_waf_rule_with_options(
        self,
        request: esa20240910_models.GetWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafRuleResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) rule, such as its configuration and status.
        
        @param request: GetWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_waf_rule_with_options_async(
        self,
        request: esa20240910_models.GetWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafRuleResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) rule, such as its configuration and status.
        
        @param request: GetWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_waf_rule(
        self,
        request: esa20240910_models.GetWafRuleRequest,
    ) -> esa20240910_models.GetWafRuleResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) rule, such as its configuration and status.
        
        @param request: GetWafRuleRequest
        @return: GetWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_waf_rule_with_options(request, runtime)

    async def get_waf_rule_async(
        self,
        request: esa20240910_models.GetWafRuleRequest,
    ) -> esa20240910_models.GetWafRuleResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) rule, such as its configuration and status.
        
        @param request: GetWafRuleRequest
        @return: GetWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_waf_rule_with_options_async(request, runtime)

    def get_waf_ruleset_with_options(
        self,
        request: esa20240910_models.GetWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafRulesetResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) ruleset, such as the configuration and status.
        
        @param request: GetWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafRulesetResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_waf_ruleset_with_options_async(
        self,
        request: esa20240910_models.GetWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.GetWafRulesetResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) ruleset, such as the configuration and status.
        
        @param request: GetWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.GetWafRulesetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_waf_ruleset(
        self,
        request: esa20240910_models.GetWafRulesetRequest,
    ) -> esa20240910_models.GetWafRulesetResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) ruleset, such as the configuration and status.
        
        @param request: GetWafRulesetRequest
        @return: GetWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_waf_ruleset_with_options(request, runtime)

    async def get_waf_ruleset_async(
        self,
        request: esa20240910_models.GetWafRulesetRequest,
    ) -> esa20240910_models.GetWafRulesetResponse:
        """
        @summary Queries the details of a Web Application Firewall (WAF) ruleset, such as the configuration and status.
        
        @param request: GetWafRulesetRequest
        @return: GetWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_waf_ruleset_with_options_async(request, runtime)

    def list_cache_reserve_instances_with_options(
        self,
        request: esa20240910_models.ListCacheReserveInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListCacheReserveInstancesResponse:
        """
        @summary Queries the cache reserve instances in your Alibaba Cloud account.
        
        @param request: ListCacheReserveInstancesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCacheReserveInstancesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCacheReserveInstances',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListCacheReserveInstancesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cache_reserve_instances_with_options_async(
        self,
        request: esa20240910_models.ListCacheReserveInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListCacheReserveInstancesResponse:
        """
        @summary Queries the cache reserve instances in your Alibaba Cloud account.
        
        @param request: ListCacheReserveInstancesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCacheReserveInstancesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCacheReserveInstances',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListCacheReserveInstancesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cache_reserve_instances(
        self,
        request: esa20240910_models.ListCacheReserveInstancesRequest,
    ) -> esa20240910_models.ListCacheReserveInstancesResponse:
        """
        @summary Queries the cache reserve instances in your Alibaba Cloud account.
        
        @param request: ListCacheReserveInstancesRequest
        @return: ListCacheReserveInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_cache_reserve_instances_with_options(request, runtime)

    async def list_cache_reserve_instances_async(
        self,
        request: esa20240910_models.ListCacheReserveInstancesRequest,
    ) -> esa20240910_models.ListCacheReserveInstancesResponse:
        """
        @summary Queries the cache reserve instances in your Alibaba Cloud account.
        
        @param request: ListCacheReserveInstancesRequest
        @return: ListCacheReserveInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_cache_reserve_instances_with_options_async(request, runtime)

    def list_ciphers_with_options(
        self,
        request: esa20240910_models.ListCiphersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListCiphersResponse:
        """
        @summary 查询TLS密码套件列表
        
        @param request: ListCiphersRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCiphersResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCiphers',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListCiphersResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_ciphers_with_options_async(
        self,
        request: esa20240910_models.ListCiphersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListCiphersResponse:
        """
        @summary 查询TLS密码套件列表
        
        @param request: ListCiphersRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListCiphersResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListCiphers',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListCiphersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_ciphers(
        self,
        request: esa20240910_models.ListCiphersRequest,
    ) -> esa20240910_models.ListCiphersResponse:
        """
        @summary 查询TLS密码套件列表
        
        @param request: ListCiphersRequest
        @return: ListCiphersResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_ciphers_with_options(request, runtime)

    async def list_ciphers_async(
        self,
        request: esa20240910_models.ListCiphersRequest,
    ) -> esa20240910_models.ListCiphersResponse:
        """
        @summary 查询TLS密码套件列表
        
        @param request: ListCiphersRequest
        @return: ListCiphersResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_ciphers_with_options_async(request, runtime)

    def list_client_ca_certificates_with_options(
        self,
        request: esa20240910_models.ListClientCaCertificatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListClientCaCertificatesResponse:
        """
        @summary Queries a list of client certificate authority (CA) certificates for a website.
        
        @param request: ListClientCaCertificatesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListClientCaCertificatesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClientCaCertificates',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListClientCaCertificatesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_client_ca_certificates_with_options_async(
        self,
        request: esa20240910_models.ListClientCaCertificatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListClientCaCertificatesResponse:
        """
        @summary Queries a list of client certificate authority (CA) certificates for a website.
        
        @param request: ListClientCaCertificatesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListClientCaCertificatesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClientCaCertificates',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListClientCaCertificatesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_client_ca_certificates(
        self,
        request: esa20240910_models.ListClientCaCertificatesRequest,
    ) -> esa20240910_models.ListClientCaCertificatesResponse:
        """
        @summary Queries a list of client certificate authority (CA) certificates for a website.
        
        @param request: ListClientCaCertificatesRequest
        @return: ListClientCaCertificatesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_client_ca_certificates_with_options(request, runtime)

    async def list_client_ca_certificates_async(
        self,
        request: esa20240910_models.ListClientCaCertificatesRequest,
    ) -> esa20240910_models.ListClientCaCertificatesResponse:
        """
        @summary Queries a list of client certificate authority (CA) certificates for a website.
        
        @param request: ListClientCaCertificatesRequest
        @return: ListClientCaCertificatesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_client_ca_certificates_with_options_async(request, runtime)

    def list_client_certificates_with_options(
        self,
        request: esa20240910_models.ListClientCertificatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListClientCertificatesResponse:
        """
        @summary Queries client certificates configured for a website.
        
        @param request: ListClientCertificatesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListClientCertificatesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClientCertificates',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListClientCertificatesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_client_certificates_with_options_async(
        self,
        request: esa20240910_models.ListClientCertificatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListClientCertificatesResponse:
        """
        @summary Queries client certificates configured for a website.
        
        @param request: ListClientCertificatesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListClientCertificatesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClientCertificates',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListClientCertificatesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_client_certificates(
        self,
        request: esa20240910_models.ListClientCertificatesRequest,
    ) -> esa20240910_models.ListClientCertificatesResponse:
        """
        @summary Queries client certificates configured for a website.
        
        @param request: ListClientCertificatesRequest
        @return: ListClientCertificatesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_client_certificates_with_options(request, runtime)

    async def list_client_certificates_async(
        self,
        request: esa20240910_models.ListClientCertificatesRequest,
    ) -> esa20240910_models.ListClientCertificatesResponse:
        """
        @summary Queries client certificates configured for a website.
        
        @param request: ListClientCertificatesRequest
        @return: ListClientCertificatesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_client_certificates_with_options_async(request, runtime)

    def list_edge_container_app_records_with_options(
        self,
        request: esa20240910_models.ListEdgeContainerAppRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppRecordsResponse:
        """
        @summary Lists domain names that are associated with a containerized application.
        
        @param request: ListEdgeContainerAppRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerAppRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_container_app_records_with_options_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppRecordsResponse:
        """
        @summary Lists domain names that are associated with a containerized application.
        
        @param request: ListEdgeContainerAppRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerAppRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_container_app_records(
        self,
        request: esa20240910_models.ListEdgeContainerAppRecordsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppRecordsResponse:
        """
        @summary Lists domain names that are associated with a containerized application.
        
        @param request: ListEdgeContainerAppRecordsRequest
        @return: ListEdgeContainerAppRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_container_app_records_with_options(request, runtime)

    async def list_edge_container_app_records_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppRecordsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppRecordsResponse:
        """
        @summary Lists domain names that are associated with a containerized application.
        
        @param request: ListEdgeContainerAppRecordsRequest
        @return: ListEdgeContainerAppRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_container_app_records_with_options_async(request, runtime)

    def list_edge_container_app_versions_with_options(
        self,
        request: esa20240910_models.ListEdgeContainerAppVersionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppVersionsResponse:
        """
        @summary Lists versions of all containerized applications.
        
        @param request: ListEdgeContainerAppVersionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppVersionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerAppVersions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppVersionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_container_app_versions_with_options_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppVersionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppVersionsResponse:
        """
        @summary Lists versions of all containerized applications.
        
        @param request: ListEdgeContainerAppVersionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppVersionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerAppVersions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppVersionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_container_app_versions(
        self,
        request: esa20240910_models.ListEdgeContainerAppVersionsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppVersionsResponse:
        """
        @summary Lists versions of all containerized applications.
        
        @param request: ListEdgeContainerAppVersionsRequest
        @return: ListEdgeContainerAppVersionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_container_app_versions_with_options(request, runtime)

    async def list_edge_container_app_versions_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppVersionsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppVersionsResponse:
        """
        @summary Lists versions of all containerized applications.
        
        @param request: ListEdgeContainerAppVersionsRequest
        @return: ListEdgeContainerAppVersionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_container_app_versions_with_options_async(request, runtime)

    def list_edge_container_apps_with_options(
        self,
        request: esa20240910_models.ListEdgeContainerAppsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppsResponse:
        """
        @summary Queries all containerized applications in your Alibaba Cloud account.
        
        @param request: ListEdgeContainerAppsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_key):
            query['OrderKey'] = request.order_key
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_key):
            query['SearchKey'] = request.search_key
        if not UtilClient.is_unset(request.search_type):
            query['SearchType'] = request.search_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerApps',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_container_apps_with_options_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerAppsResponse:
        """
        @summary Queries all containerized applications in your Alibaba Cloud account.
        
        @param request: ListEdgeContainerAppsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerAppsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_key):
            query['OrderKey'] = request.order_key
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_key):
            query['SearchKey'] = request.search_key
        if not UtilClient.is_unset(request.search_type):
            query['SearchType'] = request.search_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerApps',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerAppsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_container_apps(
        self,
        request: esa20240910_models.ListEdgeContainerAppsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppsResponse:
        """
        @summary Queries all containerized applications in your Alibaba Cloud account.
        
        @param request: ListEdgeContainerAppsRequest
        @return: ListEdgeContainerAppsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_container_apps_with_options(request, runtime)

    async def list_edge_container_apps_async(
        self,
        request: esa20240910_models.ListEdgeContainerAppsRequest,
    ) -> esa20240910_models.ListEdgeContainerAppsResponse:
        """
        @summary Queries all containerized applications in your Alibaba Cloud account.
        
        @param request: ListEdgeContainerAppsRequest
        @return: ListEdgeContainerAppsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_container_apps_with_options_async(request, runtime)

    def list_edge_container_records_with_options(
        self,
        request: esa20240910_models.ListEdgeContainerRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Container for a website.
        
        @param request: ListEdgeContainerRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_container_records_with_options_async(
        self,
        request: esa20240910_models.ListEdgeContainerRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeContainerRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Container for a website.
        
        @param request: ListEdgeContainerRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeContainerRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeContainerRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeContainerRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_container_records(
        self,
        request: esa20240910_models.ListEdgeContainerRecordsRequest,
    ) -> esa20240910_models.ListEdgeContainerRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Container for a website.
        
        @param request: ListEdgeContainerRecordsRequest
        @return: ListEdgeContainerRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_container_records_with_options(request, runtime)

    async def list_edge_container_records_async(
        self,
        request: esa20240910_models.ListEdgeContainerRecordsRequest,
    ) -> esa20240910_models.ListEdgeContainerRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Container for a website.
        
        @param request: ListEdgeContainerRecordsRequest
        @return: ListEdgeContainerRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_container_records_with_options_async(request, runtime)

    def list_edge_routine_plans_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeRoutinePlansResponse:
        """
        @summary Queries Edge Routine plans.
        
        @param request: ListEdgeRoutinePlansRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeRoutinePlansResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListEdgeRoutinePlans',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeRoutinePlansResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_routine_plans_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeRoutinePlansResponse:
        """
        @summary Queries Edge Routine plans.
        
        @param request: ListEdgeRoutinePlansRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeRoutinePlansResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListEdgeRoutinePlans',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeRoutinePlansResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_routine_plans(self) -> esa20240910_models.ListEdgeRoutinePlansResponse:
        """
        @summary Queries Edge Routine plans.
        
        @return: ListEdgeRoutinePlansResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_routine_plans_with_options(runtime)

    async def list_edge_routine_plans_async(self) -> esa20240910_models.ListEdgeRoutinePlansResponse:
        """
        @summary Queries Edge Routine plans.
        
        @return: ListEdgeRoutinePlansResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_routine_plans_with_options_async(runtime)

    def list_edge_routine_records_with_options(
        self,
        request: esa20240910_models.ListEdgeRoutineRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeRoutineRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Routine routes for a website.
        
        @description >  You can call this operation 100 times per second.
        
        @param request: ListEdgeRoutineRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeRoutineRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeRoutineRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeRoutineRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_edge_routine_records_with_options_async(
        self,
        request: esa20240910_models.ListEdgeRoutineRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListEdgeRoutineRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Routine routes for a website.
        
        @description >  You can call this operation 100 times per second.
        
        @param request: ListEdgeRoutineRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListEdgeRoutineRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEdgeRoutineRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListEdgeRoutineRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_edge_routine_records(
        self,
        request: esa20240910_models.ListEdgeRoutineRecordsRequest,
    ) -> esa20240910_models.ListEdgeRoutineRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Routine routes for a website.
        
        @description >  You can call this operation 100 times per second.
        
        @param request: ListEdgeRoutineRecordsRequest
        @return: ListEdgeRoutineRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_edge_routine_records_with_options(request, runtime)

    async def list_edge_routine_records_async(
        self,
        request: esa20240910_models.ListEdgeRoutineRecordsRequest,
    ) -> esa20240910_models.ListEdgeRoutineRecordsResponse:
        """
        @summary Queries the records that are associated with Edge Routine routes for a website.
        
        @description >  You can call this operation 100 times per second.
        
        @param request: ListEdgeRoutineRecordsRequest
        @return: ListEdgeRoutineRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_edge_routine_records_with_options_async(request, runtime)

    def list_instance_quotas_with_options(
        self,
        request: esa20240910_models.ListInstanceQuotasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListInstanceQuotasResponse:
        """
        @summary Queries the quota details in a subscription plan.
        
        @param request: ListInstanceQuotasRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstanceQuotasResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceQuotas',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListInstanceQuotasResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_instance_quotas_with_options_async(
        self,
        request: esa20240910_models.ListInstanceQuotasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListInstanceQuotasResponse:
        """
        @summary Queries the quota details in a subscription plan.
        
        @param request: ListInstanceQuotasRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstanceQuotasResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceQuotas',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListInstanceQuotasResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_instance_quotas(
        self,
        request: esa20240910_models.ListInstanceQuotasRequest,
    ) -> esa20240910_models.ListInstanceQuotasResponse:
        """
        @summary Queries the quota details in a subscription plan.
        
        @param request: ListInstanceQuotasRequest
        @return: ListInstanceQuotasResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_instance_quotas_with_options(request, runtime)

    async def list_instance_quotas_async(
        self,
        request: esa20240910_models.ListInstanceQuotasRequest,
    ) -> esa20240910_models.ListInstanceQuotasResponse:
        """
        @summary Queries the quota details in a subscription plan.
        
        @param request: ListInstanceQuotasRequest
        @return: ListInstanceQuotasResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_instance_quotas_with_options_async(request, runtime)

    def list_instance_quotas_with_usage_with_options(
        self,
        request: esa20240910_models.ListInstanceQuotasWithUsageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListInstanceQuotasWithUsageResponse:
        """
        @summary Queries quotas and the actual usage in a plan based on the website or plan ID.
        
        @param request: ListInstanceQuotasWithUsageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstanceQuotasWithUsageResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceQuotasWithUsage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListInstanceQuotasWithUsageResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_instance_quotas_with_usage_with_options_async(
        self,
        request: esa20240910_models.ListInstanceQuotasWithUsageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListInstanceQuotasWithUsageResponse:
        """
        @summary Queries quotas and the actual usage in a plan based on the website or plan ID.
        
        @param request: ListInstanceQuotasWithUsageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstanceQuotasWithUsageResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstanceQuotasWithUsage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListInstanceQuotasWithUsageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_instance_quotas_with_usage(
        self,
        request: esa20240910_models.ListInstanceQuotasWithUsageRequest,
    ) -> esa20240910_models.ListInstanceQuotasWithUsageResponse:
        """
        @summary Queries quotas and the actual usage in a plan based on the website or plan ID.
        
        @param request: ListInstanceQuotasWithUsageRequest
        @return: ListInstanceQuotasWithUsageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_instance_quotas_with_usage_with_options(request, runtime)

    async def list_instance_quotas_with_usage_async(
        self,
        request: esa20240910_models.ListInstanceQuotasWithUsageRequest,
    ) -> esa20240910_models.ListInstanceQuotasWithUsageResponse:
        """
        @summary Queries quotas and the actual usage in a plan based on the website or plan ID.
        
        @param request: ListInstanceQuotasWithUsageRequest
        @return: ListInstanceQuotasWithUsageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_instance_quotas_with_usage_with_options_async(request, runtime)

    def list_kvs_with_options(
        self,
        request: esa20240910_models.ListKvsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListKvsResponse:
        """
        @summary Lists all key-value pairs in a namespace in your Alibaba Cloud account.
        
        @param request: ListKvsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListKvsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListKvs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListKvsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_kvs_with_options_async(
        self,
        request: esa20240910_models.ListKvsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListKvsResponse:
        """
        @summary Lists all key-value pairs in a namespace in your Alibaba Cloud account.
        
        @param request: ListKvsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListKvsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListKvs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListKvsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_kvs(
        self,
        request: esa20240910_models.ListKvsRequest,
    ) -> esa20240910_models.ListKvsResponse:
        """
        @summary Lists all key-value pairs in a namespace in your Alibaba Cloud account.
        
        @param request: ListKvsRequest
        @return: ListKvsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_kvs_with_options(request, runtime)

    async def list_kvs_async(
        self,
        request: esa20240910_models.ListKvsRequest,
    ) -> esa20240910_models.ListKvsResponse:
        """
        @summary Lists all key-value pairs in a namespace in your Alibaba Cloud account.
        
        @param request: ListKvsRequest
        @return: ListKvsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_kvs_with_options_async(request, runtime)

    def list_lists_with_options(
        self,
        tmp_req: esa20240910_models.ListListsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListListsResponse:
        """
        @summary Queries all custom lists and their details in an Alibaba Cloud account. You can specify query arguments to filter the results and display the returned lists by page.
        
        @param tmp_req: ListListsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListListsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListListsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLists',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListListsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_lists_with_options_async(
        self,
        tmp_req: esa20240910_models.ListListsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListListsResponse:
        """
        @summary Queries all custom lists and their details in an Alibaba Cloud account. You can specify query arguments to filter the results and display the returned lists by page.
        
        @param tmp_req: ListListsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListListsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListListsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLists',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListListsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_lists(
        self,
        request: esa20240910_models.ListListsRequest,
    ) -> esa20240910_models.ListListsResponse:
        """
        @summary Queries all custom lists and their details in an Alibaba Cloud account. You can specify query arguments to filter the results and display the returned lists by page.
        
        @param request: ListListsRequest
        @return: ListListsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_lists_with_options(request, runtime)

    async def list_lists_async(
        self,
        request: esa20240910_models.ListListsRequest,
    ) -> esa20240910_models.ListListsResponse:
        """
        @summary Queries all custom lists and their details in an Alibaba Cloud account. You can specify query arguments to filter the results and display the returned lists by page.
        
        @param request: ListListsRequest
        @return: ListListsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_lists_with_options_async(request, runtime)

    def list_load_balancer_regions_with_options(
        self,
        request: esa20240910_models.ListLoadBalancerRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListLoadBalancerRegionsResponse:
        """
        @summary Queries the information that can be used to configure a traffic steering policy based on the originating country or region for a load balancer, such as the code and code descriptions of the regions and subregions of the load balancer.
        
        @description When you call an operation to create a traffic steering policy based on the originating country or region for a load balancer, you can use the code of a region or subregion to specify traffic that is sent from the region or subregion.
        
        @param request: ListLoadBalancerRegionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListLoadBalancerRegionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLoadBalancerRegions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListLoadBalancerRegionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_load_balancer_regions_with_options_async(
        self,
        request: esa20240910_models.ListLoadBalancerRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListLoadBalancerRegionsResponse:
        """
        @summary Queries the information that can be used to configure a traffic steering policy based on the originating country or region for a load balancer, such as the code and code descriptions of the regions and subregions of the load balancer.
        
        @description When you call an operation to create a traffic steering policy based on the originating country or region for a load balancer, you can use the code of a region or subregion to specify traffic that is sent from the region or subregion.
        
        @param request: ListLoadBalancerRegionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListLoadBalancerRegionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLoadBalancerRegions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListLoadBalancerRegionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_load_balancer_regions(
        self,
        request: esa20240910_models.ListLoadBalancerRegionsRequest,
    ) -> esa20240910_models.ListLoadBalancerRegionsResponse:
        """
        @summary Queries the information that can be used to configure a traffic steering policy based on the originating country or region for a load balancer, such as the code and code descriptions of the regions and subregions of the load balancer.
        
        @description When you call an operation to create a traffic steering policy based on the originating country or region for a load balancer, you can use the code of a region or subregion to specify traffic that is sent from the region or subregion.
        
        @param request: ListLoadBalancerRegionsRequest
        @return: ListLoadBalancerRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_load_balancer_regions_with_options(request, runtime)

    async def list_load_balancer_regions_async(
        self,
        request: esa20240910_models.ListLoadBalancerRegionsRequest,
    ) -> esa20240910_models.ListLoadBalancerRegionsResponse:
        """
        @summary Queries the information that can be used to configure a traffic steering policy based on the originating country or region for a load balancer, such as the code and code descriptions of the regions and subregions of the load balancer.
        
        @description When you call an operation to create a traffic steering policy based on the originating country or region for a load balancer, you can use the code of a region or subregion to specify traffic that is sent from the region or subregion.
        
        @param request: ListLoadBalancerRegionsRequest
        @return: ListLoadBalancerRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_load_balancer_regions_with_options_async(request, runtime)

    def list_managed_rules_groups_with_options(
        self,
        request: esa20240910_models.ListManagedRulesGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListManagedRulesGroupsResponse:
        """
        @summary Queries all WAF managed rule groups in your Alibaba Cloud account.
        
        @param request: ListManagedRulesGroupsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListManagedRulesGroupsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListManagedRulesGroups',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListManagedRulesGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_managed_rules_groups_with_options_async(
        self,
        request: esa20240910_models.ListManagedRulesGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListManagedRulesGroupsResponse:
        """
        @summary Queries all WAF managed rule groups in your Alibaba Cloud account.
        
        @param request: ListManagedRulesGroupsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListManagedRulesGroupsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListManagedRulesGroups',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListManagedRulesGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_managed_rules_groups(
        self,
        request: esa20240910_models.ListManagedRulesGroupsRequest,
    ) -> esa20240910_models.ListManagedRulesGroupsResponse:
        """
        @summary Queries all WAF managed rule groups in your Alibaba Cloud account.
        
        @param request: ListManagedRulesGroupsRequest
        @return: ListManagedRulesGroupsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_managed_rules_groups_with_options(request, runtime)

    async def list_managed_rules_groups_async(
        self,
        request: esa20240910_models.ListManagedRulesGroupsRequest,
    ) -> esa20240910_models.ListManagedRulesGroupsResponse:
        """
        @summary Queries all WAF managed rule groups in your Alibaba Cloud account.
        
        @param request: ListManagedRulesGroupsRequest
        @return: ListManagedRulesGroupsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_managed_rules_groups_with_options_async(request, runtime)

    def list_pages_with_options(
        self,
        request: esa20240910_models.ListPagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListPagesResponse:
        """
        @summary Lists all custom error pages that you created. You can define the page number and the number of entries per page to display the response.
        
        @param request: ListPagesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListPagesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListPages',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListPagesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_pages_with_options_async(
        self,
        request: esa20240910_models.ListPagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListPagesResponse:
        """
        @summary Lists all custom error pages that you created. You can define the page number and the number of entries per page to display the response.
        
        @param request: ListPagesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListPagesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListPages',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListPagesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_pages(
        self,
        request: esa20240910_models.ListPagesRequest,
    ) -> esa20240910_models.ListPagesResponse:
        """
        @summary Lists all custom error pages that you created. You can define the page number and the number of entries per page to display the response.
        
        @param request: ListPagesRequest
        @return: ListPagesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_pages_with_options(request, runtime)

    async def list_pages_async(
        self,
        request: esa20240910_models.ListPagesRequest,
    ) -> esa20240910_models.ListPagesResponse:
        """
        @summary Lists all custom error pages that you created. You can define the page number and the number of entries per page to display the response.
        
        @param request: ListPagesRequest
        @return: ListPagesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_pages_with_options_async(request, runtime)

    def list_records_with_options(
        self,
        request: esa20240910_models.ListRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRecordsResponse:
        """
        @summary Queries a list of Domain Name System (DNS) records of a website, including the record value, priority, and authentication configurations. Supports filtering by specifying parameters such as RecordName and RecordMatchType.
        
        @description The DNS records related to Edge Container, Edge Routine, and TCP/UDP proxy are not returned in this operation.
        
        @param request: ListRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRecordsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_records_with_options_async(
        self,
        request: esa20240910_models.ListRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRecordsResponse:
        """
        @summary Queries a list of Domain Name System (DNS) records of a website, including the record value, priority, and authentication configurations. Supports filtering by specifying parameters such as RecordName and RecordMatchType.
        
        @description The DNS records related to Edge Container, Edge Routine, and TCP/UDP proxy are not returned in this operation.
        
        @param request: ListRecordsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRecordsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListRecords',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRecordsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_records(
        self,
        request: esa20240910_models.ListRecordsRequest,
    ) -> esa20240910_models.ListRecordsResponse:
        """
        @summary Queries a list of Domain Name System (DNS) records of a website, including the record value, priority, and authentication configurations. Supports filtering by specifying parameters such as RecordName and RecordMatchType.
        
        @description The DNS records related to Edge Container, Edge Routine, and TCP/UDP proxy are not returned in this operation.
        
        @param request: ListRecordsRequest
        @return: ListRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_records_with_options(request, runtime)

    async def list_records_async(
        self,
        request: esa20240910_models.ListRecordsRequest,
    ) -> esa20240910_models.ListRecordsResponse:
        """
        @summary Queries a list of Domain Name System (DNS) records of a website, including the record value, priority, and authentication configurations. Supports filtering by specifying parameters such as RecordName and RecordMatchType.
        
        @description The DNS records related to Edge Container, Edge Routine, and TCP/UDP proxy are not returned in this operation.
        
        @param request: ListRecordsRequest
        @return: ListRecordsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_records_with_options_async(request, runtime)

    def list_routine_canary_areas_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRoutineCanaryAreasResponse:
        """
        @summary Lists the regions to which Edge Routine code can be released for canary deployment.
        
        @param request: ListRoutineCanaryAreasRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRoutineCanaryAreasResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListRoutineCanaryAreas',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRoutineCanaryAreasResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_routine_canary_areas_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRoutineCanaryAreasResponse:
        """
        @summary Lists the regions to which Edge Routine code can be released for canary deployment.
        
        @param request: ListRoutineCanaryAreasRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRoutineCanaryAreasResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListRoutineCanaryAreas',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRoutineCanaryAreasResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_routine_canary_areas(self) -> esa20240910_models.ListRoutineCanaryAreasResponse:
        """
        @summary Lists the regions to which Edge Routine code can be released for canary deployment.
        
        @return: ListRoutineCanaryAreasResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_routine_canary_areas_with_options(runtime)

    async def list_routine_canary_areas_async(self) -> esa20240910_models.ListRoutineCanaryAreasResponse:
        """
        @summary Lists the regions to which Edge Routine code can be released for canary deployment.
        
        @return: ListRoutineCanaryAreasResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_routine_canary_areas_with_options_async(runtime)

    def list_routine_optional_specs_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRoutineOptionalSpecsResponse:
        """
        @summary Queries the specifications that you can select for a routine based on the plan type. The response contains all specifications that you can select for a routine. The IsAvailable parameter indicates whether a specification is available.
        
        @description You can call this operation to query the specifications that you can select for a routine.
        
        @param request: ListRoutineOptionalSpecsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRoutineOptionalSpecsResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListRoutineOptionalSpecs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRoutineOptionalSpecsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_routine_optional_specs_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListRoutineOptionalSpecsResponse:
        """
        @summary Queries the specifications that you can select for a routine based on the plan type. The response contains all specifications that you can select for a routine. The IsAvailable parameter indicates whether a specification is available.
        
        @description You can call this operation to query the specifications that you can select for a routine.
        
        @param request: ListRoutineOptionalSpecsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRoutineOptionalSpecsResponse
        """
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='ListRoutineOptionalSpecs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListRoutineOptionalSpecsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_routine_optional_specs(self) -> esa20240910_models.ListRoutineOptionalSpecsResponse:
        """
        @summary Queries the specifications that you can select for a routine based on the plan type. The response contains all specifications that you can select for a routine. The IsAvailable parameter indicates whether a specification is available.
        
        @description You can call this operation to query the specifications that you can select for a routine.
        
        @return: ListRoutineOptionalSpecsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_routine_optional_specs_with_options(runtime)

    async def list_routine_optional_specs_async(self) -> esa20240910_models.ListRoutineOptionalSpecsResponse:
        """
        @summary Queries the specifications that you can select for a routine based on the plan type. The response contains all specifications that you can select for a routine. The IsAvailable parameter indicates whether a specification is available.
        
        @description You can call this operation to query the specifications that you can select for a routine.
        
        @return: ListRoutineOptionalSpecsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_routine_optional_specs_with_options_async(runtime)

    def list_scheduled_preload_executions_with_options(
        self,
        request: esa20240910_models.ListScheduledPreloadExecutionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListScheduledPreloadExecutionsResponse:
        """
        @summary Lists the plans in a scheduled prefetch task by task ID.
        
        @param request: ListScheduledPreloadExecutionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListScheduledPreloadExecutionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScheduledPreloadExecutions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListScheduledPreloadExecutionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_scheduled_preload_executions_with_options_async(
        self,
        request: esa20240910_models.ListScheduledPreloadExecutionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListScheduledPreloadExecutionsResponse:
        """
        @summary Lists the plans in a scheduled prefetch task by task ID.
        
        @param request: ListScheduledPreloadExecutionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListScheduledPreloadExecutionsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScheduledPreloadExecutions',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListScheduledPreloadExecutionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_scheduled_preload_executions(
        self,
        request: esa20240910_models.ListScheduledPreloadExecutionsRequest,
    ) -> esa20240910_models.ListScheduledPreloadExecutionsResponse:
        """
        @summary Lists the plans in a scheduled prefetch task by task ID.
        
        @param request: ListScheduledPreloadExecutionsRequest
        @return: ListScheduledPreloadExecutionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_scheduled_preload_executions_with_options(request, runtime)

    async def list_scheduled_preload_executions_async(
        self,
        request: esa20240910_models.ListScheduledPreloadExecutionsRequest,
    ) -> esa20240910_models.ListScheduledPreloadExecutionsResponse:
        """
        @summary Lists the plans in a scheduled prefetch task by task ID.
        
        @param request: ListScheduledPreloadExecutionsRequest
        @return: ListScheduledPreloadExecutionsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_scheduled_preload_executions_with_options_async(request, runtime)

    def list_scheduled_preload_jobs_with_options(
        self,
        request: esa20240910_models.ListScheduledPreloadJobsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListScheduledPreloadJobsResponse:
        """
        @summary Queries the scheduled prefetch tasks for a website.
        
        @param request: ListScheduledPreloadJobsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListScheduledPreloadJobsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScheduledPreloadJobs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListScheduledPreloadJobsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_scheduled_preload_jobs_with_options_async(
        self,
        request: esa20240910_models.ListScheduledPreloadJobsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListScheduledPreloadJobsResponse:
        """
        @summary Queries the scheduled prefetch tasks for a website.
        
        @param request: ListScheduledPreloadJobsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListScheduledPreloadJobsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScheduledPreloadJobs',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListScheduledPreloadJobsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_scheduled_preload_jobs(
        self,
        request: esa20240910_models.ListScheduledPreloadJobsRequest,
    ) -> esa20240910_models.ListScheduledPreloadJobsResponse:
        """
        @summary Queries the scheduled prefetch tasks for a website.
        
        @param request: ListScheduledPreloadJobsRequest
        @return: ListScheduledPreloadJobsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_scheduled_preload_jobs_with_options(request, runtime)

    async def list_scheduled_preload_jobs_async(
        self,
        request: esa20240910_models.ListScheduledPreloadJobsRequest,
    ) -> esa20240910_models.ListScheduledPreloadJobsResponse:
        """
        @summary Queries the scheduled prefetch tasks for a website.
        
        @param request: ListScheduledPreloadJobsRequest
        @return: ListScheduledPreloadJobsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_scheduled_preload_jobs_with_options_async(request, runtime)

    def list_site_delivery_tasks_with_options(
        self,
        request: esa20240910_models.ListSiteDeliveryTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListSiteDeliveryTasksResponse:
        """
        @summary Lists all log delivery tasks that are in progress.
        
        @param request: ListSiteDeliveryTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListSiteDeliveryTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSiteDeliveryTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListSiteDeliveryTasksResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_site_delivery_tasks_with_options_async(
        self,
        request: esa20240910_models.ListSiteDeliveryTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListSiteDeliveryTasksResponse:
        """
        @summary Lists all log delivery tasks that are in progress.
        
        @param request: ListSiteDeliveryTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListSiteDeliveryTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSiteDeliveryTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListSiteDeliveryTasksResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_site_delivery_tasks(
        self,
        request: esa20240910_models.ListSiteDeliveryTasksRequest,
    ) -> esa20240910_models.ListSiteDeliveryTasksResponse:
        """
        @summary Lists all log delivery tasks that are in progress.
        
        @param request: ListSiteDeliveryTasksRequest
        @return: ListSiteDeliveryTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_site_delivery_tasks_with_options(request, runtime)

    async def list_site_delivery_tasks_async(
        self,
        request: esa20240910_models.ListSiteDeliveryTasksRequest,
    ) -> esa20240910_models.ListSiteDeliveryTasksResponse:
        """
        @summary Lists all log delivery tasks that are in progress.
        
        @param request: ListSiteDeliveryTasksRequest
        @return: ListSiteDeliveryTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_site_delivery_tasks_with_options_async(request, runtime)

    def list_sites_with_options(
        self,
        tmp_req: esa20240910_models.ListSitesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListSitesResponse:
        """
        @summary Queries the information about websites in your account, such as the name, status, and configuration of each website.
        
        @param tmp_req: ListSitesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListSitesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListSitesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.tag_filter):
            request.tag_filter_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.tag_filter, 'TagFilter', 'json')
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSites',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListSitesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_sites_with_options_async(
        self,
        tmp_req: esa20240910_models.ListSitesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListSitesResponse:
        """
        @summary Queries the information about websites in your account, such as the name, status, and configuration of each website.
        
        @param tmp_req: ListSitesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListSitesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListSitesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.tag_filter):
            request.tag_filter_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.tag_filter, 'TagFilter', 'json')
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListSites',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListSitesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_sites(
        self,
        request: esa20240910_models.ListSitesRequest,
    ) -> esa20240910_models.ListSitesResponse:
        """
        @summary Queries the information about websites in your account, such as the name, status, and configuration of each website.
        
        @param request: ListSitesRequest
        @return: ListSitesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_sites_with_options(request, runtime)

    async def list_sites_async(
        self,
        request: esa20240910_models.ListSitesRequest,
    ) -> esa20240910_models.ListSitesResponse:
        """
        @summary Queries the information about websites in your account, such as the name, status, and configuration of each website.
        
        @param request: ListSitesRequest
        @return: ListSitesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_sites_with_options_async(request, runtime)

    def list_tag_resources_with_options(
        self,
        request: esa20240910_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListTagResourcesResponse:
        """
        @summary Queries tags based on the region ID and resource type.
        
        @param request: ListTagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTagResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.max_item):
            query['MaxItem'] = request.max_item
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListTagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_tag_resources_with_options_async(
        self,
        request: esa20240910_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListTagResourcesResponse:
        """
        @summary Queries tags based on the region ID and resource type.
        
        @param request: ListTagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTagResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.max_item):
            query['MaxItem'] = request.max_item
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListTagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_tag_resources(
        self,
        request: esa20240910_models.ListTagResourcesRequest,
    ) -> esa20240910_models.ListTagResourcesResponse:
        """
        @summary Queries tags based on the region ID and resource type.
        
        @param request: ListTagResourcesRequest
        @return: ListTagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_tag_resources_with_options(request, runtime)

    async def list_tag_resources_async(
        self,
        request: esa20240910_models.ListTagResourcesRequest,
    ) -> esa20240910_models.ListTagResourcesResponse:
        """
        @summary Queries tags based on the region ID and resource type.
        
        @param request: ListTagResourcesRequest
        @return: ListTagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_tag_resources_with_options_async(request, runtime)

    def list_upload_tasks_with_options(
        self,
        request: esa20240910_models.ListUploadTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUploadTasksResponse:
        """
        @summary Queries the execution status and running information of file upload tasks based on the task time and type.
        
        @param request: ListUploadTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUploadTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUploadTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUploadTasksResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_upload_tasks_with_options_async(
        self,
        request: esa20240910_models.ListUploadTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUploadTasksResponse:
        """
        @summary Queries the execution status and running information of file upload tasks based on the task time and type.
        
        @param request: ListUploadTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUploadTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUploadTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUploadTasksResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_upload_tasks(
        self,
        request: esa20240910_models.ListUploadTasksRequest,
    ) -> esa20240910_models.ListUploadTasksResponse:
        """
        @summary Queries the execution status and running information of file upload tasks based on the task time and type.
        
        @param request: ListUploadTasksRequest
        @return: ListUploadTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_upload_tasks_with_options(request, runtime)

    async def list_upload_tasks_async(
        self,
        request: esa20240910_models.ListUploadTasksRequest,
    ) -> esa20240910_models.ListUploadTasksResponse:
        """
        @summary Queries the execution status and running information of file upload tasks based on the task time and type.
        
        @param request: ListUploadTasksRequest
        @return: ListUploadTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_upload_tasks_with_options_async(request, runtime)

    def list_user_delivery_tasks_with_options(
        self,
        request: esa20240910_models.ListUserDeliveryTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUserDeliveryTasksResponse:
        """
        @summary Queries all delivery tasks in your Alibaba Cloud account by page. You can filter the delivery tasks by the category of the delivered real-time logs.
        
        @param request: ListUserDeliveryTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserDeliveryTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserDeliveryTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUserDeliveryTasksResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_user_delivery_tasks_with_options_async(
        self,
        request: esa20240910_models.ListUserDeliveryTasksRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUserDeliveryTasksResponse:
        """
        @summary Queries all delivery tasks in your Alibaba Cloud account by page. You can filter the delivery tasks by the category of the delivered real-time logs.
        
        @param request: ListUserDeliveryTasksRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserDeliveryTasksResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserDeliveryTasks',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUserDeliveryTasksResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_user_delivery_tasks(
        self,
        request: esa20240910_models.ListUserDeliveryTasksRequest,
    ) -> esa20240910_models.ListUserDeliveryTasksResponse:
        """
        @summary Queries all delivery tasks in your Alibaba Cloud account by page. You can filter the delivery tasks by the category of the delivered real-time logs.
        
        @param request: ListUserDeliveryTasksRequest
        @return: ListUserDeliveryTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_user_delivery_tasks_with_options(request, runtime)

    async def list_user_delivery_tasks_async(
        self,
        request: esa20240910_models.ListUserDeliveryTasksRequest,
    ) -> esa20240910_models.ListUserDeliveryTasksResponse:
        """
        @summary Queries all delivery tasks in your Alibaba Cloud account by page. You can filter the delivery tasks by the category of the delivered real-time logs.
        
        @param request: ListUserDeliveryTasksRequest
        @return: ListUserDeliveryTasksResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_user_delivery_tasks_with_options_async(request, runtime)

    def list_user_rate_plan_instances_with_options(
        self,
        request: esa20240910_models.ListUserRatePlanInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUserRatePlanInstancesResponse:
        """
        @summary Queries the plans that you purchased and the details of the plans.
        
        @param request: ListUserRatePlanInstancesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserRatePlanInstancesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserRatePlanInstances',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUserRatePlanInstancesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_user_rate_plan_instances_with_options_async(
        self,
        request: esa20240910_models.ListUserRatePlanInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListUserRatePlanInstancesResponse:
        """
        @summary Queries the plans that you purchased and the details of the plans.
        
        @param request: ListUserRatePlanInstancesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListUserRatePlanInstancesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListUserRatePlanInstances',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListUserRatePlanInstancesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_user_rate_plan_instances(
        self,
        request: esa20240910_models.ListUserRatePlanInstancesRequest,
    ) -> esa20240910_models.ListUserRatePlanInstancesResponse:
        """
        @summary Queries the plans that you purchased and the details of the plans.
        
        @param request: ListUserRatePlanInstancesRequest
        @return: ListUserRatePlanInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_user_rate_plan_instances_with_options(request, runtime)

    async def list_user_rate_plan_instances_async(
        self,
        request: esa20240910_models.ListUserRatePlanInstancesRequest,
    ) -> esa20240910_models.ListUserRatePlanInstancesResponse:
        """
        @summary Queries the plans that you purchased and the details of the plans.
        
        @param request: ListUserRatePlanInstancesRequest
        @return: ListUserRatePlanInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_user_rate_plan_instances_with_options_async(request, runtime)

    def list_waf_managed_rules_with_options(
        self,
        tmp_req: esa20240910_models.ListWafManagedRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafManagedRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) managed rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param tmp_req: ListWafManagedRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafManagedRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafManagedRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.attack_type):
            query['AttackType'] = request.attack_type
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.protection_level):
            query['ProtectionLevel'] = request.protection_level
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafManagedRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafManagedRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_managed_rules_with_options_async(
        self,
        tmp_req: esa20240910_models.ListWafManagedRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafManagedRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) managed rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param tmp_req: ListWafManagedRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafManagedRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafManagedRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.attack_type):
            query['AttackType'] = request.attack_type
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.protection_level):
            query['ProtectionLevel'] = request.protection_level
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafManagedRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafManagedRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_managed_rules(
        self,
        request: esa20240910_models.ListWafManagedRulesRequest,
    ) -> esa20240910_models.ListWafManagedRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) managed rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param request: ListWafManagedRulesRequest
        @return: ListWafManagedRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_managed_rules_with_options(request, runtime)

    async def list_waf_managed_rules_async(
        self,
        request: esa20240910_models.ListWafManagedRulesRequest,
    ) -> esa20240910_models.ListWafManagedRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) managed rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param request: ListWafManagedRulesRequest
        @return: ListWafManagedRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_managed_rules_with_options_async(request, runtime)

    def list_waf_phases_with_options(
        self,
        request: esa20240910_models.ListWafPhasesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafPhasesResponse:
        """
        @summary Queries the WAF rule categories that are applied to a website and related rulesets.
        
        @param request: ListWafPhasesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafPhasesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafPhases',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafPhasesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_phases_with_options_async(
        self,
        request: esa20240910_models.ListWafPhasesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafPhasesResponse:
        """
        @summary Queries the WAF rule categories that are applied to a website and related rulesets.
        
        @param request: ListWafPhasesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafPhasesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafPhases',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafPhasesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_phases(
        self,
        request: esa20240910_models.ListWafPhasesRequest,
    ) -> esa20240910_models.ListWafPhasesResponse:
        """
        @summary Queries the WAF rule categories that are applied to a website and related rulesets.
        
        @param request: ListWafPhasesRequest
        @return: ListWafPhasesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_phases_with_options(request, runtime)

    async def list_waf_phases_async(
        self,
        request: esa20240910_models.ListWafPhasesRequest,
    ) -> esa20240910_models.ListWafPhasesResponse:
        """
        @summary Queries the WAF rule categories that are applied to a website and related rulesets.
        
        @param request: ListWafPhasesRequest
        @return: ListWafPhasesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_phases_with_options_async(request, runtime)

    def list_waf_rules_with_options(
        self,
        tmp_req: esa20240910_models.ListWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param tmp_req: ListWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_rules_with_options_async(
        self,
        tmp_req: esa20240910_models.ListWafRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param tmp_req: ListWafRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_rules(
        self,
        request: esa20240910_models.ListWafRulesRequest,
    ) -> esa20240910_models.ListWafRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param request: ListWafRulesRequest
        @return: ListWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_rules_with_options(request, runtime)

    async def list_waf_rules_async(
        self,
        request: esa20240910_models.ListWafRulesRequest,
    ) -> esa20240910_models.ListWafRulesResponse:
        """
        @summary Lists all Web Application Firewall (WAF) rules or some of them based on specific conditions. You can call this operation to query the details of WAF rules by page.
        
        @param request: ListWafRulesRequest
        @return: ListWafRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_rules_with_options_async(request, runtime)

    def list_waf_rulesets_with_options(
        self,
        tmp_req: esa20240910_models.ListWafRulesetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafRulesetsResponse:
        """
        @summary Lists the rulesets in a Web Application Firewall (WAF) rule category. You can call this operation to query the basic information about and status of rulesets by page.
        
        @param tmp_req: ListWafRulesetsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafRulesetsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafRulesetsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafRulesets',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafRulesetsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_rulesets_with_options_async(
        self,
        tmp_req: esa20240910_models.ListWafRulesetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafRulesetsResponse:
        """
        @summary Lists the rulesets in a Web Application Firewall (WAF) rule category. You can call this operation to query the basic information about and status of rulesets by page.
        
        @param tmp_req: ListWafRulesetsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafRulesetsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafRulesetsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafRulesets',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafRulesetsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_rulesets(
        self,
        request: esa20240910_models.ListWafRulesetsRequest,
    ) -> esa20240910_models.ListWafRulesetsResponse:
        """
        @summary Lists the rulesets in a Web Application Firewall (WAF) rule category. You can call this operation to query the basic information about and status of rulesets by page.
        
        @param request: ListWafRulesetsRequest
        @return: ListWafRulesetsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_rulesets_with_options(request, runtime)

    async def list_waf_rulesets_async(
        self,
        request: esa20240910_models.ListWafRulesetsRequest,
    ) -> esa20240910_models.ListWafRulesetsResponse:
        """
        @summary Lists the rulesets in a Web Application Firewall (WAF) rule category. You can call this operation to query the basic information about and status of rulesets by page.
        
        @param request: ListWafRulesetsRequest
        @return: ListWafRulesetsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_rulesets_with_options_async(request, runtime)

    def list_waf_template_rules_with_options(
        self,
        tmp_req: esa20240910_models.ListWafTemplateRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafTemplateRulesResponse:
        """
        @summary Queries template rules in Web Application Firewall (WAF). In most cases, these rules are pre-defined rulesets that are used to quickly enable protection against common types of attacks.
        
        @param tmp_req: ListWafTemplateRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafTemplateRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafTemplateRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafTemplateRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafTemplateRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_template_rules_with_options_async(
        self,
        tmp_req: esa20240910_models.ListWafTemplateRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafTemplateRulesResponse:
        """
        @summary Queries template rules in Web Application Firewall (WAF). In most cases, these rules are pre-defined rulesets that are used to quickly enable protection against common types of attacks.
        
        @param tmp_req: ListWafTemplateRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafTemplateRulesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.ListWafTemplateRulesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.query_args):
            request.query_args_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.query_args, 'QueryArgs', 'json')
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.query_args_shrink):
            query['QueryArgs'] = request.query_args_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafTemplateRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafTemplateRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_template_rules(
        self,
        request: esa20240910_models.ListWafTemplateRulesRequest,
    ) -> esa20240910_models.ListWafTemplateRulesResponse:
        """
        @summary Queries template rules in Web Application Firewall (WAF). In most cases, these rules are pre-defined rulesets that are used to quickly enable protection against common types of attacks.
        
        @param request: ListWafTemplateRulesRequest
        @return: ListWafTemplateRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_template_rules_with_options(request, runtime)

    async def list_waf_template_rules_async(
        self,
        request: esa20240910_models.ListWafTemplateRulesRequest,
    ) -> esa20240910_models.ListWafTemplateRulesResponse:
        """
        @summary Queries template rules in Web Application Firewall (WAF). In most cases, these rules are pre-defined rulesets that are used to quickly enable protection against common types of attacks.
        
        @param request: ListWafTemplateRulesRequest
        @return: ListWafTemplateRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_template_rules_with_options_async(request, runtime)

    def list_waf_usage_of_rules_with_options(
        self,
        request: esa20240910_models.ListWafUsageOfRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafUsageOfRulesResponse:
        """
        @summary Queries the usage details of WAF rules.
        
        @param request: ListWafUsageOfRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafUsageOfRulesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafUsageOfRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafUsageOfRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waf_usage_of_rules_with_options_async(
        self,
        request: esa20240910_models.ListWafUsageOfRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWafUsageOfRulesResponse:
        """
        @summary Queries the usage details of WAF rules.
        
        @param request: ListWafUsageOfRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWafUsageOfRulesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.phase):
            query['Phase'] = request.phase
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWafUsageOfRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWafUsageOfRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waf_usage_of_rules(
        self,
        request: esa20240910_models.ListWafUsageOfRulesRequest,
    ) -> esa20240910_models.ListWafUsageOfRulesResponse:
        """
        @summary Queries the usage details of WAF rules.
        
        @param request: ListWafUsageOfRulesRequest
        @return: ListWafUsageOfRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waf_usage_of_rules_with_options(request, runtime)

    async def list_waf_usage_of_rules_async(
        self,
        request: esa20240910_models.ListWafUsageOfRulesRequest,
    ) -> esa20240910_models.ListWafUsageOfRulesResponse:
        """
        @summary Queries the usage details of WAF rules.
        
        @param request: ListWafUsageOfRulesRequest
        @return: ListWafUsageOfRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waf_usage_of_rules_with_options_async(request, runtime)

    def list_waiting_room_events_with_options(
        self,
        request: esa20240910_models.ListWaitingRoomEventsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomEventsResponse:
        """
        @summary Queries the information about waiting room events for a waiting room.
        
        @description You can call this operation to query details of all waiting room events related to a waiting room in a website.
        
        @param request: ListWaitingRoomEventsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomEventsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRoomEvents',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomEventsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waiting_room_events_with_options_async(
        self,
        request: esa20240910_models.ListWaitingRoomEventsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomEventsResponse:
        """
        @summary Queries the information about waiting room events for a waiting room.
        
        @description You can call this operation to query details of all waiting room events related to a waiting room in a website.
        
        @param request: ListWaitingRoomEventsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomEventsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRoomEvents',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomEventsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waiting_room_events(
        self,
        request: esa20240910_models.ListWaitingRoomEventsRequest,
    ) -> esa20240910_models.ListWaitingRoomEventsResponse:
        """
        @summary Queries the information about waiting room events for a waiting room.
        
        @description You can call this operation to query details of all waiting room events related to a waiting room in a website.
        
        @param request: ListWaitingRoomEventsRequest
        @return: ListWaitingRoomEventsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waiting_room_events_with_options(request, runtime)

    async def list_waiting_room_events_async(
        self,
        request: esa20240910_models.ListWaitingRoomEventsRequest,
    ) -> esa20240910_models.ListWaitingRoomEventsResponse:
        """
        @summary Queries the information about waiting room events for a waiting room.
        
        @description You can call this operation to query details of all waiting room events related to a waiting room in a website.
        
        @param request: ListWaitingRoomEventsRequest
        @return: ListWaitingRoomEventsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waiting_room_events_with_options_async(request, runtime)

    def list_waiting_room_rules_with_options(
        self,
        request: esa20240910_models.ListWaitingRoomRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomRulesResponse:
        """
        @summary Queries the waiting room bypass rules configured for a waiting room.
        
        @description You can call this operation to query the waiting room bypass rules that are associated with a website.
        
        @param request: ListWaitingRoomRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomRulesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRoomRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomRulesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waiting_room_rules_with_options_async(
        self,
        request: esa20240910_models.ListWaitingRoomRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomRulesResponse:
        """
        @summary Queries the waiting room bypass rules configured for a waiting room.
        
        @description You can call this operation to query the waiting room bypass rules that are associated with a website.
        
        @param request: ListWaitingRoomRulesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomRulesResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRoomRules',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomRulesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waiting_room_rules(
        self,
        request: esa20240910_models.ListWaitingRoomRulesRequest,
    ) -> esa20240910_models.ListWaitingRoomRulesResponse:
        """
        @summary Queries the waiting room bypass rules configured for a waiting room.
        
        @description You can call this operation to query the waiting room bypass rules that are associated with a website.
        
        @param request: ListWaitingRoomRulesRequest
        @return: ListWaitingRoomRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waiting_room_rules_with_options(request, runtime)

    async def list_waiting_room_rules_async(
        self,
        request: esa20240910_models.ListWaitingRoomRulesRequest,
    ) -> esa20240910_models.ListWaitingRoomRulesResponse:
        """
        @summary Queries the waiting room bypass rules configured for a waiting room.
        
        @description You can call this operation to query the waiting room bypass rules that are associated with a website.
        
        @param request: ListWaitingRoomRulesRequest
        @return: ListWaitingRoomRulesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waiting_room_rules_with_options_async(request, runtime)

    def list_waiting_rooms_with_options(
        self,
        request: esa20240910_models.ListWaitingRoomsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomsResponse:
        """
        @summary Queries the information about all waiting rooms in a website.
        
        @description You can call this operation to query detailed configurations about all waiting rooms in a website, including the status, name, and queuing rules of each waiting room.
        
        @param request: ListWaitingRoomsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRooms',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_waiting_rooms_with_options_async(
        self,
        request: esa20240910_models.ListWaitingRoomsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ListWaitingRoomsResponse:
        """
        @summary Queries the information about all waiting rooms in a website.
        
        @description You can call this operation to query detailed configurations about all waiting rooms in a website, including the status, name, and queuing rules of each waiting room.
        
        @param request: ListWaitingRoomsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListWaitingRoomsResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListWaitingRooms',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ListWaitingRoomsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_waiting_rooms(
        self,
        request: esa20240910_models.ListWaitingRoomsRequest,
    ) -> esa20240910_models.ListWaitingRoomsResponse:
        """
        @summary Queries the information about all waiting rooms in a website.
        
        @description You can call this operation to query detailed configurations about all waiting rooms in a website, including the status, name, and queuing rules of each waiting room.
        
        @param request: ListWaitingRoomsRequest
        @return: ListWaitingRoomsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_waiting_rooms_with_options(request, runtime)

    async def list_waiting_rooms_async(
        self,
        request: esa20240910_models.ListWaitingRoomsRequest,
    ) -> esa20240910_models.ListWaitingRoomsResponse:
        """
        @summary Queries the information about all waiting rooms in a website.
        
        @description You can call this operation to query detailed configurations about all waiting rooms in a website, including the status, name, and queuing rules of each waiting room.
        
        @param request: ListWaitingRoomsRequest
        @return: ListWaitingRoomsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_waiting_rooms_with_options_async(request, runtime)

    def preload_caches_with_options(
        self,
        tmp_req: esa20240910_models.PreloadCachesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PreloadCachesResponse:
        """
        @summary Prefetches cache.
        
        @param tmp_req: PreloadCachesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PreloadCachesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PreloadCachesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        if not UtilClient.is_unset(tmp_req.headers):
            request.headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.headers, 'Headers', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.headers_shrink):
            query['Headers'] = request.headers_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PreloadCaches',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PreloadCachesResponse(),
            self.call_api(params, req, runtime)
        )

    async def preload_caches_with_options_async(
        self,
        tmp_req: esa20240910_models.PreloadCachesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PreloadCachesResponse:
        """
        @summary Prefetches cache.
        
        @param tmp_req: PreloadCachesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PreloadCachesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PreloadCachesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        if not UtilClient.is_unset(tmp_req.headers):
            request.headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.headers, 'Headers', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.headers_shrink):
            query['Headers'] = request.headers_shrink
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PreloadCaches',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PreloadCachesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def preload_caches(
        self,
        request: esa20240910_models.PreloadCachesRequest,
    ) -> esa20240910_models.PreloadCachesResponse:
        """
        @summary Prefetches cache.
        
        @param request: PreloadCachesRequest
        @return: PreloadCachesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.preload_caches_with_options(request, runtime)

    async def preload_caches_async(
        self,
        request: esa20240910_models.PreloadCachesRequest,
    ) -> esa20240910_models.PreloadCachesResponse:
        """
        @summary Prefetches cache.
        
        @param request: PreloadCachesRequest
        @return: PreloadCachesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.preload_caches_with_options_async(request, runtime)

    def publish_edge_container_app_version_with_options(
        self,
        tmp_req: esa20240910_models.PublishEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PublishEdgeContainerAppVersionResponse:
        """
        @summary Releases a specific version of a containerized application. You can call this operation to iterate an application.
        
        @param tmp_req: PublishEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PublishEdgeContainerAppVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.regions):
            request.regions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.regions, 'Regions', 'json')
        query = {}
        if not UtilClient.is_unset(request.full_release):
            query['FullRelease'] = request.full_release
        if not UtilClient.is_unset(request.publish_type):
            query['PublishType'] = request.publish_type
        if not UtilClient.is_unset(request.regions_shrink):
            query['Regions'] = request.regions_shrink
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.percentage):
            body['Percentage'] = request.percentage
        if not UtilClient.is_unset(request.publish_env):
            body['PublishEnv'] = request.publish_env
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        if not UtilClient.is_unset(request.start_time):
            body['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PublishEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PublishEdgeContainerAppVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def publish_edge_container_app_version_with_options_async(
        self,
        tmp_req: esa20240910_models.PublishEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PublishEdgeContainerAppVersionResponse:
        """
        @summary Releases a specific version of a containerized application. You can call this operation to iterate an application.
        
        @param tmp_req: PublishEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PublishEdgeContainerAppVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.regions):
            request.regions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.regions, 'Regions', 'json')
        query = {}
        if not UtilClient.is_unset(request.full_release):
            query['FullRelease'] = request.full_release
        if not UtilClient.is_unset(request.publish_type):
            query['PublishType'] = request.publish_type
        if not UtilClient.is_unset(request.regions_shrink):
            query['Regions'] = request.regions_shrink
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.percentage):
            body['Percentage'] = request.percentage
        if not UtilClient.is_unset(request.publish_env):
            body['PublishEnv'] = request.publish_env
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        if not UtilClient.is_unset(request.start_time):
            body['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PublishEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PublishEdgeContainerAppVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def publish_edge_container_app_version(
        self,
        request: esa20240910_models.PublishEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.PublishEdgeContainerAppVersionResponse:
        """
        @summary Releases a specific version of a containerized application. You can call this operation to iterate an application.
        
        @param request: PublishEdgeContainerAppVersionRequest
        @return: PublishEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.publish_edge_container_app_version_with_options(request, runtime)

    async def publish_edge_container_app_version_async(
        self,
        request: esa20240910_models.PublishEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.PublishEdgeContainerAppVersionResponse:
        """
        @summary Releases a specific version of a containerized application. You can call this operation to iterate an application.
        
        @param request: PublishEdgeContainerAppVersionRequest
        @return: PublishEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.publish_edge_container_app_version_with_options_async(request, runtime)

    def publish_routine_code_version_with_options(
        self,
        tmp_req: esa20240910_models.PublishRoutineCodeVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PublishRoutineCodeVersionResponse:
        """
        @summary Releases a code version of a routine to the staging, canary, or production environment. You can specify the regions where the canary environment is deployed to release your code.
        
        @param tmp_req: PublishRoutineCodeVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishRoutineCodeVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PublishRoutineCodeVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.canary_area_list):
            request.canary_area_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.canary_area_list, 'CanaryAreaList', 'json')
        body = {}
        if not UtilClient.is_unset(request.canary_area_list_shrink):
            body['CanaryAreaList'] = request.canary_area_list_shrink
        if not UtilClient.is_unset(request.canary_code_version):
            body['CanaryCodeVersion'] = request.canary_code_version
        if not UtilClient.is_unset(request.code_version):
            body['CodeVersion'] = request.code_version
        if not UtilClient.is_unset(request.env):
            body['Env'] = request.env
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PublishRoutineCodeVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PublishRoutineCodeVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def publish_routine_code_version_with_options_async(
        self,
        tmp_req: esa20240910_models.PublishRoutineCodeVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PublishRoutineCodeVersionResponse:
        """
        @summary Releases a code version of a routine to the staging, canary, or production environment. You can specify the regions where the canary environment is deployed to release your code.
        
        @param tmp_req: PublishRoutineCodeVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PublishRoutineCodeVersionResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PublishRoutineCodeVersionShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.canary_area_list):
            request.canary_area_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.canary_area_list, 'CanaryAreaList', 'json')
        body = {}
        if not UtilClient.is_unset(request.canary_area_list_shrink):
            body['CanaryAreaList'] = request.canary_area_list_shrink
        if not UtilClient.is_unset(request.canary_code_version):
            body['CanaryCodeVersion'] = request.canary_code_version
        if not UtilClient.is_unset(request.code_version):
            body['CodeVersion'] = request.code_version
        if not UtilClient.is_unset(request.env):
            body['Env'] = request.env
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PublishRoutineCodeVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PublishRoutineCodeVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def publish_routine_code_version(
        self,
        request: esa20240910_models.PublishRoutineCodeVersionRequest,
    ) -> esa20240910_models.PublishRoutineCodeVersionResponse:
        """
        @summary Releases a code version of a routine to the staging, canary, or production environment. You can specify the regions where the canary environment is deployed to release your code.
        
        @param request: PublishRoutineCodeVersionRequest
        @return: PublishRoutineCodeVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.publish_routine_code_version_with_options(request, runtime)

    async def publish_routine_code_version_async(
        self,
        request: esa20240910_models.PublishRoutineCodeVersionRequest,
    ) -> esa20240910_models.PublishRoutineCodeVersionResponse:
        """
        @summary Releases a code version of a routine to the staging, canary, or production environment. You can specify the regions where the canary environment is deployed to release your code.
        
        @param request: PublishRoutineCodeVersionRequest
        @return: PublishRoutineCodeVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.publish_routine_code_version_with_options_async(request, runtime)

    def purge_caches_with_options(
        self,
        tmp_req: esa20240910_models.PurgeCachesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PurgeCachesResponse:
        """
        @summary Purges resources cached on points of presence (POPs). You can purge the cache by file URL, directory, cache tag, hostname, or URL with specified parameters ignored, or purge all the cache.
        
        @param tmp_req: PurgeCachesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PurgeCachesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PurgeCachesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.edge_compute_purge):
            query['EdgeComputePurge'] = request.edge_compute_purge
        if not UtilClient.is_unset(request.force):
            query['Force'] = request.force
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PurgeCaches',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PurgeCachesResponse(),
            self.call_api(params, req, runtime)
        )

    async def purge_caches_with_options_async(
        self,
        tmp_req: esa20240910_models.PurgeCachesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PurgeCachesResponse:
        """
        @summary Purges resources cached on points of presence (POPs). You can purge the cache by file URL, directory, cache tag, hostname, or URL with specified parameters ignored, or purge all the cache.
        
        @param tmp_req: PurgeCachesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PurgeCachesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.PurgeCachesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.content):
            request.content_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.content, 'Content', 'json')
        query = {}
        if not UtilClient.is_unset(request.content_shrink):
            query['Content'] = request.content_shrink
        if not UtilClient.is_unset(request.edge_compute_purge):
            query['EdgeComputePurge'] = request.edge_compute_purge
        if not UtilClient.is_unset(request.force):
            query['Force'] = request.force
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PurgeCaches',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PurgeCachesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def purge_caches(
        self,
        request: esa20240910_models.PurgeCachesRequest,
    ) -> esa20240910_models.PurgeCachesResponse:
        """
        @summary Purges resources cached on points of presence (POPs). You can purge the cache by file URL, directory, cache tag, hostname, or URL with specified parameters ignored, or purge all the cache.
        
        @param request: PurgeCachesRequest
        @return: PurgeCachesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.purge_caches_with_options(request, runtime)

    async def purge_caches_async(
        self,
        request: esa20240910_models.PurgeCachesRequest,
    ) -> esa20240910_models.PurgeCachesResponse:
        """
        @summary Purges resources cached on points of presence (POPs). You can purge the cache by file URL, directory, cache tag, hostname, or URL with specified parameters ignored, or purge all the cache.
        
        @param request: PurgeCachesRequest
        @return: PurgeCachesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.purge_caches_with_options_async(request, runtime)

    def put_kv_with_options(
        self,
        request: esa20240910_models.PutKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvResponse:
        """
        @summary Configures a key-value pair for a namespace. The request body can be up to 2 MB.
        
        @param request: PutKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PutKvResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.base_64):
            query['Base64'] = request.base_64
        if not UtilClient.is_unset(request.expiration):
            query['Expiration'] = request.expiration
        if not UtilClient.is_unset(request.expiration_ttl):
            query['ExpirationTtl'] = request.expiration_ttl
        if not UtilClient.is_unset(request.key):
            query['Key'] = request.key
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.value):
            body['Value'] = request.value
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PutKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PutKvResponse(),
            self.call_api(params, req, runtime)
        )

    async def put_kv_with_options_async(
        self,
        request: esa20240910_models.PutKvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvResponse:
        """
        @summary Configures a key-value pair for a namespace. The request body can be up to 2 MB.
        
        @param request: PutKvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PutKvResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.base_64):
            query['Base64'] = request.base_64
        if not UtilClient.is_unset(request.expiration):
            query['Expiration'] = request.expiration
        if not UtilClient.is_unset(request.expiration_ttl):
            query['ExpirationTtl'] = request.expiration_ttl
        if not UtilClient.is_unset(request.key):
            query['Key'] = request.key
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        body = {}
        if not UtilClient.is_unset(request.value):
            body['Value'] = request.value
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='PutKv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PutKvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def put_kv(
        self,
        request: esa20240910_models.PutKvRequest,
    ) -> esa20240910_models.PutKvResponse:
        """
        @summary Configures a key-value pair for a namespace. The request body can be up to 2 MB.
        
        @param request: PutKvRequest
        @return: PutKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.put_kv_with_options(request, runtime)

    async def put_kv_async(
        self,
        request: esa20240910_models.PutKvRequest,
    ) -> esa20240910_models.PutKvResponse:
        """
        @summary Configures a key-value pair for a namespace. The request body can be up to 2 MB.
        
        @param request: PutKvRequest
        @return: PutKvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.put_kv_with_options_async(request, runtime)

    def put_kv_with_high_capacity_with_options(
        self,
        request: esa20240910_models.PutKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        """
        @summary Configures a large key-value pair for a namespace. The request body can be up to 25 MB.
        
        @description This operation allows you to upload a larger request body than by using [PutKv](~~PutKv~~). For small request bodies, we recommend that you use [PutKv](~~PutKv~~) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and PutKvWithHighCapacityAdvance to call the operation.
        func TestPutKvWithHighCapacity() {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs.
        namespace := "test-put-kv"
        key := "test_PutKvWithHighCapacity_0"
        value := strings.Repeat("t", 101024*1024)
        rawReq := &PutKvRequest{
        Namespace: &namespace,
        Key:       &key,
        Value:     &value,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the PutKvWithHighCapacity operation for upload.
        reqHighCapacity := &PutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        Key:       &key,
        UrlObject: bytes.NewReader([]byte(payload)),
        }
        resp, err := cli.PutKvWithHighCapacityAdvance(reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: PutKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PutKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.key):
            query['Key'] = request.key
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PutKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PutKvWithHighCapacityResponse(),
            self.call_api(params, req, runtime)
        )

    async def put_kv_with_high_capacity_with_options_async(
        self,
        request: esa20240910_models.PutKvWithHighCapacityRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        """
        @summary Configures a large key-value pair for a namespace. The request body can be up to 25 MB.
        
        @description This operation allows you to upload a larger request body than by using [PutKv](~~PutKv~~). For small request bodies, we recommend that you use [PutKv](~~PutKv~~) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and PutKvWithHighCapacityAdvance to call the operation.
        func TestPutKvWithHighCapacity() {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs.
        namespace := "test-put-kv"
        key := "test_PutKvWithHighCapacity_0"
        value := strings.Repeat("t", 101024*1024)
        rawReq := &PutKvRequest{
        Namespace: &namespace,
        Key:       &key,
        Value:     &value,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the PutKvWithHighCapacity operation for upload.
        reqHighCapacity := &PutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        Key:       &key,
        UrlObject: bytes.NewReader([]byte(payload)),
        }
        resp, err := cli.PutKvWithHighCapacityAdvance(reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: PutKvWithHighCapacityRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PutKvWithHighCapacityResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.key):
            query['Key'] = request.key
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PutKvWithHighCapacity',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.PutKvWithHighCapacityResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def put_kv_with_high_capacity(
        self,
        request: esa20240910_models.PutKvWithHighCapacityRequest,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        """
        @summary Configures a large key-value pair for a namespace. The request body can be up to 25 MB.
        
        @description This operation allows you to upload a larger request body than by using [PutKv](~~PutKv~~). For small request bodies, we recommend that you use [PutKv](~~PutKv~~) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and PutKvWithHighCapacityAdvance to call the operation.
        func TestPutKvWithHighCapacity() {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs.
        namespace := "test-put-kv"
        key := "test_PutKvWithHighCapacity_0"
        value := strings.Repeat("t", 101024*1024)
        rawReq := &PutKvRequest{
        Namespace: &namespace,
        Key:       &key,
        Value:     &value,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the PutKvWithHighCapacity operation for upload.
        reqHighCapacity := &PutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        Key:       &key,
        UrlObject: bytes.NewReader([]byte(payload)),
        }
        resp, err := cli.PutKvWithHighCapacityAdvance(reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: PutKvWithHighCapacityRequest
        @return: PutKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.put_kv_with_high_capacity_with_options(request, runtime)

    async def put_kv_with_high_capacity_async(
        self,
        request: esa20240910_models.PutKvWithHighCapacityRequest,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        """
        @summary Configures a large key-value pair for a namespace. The request body can be up to 25 MB.
        
        @description This operation allows you to upload a larger request body than by using [PutKv](~~PutKv~~). For small request bodies, we recommend that you use [PutKv](~~PutKv~~) to minimize the server processing time. This operation must be called by using SDKs. The following sample code uses the Golang SDK and PutKvWithHighCapacityAdvance to call the operation.
        func TestPutKvWithHighCapacity() {
        // Initialize the configurations.
        cfg := new(openapi.Config)
        cfg.SetAccessKeyId("xxxxxxxxx")
        cfg.SetAccessKeySecret("xxxxxxxxxx")
        cli, err := NewClient(cfg)
        if err != nil {
        return err
        }
        runtime := &util.RuntimeOptions{}
        // Construct a request for uploading key-value pairs.
        namespace := "test-put-kv"
        key := "test_PutKvWithHighCapacity_0"
        value := strings.Repeat("t", 101024*1024)
        rawReq := &PutKvRequest{
        Namespace: &namespace,
        Key:       &key,
        Value:     &value,
        }
        payload, err := json.Marshal(rawReq)
        if err != nil {
        return err
        }
        // If the payload is greater than 2 MB, call the PutKvWithHighCapacity operation for upload.
        reqHighCapacity := &PutKvWithHighCapacityAdvanceRequest{
        Namespace: &namespace,
        Key:       &key,
        UrlObject: bytes.NewReader([]byte(payload)),
        }
        resp, err := cli.PutKvWithHighCapacityAdvance(reqHighCapacity, runtime)
        if err != nil {
        return err
        }
        return nil
        }
        
        @param request: PutKvWithHighCapacityRequest
        @return: PutKvWithHighCapacityResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.put_kv_with_high_capacity_with_options_async(request, runtime)

    def put_kv_with_high_capacity_advance(
        self,
        request: esa20240910_models.PutKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        put_kv_with_high_capacity_req = esa20240910_models.PutKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, put_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            put_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        put_kv_with_high_capacity_resp = self.put_kv_with_high_capacity_with_options(put_kv_with_high_capacity_req, runtime)
        return put_kv_with_high_capacity_resp

    async def put_kv_with_high_capacity_advance_async(
        self,
        request: esa20240910_models.PutKvWithHighCapacityAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.PutKvWithHighCapacityResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        put_kv_with_high_capacity_req = esa20240910_models.PutKvWithHighCapacityRequest()
        OpenApiUtilClient.convert(request, put_kv_with_high_capacity_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            put_kv_with_high_capacity_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        put_kv_with_high_capacity_resp = await self.put_kv_with_high_capacity_with_options_async(put_kv_with_high_capacity_req, runtime)
        return put_kv_with_high_capacity_resp

    def rebuild_edge_container_app_staging_env_with_options(
        self,
        request: esa20240910_models.RebuildEdgeContainerAppStagingEnvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse:
        """
        @summary Rebuilds the staging environment for containerized applications.
        
        @param request: RebuildEdgeContainerAppStagingEnvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RebuildEdgeContainerAppStagingEnvResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RebuildEdgeContainerAppStagingEnv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse(),
            self.call_api(params, req, runtime)
        )

    async def rebuild_edge_container_app_staging_env_with_options_async(
        self,
        request: esa20240910_models.RebuildEdgeContainerAppStagingEnvRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse:
        """
        @summary Rebuilds the staging environment for containerized applications.
        
        @param request: RebuildEdgeContainerAppStagingEnvRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RebuildEdgeContainerAppStagingEnvResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RebuildEdgeContainerAppStagingEnv',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def rebuild_edge_container_app_staging_env(
        self,
        request: esa20240910_models.RebuildEdgeContainerAppStagingEnvRequest,
    ) -> esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse:
        """
        @summary Rebuilds the staging environment for containerized applications.
        
        @param request: RebuildEdgeContainerAppStagingEnvRequest
        @return: RebuildEdgeContainerAppStagingEnvResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.rebuild_edge_container_app_staging_env_with_options(request, runtime)

    async def rebuild_edge_container_app_staging_env_async(
        self,
        request: esa20240910_models.RebuildEdgeContainerAppStagingEnvRequest,
    ) -> esa20240910_models.RebuildEdgeContainerAppStagingEnvResponse:
        """
        @summary Rebuilds the staging environment for containerized applications.
        
        @param request: RebuildEdgeContainerAppStagingEnvRequest
        @return: RebuildEdgeContainerAppStagingEnvResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.rebuild_edge_container_app_staging_env_with_options_async(request, runtime)

    def reset_scheduled_preload_job_with_options(
        self,
        request: esa20240910_models.ResetScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ResetScheduledPreloadJobResponse:
        """
        @summary Resets the progress of a scheduled prefetch task and starts the prefetch from the beginning.
        
        @param request: ResetScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ResetScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResetScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ResetScheduledPreloadJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def reset_scheduled_preload_job_with_options_async(
        self,
        request: esa20240910_models.ResetScheduledPreloadJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.ResetScheduledPreloadJobResponse:
        """
        @summary Resets the progress of a scheduled prefetch task and starts the prefetch from the beginning.
        
        @param request: ResetScheduledPreloadJobRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ResetScheduledPreloadJobResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResetScheduledPreloadJob',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.ResetScheduledPreloadJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def reset_scheduled_preload_job(
        self,
        request: esa20240910_models.ResetScheduledPreloadJobRequest,
    ) -> esa20240910_models.ResetScheduledPreloadJobResponse:
        """
        @summary Resets the progress of a scheduled prefetch task and starts the prefetch from the beginning.
        
        @param request: ResetScheduledPreloadJobRequest
        @return: ResetScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.reset_scheduled_preload_job_with_options(request, runtime)

    async def reset_scheduled_preload_job_async(
        self,
        request: esa20240910_models.ResetScheduledPreloadJobRequest,
    ) -> esa20240910_models.ResetScheduledPreloadJobResponse:
        """
        @summary Resets the progress of a scheduled prefetch task and starts the prefetch from the beginning.
        
        @param request: ResetScheduledPreloadJobRequest
        @return: ResetScheduledPreloadJobResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.reset_scheduled_preload_job_with_options_async(request, runtime)

    def revoke_client_certificate_with_options(
        self,
        request: esa20240910_models.RevokeClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RevokeClientCertificateResponse:
        """
        @summary Revokes an activated client certificate.
        
        @param request: RevokeClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RevokeClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RevokeClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RevokeClientCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def revoke_client_certificate_with_options_async(
        self,
        request: esa20240910_models.RevokeClientCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RevokeClientCertificateResponse:
        """
        @summary Revokes an activated client certificate.
        
        @param request: RevokeClientCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RevokeClientCertificateResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RevokeClientCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RevokeClientCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def revoke_client_certificate(
        self,
        request: esa20240910_models.RevokeClientCertificateRequest,
    ) -> esa20240910_models.RevokeClientCertificateResponse:
        """
        @summary Revokes an activated client certificate.
        
        @param request: RevokeClientCertificateRequest
        @return: RevokeClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.revoke_client_certificate_with_options(request, runtime)

    async def revoke_client_certificate_async(
        self,
        request: esa20240910_models.RevokeClientCertificateRequest,
    ) -> esa20240910_models.RevokeClientCertificateResponse:
        """
        @summary Revokes an activated client certificate.
        
        @param request: RevokeClientCertificateRequest
        @return: RevokeClientCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.revoke_client_certificate_with_options_async(request, runtime)

    def rollback_edge_container_app_version_with_options(
        self,
        request: esa20240910_models.RollbackEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RollbackEdgeContainerAppVersionResponse:
        """
        @summary Rolls back a version of a containerized application.
        
        @param request: RollbackEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RollbackEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RollbackEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RollbackEdgeContainerAppVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def rollback_edge_container_app_version_with_options_async(
        self,
        request: esa20240910_models.RollbackEdgeContainerAppVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.RollbackEdgeContainerAppVersionResponse:
        """
        @summary Rolls back a version of a containerized application.
        
        @param request: RollbackEdgeContainerAppVersionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RollbackEdgeContainerAppVersionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.version_id):
            query['VersionId'] = request.version_id
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['AppId'] = request.app_id
        if not UtilClient.is_unset(request.remarks):
            body['Remarks'] = request.remarks
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RollbackEdgeContainerAppVersion',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.RollbackEdgeContainerAppVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def rollback_edge_container_app_version(
        self,
        request: esa20240910_models.RollbackEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.RollbackEdgeContainerAppVersionResponse:
        """
        @summary Rolls back a version of a containerized application.
        
        @param request: RollbackEdgeContainerAppVersionRequest
        @return: RollbackEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.rollback_edge_container_app_version_with_options(request, runtime)

    async def rollback_edge_container_app_version_async(
        self,
        request: esa20240910_models.RollbackEdgeContainerAppVersionRequest,
    ) -> esa20240910_models.RollbackEdgeContainerAppVersionResponse:
        """
        @summary Rolls back a version of a containerized application.
        
        @param request: RollbackEdgeContainerAppVersionRequest
        @return: RollbackEdgeContainerAppVersionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.rollback_edge_container_app_version_with_options_async(request, runtime)

    def set_certificate_with_options(
        self,
        request: esa20240910_models.SetCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetCertificateResponse:
        """
        @summary Configures whether to enable certificates and update certificate information for a website.
        
        @param request: SetCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        body = {}
        if not UtilClient.is_unset(request.cas_id):
            body['CasId'] = request.cas_id
        if not UtilClient.is_unset(request.certificate):
            body['Certificate'] = request.certificate
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.private_key):
            body['PrivateKey'] = request.private_key
        if not UtilClient.is_unset(request.region):
            body['Region'] = request.region
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            body['Type'] = request.type
        if not UtilClient.is_unset(request.update):
            body['Update'] = request.update
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_certificate_with_options_async(
        self,
        request: esa20240910_models.SetCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetCertificateResponse:
        """
        @summary Configures whether to enable certificates and update certificate information for a website.
        
        @param request: SetCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        body = {}
        if not UtilClient.is_unset(request.cas_id):
            body['CasId'] = request.cas_id
        if not UtilClient.is_unset(request.certificate):
            body['Certificate'] = request.certificate
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.private_key):
            body['PrivateKey'] = request.private_key
        if not UtilClient.is_unset(request.region):
            body['Region'] = request.region
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            body['Type'] = request.type
        if not UtilClient.is_unset(request.update):
            body['Update'] = request.update
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_certificate(
        self,
        request: esa20240910_models.SetCertificateRequest,
    ) -> esa20240910_models.SetCertificateResponse:
        """
        @summary Configures whether to enable certificates and update certificate information for a website.
        
        @param request: SetCertificateRequest
        @return: SetCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.set_certificate_with_options(request, runtime)

    async def set_certificate_async(
        self,
        request: esa20240910_models.SetCertificateRequest,
    ) -> esa20240910_models.SetCertificateResponse:
        """
        @summary Configures whether to enable certificates and update certificate information for a website.
        
        @param request: SetCertificateRequest
        @return: SetCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.set_certificate_with_options_async(request, runtime)

    def set_client_certificate_hostnames_with_options(
        self,
        tmp_req: esa20240910_models.SetClientCertificateHostnamesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetClientCertificateHostnamesResponse:
        """
        @summary 为客户端证书绑定域名
        
        @param tmp_req: SetClientCertificateHostnamesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetClientCertificateHostnamesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.SetClientCertificateHostnamesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hostnames):
            request.hostnames_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hostnames, 'Hostnames', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.hostnames_shrink):
            body['Hostnames'] = request.hostnames_shrink
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetClientCertificateHostnames',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetClientCertificateHostnamesResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_client_certificate_hostnames_with_options_async(
        self,
        tmp_req: esa20240910_models.SetClientCertificateHostnamesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetClientCertificateHostnamesResponse:
        """
        @summary 为客户端证书绑定域名
        
        @param tmp_req: SetClientCertificateHostnamesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetClientCertificateHostnamesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.SetClientCertificateHostnamesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hostnames):
            request.hostnames_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hostnames, 'Hostnames', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.hostnames_shrink):
            body['Hostnames'] = request.hostnames_shrink
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SetClientCertificateHostnames',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetClientCertificateHostnamesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_client_certificate_hostnames(
        self,
        request: esa20240910_models.SetClientCertificateHostnamesRequest,
    ) -> esa20240910_models.SetClientCertificateHostnamesResponse:
        """
        @summary 为客户端证书绑定域名
        
        @param request: SetClientCertificateHostnamesRequest
        @return: SetClientCertificateHostnamesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.set_client_certificate_hostnames_with_options(request, runtime)

    async def set_client_certificate_hostnames_async(
        self,
        request: esa20240910_models.SetClientCertificateHostnamesRequest,
    ) -> esa20240910_models.SetClientCertificateHostnamesResponse:
        """
        @summary 为客户端证书绑定域名
        
        @param request: SetClientCertificateHostnamesRequest
        @return: SetClientCertificateHostnamesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.set_client_certificate_hostnames_with_options_async(request, runtime)

    def set_http_ddo_sattack_intelligent_protection_with_options(
        self,
        request: esa20240910_models.SetHttpDDoSAttackIntelligentProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Configures smart HTTP DDoS protection.
        
        @param request: SetHttpDDoSAttackIntelligentProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetHttpDDoSAttackIntelligentProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.ai_mode):
            query['AiMode'] = request.ai_mode
        if not UtilClient.is_unset(request.ai_template):
            query['AiTemplate'] = request.ai_template
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SetHttpDDoSAttackIntelligentProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_http_ddo_sattack_intelligent_protection_with_options_async(
        self,
        request: esa20240910_models.SetHttpDDoSAttackIntelligentProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Configures smart HTTP DDoS protection.
        
        @param request: SetHttpDDoSAttackIntelligentProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetHttpDDoSAttackIntelligentProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.ai_mode):
            query['AiMode'] = request.ai_mode
        if not UtilClient.is_unset(request.ai_template):
            query['AiTemplate'] = request.ai_template
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SetHttpDDoSAttackIntelligentProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_http_ddo_sattack_intelligent_protection(
        self,
        request: esa20240910_models.SetHttpDDoSAttackIntelligentProtectionRequest,
    ) -> esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Configures smart HTTP DDoS protection.
        
        @param request: SetHttpDDoSAttackIntelligentProtectionRequest
        @return: SetHttpDDoSAttackIntelligentProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.set_http_ddo_sattack_intelligent_protection_with_options(request, runtime)

    async def set_http_ddo_sattack_intelligent_protection_async(
        self,
        request: esa20240910_models.SetHttpDDoSAttackIntelligentProtectionRequest,
    ) -> esa20240910_models.SetHttpDDoSAttackIntelligentProtectionResponse:
        """
        @summary Configures smart HTTP DDoS protection.
        
        @param request: SetHttpDDoSAttackIntelligentProtectionRequest
        @return: SetHttpDDoSAttackIntelligentProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.set_http_ddo_sattack_intelligent_protection_with_options_async(request, runtime)

    def set_http_ddo_sattack_protection_with_options(
        self,
        request: esa20240910_models.SetHttpDDoSAttackProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetHttpDDoSAttackProtectionResponse:
        """
        @summary Configures HTTP DDoS attack protection for a website.
        
        @param request: SetHttpDDoSAttackProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetHttpDDoSAttackProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.global_mode):
            query['GlobalMode'] = request.global_mode
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SetHttpDDoSAttackProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetHttpDDoSAttackProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def set_http_ddo_sattack_protection_with_options_async(
        self,
        request: esa20240910_models.SetHttpDDoSAttackProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.SetHttpDDoSAttackProtectionResponse:
        """
        @summary Configures HTTP DDoS attack protection for a website.
        
        @param request: SetHttpDDoSAttackProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SetHttpDDoSAttackProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.global_mode):
            query['GlobalMode'] = request.global_mode
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SetHttpDDoSAttackProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.SetHttpDDoSAttackProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def set_http_ddo_sattack_protection(
        self,
        request: esa20240910_models.SetHttpDDoSAttackProtectionRequest,
    ) -> esa20240910_models.SetHttpDDoSAttackProtectionResponse:
        """
        @summary Configures HTTP DDoS attack protection for a website.
        
        @param request: SetHttpDDoSAttackProtectionRequest
        @return: SetHttpDDoSAttackProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.set_http_ddo_sattack_protection_with_options(request, runtime)

    async def set_http_ddo_sattack_protection_async(
        self,
        request: esa20240910_models.SetHttpDDoSAttackProtectionRequest,
    ) -> esa20240910_models.SetHttpDDoSAttackProtectionResponse:
        """
        @summary Configures HTTP DDoS attack protection for a website.
        
        @param request: SetHttpDDoSAttackProtectionRequest
        @return: SetHttpDDoSAttackProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.set_http_ddo_sattack_protection_with_options_async(request, runtime)

    def start_scheduled_preload_execution_with_options(
        self,
        request: esa20240910_models.StartScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.StartScheduledPreloadExecutionResponse:
        """
        @summary Starts a scheduled prefetch plan based on the plan ID.
        
        @param request: StartScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: StartScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.StartScheduledPreloadExecutionResponse(),
            self.call_api(params, req, runtime)
        )

    async def start_scheduled_preload_execution_with_options_async(
        self,
        request: esa20240910_models.StartScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.StartScheduledPreloadExecutionResponse:
        """
        @summary Starts a scheduled prefetch plan based on the plan ID.
        
        @param request: StartScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: StartScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.StartScheduledPreloadExecutionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def start_scheduled_preload_execution(
        self,
        request: esa20240910_models.StartScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.StartScheduledPreloadExecutionResponse:
        """
        @summary Starts a scheduled prefetch plan based on the plan ID.
        
        @param request: StartScheduledPreloadExecutionRequest
        @return: StartScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.start_scheduled_preload_execution_with_options(request, runtime)

    async def start_scheduled_preload_execution_async(
        self,
        request: esa20240910_models.StartScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.StartScheduledPreloadExecutionResponse:
        """
        @summary Starts a scheduled prefetch plan based on the plan ID.
        
        @param request: StartScheduledPreloadExecutionRequest
        @return: StartScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.start_scheduled_preload_execution_with_options_async(request, runtime)

    def stop_scheduled_preload_execution_with_options(
        self,
        request: esa20240910_models.StopScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.StopScheduledPreloadExecutionResponse:
        """
        @summary Stops a scheduled prefetch plan based on the plan ID.
        
        @param request: StopScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: StopScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StopScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.StopScheduledPreloadExecutionResponse(),
            self.call_api(params, req, runtime)
        )

    async def stop_scheduled_preload_execution_with_options_async(
        self,
        request: esa20240910_models.StopScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.StopScheduledPreloadExecutionResponse:
        """
        @summary Stops a scheduled prefetch plan based on the plan ID.
        
        @param request: StopScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: StopScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StopScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.StopScheduledPreloadExecutionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def stop_scheduled_preload_execution(
        self,
        request: esa20240910_models.StopScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.StopScheduledPreloadExecutionResponse:
        """
        @summary Stops a scheduled prefetch plan based on the plan ID.
        
        @param request: StopScheduledPreloadExecutionRequest
        @return: StopScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.stop_scheduled_preload_execution_with_options(request, runtime)

    async def stop_scheduled_preload_execution_async(
        self,
        request: esa20240910_models.StopScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.StopScheduledPreloadExecutionResponse:
        """
        @summary Stops a scheduled prefetch plan based on the plan ID.
        
        @param request: StopScheduledPreloadExecutionRequest
        @return: StopScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.stop_scheduled_preload_execution_with_options_async(request, runtime)

    def untag_resources_with_options(
        self,
        request: esa20240910_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UntagResourcesResponse:
        """
        @summary Deletes a resource tag based on a specified resource ID.
        
        @param request: UntagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UntagResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UntagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def untag_resources_with_options_async(
        self,
        request: esa20240910_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UntagResourcesResponse:
        """
        @summary Deletes a resource tag based on a specified resource ID.
        
        @param request: UntagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UntagResourcesResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UntagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def untag_resources(
        self,
        request: esa20240910_models.UntagResourcesRequest,
    ) -> esa20240910_models.UntagResourcesResponse:
        """
        @summary Deletes a resource tag based on a specified resource ID.
        
        @param request: UntagResourcesRequest
        @return: UntagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.untag_resources_with_options(request, runtime)

    async def untag_resources_async(
        self,
        request: esa20240910_models.UntagResourcesRequest,
    ) -> esa20240910_models.UntagResourcesResponse:
        """
        @summary Deletes a resource tag based on a specified resource ID.
        
        @param request: UntagResourcesRequest
        @return: UntagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.untag_resources_with_options_async(request, runtime)

    def update_custom_scene_policy_with_options(
        self,
        request: esa20240910_models.UpdateCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateCustomScenePolicyResponse:
        """
        @summary Modifies the configurations of a custom scenario-specific policy.
        
        @param request: UpdateCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.objects):
            query['Objects'] = request.objects
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.template):
            query['Template'] = request.template
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateCustomScenePolicyResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_custom_scene_policy_with_options_async(
        self,
        request: esa20240910_models.UpdateCustomScenePolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateCustomScenePolicyResponse:
        """
        @summary Modifies the configurations of a custom scenario-specific policy.
        
        @param request: UpdateCustomScenePolicyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateCustomScenePolicyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.objects):
            query['Objects'] = request.objects
        if not UtilClient.is_unset(request.policy_id):
            query['PolicyId'] = request.policy_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.template):
            query['Template'] = request.template
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateCustomScenePolicy',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateCustomScenePolicyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_custom_scene_policy(
        self,
        request: esa20240910_models.UpdateCustomScenePolicyRequest,
    ) -> esa20240910_models.UpdateCustomScenePolicyResponse:
        """
        @summary Modifies the configurations of a custom scenario-specific policy.
        
        @param request: UpdateCustomScenePolicyRequest
        @return: UpdateCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_custom_scene_policy_with_options(request, runtime)

    async def update_custom_scene_policy_async(
        self,
        request: esa20240910_models.UpdateCustomScenePolicyRequest,
    ) -> esa20240910_models.UpdateCustomScenePolicyResponse:
        """
        @summary Modifies the configurations of a custom scenario-specific policy.
        
        @param request: UpdateCustomScenePolicyRequest
        @return: UpdateCustomScenePolicyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_custom_scene_policy_with_options_async(request, runtime)

    def update_kv_namespace_with_options(
        self,
        request: esa20240910_models.UpdateKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateKvNamespaceResponse:
        """
        @summary Updates the name of a namespace in Edge KV.
        
        @param request: UpdateKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.title):
            query['Title'] = request.title
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateKvNamespaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_kv_namespace_with_options_async(
        self,
        request: esa20240910_models.UpdateKvNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateKvNamespaceResponse:
        """
        @summary Updates the name of a namespace in Edge KV.
        
        @param request: UpdateKvNamespaceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateKvNamespaceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.title):
            query['Title'] = request.title
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateKvNamespace',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateKvNamespaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_kv_namespace(
        self,
        request: esa20240910_models.UpdateKvNamespaceRequest,
    ) -> esa20240910_models.UpdateKvNamespaceResponse:
        """
        @summary Updates the name of a namespace in Edge KV.
        
        @param request: UpdateKvNamespaceRequest
        @return: UpdateKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_kv_namespace_with_options(request, runtime)

    async def update_kv_namespace_async(
        self,
        request: esa20240910_models.UpdateKvNamespaceRequest,
    ) -> esa20240910_models.UpdateKvNamespaceResponse:
        """
        @summary Updates the name of a namespace in Edge KV.
        
        @param request: UpdateKvNamespaceRequest
        @return: UpdateKvNamespaceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_kv_namespace_with_options_async(request, runtime)

    def update_list_with_options(
        self,
        tmp_req: esa20240910_models.UpdateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateListResponse:
        """
        @summary Updates a custom list.
        
        @param tmp_req: UpdateListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.items):
            request.items_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.items, 'Items', 'json')
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.items_shrink):
            body['Items'] = request.items_shrink
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateListResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_list_with_options_async(
        self,
        tmp_req: esa20240910_models.UpdateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateListResponse:
        """
        @summary Updates a custom list.
        
        @param tmp_req: UpdateListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.items):
            request.items_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.items, 'Items', 'json')
        body = {}
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.items_shrink):
            body['Items'] = request.items_shrink
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_list(
        self,
        request: esa20240910_models.UpdateListRequest,
    ) -> esa20240910_models.UpdateListResponse:
        """
        @summary Updates a custom list.
        
        @param request: UpdateListRequest
        @return: UpdateListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_list_with_options(request, runtime)

    async def update_list_async(
        self,
        request: esa20240910_models.UpdateListRequest,
    ) -> esa20240910_models.UpdateListResponse:
        """
        @summary Updates a custom list.
        
        @param request: UpdateListRequest
        @return: UpdateListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_list_with_options_async(request, runtime)

    def update_origin_protection_with_options(
        self,
        request: esa20240910_models.UpdateOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateOriginProtectionResponse:
        """
        @summary Enables or disables IP convergence.
        
        @param request: UpdateOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.origin_converge):
            query['OriginConverge'] = request.origin_converge
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateOriginProtectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_origin_protection_with_options_async(
        self,
        request: esa20240910_models.UpdateOriginProtectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateOriginProtectionResponse:
        """
        @summary Enables or disables IP convergence.
        
        @param request: UpdateOriginProtectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateOriginProtectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.origin_converge):
            query['OriginConverge'] = request.origin_converge
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateOriginProtection',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateOriginProtectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_origin_protection(
        self,
        request: esa20240910_models.UpdateOriginProtectionRequest,
    ) -> esa20240910_models.UpdateOriginProtectionResponse:
        """
        @summary Enables or disables IP convergence.
        
        @param request: UpdateOriginProtectionRequest
        @return: UpdateOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_origin_protection_with_options(request, runtime)

    async def update_origin_protection_async(
        self,
        request: esa20240910_models.UpdateOriginProtectionRequest,
    ) -> esa20240910_models.UpdateOriginProtectionResponse:
        """
        @summary Enables or disables IP convergence.
        
        @param request: UpdateOriginProtectionRequest
        @return: UpdateOriginProtectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_origin_protection_with_options_async(request, runtime)

    def update_origin_protection_ip_white_list_with_options(
        self,
        request: esa20240910_models.UpdateOriginProtectionIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateOriginProtectionIpWhiteListResponse:
        """
        @summary Updates the IP whitelist for origin protection used by a website to the latest version.
        
        @param request: UpdateOriginProtectionIpWhiteListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateOriginProtectionIpWhiteListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateOriginProtectionIpWhiteList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateOriginProtectionIpWhiteListResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_origin_protection_ip_white_list_with_options_async(
        self,
        request: esa20240910_models.UpdateOriginProtectionIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateOriginProtectionIpWhiteListResponse:
        """
        @summary Updates the IP whitelist for origin protection used by a website to the latest version.
        
        @param request: UpdateOriginProtectionIpWhiteListRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateOriginProtectionIpWhiteListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateOriginProtectionIpWhiteList',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateOriginProtectionIpWhiteListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_origin_protection_ip_white_list(
        self,
        request: esa20240910_models.UpdateOriginProtectionIpWhiteListRequest,
    ) -> esa20240910_models.UpdateOriginProtectionIpWhiteListResponse:
        """
        @summary Updates the IP whitelist for origin protection used by a website to the latest version.
        
        @param request: UpdateOriginProtectionIpWhiteListRequest
        @return: UpdateOriginProtectionIpWhiteListResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_origin_protection_ip_white_list_with_options(request, runtime)

    async def update_origin_protection_ip_white_list_async(
        self,
        request: esa20240910_models.UpdateOriginProtectionIpWhiteListRequest,
    ) -> esa20240910_models.UpdateOriginProtectionIpWhiteListResponse:
        """
        @summary Updates the IP whitelist for origin protection used by a website to the latest version.
        
        @param request: UpdateOriginProtectionIpWhiteListRequest
        @return: UpdateOriginProtectionIpWhiteListResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_origin_protection_ip_white_list_with_options_async(request, runtime)

    def update_page_with_options(
        self,
        request: esa20240910_models.UpdatePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdatePageResponse:
        """
        @summary Modifies the configurations of a custom error page, such as the name, description, content type, and content of the page.
        
        @param request: UpdatePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdatePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.content_type):
            body['ContentType'] = request.content_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdatePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdatePageResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_page_with_options_async(
        self,
        request: esa20240910_models.UpdatePageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdatePageResponse:
        """
        @summary Modifies the configurations of a custom error page, such as the name, description, content type, and content of the page.
        
        @param request: UpdatePageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdatePageResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['Content'] = request.content
        if not UtilClient.is_unset(request.content_type):
            body['ContentType'] = request.content_type
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdatePage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdatePageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_page(
        self,
        request: esa20240910_models.UpdatePageRequest,
    ) -> esa20240910_models.UpdatePageResponse:
        """
        @summary Modifies the configurations of a custom error page, such as the name, description, content type, and content of the page.
        
        @param request: UpdatePageRequest
        @return: UpdatePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_page_with_options(request, runtime)

    async def update_page_async(
        self,
        request: esa20240910_models.UpdatePageRequest,
    ) -> esa20240910_models.UpdatePageResponse:
        """
        @summary Modifies the configurations of a custom error page, such as the name, description, content type, and content of the page.
        
        @param request: UpdatePageRequest
        @return: UpdatePageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_page_with_options_async(request, runtime)

    def update_record_with_options(
        self,
        tmp_req: esa20240910_models.UpdateRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateRecordResponse:
        """
        @summary Updates multiple types of DNS records and origin authentication configurations.
        
        @description This operation allows you to update multiple types of DNS records, including but not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. You can modify the record content by providing the necessary fields such as Value, Priority, and Flag. For origins added in CNAME records such as OSS and S3, the API enables you to configure authentication details to ensure secure access.
        ### [](#)Usage notes
        The record value (Value) must match the record type. For example, the CNAME record should correspond to the target domain name.
        You must specify a priority (Priority) for some record types, such as MX and SRV.
        You must specify specific fields such as Flag and Tag for CAA records.
        When you update security records such as CERT and SSHFP, you must accurately set fields such as Type and Algorithm.
        If your origin type is OSS or S3, configure the authentication details in AuthConf based on the permissions.
        
        @param tmp_req: UpdateRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateRecordResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateRecordShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.auth_conf):
            request.auth_conf_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.auth_conf, 'AuthConf', 'json')
        if not UtilClient.is_unset(tmp_req.data):
            request.data_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.data, 'Data', 'json')
        query = {}
        if not UtilClient.is_unset(request.auth_conf_shrink):
            query['AuthConf'] = request.auth_conf_shrink
        if not UtilClient.is_unset(request.biz_name):
            query['BizName'] = request.biz_name
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.data_shrink):
            query['Data'] = request.data_shrink
        if not UtilClient.is_unset(request.host_policy):
            query['HostPolicy'] = request.host_policy
        if not UtilClient.is_unset(request.proxied):
            query['Proxied'] = request.proxied
        if not UtilClient.is_unset(request.record_id):
            query['RecordId'] = request.record_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.ttl):
            query['Ttl'] = request.ttl
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateRecordResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_record_with_options_async(
        self,
        tmp_req: esa20240910_models.UpdateRecordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateRecordResponse:
        """
        @summary Updates multiple types of DNS records and origin authentication configurations.
        
        @description This operation allows you to update multiple types of DNS records, including but not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. You can modify the record content by providing the necessary fields such as Value, Priority, and Flag. For origins added in CNAME records such as OSS and S3, the API enables you to configure authentication details to ensure secure access.
        ### [](#)Usage notes
        The record value (Value) must match the record type. For example, the CNAME record should correspond to the target domain name.
        You must specify a priority (Priority) for some record types, such as MX and SRV.
        You must specify specific fields such as Flag and Tag for CAA records.
        When you update security records such as CERT and SSHFP, you must accurately set fields such as Type and Algorithm.
        If your origin type is OSS or S3, configure the authentication details in AuthConf based on the permissions.
        
        @param tmp_req: UpdateRecordRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateRecordResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateRecordShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.auth_conf):
            request.auth_conf_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.auth_conf, 'AuthConf', 'json')
        if not UtilClient.is_unset(tmp_req.data):
            request.data_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.data, 'Data', 'json')
        query = {}
        if not UtilClient.is_unset(request.auth_conf_shrink):
            query['AuthConf'] = request.auth_conf_shrink
        if not UtilClient.is_unset(request.biz_name):
            query['BizName'] = request.biz_name
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.data_shrink):
            query['Data'] = request.data_shrink
        if not UtilClient.is_unset(request.host_policy):
            query['HostPolicy'] = request.host_policy
        if not UtilClient.is_unset(request.proxied):
            query['Proxied'] = request.proxied
        if not UtilClient.is_unset(request.record_id):
            query['RecordId'] = request.record_id
        if not UtilClient.is_unset(request.source_type):
            query['SourceType'] = request.source_type
        if not UtilClient.is_unset(request.ttl):
            query['Ttl'] = request.ttl
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateRecord',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateRecordResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_record(
        self,
        request: esa20240910_models.UpdateRecordRequest,
    ) -> esa20240910_models.UpdateRecordResponse:
        """
        @summary Updates multiple types of DNS records and origin authentication configurations.
        
        @description This operation allows you to update multiple types of DNS records, including but not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. You can modify the record content by providing the necessary fields such as Value, Priority, and Flag. For origins added in CNAME records such as OSS and S3, the API enables you to configure authentication details to ensure secure access.
        ### [](#)Usage notes
        The record value (Value) must match the record type. For example, the CNAME record should correspond to the target domain name.
        You must specify a priority (Priority) for some record types, such as MX and SRV.
        You must specify specific fields such as Flag and Tag for CAA records.
        When you update security records such as CERT and SSHFP, you must accurately set fields such as Type and Algorithm.
        If your origin type is OSS or S3, configure the authentication details in AuthConf based on the permissions.
        
        @param request: UpdateRecordRequest
        @return: UpdateRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_record_with_options(request, runtime)

    async def update_record_async(
        self,
        request: esa20240910_models.UpdateRecordRequest,
    ) -> esa20240910_models.UpdateRecordResponse:
        """
        @summary Updates multiple types of DNS records and origin authentication configurations.
        
        @description This operation allows you to update multiple types of DNS records, including but not limited to A/AAAA, CNAME, NS, MX, TXT, CAA, SRV, and URI. You can modify the record content by providing the necessary fields such as Value, Priority, and Flag. For origins added in CNAME records such as OSS and S3, the API enables you to configure authentication details to ensure secure access.
        ### [](#)Usage notes
        The record value (Value) must match the record type. For example, the CNAME record should correspond to the target domain name.
        You must specify a priority (Priority) for some record types, such as MX and SRV.
        You must specify specific fields such as Flag and Tag for CAA records.
        When you update security records such as CERT and SSHFP, you must accurately set fields such as Type and Algorithm.
        If your origin type is OSS or S3, configure the authentication details in AuthConf based on the permissions.
        
        @param request: UpdateRecordRequest
        @return: UpdateRecordResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_record_with_options_async(request, runtime)

    def update_scheduled_preload_execution_with_options(
        self,
        request: esa20240910_models.UpdateScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateScheduledPreloadExecutionResponse:
        """
        @summary Updates a scheduled prefetch plan based on the plan ID.
        
        @param request: UpdateScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        body = {}
        if not UtilClient.is_unset(request.end_time):
            body['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.interval):
            body['Interval'] = request.interval
        if not UtilClient.is_unset(request.slice_len):
            body['SliceLen'] = request.slice_len
        if not UtilClient.is_unset(request.start_time):
            body['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateScheduledPreloadExecutionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_scheduled_preload_execution_with_options_async(
        self,
        request: esa20240910_models.UpdateScheduledPreloadExecutionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateScheduledPreloadExecutionResponse:
        """
        @summary Updates a scheduled prefetch plan based on the plan ID.
        
        @param request: UpdateScheduledPreloadExecutionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateScheduledPreloadExecutionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        body = {}
        if not UtilClient.is_unset(request.end_time):
            body['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.interval):
            body['Interval'] = request.interval
        if not UtilClient.is_unset(request.slice_len):
            body['SliceLen'] = request.slice_len
        if not UtilClient.is_unset(request.start_time):
            body['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateScheduledPreloadExecution',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateScheduledPreloadExecutionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_scheduled_preload_execution(
        self,
        request: esa20240910_models.UpdateScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.UpdateScheduledPreloadExecutionResponse:
        """
        @summary Updates a scheduled prefetch plan based on the plan ID.
        
        @param request: UpdateScheduledPreloadExecutionRequest
        @return: UpdateScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_scheduled_preload_execution_with_options(request, runtime)

    async def update_scheduled_preload_execution_async(
        self,
        request: esa20240910_models.UpdateScheduledPreloadExecutionRequest,
    ) -> esa20240910_models.UpdateScheduledPreloadExecutionResponse:
        """
        @summary Updates a scheduled prefetch plan based on the plan ID.
        
        @param request: UpdateScheduledPreloadExecutionRequest
        @return: UpdateScheduledPreloadExecutionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_scheduled_preload_execution_with_options_async(request, runtime)

    def update_site_access_type_with_options(
        self,
        request: esa20240910_models.UpdateSiteAccessTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteAccessTypeResponse:
        """
        @summary Converts the DNS setup option of a website.
        
        @description When you change the DNS setup of a website from NS to CNAME, take note of the following items:
        Make sure that the website has only proxied A/AAAA and CNAME records.
        Make sure that ESA proxy is not disabled for the website and custom nameservers are not configured.
        
        @param request: UpdateSiteAccessTypeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteAccessTypeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_type):
            query['AccessType'] = request.access_type
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteAccessType',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteAccessTypeResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_access_type_with_options_async(
        self,
        request: esa20240910_models.UpdateSiteAccessTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteAccessTypeResponse:
        """
        @summary Converts the DNS setup option of a website.
        
        @description When you change the DNS setup of a website from NS to CNAME, take note of the following items:
        Make sure that the website has only proxied A/AAAA and CNAME records.
        Make sure that ESA proxy is not disabled for the website and custom nameservers are not configured.
        
        @param request: UpdateSiteAccessTypeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteAccessTypeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_type):
            query['AccessType'] = request.access_type
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteAccessType',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteAccessTypeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_access_type(
        self,
        request: esa20240910_models.UpdateSiteAccessTypeRequest,
    ) -> esa20240910_models.UpdateSiteAccessTypeResponse:
        """
        @summary Converts the DNS setup option of a website.
        
        @description When you change the DNS setup of a website from NS to CNAME, take note of the following items:
        Make sure that the website has only proxied A/AAAA and CNAME records.
        Make sure that ESA proxy is not disabled for the website and custom nameservers are not configured.
        
        @param request: UpdateSiteAccessTypeRequest
        @return: UpdateSiteAccessTypeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_access_type_with_options(request, runtime)

    async def update_site_access_type_async(
        self,
        request: esa20240910_models.UpdateSiteAccessTypeRequest,
    ) -> esa20240910_models.UpdateSiteAccessTypeResponse:
        """
        @summary Converts the DNS setup option of a website.
        
        @description When you change the DNS setup of a website from NS to CNAME, take note of the following items:
        Make sure that the website has only proxied A/AAAA and CNAME records.
        Make sure that ESA proxy is not disabled for the website and custom nameservers are not configured.
        
        @param request: UpdateSiteAccessTypeRequest
        @return: UpdateSiteAccessTypeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_access_type_with_options_async(request, runtime)

    def update_site_coverage_with_options(
        self,
        request: esa20240910_models.UpdateSiteCoverageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteCoverageResponse:
        """
        @summary Modifies the service location for a single website. This updates the acceleration configuration of the website to adapt to changes in traffic distribution, and improve user experience in specific regions.
        
        @param request: UpdateSiteCoverageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteCoverageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.coverage):
            query['Coverage'] = request.coverage
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteCoverage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteCoverageResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_coverage_with_options_async(
        self,
        request: esa20240910_models.UpdateSiteCoverageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteCoverageResponse:
        """
        @summary Modifies the service location for a single website. This updates the acceleration configuration of the website to adapt to changes in traffic distribution, and improve user experience in specific regions.
        
        @param request: UpdateSiteCoverageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteCoverageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.coverage):
            query['Coverage'] = request.coverage
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteCoverage',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteCoverageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_coverage(
        self,
        request: esa20240910_models.UpdateSiteCoverageRequest,
    ) -> esa20240910_models.UpdateSiteCoverageResponse:
        """
        @summary Modifies the service location for a single website. This updates the acceleration configuration of the website to adapt to changes in traffic distribution, and improve user experience in specific regions.
        
        @param request: UpdateSiteCoverageRequest
        @return: UpdateSiteCoverageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_coverage_with_options(request, runtime)

    async def update_site_coverage_async(
        self,
        request: esa20240910_models.UpdateSiteCoverageRequest,
    ) -> esa20240910_models.UpdateSiteCoverageResponse:
        """
        @summary Modifies the service location for a single website. This updates the acceleration configuration of the website to adapt to changes in traffic distribution, and improve user experience in specific regions.
        
        @param request: UpdateSiteCoverageRequest
        @return: UpdateSiteCoverageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_coverage_with_options_async(request, runtime)

    def update_site_custom_log_with_options(
        self,
        tmp_req: esa20240910_models.UpdateSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteCustomLogResponse:
        """
        @summary Modifies the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @param tmp_req: UpdateSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteCustomLogResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateSiteCustomLogShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cookies):
            request.cookies_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cookies, 'Cookies', 'json')
        if not UtilClient.is_unset(tmp_req.request_headers):
            request.request_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.request_headers, 'RequestHeaders', 'json')
        if not UtilClient.is_unset(tmp_req.response_headers):
            request.response_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.response_headers, 'ResponseHeaders', 'json')
        body = {}
        if not UtilClient.is_unset(request.cookies_shrink):
            body['Cookies'] = request.cookies_shrink
        if not UtilClient.is_unset(request.request_headers_shrink):
            body['RequestHeaders'] = request.request_headers_shrink
        if not UtilClient.is_unset(request.response_headers_shrink):
            body['ResponseHeaders'] = request.response_headers_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteCustomLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_custom_log_with_options_async(
        self,
        tmp_req: esa20240910_models.UpdateSiteCustomLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteCustomLogResponse:
        """
        @summary Modifies the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @param tmp_req: UpdateSiteCustomLogRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteCustomLogResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateSiteCustomLogShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cookies):
            request.cookies_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cookies, 'Cookies', 'json')
        if not UtilClient.is_unset(tmp_req.request_headers):
            request.request_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.request_headers, 'RequestHeaders', 'json')
        if not UtilClient.is_unset(tmp_req.response_headers):
            request.response_headers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.response_headers, 'ResponseHeaders', 'json')
        body = {}
        if not UtilClient.is_unset(request.cookies_shrink):
            body['Cookies'] = request.cookies_shrink
        if not UtilClient.is_unset(request.request_headers_shrink):
            body['RequestHeaders'] = request.request_headers_shrink
        if not UtilClient.is_unset(request.response_headers_shrink):
            body['ResponseHeaders'] = request.response_headers_shrink
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateSiteCustomLog',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteCustomLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_custom_log(
        self,
        request: esa20240910_models.UpdateSiteCustomLogRequest,
    ) -> esa20240910_models.UpdateSiteCustomLogResponse:
        """
        @summary Modifies the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @param request: UpdateSiteCustomLogRequest
        @return: UpdateSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_custom_log_with_options(request, runtime)

    async def update_site_custom_log_async(
        self,
        request: esa20240910_models.UpdateSiteCustomLogRequest,
    ) -> esa20240910_models.UpdateSiteCustomLogResponse:
        """
        @summary Modifies the configuration of custom request header, response header, and cookie fields that are used to capture logs of a website.
        
        @param request: UpdateSiteCustomLogRequest
        @return: UpdateSiteCustomLogResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_custom_log_with_options_async(request, runtime)

    def update_site_delivery_task_with_options(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskResponse:
        """
        @summary Modifies a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_delivery_task_with_options_async(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskResponse:
        """
        @summary Modifies a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.site_id):
            body['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateSiteDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_delivery_task(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskRequest,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskResponse:
        """
        @summary Modifies a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskRequest
        @return: UpdateSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_delivery_task_with_options(request, runtime)

    async def update_site_delivery_task_async(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskRequest,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskResponse:
        """
        @summary Modifies a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskRequest
        @return: UpdateSiteDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_delivery_task_with_options_async(request, runtime)

    def update_site_delivery_task_status_with_options(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteDeliveryTaskStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteDeliveryTaskStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteDeliveryTaskStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_delivery_task_status_with_options_async(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteDeliveryTaskStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteDeliveryTaskStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteDeliveryTaskStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_delivery_task_status(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskStatusRequest,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskStatusRequest
        @return: UpdateSiteDeliveryTaskStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_delivery_task_status_with_options(request, runtime)

    async def update_site_delivery_task_status_async(
        self,
        request: esa20240910_models.UpdateSiteDeliveryTaskStatusRequest,
    ) -> esa20240910_models.UpdateSiteDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a real-time log delivery task.
        
        @param request: UpdateSiteDeliveryTaskStatusRequest
        @return: UpdateSiteDeliveryTaskStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_delivery_task_status_with_options_async(request, runtime)

    def update_site_vanity_nswith_options(
        self,
        request: esa20240910_models.UpdateSiteVanityNSRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteVanityNSResponse:
        """
        @summary Updates the custom nameserver names for a single website.
        
        @param request: UpdateSiteVanityNSRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteVanityNSResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.vanity_nslist):
            query['VanityNSList'] = request.vanity_nslist
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteVanityNS',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteVanityNSResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_site_vanity_nswith_options_async(
        self,
        request: esa20240910_models.UpdateSiteVanityNSRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateSiteVanityNSResponse:
        """
        @summary Updates the custom nameserver names for a single website.
        
        @param request: UpdateSiteVanityNSRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateSiteVanityNSResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.vanity_nslist):
            query['VanityNSList'] = request.vanity_nslist
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateSiteVanityNS',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateSiteVanityNSResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_site_vanity_ns(
        self,
        request: esa20240910_models.UpdateSiteVanityNSRequest,
    ) -> esa20240910_models.UpdateSiteVanityNSResponse:
        """
        @summary Updates the custom nameserver names for a single website.
        
        @param request: UpdateSiteVanityNSRequest
        @return: UpdateSiteVanityNSResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_site_vanity_nswith_options(request, runtime)

    async def update_site_vanity_ns_async(
        self,
        request: esa20240910_models.UpdateSiteVanityNSRequest,
    ) -> esa20240910_models.UpdateSiteVanityNSResponse:
        """
        @summary Updates the custom nameserver names for a single website.
        
        @param request: UpdateSiteVanityNSRequest
        @return: UpdateSiteVanityNSResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_site_vanity_nswith_options_async(request, runtime)

    def update_user_delivery_task_with_options(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateUserDeliveryTaskResponse:
        """
        @summary Modifies the configurations of a delivery task, including the task name, log field, log category, and discard rate.
        
        @param request: UpdateUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateUserDeliveryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_user_delivery_task_with_options_async(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateUserDeliveryTaskResponse:
        """
        @summary Modifies the configurations of a delivery task, including the task name, log field, log category, and discard rate.
        
        @param request: UpdateUserDeliveryTaskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateUserDeliveryTaskResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.business_type):
            body['BusinessType'] = request.business_type
        if not UtilClient.is_unset(request.discard_rate):
            body['DiscardRate'] = request.discard_rate
        if not UtilClient.is_unset(request.field_name):
            body['FieldName'] = request.field_name
        if not UtilClient.is_unset(request.task_name):
            body['TaskName'] = request.task_name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateUserDeliveryTask',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateUserDeliveryTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_user_delivery_task(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskRequest,
    ) -> esa20240910_models.UpdateUserDeliveryTaskResponse:
        """
        @summary Modifies the configurations of a delivery task, including the task name, log field, log category, and discard rate.
        
        @param request: UpdateUserDeliveryTaskRequest
        @return: UpdateUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_user_delivery_task_with_options(request, runtime)

    async def update_user_delivery_task_async(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskRequest,
    ) -> esa20240910_models.UpdateUserDeliveryTaskResponse:
        """
        @summary Modifies the configurations of a delivery task, including the task name, log field, log category, and discard rate.
        
        @param request: UpdateUserDeliveryTaskRequest
        @return: UpdateUserDeliveryTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_user_delivery_task_with_options_async(request, runtime)

    def update_user_delivery_task_status_with_options(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateUserDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a delivery task in your Alibaba Cloud account.
        
        @description ## [](#)
        You can call this operation to enable or disable a delivery task by using TaskName and Method. The response includes the most recent status and operation result details of the task.
        
        @param request: UpdateUserDeliveryTaskStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateUserDeliveryTaskStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateUserDeliveryTaskStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateUserDeliveryTaskStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_user_delivery_task_status_with_options_async(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateUserDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a delivery task in your Alibaba Cloud account.
        
        @description ## [](#)
        You can call this operation to enable or disable a delivery task by using TaskName and Method. The response includes the most recent status and operation result details of the task.
        
        @param request: UpdateUserDeliveryTaskStatusRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateUserDeliveryTaskStatusResponse
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateUserDeliveryTaskStatus',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateUserDeliveryTaskStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_user_delivery_task_status(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskStatusRequest,
    ) -> esa20240910_models.UpdateUserDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a delivery task in your Alibaba Cloud account.
        
        @description ## [](#)
        You can call this operation to enable or disable a delivery task by using TaskName and Method. The response includes the most recent status and operation result details of the task.
        
        @param request: UpdateUserDeliveryTaskStatusRequest
        @return: UpdateUserDeliveryTaskStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_user_delivery_task_status_with_options(request, runtime)

    async def update_user_delivery_task_status_async(
        self,
        request: esa20240910_models.UpdateUserDeliveryTaskStatusRequest,
    ) -> esa20240910_models.UpdateUserDeliveryTaskStatusResponse:
        """
        @summary Changes the status of a delivery task in your Alibaba Cloud account.
        
        @description ## [](#)
        You can call this operation to enable or disable a delivery task by using TaskName and Method. The response includes the most recent status and operation result details of the task.
        
        @param request: UpdateUserDeliveryTaskStatusRequest
        @return: UpdateUserDeliveryTaskStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_user_delivery_task_status_with_options_async(request, runtime)

    def update_waf_rule_with_options(
        self,
        tmp_req: esa20240910_models.UpdateWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWafRuleResponse:
        """
        @summary Modifies the configuration or status of a Web Application Firewall (WAF) rule.
        
        @param tmp_req: UpdateWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWafRuleResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateWafRuleShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.config):
            request.config_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.config, 'Config', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.config_shrink):
            body['Config'] = request.config_shrink
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.position):
            body['Position'] = request.position
        if not UtilClient.is_unset(request.status):
            body['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWafRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_waf_rule_with_options_async(
        self,
        tmp_req: esa20240910_models.UpdateWafRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWafRuleResponse:
        """
        @summary Modifies the configuration or status of a Web Application Firewall (WAF) rule.
        
        @param tmp_req: UpdateWafRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWafRuleResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateWafRuleShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.config):
            request.config_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.config, 'Config', 'json')
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.config_shrink):
            body['Config'] = request.config_shrink
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.position):
            body['Position'] = request.position
        if not UtilClient.is_unset(request.status):
            body['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWafRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWafRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_waf_rule(
        self,
        request: esa20240910_models.UpdateWafRuleRequest,
    ) -> esa20240910_models.UpdateWafRuleResponse:
        """
        @summary Modifies the configuration or status of a Web Application Firewall (WAF) rule.
        
        @param request: UpdateWafRuleRequest
        @return: UpdateWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_waf_rule_with_options(request, runtime)

    async def update_waf_rule_async(
        self,
        request: esa20240910_models.UpdateWafRuleRequest,
    ) -> esa20240910_models.UpdateWafRuleResponse:
        """
        @summary Modifies the configuration or status of a Web Application Firewall (WAF) rule.
        
        @param request: UpdateWafRuleRequest
        @return: UpdateWafRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_waf_rule_with_options_async(request, runtime)

    def update_waf_ruleset_with_options(
        self,
        request: esa20240910_models.UpdateWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWafRulesetResponse:
        """
        @summary Updates a WAF ruleset based on its ID.
        
        @param request: UpdateWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.status):
            body['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWafRulesetResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_waf_ruleset_with_options_async(
        self,
        request: esa20240910_models.UpdateWafRulesetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWafRulesetResponse:
        """
        @summary Updates a WAF ruleset based on its ID.
        
        @param request: UpdateWafRulesetRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWafRulesetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.site_version):
            query['SiteVersion'] = request.site_version
        body = {}
        if not UtilClient.is_unset(request.id):
            body['Id'] = request.id
        if not UtilClient.is_unset(request.status):
            body['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateWafRuleset',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWafRulesetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_waf_ruleset(
        self,
        request: esa20240910_models.UpdateWafRulesetRequest,
    ) -> esa20240910_models.UpdateWafRulesetResponse:
        """
        @summary Updates a WAF ruleset based on its ID.
        
        @param request: UpdateWafRulesetRequest
        @return: UpdateWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_waf_ruleset_with_options(request, runtime)

    async def update_waf_ruleset_async(
        self,
        request: esa20240910_models.UpdateWafRulesetRequest,
    ) -> esa20240910_models.UpdateWafRulesetResponse:
        """
        @summary Updates a WAF ruleset based on its ID.
        
        @param request: UpdateWafRulesetRequest
        @return: UpdateWafRulesetResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_waf_ruleset_with_options_async(request, runtime)

    def update_waiting_room_with_options(
        self,
        tmp_req: esa20240910_models.UpdateWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomResponse:
        """
        @summary Modifies the configurations of a waiting room.
        
        @param tmp_req: UpdateWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateWaitingRoomShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.host_name_and_path):
            request.host_name_and_path_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.host_name_and_path, 'HostNameAndPath', 'json')
        query = {}
        if not UtilClient.is_unset(request.cookie_name):
            query['CookieName'] = request.cookie_name
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.host_name_and_path_shrink):
            query['HostNameAndPath'] = request.host_name_and_path_shrink
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.queue_all_enable):
            query['QueueAllEnable'] = request.queue_all_enable
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_waiting_room_with_options_async(
        self,
        tmp_req: esa20240910_models.UpdateWaitingRoomRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomResponse:
        """
        @summary Modifies the configurations of a waiting room.
        
        @param tmp_req: UpdateWaitingRoomRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomResponse
        """
        UtilClient.validate_model(tmp_req)
        request = esa20240910_models.UpdateWaitingRoomShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.host_name_and_path):
            request.host_name_and_path_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.host_name_and_path, 'HostNameAndPath', 'json')
        query = {}
        if not UtilClient.is_unset(request.cookie_name):
            query['CookieName'] = request.cookie_name
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.host_name_and_path_shrink):
            query['HostNameAndPath'] = request.host_name_and_path_shrink
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.queue_all_enable):
            query['QueueAllEnable'] = request.queue_all_enable
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_id):
            query['WaitingRoomId'] = request.waiting_room_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoom',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_waiting_room(
        self,
        request: esa20240910_models.UpdateWaitingRoomRequest,
    ) -> esa20240910_models.UpdateWaitingRoomResponse:
        """
        @summary Modifies the configurations of a waiting room.
        
        @param request: UpdateWaitingRoomRequest
        @return: UpdateWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_waiting_room_with_options(request, runtime)

    async def update_waiting_room_async(
        self,
        request: esa20240910_models.UpdateWaitingRoomRequest,
    ) -> esa20240910_models.UpdateWaitingRoomResponse:
        """
        @summary Modifies the configurations of a waiting room.
        
        @param request: UpdateWaitingRoomRequest
        @return: UpdateWaitingRoomResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_waiting_room_with_options_async(request, runtime)

    def update_waiting_room_event_with_options(
        self,
        request: esa20240910_models.UpdateWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomEventResponse:
        """
        @summary Modifies the configurations of a waiting room event.
        
        @param request: UpdateWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.pre_queue_enable):
            query['PreQueueEnable'] = request.pre_queue_enable
        if not UtilClient.is_unset(request.pre_queue_start_time):
            query['PreQueueStartTime'] = request.pre_queue_start_time
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.random_pre_queue_enable):
            query['RandomPreQueueEnable'] = request.random_pre_queue_enable
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_event_id):
            query['WaitingRoomEventId'] = request.waiting_room_event_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomEventResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_waiting_room_event_with_options_async(
        self,
        request: esa20240910_models.UpdateWaitingRoomEventRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomEventResponse:
        """
        @summary Modifies the configurations of a waiting room event.
        
        @param request: UpdateWaitingRoomEventRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomEventResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.custom_page_html):
            query['CustomPageHtml'] = request.custom_page_html
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.disable_session_renewal_enable):
            query['DisableSessionRenewalEnable'] = request.disable_session_renewal_enable
        if not UtilClient.is_unset(request.enable):
            query['Enable'] = request.enable
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.json_response_enable):
            query['JsonResponseEnable'] = request.json_response_enable
        if not UtilClient.is_unset(request.language):
            query['Language'] = request.language
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.new_users_per_minute):
            query['NewUsersPerMinute'] = request.new_users_per_minute
        if not UtilClient.is_unset(request.pre_queue_enable):
            query['PreQueueEnable'] = request.pre_queue_enable
        if not UtilClient.is_unset(request.pre_queue_start_time):
            query['PreQueueStartTime'] = request.pre_queue_start_time
        if not UtilClient.is_unset(request.queuing_method):
            query['QueuingMethod'] = request.queuing_method
        if not UtilClient.is_unset(request.queuing_status_code):
            query['QueuingStatusCode'] = request.queuing_status_code
        if not UtilClient.is_unset(request.random_pre_queue_enable):
            query['RandomPreQueueEnable'] = request.random_pre_queue_enable
        if not UtilClient.is_unset(request.session_duration):
            query['SessionDuration'] = request.session_duration
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.total_active_users):
            query['TotalActiveUsers'] = request.total_active_users
        if not UtilClient.is_unset(request.waiting_room_event_id):
            query['WaitingRoomEventId'] = request.waiting_room_event_id
        if not UtilClient.is_unset(request.waiting_room_type):
            query['WaitingRoomType'] = request.waiting_room_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoomEvent',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomEventResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_waiting_room_event(
        self,
        request: esa20240910_models.UpdateWaitingRoomEventRequest,
    ) -> esa20240910_models.UpdateWaitingRoomEventResponse:
        """
        @summary Modifies the configurations of a waiting room event.
        
        @param request: UpdateWaitingRoomEventRequest
        @return: UpdateWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_waiting_room_event_with_options(request, runtime)

    async def update_waiting_room_event_async(
        self,
        request: esa20240910_models.UpdateWaitingRoomEventRequest,
    ) -> esa20240910_models.UpdateWaitingRoomEventResponse:
        """
        @summary Modifies the configurations of a waiting room event.
        
        @param request: UpdateWaitingRoomEventRequest
        @return: UpdateWaitingRoomEventResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_waiting_room_event_with_options_async(request, runtime)

    def update_waiting_room_rule_with_options(
        self,
        request: esa20240910_models.UpdateWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomRuleResponse:
        """
        @summary Updates the configurations of a waiting room bypass rule for a website.
        
        @description You can call this API operation to modify the configurations of a waiting room bypass rule for your website, including the rule name, status, and rule content.
        
        @param request: UpdateWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.rule):
            query['Rule'] = request.rule
        if not UtilClient.is_unset(request.rule_enable):
            query['RuleEnable'] = request.rule_enable
        if not UtilClient.is_unset(request.rule_name):
            query['RuleName'] = request.rule_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_rule_id):
            query['WaitingRoomRuleId'] = request.waiting_room_rule_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_waiting_room_rule_with_options_async(
        self,
        request: esa20240910_models.UpdateWaitingRoomRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UpdateWaitingRoomRuleResponse:
        """
        @summary Updates the configurations of a waiting room bypass rule for a website.
        
        @description You can call this API operation to modify the configurations of a waiting room bypass rule for your website, including the rule name, status, and rule content.
        
        @param request: UpdateWaitingRoomRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateWaitingRoomRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.rule):
            query['Rule'] = request.rule
        if not UtilClient.is_unset(request.rule_enable):
            query['RuleEnable'] = request.rule_enable
        if not UtilClient.is_unset(request.rule_name):
            query['RuleName'] = request.rule_name
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.waiting_room_rule_id):
            query['WaitingRoomRuleId'] = request.waiting_room_rule_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateWaitingRoomRule',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UpdateWaitingRoomRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_waiting_room_rule(
        self,
        request: esa20240910_models.UpdateWaitingRoomRuleRequest,
    ) -> esa20240910_models.UpdateWaitingRoomRuleResponse:
        """
        @summary Updates the configurations of a waiting room bypass rule for a website.
        
        @description You can call this API operation to modify the configurations of a waiting room bypass rule for your website, including the rule name, status, and rule content.
        
        @param request: UpdateWaitingRoomRuleRequest
        @return: UpdateWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.update_waiting_room_rule_with_options(request, runtime)

    async def update_waiting_room_rule_async(
        self,
        request: esa20240910_models.UpdateWaitingRoomRuleRequest,
    ) -> esa20240910_models.UpdateWaitingRoomRuleResponse:
        """
        @summary Updates the configurations of a waiting room bypass rule for a website.
        
        @description You can call this API operation to modify the configurations of a waiting room bypass rule for your website, including the rule name, status, and rule content.
        
        @param request: UpdateWaitingRoomRuleRequest
        @return: UpdateWaitingRoomRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.update_waiting_room_rule_with_options_async(request, runtime)

    def upload_client_ca_certificate_with_options(
        self,
        request: esa20240910_models.UploadClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadClientCaCertificateResponse:
        """
        @summary 上传客户端CA证书
        
        @param request: UploadClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UploadClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.certificate):
            body['Certificate'] = request.certificate
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UploadClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UploadClientCaCertificateResponse(),
            self.call_api(params, req, runtime)
        )

    async def upload_client_ca_certificate_with_options_async(
        self,
        request: esa20240910_models.UploadClientCaCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadClientCaCertificateResponse:
        """
        @summary 上传客户端CA证书
        
        @param request: UploadClientCaCertificateRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UploadClientCaCertificateResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        body = {}
        if not UtilClient.is_unset(request.certificate):
            body['Certificate'] = request.certificate
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UploadClientCaCertificate',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UploadClientCaCertificateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def upload_client_ca_certificate(
        self,
        request: esa20240910_models.UploadClientCaCertificateRequest,
    ) -> esa20240910_models.UploadClientCaCertificateResponse:
        """
        @summary 上传客户端CA证书
        
        @param request: UploadClientCaCertificateRequest
        @return: UploadClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.upload_client_ca_certificate_with_options(request, runtime)

    async def upload_client_ca_certificate_async(
        self,
        request: esa20240910_models.UploadClientCaCertificateRequest,
    ) -> esa20240910_models.UploadClientCaCertificateResponse:
        """
        @summary 上传客户端CA证书
        
        @param request: UploadClientCaCertificateRequest
        @return: UploadClientCaCertificateResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.upload_client_ca_certificate_with_options_async(request, runtime)

    def upload_file_with_options(
        self,
        request: esa20240910_models.UploadFileRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadFileResponse:
        """
        @summary Uploads the file that contains resources to be purged or prefetched.
        
        @description >
        The file can be up to 10 MB in size.
        
        @param request: UploadFileRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UploadFileResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        if not UtilClient.is_unset(request.upload_task_name):
            query['UploadTaskName'] = request.upload_task_name
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UploadFile',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UploadFileResponse(),
            self.call_api(params, req, runtime)
        )

    async def upload_file_with_options_async(
        self,
        request: esa20240910_models.UploadFileRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadFileResponse:
        """
        @summary Uploads the file that contains resources to be purged or prefetched.
        
        @description >
        The file can be up to 10 MB in size.
        
        @param request: UploadFileRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UploadFileResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        if not UtilClient.is_unset(request.upload_task_name):
            query['UploadTaskName'] = request.upload_task_name
        if not UtilClient.is_unset(request.url):
            query['Url'] = request.url
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UploadFile',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.UploadFileResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def upload_file(
        self,
        request: esa20240910_models.UploadFileRequest,
    ) -> esa20240910_models.UploadFileResponse:
        """
        @summary Uploads the file that contains resources to be purged or prefetched.
        
        @description >
        The file can be up to 10 MB in size.
        
        @param request: UploadFileRequest
        @return: UploadFileResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.upload_file_with_options(request, runtime)

    async def upload_file_async(
        self,
        request: esa20240910_models.UploadFileRequest,
    ) -> esa20240910_models.UploadFileResponse:
        """
        @summary Uploads the file that contains resources to be purged or prefetched.
        
        @description >
        The file can be up to 10 MB in size.
        
        @param request: UploadFileRequest
        @return: UploadFileResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.upload_file_with_options_async(request, runtime)

    def upload_file_advance(
        self,
        request: esa20240910_models.UploadFileAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadFileResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        upload_file_req = esa20240910_models.UploadFileRequest()
        OpenApiUtilClient.convert(request, upload_file_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            upload_file_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        upload_file_resp = self.upload_file_with_options(upload_file_req, runtime)
        return upload_file_resp

    async def upload_file_advance_async(
        self,
        request: esa20240910_models.UploadFileAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.UploadFileResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        open_platform_endpoint = self._open_platform_endpoint
        if UtilClient.empty(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ESA',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        upload_file_req = esa20240910_models.UploadFileRequest()
        OpenApiUtilClient.convert(request, upload_file_req)
        if not UtilClient.is_unset(request.url_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.body.access_key_id
            oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.body.endpoint, auth_response.body.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.body.object_key,
                content=request.url_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.body.access_key_id,
                policy=auth_response.body.encoded_policy,
                signature=auth_response.body.signature,
                key=auth_response.body.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.body.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            upload_file_req.url = f'http://{auth_response.body.bucket}.{auth_response.body.endpoint}/{auth_response.body.object_key}'
        upload_file_resp = await self.upload_file_with_options_async(upload_file_req, runtime)
        return upload_file_resp

    def verify_site_with_options(
        self,
        request: esa20240910_models.VerifySiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.VerifySiteResponse:
        """
        @summary Verifies the ownership of a website domain. Websites that pass the verification are automatically activated.
        
        @description 1.  For a website connected by using NS setup, this operation verifies whether the nameservers of the website are the nameservers assigned by Alibaba Cloud.
        2.  For a website connected by using CNAME setup, this operation verifies whether the website has a TXT record whose hostname is  _esaauth.[websiteDomainName] and record value is the value of VerifyCode to the DNS records of your domain. You can see the VerifyCode field in the site information.
        
        @param request: VerifySiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: VerifySiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='VerifySite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.VerifySiteResponse(),
            self.call_api(params, req, runtime)
        )

    async def verify_site_with_options_async(
        self,
        request: esa20240910_models.VerifySiteRequest,
        runtime: util_models.RuntimeOptions,
    ) -> esa20240910_models.VerifySiteResponse:
        """
        @summary Verifies the ownership of a website domain. Websites that pass the verification are automatically activated.
        
        @description 1.  For a website connected by using NS setup, this operation verifies whether the nameservers of the website are the nameservers assigned by Alibaba Cloud.
        2.  For a website connected by using CNAME setup, this operation verifies whether the website has a TXT record whose hostname is  _esaauth.[websiteDomainName] and record value is the value of VerifyCode to the DNS records of your domain. You can see the VerifyCode field in the site information.
        
        @param request: VerifySiteRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: VerifySiteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.site_id):
            query['SiteId'] = request.site_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='VerifySite',
            version='2024-09-10',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            esa20240910_models.VerifySiteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def verify_site(
        self,
        request: esa20240910_models.VerifySiteRequest,
    ) -> esa20240910_models.VerifySiteResponse:
        """
        @summary Verifies the ownership of a website domain. Websites that pass the verification are automatically activated.
        
        @description 1.  For a website connected by using NS setup, this operation verifies whether the nameservers of the website are the nameservers assigned by Alibaba Cloud.
        2.  For a website connected by using CNAME setup, this operation verifies whether the website has a TXT record whose hostname is  _esaauth.[websiteDomainName] and record value is the value of VerifyCode to the DNS records of your domain. You can see the VerifyCode field in the site information.
        
        @param request: VerifySiteRequest
        @return: VerifySiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.verify_site_with_options(request, runtime)

    async def verify_site_async(
        self,
        request: esa20240910_models.VerifySiteRequest,
    ) -> esa20240910_models.VerifySiteResponse:
        """
        @summary Verifies the ownership of a website domain. Websites that pass the verification are automatically activated.
        
        @description 1.  For a website connected by using NS setup, this operation verifies whether the nameservers of the website are the nameservers assigned by Alibaba Cloud.
        2.  For a website connected by using CNAME setup, this operation verifies whether the website has a TXT record whose hostname is  _esaauth.[websiteDomainName] and record value is the value of VerifyCode to the DNS records of your domain. You can see the VerifyCode field in the site information.
        
        @param request: VerifySiteRequest
        @return: VerifySiteResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.verify_site_with_options_async(request, runtime)
