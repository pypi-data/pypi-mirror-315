import pytest
import requests

from localstack import config
from localstack.aws.handlers import cors as cors_handler
from localstack.aws.handlers.cors import _get_allowed_cors_origins
from localstack.testing.config import TEST_AWS_ACCESS_KEY_ID, TEST_AWS_REGION_NAME
from localstack.utils.aws.request_context import mock_aws_request_headers
from localstack.utils.strings import short_uid, to_str


class TestCSRF:
    def test_CSRF(self):
        headers = {"Origin": "http://attacker.com"}
        # Test if lambdas are enumerable
        response = requests.get(
            f"{config.internal_service_url()}/2015-03-31/functions/", headers=headers
        )
        assert response.status_code == 403

        # Test if config endpoint is reachable
        config_body = {"variable": "harmful", "value": "config"}

        response = requests.post(
            f"{config.internal_service_url()}/?_config_", headers=headers, json=config_body
        )
        assert response.status_code == 403

        # Test if endpoints are reachable without origin header
        response = requests.get(f"{config.internal_service_url()}/2015-03-31/functions/")
        assert response.status_code == 200

    def test_default_cors_headers(self):
        headers = {"Origin": "https://app.localstack.cloud"}
        response = requests.get(
            f"{config.internal_service_url()}/2015-03-31/functions/", headers=headers
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "https://app.localstack.cloud"
        assert "GET" in response.headers["access-control-allow-methods"].split(",")
        assert response.headers["Vary"] == "Origin"
        assert response.headers["Access-Control-Allow-Credentials"] == "true"

    @pytest.mark.parametrize("path", ["/_localstack/health"])
    def test_internal_route_cors_headers(self, path):
        headers = {"Origin": "https://app.localstack.cloud"}
        response = requests.get(f"{config.internal_service_url()}{path}", headers=headers)
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "https://app.localstack.cloud"
        assert "GET" in response.headers["access-control-allow-methods"].split(",")

    def test_cors_s3_override(self, s3_bucket, monkeypatch, aws_client):
        monkeypatch.setattr(config, "DISABLE_CUSTOM_CORS_S3", True)

        BUCKET_CORS_CONFIG = {
            "CORSRules": [
                {
                    "AllowedOrigins": ["https://localhost:4200"],
                    "AllowedMethods": ["GET", "PUT"],
                    "MaxAgeSeconds": 3000,
                    "AllowedHeaders": ["*"],
                }
            ]
        }

        aws_client.s3.put_bucket_cors(Bucket=s3_bucket, CORSConfiguration=BUCKET_CORS_CONFIG)

        # create signed url
        url = aws_client.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": s3_bucket,
                "Key": "424f6bae-c48f-42d8-9e25-52046aecc64d/document.pdf",
                "ContentType": "application/pdf",
                "ACL": "bucket-owner-full-control",
            },
            ExpiresIn=3600,
        )
        result = requests.put(
            url,
            data="something",
            verify=False,
            headers={
                "Origin": "https://localhost:4200",
                "Content-Type": "application/pdf",
            },
        )
        assert result.status_code == 403

    def test_disable_cors_checks(self, monkeypatch):
        """Test DISABLE_CORS_CHECKS=1 (most permissive setting)"""
        headers = {"Origin": "https://invalid.localstack.cloud"}
        url = f"{config.internal_service_url()}/2015-03-31/functions/"
        response = requests.get(url, headers=headers)
        assert response.status_code == 403

        monkeypatch.setattr(config, "DISABLE_CORS_CHECKS", True)
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        # assert that because the invalid Origin was not in the AllowedOrigin, we set '*'
        assert response.headers["access-control-allow-origin"] == "*"
        assert "GET" in response.headers["access-control-allow-methods"].split(",")
        # because the Allow-Origin is '*', we cannot allow credentials (the browser won't allow it)
        assert "Access-Control-Allow-Credentials" not in response.headers

    def test_disable_cors_headers(self, monkeypatch):
        """Test DISABLE_CORS_CHECKS=1 (most restrictive setting, not sending any CORS headers)"""
        headers = mock_aws_request_headers(
            "sns", aws_access_key_id=TEST_AWS_ACCESS_KEY_ID, region_name=TEST_AWS_REGION_NAME
        )
        headers["Origin"] = "https://app.localstack.cloud"
        url = config.internal_service_url()
        data = {"Action": "ListTopics", "Version": "2010-03-31"}
        response = requests.post(url, headers=headers, data=data)
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == headers["Origin"]
        assert "authorization" in response.headers["access-control-allow-headers"].lower()
        assert "GET" in response.headers["access-control-allow-methods"].split(",")
        assert "<ListTopicsResponse" in to_str(response.content)

        monkeypatch.setattr(config, "DISABLE_CORS_HEADERS", True)
        response = requests.post(url, headers=headers, data=data)
        assert response.status_code == 200
        assert "<ListTopicsResponse" in to_str(response.content)
        assert not response.headers.get("access-control-allow-headers")
        assert not response.headers.get("access-control-allow-methods")
        assert not response.headers.get("access-control-allow-origin")
        assert not response.headers.get("access-control-allow-credentials")

    def test_additional_allowed_origins(self, monkeypatch):
        test_domain = f"test-{short_uid()}.com"
        monkeypatch.setattr(config, "EXTRA_CORS_ALLOWED_ORIGINS", f"https://{test_domain}")
        monkeypatch.setattr(cors_handler, "ALLOWED_CORS_ORIGINS", _get_allowed_cors_origins())

        url = config.internal_service_url()
        headers = mock_aws_request_headers(
            "sns", aws_access_key_id=TEST_AWS_ACCESS_KEY_ID, region_name=TEST_AWS_REGION_NAME
        )
        data = {"Action": "ListTopics", "Version": "2010-03-31"}

        # test successful request
        headers["Origin"] = f"https://{test_domain}"
        response = requests.post(url, headers=headers, data=data)
        assert response.ok
        assert response.headers["access-control-allow-origin"] == headers["Origin"]

        # test unsuccessful (non-HTTPS) request
        headers["Origin"] = f"http://{test_domain}"
        response = requests.post(url, headers=headers, data=data)
        assert not response.ok

    def test_no_cors_without_origin_header(self):
        response = requests.get(f"{config.internal_service_url()}/2015-03-31/functions/")
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers

    def test_cors_apigw_not_applied(self, aws_client):
        # make sure the service is loaded and has registered routes
        aws_client.apigateway.get_rest_apis()

        cors_headers = [
            "access-control-allow-headers",
            "access-control-allow-methods",
            "access-control-allow-origin",
            "access-control-allow-credentials",
        ]

        # assert that the registered routes for APIGW are handled by themselves on the CORS/CRSF level
        # note: we have tests for asserting proper return of CORS headers in APIGW itself when configured to do so
        #
        rest_api_url_user_request = (
            f"{config.internal_service_url()}/restapis/myapiid/stage/_user_request_"
        )
        response = requests.get(
            rest_api_url_user_request,
            verify=False,
            headers={
                "Origin": "https://app.localstack.cloud",
            },
        )
        assert response.status_code == 404

        assert not any(response.headers.get(cors_header) for cors_header in cors_headers)

        rest_api_url_host = f"{config.internal_service_url()}/stage"
        host_header = "myapiid.execute-api.localhost.localstack.cloud:4566"
        response = requests.get(
            rest_api_url_host,
            verify=False,
            headers={
                "Origin": "https://app.localstack.cloud",
                "Host": host_header,
            },
        )

        assert response.status_code == 404
        assert not any(response.headers.get(cors_header) for cors_header in cors_headers)

        # now we give it a try with a route from the provider defined in the specs: GetRestApi, and an authorized origin
        rest_api_url = f"{config.internal_service_url()}/restapis/myapiid"
        response = requests.get(
            rest_api_url,
            verify=False,
            headers={
                "Origin": "https://app.localstack.cloud",
                "Authorization": "AWS4-HMAC-SHA256 Credential=test/20240418/us-east-1/apigateway/aws4_request, SignedHeaders=accept;host;x-amz-date, Signature=88259852931bc389bd7c2e1fb8b700b935e9d6b14bd2ef72efc3a9b20b415701",
            },
        )
        assert response.status_code == 404
        assert all(response.headers.get(cors_header) for cors_header in cors_headers)

        # now do the same from an unauthorized Origin
        response = requests.get(
            rest_api_url,
            verify=False,
            headers={
                "Origin": "http://localhost:4200",
                "Authorization": "AWS4-HMAC-SHA256 Credential=test/20240418/us-east-1/apigateway/aws4_request, SignedHeaders=accept;host;x-amz-date, Signature=88259852931bc389bd7c2e1fb8b700b935e9d6b14bd2ef72efc3a9b20b415701",
            },
        )
        assert response.status_code == 403
        assert not any(response.headers.get(cors_header) for cors_header in cors_headers)
