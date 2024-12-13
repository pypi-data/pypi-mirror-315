# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class EC2PrefixListProperties(TypedDict):
    AddressFamily: Optional[str]
    MaxEntries: Optional[int]
    PrefixListName: Optional[str]
    Arn: Optional[str]
    Entries: Optional[list[Entry]]
    OwnerId: Optional[str]
    PrefixListId: Optional[str]
    Tags: Optional[list[Tag]]
    Version: Optional[int]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


class Entry(TypedDict):
    Cidr: Optional[str]
    Description: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2PrefixListProvider(ResourceProvider[EC2PrefixListProperties]):
    TYPE = "AWS::EC2::PrefixList"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2PrefixListProperties],
    ) -> ProgressEvent[EC2PrefixListProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/PrefixListId

        Required properties:
          - PrefixListName
          - MaxEntries
          - AddressFamily



        Read-only properties:
          - /properties/PrefixListId
          - /properties/OwnerId
          - /properties/Version
          - /properties/Arn

        IAM permissions required:
          - EC2:CreateManagedPrefixList
          - EC2:DescribeManagedPrefixLists
          - EC2:CreateTags

        """
        model = request.desired_state

        if not request.custom_context.get(REPEATED_INVOCATION):
            create_params = util.select_attributes(
                model, ["PrefixListName", "Entries", "MaxEntries", "AddressFamily", "Tags"]
            )

            if "Tags" in create_params:
                create_params["TagSpecifications"] = [
                    {"ResourceType": "prefix-list", "Tags": create_params.pop("Tags")}
                ]

            response = request.aws_client_factory.ec2.create_managed_prefix_list(**create_params)
            model["Arn"] = response["PrefixList"]["PrefixListId"]
            model["OwnerId"] = response["PrefixList"]["OwnerId"]
            model["PrefixListId"] = response["PrefixList"]["PrefixListId"]
            model["Version"] = response["PrefixList"]["Version"]
            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        response = request.aws_client_factory.ec2.describe_managed_prefix_lists(
            PrefixListIds=[model["PrefixListId"]]
        )
        if not response["PrefixLists"]:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resource_model=model,
                custom_context=request.custom_context,
                message="Resource not found after creation",
            )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2PrefixListProperties],
    ) -> ProgressEvent[EC2PrefixListProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - EC2:GetManagedPrefixListEntries
          - EC2:DescribeManagedPrefixLists
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2PrefixListProperties],
    ) -> ProgressEvent[EC2PrefixListProperties]:
        """
        Delete a resource

        IAM permissions required:
          - EC2:DeleteManagedPrefixList
          - EC2:DescribeManagedPrefixLists
        """

        model = request.previous_state
        response = request.aws_client_factory.ec2.describe_managed_prefix_lists(
            PrefixListIds=[model["PrefixListId"]]
        )

        if not response["PrefixLists"]:
            return ProgressEvent(status=OperationStatus.SUCCESS, resource_model=model)

        request.aws_client_factory.ec2.delete_managed_prefix_list(
            PrefixListId=request.previous_state["PrefixListId"]
        )
        return ProgressEvent(status=OperationStatus.IN_PROGRESS, resource_model=model)

    def update(
        self,
        request: ResourceRequest[EC2PrefixListProperties],
    ) -> ProgressEvent[EC2PrefixListProperties]:
        """
        Update a resource

        IAM permissions required:
          - EC2:DescribeManagedPrefixLists
          - EC2:GetManagedPrefixListEntries
          - EC2:ModifyManagedPrefixList
          - EC2:CreateTags
          - EC2:DeleteTags
        """
        raise NotImplementedError
