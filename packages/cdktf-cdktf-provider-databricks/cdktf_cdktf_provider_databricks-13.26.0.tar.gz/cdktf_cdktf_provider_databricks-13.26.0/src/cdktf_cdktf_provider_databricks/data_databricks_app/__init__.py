r'''
# `data_databricks_app`

Refer to the Terraform Registry for docs: [`data_databricks_app`](https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataDatabricksApp(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksApp",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app databricks_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app databricks_app} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0ce022004568ff5e253109396eece8a5fbd277f2a640530db20fd3555f6834)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatabricksAppConfig(
            name=name,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatabricksApp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatabricksApp to import.
        :param import_from_id: The id of the existing DataDatabricksApp that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatabricksApp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b673f1de1f6da52cfb1b5896457971a4bec9ac2721f0d3b2351ca4d5117146e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="app")
    def app(self) -> "DataDatabricksAppAppOutputReference":
        return typing.cast("DataDatabricksAppAppOutputReference", jsii.get(self, "app"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3feef38a02de41c08393b96e84868d66cc6770ca3489ebc29e3c90273e99c43d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppApp",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "active_deployment": "activeDeployment",
        "app_status": "appStatus",
        "compute_status": "computeStatus",
        "create_time": "createTime",
        "creator": "creator",
        "default_source_code_path": "defaultSourceCodePath",
        "description": "description",
        "pending_deployment": "pendingDeployment",
        "resources": "resources",
        "service_principal_client_id": "servicePrincipalClientId",
        "service_principal_id": "servicePrincipalId",
        "service_principal_name": "servicePrincipalName",
        "updater": "updater",
        "update_time": "updateTime",
        "url": "url",
    },
)
class DataDatabricksAppApp:
    def __init__(
        self,
        *,
        name: builtins.str,
        active_deployment: typing.Optional[typing.Union["DataDatabricksAppAppActiveDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        app_status: typing.Optional[typing.Union["DataDatabricksAppAppAppStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        compute_status: typing.Optional[typing.Union["DataDatabricksAppAppComputeStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        create_time: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        default_source_code_path: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        pending_deployment: typing.Optional[typing.Union["DataDatabricksAppAppPendingDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksAppAppResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_principal_client_id: typing.Optional[builtins.str] = None,
        service_principal_id: typing.Optional[jsii.Number] = None,
        service_principal_name: typing.Optional[builtins.str] = None,
        updater: typing.Optional[builtins.str] = None,
        update_time: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        :param active_deployment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#active_deployment DataDatabricksApp#active_deployment}.
        :param app_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#app_status DataDatabricksApp#app_status}.
        :param compute_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#compute_status DataDatabricksApp#compute_status}.
        :param create_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.
        :param creator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.
        :param default_source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#default_source_code_path DataDatabricksApp#default_source_code_path}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#description DataDatabricksApp#description}.
        :param pending_deployment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#pending_deployment DataDatabricksApp#pending_deployment}.
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#resources DataDatabricksApp#resources}.
        :param service_principal_client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_client_id DataDatabricksApp#service_principal_client_id}.
        :param service_principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_id DataDatabricksApp#service_principal_id}.
        :param service_principal_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_name DataDatabricksApp#service_principal_name}.
        :param updater: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#updater DataDatabricksApp#updater}.
        :param update_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#url DataDatabricksApp#url}.
        '''
        if isinstance(active_deployment, dict):
            active_deployment = DataDatabricksAppAppActiveDeployment(**active_deployment)
        if isinstance(app_status, dict):
            app_status = DataDatabricksAppAppAppStatus(**app_status)
        if isinstance(compute_status, dict):
            compute_status = DataDatabricksAppAppComputeStatus(**compute_status)
        if isinstance(pending_deployment, dict):
            pending_deployment = DataDatabricksAppAppPendingDeployment(**pending_deployment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e4670df0b4e95281aa8f15f8d6f1b643ae427b77323aa965560d3c5b0f4e84)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument active_deployment", value=active_deployment, expected_type=type_hints["active_deployment"])
            check_type(argname="argument app_status", value=app_status, expected_type=type_hints["app_status"])
            check_type(argname="argument compute_status", value=compute_status, expected_type=type_hints["compute_status"])
            check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
            check_type(argname="argument creator", value=creator, expected_type=type_hints["creator"])
            check_type(argname="argument default_source_code_path", value=default_source_code_path, expected_type=type_hints["default_source_code_path"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument pending_deployment", value=pending_deployment, expected_type=type_hints["pending_deployment"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument service_principal_client_id", value=service_principal_client_id, expected_type=type_hints["service_principal_client_id"])
            check_type(argname="argument service_principal_id", value=service_principal_id, expected_type=type_hints["service_principal_id"])
            check_type(argname="argument service_principal_name", value=service_principal_name, expected_type=type_hints["service_principal_name"])
            check_type(argname="argument updater", value=updater, expected_type=type_hints["updater"])
            check_type(argname="argument update_time", value=update_time, expected_type=type_hints["update_time"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if active_deployment is not None:
            self._values["active_deployment"] = active_deployment
        if app_status is not None:
            self._values["app_status"] = app_status
        if compute_status is not None:
            self._values["compute_status"] = compute_status
        if create_time is not None:
            self._values["create_time"] = create_time
        if creator is not None:
            self._values["creator"] = creator
        if default_source_code_path is not None:
            self._values["default_source_code_path"] = default_source_code_path
        if description is not None:
            self._values["description"] = description
        if pending_deployment is not None:
            self._values["pending_deployment"] = pending_deployment
        if resources is not None:
            self._values["resources"] = resources
        if service_principal_client_id is not None:
            self._values["service_principal_client_id"] = service_principal_client_id
        if service_principal_id is not None:
            self._values["service_principal_id"] = service_principal_id
        if service_principal_name is not None:
            self._values["service_principal_name"] = service_principal_name
        if updater is not None:
            self._values["updater"] = updater
        if update_time is not None:
            self._values["update_time"] = update_time
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_deployment(
        self,
    ) -> typing.Optional["DataDatabricksAppAppActiveDeployment"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#active_deployment DataDatabricksApp#active_deployment}.'''
        result = self._values.get("active_deployment")
        return typing.cast(typing.Optional["DataDatabricksAppAppActiveDeployment"], result)

    @builtins.property
    def app_status(self) -> typing.Optional["DataDatabricksAppAppAppStatus"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#app_status DataDatabricksApp#app_status}.'''
        result = self._values.get("app_status")
        return typing.cast(typing.Optional["DataDatabricksAppAppAppStatus"], result)

    @builtins.property
    def compute_status(self) -> typing.Optional["DataDatabricksAppAppComputeStatus"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#compute_status DataDatabricksApp#compute_status}.'''
        result = self._values.get("compute_status")
        return typing.cast(typing.Optional["DataDatabricksAppAppComputeStatus"], result)

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.'''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.'''
        result = self._values.get("creator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_source_code_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#default_source_code_path DataDatabricksApp#default_source_code_path}.'''
        result = self._values.get("default_source_code_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#description DataDatabricksApp#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pending_deployment(
        self,
    ) -> typing.Optional["DataDatabricksAppAppPendingDeployment"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#pending_deployment DataDatabricksApp#pending_deployment}.'''
        result = self._values.get("pending_deployment")
        return typing.cast(typing.Optional["DataDatabricksAppAppPendingDeployment"], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksAppAppResources"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#resources DataDatabricksApp#resources}.'''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksAppAppResources"]]], result)

    @builtins.property
    def service_principal_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_client_id DataDatabricksApp#service_principal_client_id}.'''
        result = self._values.get("service_principal_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_principal_id(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_id DataDatabricksApp#service_principal_id}.'''
        result = self._values.get("service_principal_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_principal_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#service_principal_name DataDatabricksApp#service_principal_name}.'''
        result = self._values.get("service_principal_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updater(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#updater DataDatabricksApp#updater}.'''
        result = self._values.get("updater")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.'''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#url DataDatabricksApp#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppApp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "create_time": "createTime",
        "creator": "creator",
        "deployment_artifacts": "deploymentArtifacts",
        "deployment_id": "deploymentId",
        "mode": "mode",
        "source_code_path": "sourceCodePath",
        "status": "status",
        "update_time": "updateTime",
    },
)
class DataDatabricksAppAppActiveDeployment:
    def __init__(
        self,
        *,
        create_time: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        deployment_artifacts: typing.Optional[typing.Union["DataDatabricksAppAppActiveDeploymentDeploymentArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source_code_path: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union["DataDatabricksAppAppActiveDeploymentStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.
        :param creator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.
        :param deployment_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.
        :param deployment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.
        :param update_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.
        '''
        if isinstance(deployment_artifacts, dict):
            deployment_artifacts = DataDatabricksAppAppActiveDeploymentDeploymentArtifacts(**deployment_artifacts)
        if isinstance(status, dict):
            status = DataDatabricksAppAppActiveDeploymentStatus(**status)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f4711583806e7694ce67324f7c2a7d0e6a7e02d3452b53695821d7328dff9f)
            check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
            check_type(argname="argument creator", value=creator, expected_type=type_hints["creator"])
            check_type(argname="argument deployment_artifacts", value=deployment_artifacts, expected_type=type_hints["deployment_artifacts"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument source_code_path", value=source_code_path, expected_type=type_hints["source_code_path"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument update_time", value=update_time, expected_type=type_hints["update_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_time is not None:
            self._values["create_time"] = create_time
        if creator is not None:
            self._values["creator"] = creator
        if deployment_artifacts is not None:
            self._values["deployment_artifacts"] = deployment_artifacts
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id
        if mode is not None:
            self._values["mode"] = mode
        if source_code_path is not None:
            self._values["source_code_path"] = source_code_path
        if status is not None:
            self._values["status"] = status
        if update_time is not None:
            self._values["update_time"] = update_time

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.'''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.'''
        result = self._values.get("creator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_artifacts(
        self,
    ) -> typing.Optional["DataDatabricksAppAppActiveDeploymentDeploymentArtifacts"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.'''
        result = self._values.get("deployment_artifacts")
        return typing.cast(typing.Optional["DataDatabricksAppAppActiveDeploymentDeploymentArtifacts"], result)

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.'''
        result = self._values.get("deployment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_code_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.'''
        result = self._values.get("source_code_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["DataDatabricksAppAppActiveDeploymentStatus"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional["DataDatabricksAppAppActiveDeploymentStatus"], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.'''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppActiveDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeploymentDeploymentArtifacts",
    jsii_struct_bases=[],
    name_mapping={"source_code_path": "sourceCodePath"},
)
class DataDatabricksAppAppActiveDeploymentDeploymentArtifacts:
    def __init__(
        self,
        *,
        source_code_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67345022ac46cf2ae5a669c5b6d75f1c9a37433a26a699dbae27a966c9c7b8d1)
            check_type(argname="argument source_code_path", value=source_code_path, expected_type=type_hints["source_code_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_code_path is not None:
            self._values["source_code_path"] = source_code_path

    @builtins.property
    def source_code_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.'''
        result = self._values.get("source_code_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppActiveDeploymentDeploymentArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppActiveDeploymentDeploymentArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeploymentDeploymentArtifactsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e1076106fd372f777193eb77b562771a2cf5e59f0b9c44b82090c9dca57b63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceCodePath")
    def reset_source_code_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCodePath", []))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePathInput")
    def source_code_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCodePathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePath")
    def source_code_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCodePath"))

    @source_code_path.setter
    def source_code_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d38debada89b38b0668887b66db8160df281fdbe4f15bdc27f41e4cb8d8a1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCodePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc9ddcb553e377c0ce53eff68168574f7676315cdcb807c520b95d03e6d4174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksAppAppActiveDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeploymentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dac4fa7695cb41f42af1ead02f367fa98308d700c6307467a1fd6eec46138e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentArtifacts")
    def put_deployment_artifacts(
        self,
        *,
        source_code_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        '''
        value = DataDatabricksAppAppActiveDeploymentDeploymentArtifacts(
            source_code_path=source_code_path
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentArtifacts", [value]))

    @jsii.member(jsii_name="putStatus")
    def put_status(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        value = DataDatabricksAppAppActiveDeploymentStatus(
            message=message, state=state
        )

        return typing.cast(None, jsii.invoke(self, "putStatus", [value]))

    @jsii.member(jsii_name="resetCreateTime")
    def reset_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTime", []))

    @jsii.member(jsii_name="resetCreator")
    def reset_creator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreator", []))

    @jsii.member(jsii_name="resetDeploymentArtifacts")
    def reset_deployment_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentArtifacts", []))

    @jsii.member(jsii_name="resetDeploymentId")
    def reset_deployment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentId", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSourceCodePath")
    def reset_source_code_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCodePath", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetUpdateTime")
    def reset_update_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTime", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentArtifacts")
    def deployment_artifacts(
        self,
    ) -> DataDatabricksAppAppActiveDeploymentDeploymentArtifactsOutputReference:
        return typing.cast(DataDatabricksAppAppActiveDeploymentDeploymentArtifactsOutputReference, jsii.get(self, "deploymentArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "DataDatabricksAppAppActiveDeploymentStatusOutputReference":
        return typing.cast("DataDatabricksAppAppActiveDeploymentStatusOutputReference", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="createTimeInput")
    def create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="creatorInput")
    def creator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creatorInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentArtifactsInput")
    def deployment_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]], jsii.get(self, "deploymentArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePathInput")
    def source_code_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCodePathInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppActiveDeploymentStatus"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppActiveDeploymentStatus"]], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeInput")
    def update_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @create_time.setter
    def create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46a687ba61802132d2243b0b2dda3bf75ff3bdffcc7957de92f830b0cb82f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @creator.setter
    def creator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ba906c2eb376a0dbede89bf2a9bd5c241b41026be9c46bbbb513e2399d9566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34ad3d2b69cb9e973430dbb810b78cd108ce6fd0b74f910a1d8e0a26a2efaa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73d49aeb62dcb6d418177bd3ae0bbc72306c9ed8f1f91404bdc15012752ceba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceCodePath")
    def source_code_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCodePath"))

    @source_code_path.setter
    def source_code_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1ebaeed7531b8d9ec378fd1094d2ae43ce6af3d094465db74e1e3d7f38396a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCodePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1733c5d71d3ecba390e49759d370ff84f7ae4c23fcd920b23e00b8f8771925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7b189a795f6f77480ea5c93471e17d540da917c4e32db05d6430288f86a480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeploymentStatus",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "state": "state"},
)
class DataDatabricksAppAppActiveDeploymentStatus:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd09cadf4eb9cd1110c31cee3bc7902713331c0a8b530bff3016e7f6539fd62)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppActiveDeploymentStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppActiveDeploymentStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppActiveDeploymentStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0b4a396fe5c01b468bf7cd50946d4912d7be0c694b38fff952af8db4d51761)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fe0300a1d9aec55db6bc3fe667cd3bfbeb1e9544f232989051d62af81f63e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fa459459b148a5cc4db9e0cf2fb1865284716a25b9e4991c5637ab92a28173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffadc2e787f8507ea0afa102d9a601793363a09e658aae305bfd8b7a46e5b2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppAppStatus",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "state": "state"},
)
class DataDatabricksAppAppAppStatus:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34503f268216d5a85b5e7fd17b0944a099675350bcba8a3722b6fafae8a5171b)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppAppStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppAppStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppAppStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509853b1ce6017a7ca645c0a1f122efbd3b133bd6dc4c7f6accad30f91ef18bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442a69df5a5d681f5bb440c762319b0d40deaea97998c1bfe1a1cf46fd7d9295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe8922b4ef896ebc1e39b6a2bcb8671eb32fe3f42495a5b9a210a8080321d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7fafebeb2f7b70dabec078db9455f284bca4370668c050cb22c987100d4daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppComputeStatus",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "state": "state"},
)
class DataDatabricksAppAppComputeStatus:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5805975aa1b5d33161300bbb5a29ed80f3b8ad837e7f13941840a4cb305fb1)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppComputeStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppComputeStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppComputeStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c36c8b9146c54ef83ca29249df0646c537763ec5678109606844e60b8d53c3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd11944ce305c21d8f7cf7341bf3e17e809438b2f78e0f1f4b473079ed52de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468675b5653444b32eb57ae79c8fa38c7cdaa953d16aba184ac315122f366c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173c1bb6401f29596e88214f54adca1899fc7f57031bdc8e446d239fb39e5bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksAppAppOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3b2518db223e4e5310604754a41f3d739d6969131eb9db28ba824cf84d9e9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDeployment")
    def put_active_deployment(
        self,
        *,
        create_time: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        deployment_artifacts: typing.Optional[typing.Union[DataDatabricksAppAppActiveDeploymentDeploymentArtifacts, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source_code_path: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union[DataDatabricksAppAppActiveDeploymentStatus, typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.
        :param creator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.
        :param deployment_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.
        :param deployment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.
        :param update_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.
        '''
        value = DataDatabricksAppAppActiveDeployment(
            create_time=create_time,
            creator=creator,
            deployment_artifacts=deployment_artifacts,
            deployment_id=deployment_id,
            mode=mode,
            source_code_path=source_code_path,
            status=status,
            update_time=update_time,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDeployment", [value]))

    @jsii.member(jsii_name="putAppStatus")
    def put_app_status(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        value = DataDatabricksAppAppAppStatus(message=message, state=state)

        return typing.cast(None, jsii.invoke(self, "putAppStatus", [value]))

    @jsii.member(jsii_name="putComputeStatus")
    def put_compute_status(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        value = DataDatabricksAppAppComputeStatus(message=message, state=state)

        return typing.cast(None, jsii.invoke(self, "putComputeStatus", [value]))

    @jsii.member(jsii_name="putPendingDeployment")
    def put_pending_deployment(
        self,
        *,
        create_time: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        deployment_artifacts: typing.Optional[typing.Union["DataDatabricksAppAppPendingDeploymentDeploymentArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source_code_path: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union["DataDatabricksAppAppPendingDeploymentStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.
        :param creator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.
        :param deployment_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.
        :param deployment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.
        :param update_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.
        '''
        value = DataDatabricksAppAppPendingDeployment(
            create_time=create_time,
            creator=creator,
            deployment_artifacts=deployment_artifacts,
            deployment_id=deployment_id,
            mode=mode,
            source_code_path=source_code_path,
            status=status,
            update_time=update_time,
        )

        return typing.cast(None, jsii.invoke(self, "putPendingDeployment", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksAppAppResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc070e6aa75826d1aee422a08662e32b3d2e7a2d33197cbf740ffca295f7f4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetActiveDeployment")
    def reset_active_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDeployment", []))

    @jsii.member(jsii_name="resetAppStatus")
    def reset_app_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppStatus", []))

    @jsii.member(jsii_name="resetComputeStatus")
    def reset_compute_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeStatus", []))

    @jsii.member(jsii_name="resetCreateTime")
    def reset_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTime", []))

    @jsii.member(jsii_name="resetCreator")
    def reset_creator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreator", []))

    @jsii.member(jsii_name="resetDefaultSourceCodePath")
    def reset_default_source_code_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSourceCodePath", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetPendingDeployment")
    def reset_pending_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPendingDeployment", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetServicePrincipalClientId")
    def reset_service_principal_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipalClientId", []))

    @jsii.member(jsii_name="resetServicePrincipalId")
    def reset_service_principal_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipalId", []))

    @jsii.member(jsii_name="resetServicePrincipalName")
    def reset_service_principal_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipalName", []))

    @jsii.member(jsii_name="resetUpdater")
    def reset_updater(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdater", []))

    @jsii.member(jsii_name="resetUpdateTime")
    def reset_update_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTime", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="activeDeployment")
    def active_deployment(self) -> DataDatabricksAppAppActiveDeploymentOutputReference:
        return typing.cast(DataDatabricksAppAppActiveDeploymentOutputReference, jsii.get(self, "activeDeployment"))

    @builtins.property
    @jsii.member(jsii_name="appStatus")
    def app_status(self) -> DataDatabricksAppAppAppStatusOutputReference:
        return typing.cast(DataDatabricksAppAppAppStatusOutputReference, jsii.get(self, "appStatus"))

    @builtins.property
    @jsii.member(jsii_name="computeStatus")
    def compute_status(self) -> DataDatabricksAppAppComputeStatusOutputReference:
        return typing.cast(DataDatabricksAppAppComputeStatusOutputReference, jsii.get(self, "computeStatus"))

    @builtins.property
    @jsii.member(jsii_name="pendingDeployment")
    def pending_deployment(
        self,
    ) -> "DataDatabricksAppAppPendingDeploymentOutputReference":
        return typing.cast("DataDatabricksAppAppPendingDeploymentOutputReference", jsii.get(self, "pendingDeployment"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "DataDatabricksAppAppResourcesList":
        return typing.cast("DataDatabricksAppAppResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="activeDeploymentInput")
    def active_deployment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]], jsii.get(self, "activeDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="appStatusInput")
    def app_status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]], jsii.get(self, "appStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="computeStatusInput")
    def compute_status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]], jsii.get(self, "computeStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="createTimeInput")
    def create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="creatorInput")
    def creator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creatorInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSourceCodePathInput")
    def default_source_code_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSourceCodePathInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pendingDeploymentInput")
    def pending_deployment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppPendingDeployment"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppPendingDeployment"]], jsii.get(self, "pendingDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksAppAppResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksAppAppResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalClientIdInput")
    def service_principal_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalIdInput")
    def service_principal_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "servicePrincipalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalNameInput")
    def service_principal_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="updaterInput")
    def updater_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updaterInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeInput")
    def update_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @create_time.setter
    def create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d33d6a1ccddc793902a566c78885a905cb52ceda347b279216f1158af8bae83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @creator.setter
    def creator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a2a8b04e6d75fec842e2a188bec4c4acbda4e59f79687962a29d47e5771e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSourceCodePath")
    def default_source_code_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSourceCodePath"))

    @default_source_code_path.setter
    def default_source_code_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3142ecefd0d0874fe30bc21cbd22e8bd94c3957fd3f1590fd009f3e4b371164e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSourceCodePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cca80ecf9d60cbb265200b55aab089649563a7d918329e065bd5133e6e14b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9d7f845ea60a6e070a7c292af99bbabd03ccf2ca81dc4e8ab3b5229976af04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalClientId")
    def service_principal_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalClientId"))

    @service_principal_client_id.setter
    def service_principal_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e409fb1955e297600797901c5f1d082c7a243d5ac19d5e4225f28f16435aa631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalId")
    def service_principal_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "servicePrincipalId"))

    @service_principal_id.setter
    def service_principal_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d61175a850efae821c1f1f1068e2db15773aa29ba343780a29ad72d4cb3e50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalName")
    def service_principal_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalName"))

    @service_principal_name.setter
    def service_principal_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0493480854b927ed51160507bd54f13f31f8f35e0bc5f468b302d927032239d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updater")
    def updater(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updater"))

    @updater.setter
    def updater(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe19af2caa95a37f96f6156b373bf5434a0a07513cdf49c4a7b15f26cd5ca48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updater", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2d8eb47455540f3e3310c15fcccb5a7a39caa4eb005063ac6046c68f54633a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258497a153905adf9c5fa1f8b40f938ea9d01bc9976890ac0ee9002023652a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataDatabricksAppApp]:
        return typing.cast(typing.Optional[DataDatabricksAppApp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataDatabricksAppApp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c91a7ee6b91ad3f5ac2db42b0c1d027f1355be8ec46cc3d1818873072dc89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "create_time": "createTime",
        "creator": "creator",
        "deployment_artifacts": "deploymentArtifacts",
        "deployment_id": "deploymentId",
        "mode": "mode",
        "source_code_path": "sourceCodePath",
        "status": "status",
        "update_time": "updateTime",
    },
)
class DataDatabricksAppAppPendingDeployment:
    def __init__(
        self,
        *,
        create_time: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        deployment_artifacts: typing.Optional[typing.Union["DataDatabricksAppAppPendingDeploymentDeploymentArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source_code_path: typing.Optional[builtins.str] = None,
        status: typing.Optional[typing.Union["DataDatabricksAppAppPendingDeploymentStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.
        :param creator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.
        :param deployment_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.
        :param deployment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.
        :param update_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.
        '''
        if isinstance(deployment_artifacts, dict):
            deployment_artifacts = DataDatabricksAppAppPendingDeploymentDeploymentArtifacts(**deployment_artifacts)
        if isinstance(status, dict):
            status = DataDatabricksAppAppPendingDeploymentStatus(**status)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca7d1c1116c3c252ff1688989072eac86a7770c82795c695ec6b44ca12260fc)
            check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
            check_type(argname="argument creator", value=creator, expected_type=type_hints["creator"])
            check_type(argname="argument deployment_artifacts", value=deployment_artifacts, expected_type=type_hints["deployment_artifacts"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument source_code_path", value=source_code_path, expected_type=type_hints["source_code_path"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument update_time", value=update_time, expected_type=type_hints["update_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_time is not None:
            self._values["create_time"] = create_time
        if creator is not None:
            self._values["creator"] = creator
        if deployment_artifacts is not None:
            self._values["deployment_artifacts"] = deployment_artifacts
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id
        if mode is not None:
            self._values["mode"] = mode
        if source_code_path is not None:
            self._values["source_code_path"] = source_code_path
        if status is not None:
            self._values["status"] = status
        if update_time is not None:
            self._values["update_time"] = update_time

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#create_time DataDatabricksApp#create_time}.'''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#creator DataDatabricksApp#creator}.'''
        result = self._values.get("creator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_artifacts(
        self,
    ) -> typing.Optional["DataDatabricksAppAppPendingDeploymentDeploymentArtifacts"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_artifacts DataDatabricksApp#deployment_artifacts}.'''
        result = self._values.get("deployment_artifacts")
        return typing.cast(typing.Optional["DataDatabricksAppAppPendingDeploymentDeploymentArtifacts"], result)

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#deployment_id DataDatabricksApp#deployment_id}.'''
        result = self._values.get("deployment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#mode DataDatabricksApp#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_code_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.'''
        result = self._values.get("source_code_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["DataDatabricksAppAppPendingDeploymentStatus"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#status DataDatabricksApp#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional["DataDatabricksAppAppPendingDeploymentStatus"], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#update_time DataDatabricksApp#update_time}.'''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppPendingDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeploymentDeploymentArtifacts",
    jsii_struct_bases=[],
    name_mapping={"source_code_path": "sourceCodePath"},
)
class DataDatabricksAppAppPendingDeploymentDeploymentArtifacts:
    def __init__(
        self,
        *,
        source_code_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c130a3c3872f1b972cd7c2ffb16258f15cacc2df6177e19c048fb3bd0b7c176e)
            check_type(argname="argument source_code_path", value=source_code_path, expected_type=type_hints["source_code_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_code_path is not None:
            self._values["source_code_path"] = source_code_path

    @builtins.property
    def source_code_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.'''
        result = self._values.get("source_code_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppPendingDeploymentDeploymentArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppPendingDeploymentDeploymentArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeploymentDeploymentArtifactsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dd973871602a1c961d0b2820bf9fec2593600bc338c7a4e09debc399c3edcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceCodePath")
    def reset_source_code_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCodePath", []))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePathInput")
    def source_code_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCodePathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePath")
    def source_code_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCodePath"))

    @source_code_path.setter
    def source_code_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8799bafbcc0228941be5c946e23c9046b60e247dfddc8fd8b85898555fcfe0fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCodePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4305b73444632d7f0a991a51f52fe4a7c45f21842757682a96ecb60da2ea666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksAppAppPendingDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeploymentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258f8b6a3962797d0f6453b6d7155edad16a1e8984c76eb55fdf3093dcb72b02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentArtifacts")
    def put_deployment_artifacts(
        self,
        *,
        source_code_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_code_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#source_code_path DataDatabricksApp#source_code_path}.
        '''
        value = DataDatabricksAppAppPendingDeploymentDeploymentArtifacts(
            source_code_path=source_code_path
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentArtifacts", [value]))

    @jsii.member(jsii_name="putStatus")
    def put_status(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        value = DataDatabricksAppAppPendingDeploymentStatus(
            message=message, state=state
        )

        return typing.cast(None, jsii.invoke(self, "putStatus", [value]))

    @jsii.member(jsii_name="resetCreateTime")
    def reset_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTime", []))

    @jsii.member(jsii_name="resetCreator")
    def reset_creator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreator", []))

    @jsii.member(jsii_name="resetDeploymentArtifacts")
    def reset_deployment_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentArtifacts", []))

    @jsii.member(jsii_name="resetDeploymentId")
    def reset_deployment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentId", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSourceCodePath")
    def reset_source_code_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceCodePath", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetUpdateTime")
    def reset_update_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTime", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentArtifacts")
    def deployment_artifacts(
        self,
    ) -> DataDatabricksAppAppPendingDeploymentDeploymentArtifactsOutputReference:
        return typing.cast(DataDatabricksAppAppPendingDeploymentDeploymentArtifactsOutputReference, jsii.get(self, "deploymentArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "DataDatabricksAppAppPendingDeploymentStatusOutputReference":
        return typing.cast("DataDatabricksAppAppPendingDeploymentStatusOutputReference", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="createTimeInput")
    def create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="creatorInput")
    def creator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creatorInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentArtifactsInput")
    def deployment_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]], jsii.get(self, "deploymentArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCodePathInput")
    def source_code_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCodePathInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppPendingDeploymentStatus"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppPendingDeploymentStatus"]], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeInput")
    def update_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @create_time.setter
    def create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae142d64af870140dc07be025d701b484b633c52fe0b29b6bd8c1ad6ac6d879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @creator.setter
    def creator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51cf711710988298f01b5d5f072dff8f3ccda0db7938053f07ba598ff9b14f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a77a6980dfe55b86e43f2ffd7b4c816de0e8bcb509bff1f73f21a4b4cdbb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9347059a1424f7fcee0c57489543148a5838c3a9508c81df98e0cb0cd05750f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceCodePath")
    def source_code_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCodePath"))

    @source_code_path.setter
    def source_code_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4d25275aa40728f27863a6a8cf1ef20ab65b66cdd4e38621319450be975805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCodePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b03f712de144d4cd9922e1e76a64dfd573299911a21fc2a3f6dddc21e58512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeployment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeployment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeployment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3d243c9fbaa17c10df37536f858413721fa63de23aa0a722c8ef31f9f5db75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeploymentStatus",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "state": "state"},
)
class DataDatabricksAppAppPendingDeploymentStatus:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6305c4dc8bf5b301d1e81dd8ef063aa6d39147cb829c54fb17ffdf88ebfb1976)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#message DataDatabricksApp#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#state DataDatabricksApp#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppPendingDeploymentStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppPendingDeploymentStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppPendingDeploymentStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6084681e1d687edf76cbe69ead2cc45fdbdf1d1e29600f5a5463469a50b544)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2778d2984d3d5f559f904476162a0c08f9f11c16fde8c81517dbca7ca256c573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67838d483d86e466ea5e96a99c8f2d62fbc75b5c94ec9abc60e363dbc5f37198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089ad5851b337d08235f55e4f373d7c91a0793745d553732abbb3093173948bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResources",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "job": "job",
        "secret": "secret",
        "serving_endpoint": "servingEndpoint",
        "sql_warehouse": "sqlWarehouse",
    },
)
class DataDatabricksAppAppResources:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        job: typing.Optional[typing.Union["DataDatabricksAppAppResourcesJob", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["DataDatabricksAppAppResourcesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        serving_endpoint: typing.Optional[typing.Union["DataDatabricksAppAppResourcesServingEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_warehouse: typing.Optional[typing.Union["DataDatabricksAppAppResourcesSqlWarehouse", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#description DataDatabricksApp#description}.
        :param job: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#job DataDatabricksApp#job}.
        :param secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#secret DataDatabricksApp#secret}.
        :param serving_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#serving_endpoint DataDatabricksApp#serving_endpoint}.
        :param sql_warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#sql_warehouse DataDatabricksApp#sql_warehouse}.
        '''
        if isinstance(job, dict):
            job = DataDatabricksAppAppResourcesJob(**job)
        if isinstance(secret, dict):
            secret = DataDatabricksAppAppResourcesSecret(**secret)
        if isinstance(serving_endpoint, dict):
            serving_endpoint = DataDatabricksAppAppResourcesServingEndpoint(**serving_endpoint)
        if isinstance(sql_warehouse, dict):
            sql_warehouse = DataDatabricksAppAppResourcesSqlWarehouse(**sql_warehouse)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fb10be780cec5a535ea4d8b83172f041293d530254765ed0a933fa61245374)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument serving_endpoint", value=serving_endpoint, expected_type=type_hints["serving_endpoint"])
            check_type(argname="argument sql_warehouse", value=sql_warehouse, expected_type=type_hints["sql_warehouse"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if job is not None:
            self._values["job"] = job
        if secret is not None:
            self._values["secret"] = secret
        if serving_endpoint is not None:
            self._values["serving_endpoint"] = serving_endpoint
        if sql_warehouse is not None:
            self._values["sql_warehouse"] = sql_warehouse

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#description DataDatabricksApp#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job(self) -> typing.Optional["DataDatabricksAppAppResourcesJob"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#job DataDatabricksApp#job}.'''
        result = self._values.get("job")
        return typing.cast(typing.Optional["DataDatabricksAppAppResourcesJob"], result)

    @builtins.property
    def secret(self) -> typing.Optional["DataDatabricksAppAppResourcesSecret"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#secret DataDatabricksApp#secret}.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["DataDatabricksAppAppResourcesSecret"], result)

    @builtins.property
    def serving_endpoint(
        self,
    ) -> typing.Optional["DataDatabricksAppAppResourcesServingEndpoint"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#serving_endpoint DataDatabricksApp#serving_endpoint}.'''
        result = self._values.get("serving_endpoint")
        return typing.cast(typing.Optional["DataDatabricksAppAppResourcesServingEndpoint"], result)

    @builtins.property
    def sql_warehouse(
        self,
    ) -> typing.Optional["DataDatabricksAppAppResourcesSqlWarehouse"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#sql_warehouse DataDatabricksApp#sql_warehouse}.'''
        result = self._values.get("sql_warehouse")
        return typing.cast(typing.Optional["DataDatabricksAppAppResourcesSqlWarehouse"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesJob",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "permission": "permission"},
)
class DataDatabricksAppAppResourcesJob:
    def __init__(self, *, id: builtins.str, permission: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02726d903612396a1bb9ed10d8be76f7429b0ca6485e6f6008e3208a6858559)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "permission": permission,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.'''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppResourcesJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppResourcesJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesJobOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376e6b11b0cfdebc9b1c9370c19aa7594209dd3f05c3faba7e4a98398de0fec0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0106a086afb44bb07993d7342debff44e97b8ba4fb1355739ed8c43cc372521a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24043cda4e4f8e305ff81edea9c7a2095fa26ec1e059b77cb9b8cdc9b2a8abeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e12613dd2fe06054dde0960b3b2f03415acdab43c05e950a22e25af04646fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksAppAppResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435fa4c92211a5324bde412354a8d4bb6a84ec2f2ed600f22f898ccd8f2037c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataDatabricksAppAppResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418293d3bbb8099f34f29a3d39ae9a3467c2e847d3dbaee90d03ebcbe27a31f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksAppAppResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4e91a2a2d4303f9d6628e6b3f99e1312dd496ea9619a329596826763675d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e5eccdb46aeb02258d7584c7bd406e6e7b1259d0ee2cc1dc7f63c18bbbf7f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a74b643a6730956250780b4b1e489ba154acdb5025a65059fd334b38dba7c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksAppAppResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksAppAppResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksAppAppResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f0c3614501fa5762f08de90594e2eaff115ba79d98a3c96bf6ac6c6e7823a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksAppAppResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011037957b4cfae4c9b6fbc26e17a89ce17369c45425045f1abc42972416c667)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putJob")
    def put_job(self, *, id: builtins.str, permission: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        value = DataDatabricksAppAppResourcesJob(id=id, permission=permission)

        return typing.cast(None, jsii.invoke(self, "putJob", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        key: builtins.str,
        permission: builtins.str,
        scope: builtins.str,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#key DataDatabricksApp#key}.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#scope DataDatabricksApp#scope}.
        '''
        value = DataDatabricksAppAppResourcesSecret(
            key=key, permission=permission, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putServingEndpoint")
    def put_serving_endpoint(
        self,
        *,
        name: builtins.str,
        permission: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        value = DataDatabricksAppAppResourcesServingEndpoint(
            name=name, permission=permission
        )

        return typing.cast(None, jsii.invoke(self, "putServingEndpoint", [value]))

    @jsii.member(jsii_name="putSqlWarehouse")
    def put_sql_warehouse(self, *, id: builtins.str, permission: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        value = DataDatabricksAppAppResourcesSqlWarehouse(id=id, permission=permission)

        return typing.cast(None, jsii.invoke(self, "putSqlWarehouse", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetJob")
    def reset_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJob", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetServingEndpoint")
    def reset_serving_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServingEndpoint", []))

    @jsii.member(jsii_name="resetSqlWarehouse")
    def reset_sql_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlWarehouse", []))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> DataDatabricksAppAppResourcesJobOutputReference:
        return typing.cast(DataDatabricksAppAppResourcesJobOutputReference, jsii.get(self, "job"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "DataDatabricksAppAppResourcesSecretOutputReference":
        return typing.cast("DataDatabricksAppAppResourcesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="servingEndpoint")
    def serving_endpoint(
        self,
    ) -> "DataDatabricksAppAppResourcesServingEndpointOutputReference":
        return typing.cast("DataDatabricksAppAppResourcesServingEndpointOutputReference", jsii.get(self, "servingEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="sqlWarehouse")
    def sql_warehouse(
        self,
    ) -> "DataDatabricksAppAppResourcesSqlWarehouseOutputReference":
        return typing.cast("DataDatabricksAppAppResourcesSqlWarehouseOutputReference", jsii.get(self, "sqlWarehouse"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="jobInput")
    def job_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]], jsii.get(self, "jobInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesSecret"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesSecret"]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="servingEndpointInput")
    def serving_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesServingEndpoint"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesServingEndpoint"]], jsii.get(self, "servingEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlWarehouseInput")
    def sql_warehouse_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesSqlWarehouse"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksAppAppResourcesSqlWarehouse"]], jsii.get(self, "sqlWarehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82fd010ea1504abfbd19ad522fb0907c5de05eb7ce9f9745f9ba43299f8490c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604c29e8103952b0cc15f0fd0c5a8ce3c3bbf3d8cbb1d929a244215d21911985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00f3d017092fe113b59d34f702792fce8d7a6cea866eb8a00a2350bef25856c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "permission": "permission", "scope": "scope"},
)
class DataDatabricksAppAppResourcesSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        permission: builtins.str,
        scope: builtins.str,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#key DataDatabricksApp#key}.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#scope DataDatabricksApp#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1adaba5934969ccce39731ecc93354744ecc0f77d9dda6bb7ff4d0b161f4ae3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "permission": permission,
            "scope": scope,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#key DataDatabricksApp#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.'''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#scope DataDatabricksApp#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppResourcesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppResourcesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesSecretOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570b87d4aae6f61edf409be8654dd974a1346d6d6e4fefa91f6337201b0284b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab4570f5a5e75f1c6ac7cb9d5f3b187d804851362515e7f56338261c4786118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fda5a3894b531ba19758c9c4e10b840d474d956caa717e3bc167f66160eccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485b19f74f664f4269e153f1ed3bffdec7220e22da53ca835f5a6492bbd5e6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2fed2141fe39ec07f4e4ebe142a42e55fbabcac167a9847782d2193d82c12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesServingEndpoint",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "permission": "permission"},
)
class DataDatabricksAppAppResourcesServingEndpoint:
    def __init__(self, *, name: builtins.str, permission: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d828032c0f1b448dd9acc2d246e2ab1de4f358a450cc758b1ffc9eafdf38ed6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "permission": permission,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.'''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppResourcesServingEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppResourcesServingEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesServingEndpointOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d919df2eb5f0713f68e643df762b57d1c0b934554d9a2ee9f84ad88f2590f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef63f2944564e43b903760963d6fcd959cf6ff98f4e007ac4ece2beb7983fc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c95e6faf8d4d072e6dbf38104bad9de4663d768fcb9430b49f2aba56f6ef8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesServingEndpoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesServingEndpoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesServingEndpoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e376434de71e2c722311f32644f982892386bd1c7bfae712dd71673f2071317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesSqlWarehouse",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "permission": "permission"},
)
class DataDatabricksAppAppResourcesSqlWarehouse:
    def __init__(self, *, id: builtins.str, permission: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a75365f026cbc494698cf4bcc9ba3f1e9ff8651b204f32bdd4001645f7d813)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "permission": permission,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#id DataDatabricksApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#permission DataDatabricksApp#permission}.'''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppAppResourcesSqlWarehouse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksAppAppResourcesSqlWarehouseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppAppResourcesSqlWarehouseOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ca2159dc0d54954537c6c2cdeab41af566a9e3fe97f978a3d986f0473cff41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4162cfdfadc82aead255444a3a5bdf16c3cd5e721675872b00d9493a2b251f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b205aea94685bdc2bc8cfe5c348f7531ea689f0691eb8480606e0d62198a2424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSqlWarehouse]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSqlWarehouse]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSqlWarehouse]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494474b238f843d871fbddcbf71a08823e0c99d0369ce8f22baa8c6e84886c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksApp.DataDatabricksAppConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
    },
)
class DataDatabricksAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841c13f74893327a3246e8c0ebb9736571b5a1e9bbeffbb846e37f7d49c34c10)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.61.0/docs/data-sources/app#name DataDatabricksApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataDatabricksApp",
    "DataDatabricksAppApp",
    "DataDatabricksAppAppActiveDeployment",
    "DataDatabricksAppAppActiveDeploymentDeploymentArtifacts",
    "DataDatabricksAppAppActiveDeploymentDeploymentArtifactsOutputReference",
    "DataDatabricksAppAppActiveDeploymentOutputReference",
    "DataDatabricksAppAppActiveDeploymentStatus",
    "DataDatabricksAppAppActiveDeploymentStatusOutputReference",
    "DataDatabricksAppAppAppStatus",
    "DataDatabricksAppAppAppStatusOutputReference",
    "DataDatabricksAppAppComputeStatus",
    "DataDatabricksAppAppComputeStatusOutputReference",
    "DataDatabricksAppAppOutputReference",
    "DataDatabricksAppAppPendingDeployment",
    "DataDatabricksAppAppPendingDeploymentDeploymentArtifacts",
    "DataDatabricksAppAppPendingDeploymentDeploymentArtifactsOutputReference",
    "DataDatabricksAppAppPendingDeploymentOutputReference",
    "DataDatabricksAppAppPendingDeploymentStatus",
    "DataDatabricksAppAppPendingDeploymentStatusOutputReference",
    "DataDatabricksAppAppResources",
    "DataDatabricksAppAppResourcesJob",
    "DataDatabricksAppAppResourcesJobOutputReference",
    "DataDatabricksAppAppResourcesList",
    "DataDatabricksAppAppResourcesOutputReference",
    "DataDatabricksAppAppResourcesSecret",
    "DataDatabricksAppAppResourcesSecretOutputReference",
    "DataDatabricksAppAppResourcesServingEndpoint",
    "DataDatabricksAppAppResourcesServingEndpointOutputReference",
    "DataDatabricksAppAppResourcesSqlWarehouse",
    "DataDatabricksAppAppResourcesSqlWarehouseOutputReference",
    "DataDatabricksAppConfig",
]

publication.publish()

def _typecheckingstub__9f0ce022004568ff5e253109396eece8a5fbd277f2a640530db20fd3555f6834(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b673f1de1f6da52cfb1b5896457971a4bec9ac2721f0d3b2351ca4d5117146e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3feef38a02de41c08393b96e84868d66cc6770ca3489ebc29e3c90273e99c43d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e4670df0b4e95281aa8f15f8d6f1b643ae427b77323aa965560d3c5b0f4e84(
    *,
    name: builtins.str,
    active_deployment: typing.Optional[typing.Union[DataDatabricksAppAppActiveDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    app_status: typing.Optional[typing.Union[DataDatabricksAppAppAppStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_status: typing.Optional[typing.Union[DataDatabricksAppAppComputeStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    create_time: typing.Optional[builtins.str] = None,
    creator: typing.Optional[builtins.str] = None,
    default_source_code_path: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    pending_deployment: typing.Optional[typing.Union[DataDatabricksAppAppPendingDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksAppAppResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_principal_client_id: typing.Optional[builtins.str] = None,
    service_principal_id: typing.Optional[jsii.Number] = None,
    service_principal_name: typing.Optional[builtins.str] = None,
    updater: typing.Optional[builtins.str] = None,
    update_time: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f4711583806e7694ce67324f7c2a7d0e6a7e02d3452b53695821d7328dff9f(
    *,
    create_time: typing.Optional[builtins.str] = None,
    creator: typing.Optional[builtins.str] = None,
    deployment_artifacts: typing.Optional[typing.Union[DataDatabricksAppAppActiveDeploymentDeploymentArtifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_id: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source_code_path: typing.Optional[builtins.str] = None,
    status: typing.Optional[typing.Union[DataDatabricksAppAppActiveDeploymentStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    update_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67345022ac46cf2ae5a669c5b6d75f1c9a37433a26a699dbae27a966c9c7b8d1(
    *,
    source_code_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e1076106fd372f777193eb77b562771a2cf5e59f0b9c44b82090c9dca57b63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d38debada89b38b0668887b66db8160df281fdbe4f15bdc27f41e4cb8d8a1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc9ddcb553e377c0ce53eff68168574f7676315cdcb807c520b95d03e6d4174(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentDeploymentArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dac4fa7695cb41f42af1ead02f367fa98308d700c6307467a1fd6eec46138e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46a687ba61802132d2243b0b2dda3bf75ff3bdffcc7957de92f830b0cb82f2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ba906c2eb376a0dbede89bf2a9bd5c241b41026be9c46bbbb513e2399d9566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34ad3d2b69cb9e973430dbb810b78cd108ce6fd0b74f910a1d8e0a26a2efaa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73d49aeb62dcb6d418177bd3ae0bbc72306c9ed8f1f91404bdc15012752ceba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1ebaeed7531b8d9ec378fd1094d2ae43ce6af3d094465db74e1e3d7f38396a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1733c5d71d3ecba390e49759d370ff84f7ae4c23fcd920b23e00b8f8771925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7b189a795f6f77480ea5c93471e17d540da917c4e32db05d6430288f86a480(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeployment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd09cadf4eb9cd1110c31cee3bc7902713331c0a8b530bff3016e7f6539fd62(
    *,
    message: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0b4a396fe5c01b468bf7cd50946d4912d7be0c694b38fff952af8db4d51761(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fe0300a1d9aec55db6bc3fe667cd3bfbeb1e9544f232989051d62af81f63e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fa459459b148a5cc4db9e0cf2fb1865284716a25b9e4991c5637ab92a28173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffadc2e787f8507ea0afa102d9a601793363a09e658aae305bfd8b7a46e5b2d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppActiveDeploymentStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34503f268216d5a85b5e7fd17b0944a099675350bcba8a3722b6fafae8a5171b(
    *,
    message: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509853b1ce6017a7ca645c0a1f122efbd3b133bd6dc4c7f6accad30f91ef18bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442a69df5a5d681f5bb440c762319b0d40deaea97998c1bfe1a1cf46fd7d9295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe8922b4ef896ebc1e39b6a2bcb8671eb32fe3f42495a5b9a210a8080321d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7fafebeb2f7b70dabec078db9455f284bca4370668c050cb22c987100d4daa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppAppStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5805975aa1b5d33161300bbb5a29ed80f3b8ad837e7f13941840a4cb305fb1(
    *,
    message: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c36c8b9146c54ef83ca29249df0646c537763ec5678109606844e60b8d53c3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd11944ce305c21d8f7cf7341bf3e17e809438b2f78e0f1f4b473079ed52de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468675b5653444b32eb57ae79c8fa38c7cdaa953d16aba184ac315122f366c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173c1bb6401f29596e88214f54adca1899fc7f57031bdc8e446d239fb39e5bd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppComputeStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3b2518db223e4e5310604754a41f3d739d6969131eb9db28ba824cf84d9e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc070e6aa75826d1aee422a08662e32b3d2e7a2d33197cbf740ffca295f7f4d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksAppAppResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d33d6a1ccddc793902a566c78885a905cb52ceda347b279216f1158af8bae83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a2a8b04e6d75fec842e2a188bec4c4acbda4e59f79687962a29d47e5771e01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3142ecefd0d0874fe30bc21cbd22e8bd94c3957fd3f1590fd009f3e4b371164e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cca80ecf9d60cbb265200b55aab089649563a7d918329e065bd5133e6e14b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9d7f845ea60a6e070a7c292af99bbabd03ccf2ca81dc4e8ab3b5229976af04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e409fb1955e297600797901c5f1d082c7a243d5ac19d5e4225f28f16435aa631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d61175a850efae821c1f1f1068e2db15773aa29ba343780a29ad72d4cb3e50c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0493480854b927ed51160507bd54f13f31f8f35e0bc5f468b302d927032239d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe19af2caa95a37f96f6156b373bf5434a0a07513cdf49c4a7b15f26cd5ca48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2d8eb47455540f3e3310c15fcccb5a7a39caa4eb005063ac6046c68f54633a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258497a153905adf9c5fa1f8b40f938ea9d01bc9976890ac0ee9002023652a3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c91a7ee6b91ad3f5ac2db42b0c1d027f1355be8ec46cc3d1818873072dc89f(
    value: typing.Optional[DataDatabricksAppApp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca7d1c1116c3c252ff1688989072eac86a7770c82795c695ec6b44ca12260fc(
    *,
    create_time: typing.Optional[builtins.str] = None,
    creator: typing.Optional[builtins.str] = None,
    deployment_artifacts: typing.Optional[typing.Union[DataDatabricksAppAppPendingDeploymentDeploymentArtifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_id: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source_code_path: typing.Optional[builtins.str] = None,
    status: typing.Optional[typing.Union[DataDatabricksAppAppPendingDeploymentStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    update_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c130a3c3872f1b972cd7c2ffb16258f15cacc2df6177e19c048fb3bd0b7c176e(
    *,
    source_code_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dd973871602a1c961d0b2820bf9fec2593600bc338c7a4e09debc399c3edcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8799bafbcc0228941be5c946e23c9046b60e247dfddc8fd8b85898555fcfe0fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4305b73444632d7f0a991a51f52fe4a7c45f21842757682a96ecb60da2ea666(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentDeploymentArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258f8b6a3962797d0f6453b6d7155edad16a1e8984c76eb55fdf3093dcb72b02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae142d64af870140dc07be025d701b484b633c52fe0b29b6bd8c1ad6ac6d879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51cf711710988298f01b5d5f072dff8f3ccda0db7938053f07ba598ff9b14f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a77a6980dfe55b86e43f2ffd7b4c816de0e8bcb509bff1f73f21a4b4cdbb4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9347059a1424f7fcee0c57489543148a5838c3a9508c81df98e0cb0cd05750f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4d25275aa40728f27863a6a8cf1ef20ab65b66cdd4e38621319450be975805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b03f712de144d4cd9922e1e76a64dfd573299911a21fc2a3f6dddc21e58512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3d243c9fbaa17c10df37536f858413721fa63de23aa0a722c8ef31f9f5db75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeployment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6305c4dc8bf5b301d1e81dd8ef063aa6d39147cb829c54fb17ffdf88ebfb1976(
    *,
    message: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6084681e1d687edf76cbe69ead2cc45fdbdf1d1e29600f5a5463469a50b544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2778d2984d3d5f559f904476162a0c08f9f11c16fde8c81517dbca7ca256c573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67838d483d86e466ea5e96a99c8f2d62fbc75b5c94ec9abc60e363dbc5f37198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089ad5851b337d08235f55e4f373d7c91a0793745d553732abbb3093173948bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppPendingDeploymentStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fb10be780cec5a535ea4d8b83172f041293d530254765ed0a933fa61245374(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    job: typing.Optional[typing.Union[DataDatabricksAppAppResourcesJob, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[DataDatabricksAppAppResourcesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    serving_endpoint: typing.Optional[typing.Union[DataDatabricksAppAppResourcesServingEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_warehouse: typing.Optional[typing.Union[DataDatabricksAppAppResourcesSqlWarehouse, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02726d903612396a1bb9ed10d8be76f7429b0ca6485e6f6008e3208a6858559(
    *,
    id: builtins.str,
    permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376e6b11b0cfdebc9b1c9370c19aa7594209dd3f05c3faba7e4a98398de0fec0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0106a086afb44bb07993d7342debff44e97b8ba4fb1355739ed8c43cc372521a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24043cda4e4f8e305ff81edea9c7a2095fa26ec1e059b77cb9b8cdc9b2a8abeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e12613dd2fe06054dde0960b3b2f03415acdab43c05e950a22e25af04646fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesJob]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435fa4c92211a5324bde412354a8d4bb6a84ec2f2ed600f22f898ccd8f2037c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418293d3bbb8099f34f29a3d39ae9a3467c2e847d3dbaee90d03ebcbe27a31f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4e91a2a2d4303f9d6628e6b3f99e1312dd496ea9619a329596826763675d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e5eccdb46aeb02258d7584c7bd406e6e7b1259d0ee2cc1dc7f63c18bbbf7f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a74b643a6730956250780b4b1e489ba154acdb5025a65059fd334b38dba7c94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f0c3614501fa5762f08de90594e2eaff115ba79d98a3c96bf6ac6c6e7823a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksAppAppResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011037957b4cfae4c9b6fbc26e17a89ce17369c45425045f1abc42972416c667(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82fd010ea1504abfbd19ad522fb0907c5de05eb7ce9f9745f9ba43299f8490c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604c29e8103952b0cc15f0fd0c5a8ce3c3bbf3d8cbb1d929a244215d21911985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00f3d017092fe113b59d34f702792fce8d7a6cea866eb8a00a2350bef25856c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1adaba5934969ccce39731ecc93354744ecc0f77d9dda6bb7ff4d0b161f4ae3(
    *,
    key: builtins.str,
    permission: builtins.str,
    scope: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570b87d4aae6f61edf409be8654dd974a1346d6d6e4fefa91f6337201b0284b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab4570f5a5e75f1c6ac7cb9d5f3b187d804851362515e7f56338261c4786118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fda5a3894b531ba19758c9c4e10b840d474d956caa717e3bc167f66160eccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485b19f74f664f4269e153f1ed3bffdec7220e22da53ca835f5a6492bbd5e6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2fed2141fe39ec07f4e4ebe142a42e55fbabcac167a9847782d2193d82c12a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d828032c0f1b448dd9acc2d246e2ab1de4f358a450cc758b1ffc9eafdf38ed6(
    *,
    name: builtins.str,
    permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d919df2eb5f0713f68e643df762b57d1c0b934554d9a2ee9f84ad88f2590f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef63f2944564e43b903760963d6fcd959cf6ff98f4e007ac4ece2beb7983fc3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c95e6faf8d4d072e6dbf38104bad9de4663d768fcb9430b49f2aba56f6ef8d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e376434de71e2c722311f32644f982892386bd1c7bfae712dd71673f2071317(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesServingEndpoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a75365f026cbc494698cf4bcc9ba3f1e9ff8651b204f32bdd4001645f7d813(
    *,
    id: builtins.str,
    permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ca2159dc0d54954537c6c2cdeab41af566a9e3fe97f978a3d986f0473cff41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4162cfdfadc82aead255444a3a5bdf16c3cd5e721675872b00d9493a2b251f05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b205aea94685bdc2bc8cfe5c348f7531ea689f0691eb8480606e0d62198a2424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494474b238f843d871fbddcbf71a08823e0c99d0369ce8f22baa8c6e84886c9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksAppAppResourcesSqlWarehouse]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841c13f74893327a3246e8c0ebb9736571b5a1e9bbeffbb846e37f7d49c34c10(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
