# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)

LOG = logging.getLogger(__name__)


class EC2VPCProperties(TypedDict):
    CidrBlock: Optional[str]
    CidrBlockAssociations: Optional[list[str]]
    DefaultNetworkAcl: Optional[str]
    DefaultSecurityGroup: Optional[str]
    EnableDnsHostnames: Optional[bool]
    EnableDnsSupport: Optional[bool]
    InstanceTenancy: Optional[str]
    Ipv4IpamPoolId: Optional[str]
    Ipv4NetmaskLength: Optional[int]
    Ipv6CidrBlocks: Optional[list[str]]
    Tags: Optional[list[Tag]]
    VpcId: Optional[str]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


def _get_default_security_group_for_vpc(ec2_client, vpc_id: str) -> str:
    sgs = ec2_client.describe_security_groups(
        Filters=[
            {"Name": "group-name", "Values": ["default"]},
            {"Name": "vpc-id", "Values": [vpc_id]},
        ]
    )["SecurityGroups"]
    if len(sgs) != 1:
        raise Exception(f"There should only be one default group for this VPC ({vpc_id=})")
    return sgs[0]["GroupId"]


def _get_default_acl_for_vpc(ec2_client, vpc_id: str) -> str:
    acls = ec2_client.describe_network_acls(
        Filters=[
            {"Name": "default", "Values": ["true"]},
            {"Name": "vpc-id", "Values": [vpc_id]},
        ]
    )["NetworkAcls"]
    if len(acls) != 1:
        raise Exception(f"There should only be one default network ACL for this VPC ({vpc_id=})")
    return acls[0]["NetworkAclId"]


def generate_vpc_read_payload(ec2_client, vpc_id: str) -> EC2VPCProperties:
    vpc = ec2_client.describe_vpcs(VpcIds=[vpc_id])["Vpcs"][0]

    model = EC2VPCProperties(
        **util.select_attributes(vpc, EC2VPCProvider.SCHEMA["properties"].keys())
    )
    model["CidrBlockAssociations"] = [
        cba["AssociationId"] for cba in vpc["CidrBlockAssociationSet"]
    ]
    model["Ipv6CidrBlocks"] = [
        ipv6_ass["Ipv6CidrBlock"] for ipv6_ass in vpc.get("Ipv6CidrBlockAssociationSet", [])
    ]
    model["DefaultNetworkAcl"] = _get_default_acl_for_vpc(ec2_client, model["VpcId"])
    model["DefaultSecurityGroup"] = _get_default_security_group_for_vpc(ec2_client, model["VpcId"])
    model["EnableDnsHostnames"] = ec2_client.describe_vpc_attribute(
        Attribute="enableDnsHostnames", VpcId=vpc_id
    )["EnableDnsHostnames"]["Value"]
    model["EnableDnsSupport"] = ec2_client.describe_vpc_attribute(
        Attribute="enableDnsSupport", VpcId=vpc_id
    )["EnableDnsSupport"]["Value"]

    return model


class EC2VPCProvider(ResourceProvider[EC2VPCProperties]):
    TYPE = "AWS::EC2::VPC"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2VPCProperties],
    ) -> ProgressEvent[EC2VPCProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/VpcId

        Create-only properties:
          - /properties/CidrBlock
          - /properties/Ipv4IpamPoolId
          - /properties/Ipv4NetmaskLength

        Read-only properties:
          - /properties/CidrBlockAssociations
          - /properties/DefaultNetworkAcl
          - /properties/DefaultSecurityGroup
          - /properties/Ipv6CidrBlocks
          - /properties/VpcId

        IAM permissions required:
          - ec2:CreateVpc
          - ec2:DescribeVpcs
          - ec2:ModifyVpcAttribute

        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        # TODO: validations

        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked
            # TODO: defaults
            # TODO: idempotency
            params = util.select_attributes(
                model,
                ["CidrBlock", "InstanceTenancy"],
            )
            if model.get("Tags"):
                tags = [{"ResourceType": "vpc", "Tags": model.get("Tags")}]
                params["TagSpecifications"] = tags

            response = ec2.create_vpc(**params)

            request.custom_context[REPEATED_INVOCATION] = True
            model = generate_vpc_read_payload(ec2, response["Vpc"]["VpcId"])

            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        response = ec2.describe_vpcs(VpcIds=[model["VpcId"]])["Vpcs"][0]
        if response["State"] == "pending":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2VPCProperties],
    ) -> ProgressEvent[EC2VPCProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - ec2:DescribeVpcs
          - ec2:DescribeSecurityGroups
          - ec2:DescribeNetworkAcls
          - ec2:DescribeVpcAttribute
        """
        ec2 = request.aws_client_factory.ec2

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=generate_vpc_read_payload(ec2, request.desired_state["VpcId"]),
            custom_context=request.custom_context,
        )

    def delete(
        self,
        request: ResourceRequest[EC2VPCProperties],
    ) -> ProgressEvent[EC2VPCProperties]:
        """
        Delete a resource

        IAM permissions required:
          - ec2:DeleteVpc
          - ec2:DescribeVpcs
        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        # remove routes and route tables first
        resp = ec2.describe_route_tables(
            Filters=[
                {"Name": "vpc-id", "Values": [model["VpcId"]]},
                {"Name": "association.main", "Values": ["false"]},
            ]
        )
        for rt in resp["RouteTables"]:
            for assoc in rt.get("Associations", []):
                # skipping Main association (upstream moto includes default association that cannot be deleted)
                if assoc.get("Main"):
                    continue
                ec2.disassociate_route_table(AssociationId=assoc["RouteTableAssociationId"])
            ec2.delete_route_table(RouteTableId=rt["RouteTableId"])

        # TODO security groups, gateways and other attached resources need to be deleted as well
        ec2.delete_vpc(VpcId=model["VpcId"])
        return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=model)

    def update(
        self,
        request: ResourceRequest[EC2VPCProperties],
    ) -> ProgressEvent[EC2VPCProperties]:
        """
        Update a resource

        IAM permissions required:
          - ec2:CreateTags
          - ec2:ModifyVpcAttribute
          - ec2:DeleteTags
          - ec2:ModifyVpcTenancy
        """
        raise NotImplementedError

    def list(
        self,
        request: ResourceRequest[EC2VPCProperties],
    ) -> ProgressEvent[EC2VPCProperties]:
        resources = request.aws_client_factory.ec2.describe_vpcs()
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_models=[
                EC2VPCProperties(VpcId=resource["VpcId"]) for resource in resources["Vpcs"]
            ],
        )
