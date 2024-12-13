# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities
from ._enums import *

__all__ = ['TeamEnvironmentPermissionArgs', 'TeamEnvironmentPermission']

@pulumi.input_type
class TeamEnvironmentPermissionArgs:
    def __init__(__self__, *,
                 environment: pulumi.Input[str],
                 organization: pulumi.Input[str],
                 permission: pulumi.Input['EnvironmentPermission'],
                 team: pulumi.Input[str],
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TeamEnvironmentPermission resource.
        :param pulumi.Input[str] environment: Environment name.
        :param pulumi.Input[str] organization: Organization name.
        :param pulumi.Input['EnvironmentPermission'] permission: Which permission level to grant to the specified team.
        :param pulumi.Input[str] team: Team name.
        :param pulumi.Input[str] project: Project name.
        """
        pulumi.set(__self__, "environment", environment)
        pulumi.set(__self__, "organization", organization)
        pulumi.set(__self__, "permission", permission)
        pulumi.set(__self__, "team", team)
        if project is None:
            project = 'default'
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def environment(self) -> pulumi.Input[str]:
        """
        Environment name.
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter
    def organization(self) -> pulumi.Input[str]:
        """
        Organization name.
        """
        return pulumi.get(self, "organization")

    @organization.setter
    def organization(self, value: pulumi.Input[str]):
        pulumi.set(self, "organization", value)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Input['EnvironmentPermission']:
        """
        Which permission level to grant to the specified team.
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: pulumi.Input['EnvironmentPermission']):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter
    def team(self) -> pulumi.Input[str]:
        """
        Team name.
        """
        return pulumi.get(self, "team")

    @team.setter
    def team(self, value: pulumi.Input[str]):
        pulumi.set(self, "team", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        Project name.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class TeamEnvironmentPermission(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 permission: Optional[pulumi.Input['EnvironmentPermission']] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 team: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A permission for a team to use an environment.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] environment: Environment name.
        :param pulumi.Input[str] organization: Organization name.
        :param pulumi.Input['EnvironmentPermission'] permission: Which permission level to grant to the specified team.
        :param pulumi.Input[str] project: Project name.
        :param pulumi.Input[str] team: Team name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TeamEnvironmentPermissionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A permission for a team to use an environment.

        :param str resource_name: The name of the resource.
        :param TeamEnvironmentPermissionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TeamEnvironmentPermissionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 permission: Optional[pulumi.Input['EnvironmentPermission']] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 team: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TeamEnvironmentPermissionArgs.__new__(TeamEnvironmentPermissionArgs)

            if environment is None and not opts.urn:
                raise TypeError("Missing required property 'environment'")
            __props__.__dict__["environment"] = environment
            if organization is None and not opts.urn:
                raise TypeError("Missing required property 'organization'")
            __props__.__dict__["organization"] = organization
            if permission is None and not opts.urn:
                raise TypeError("Missing required property 'permission'")
            __props__.__dict__["permission"] = permission
            if project is None:
                project = 'default'
            __props__.__dict__["project"] = project
            if team is None and not opts.urn:
                raise TypeError("Missing required property 'team'")
            __props__.__dict__["team"] = team
        super(TeamEnvironmentPermission, __self__).__init__(
            'pulumiservice:index:TeamEnvironmentPermission',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TeamEnvironmentPermission':
        """
        Get an existing TeamEnvironmentPermission resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TeamEnvironmentPermissionArgs.__new__(TeamEnvironmentPermissionArgs)

        __props__.__dict__["permission"] = None
        return TeamEnvironmentPermission(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Output[Optional['EnvironmentPermission']]:
        """
        Which permission level to grant to the specified team.
        """
        return pulumi.get(self, "permission")

