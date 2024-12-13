r'''
# `snowflake_procedure`

Refer to the Terraform Registry for docs: [`snowflake_procedure`](https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure).
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


class Procedure(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedure.Procedure",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure snowflake_procedure}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        statement: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        execute_as: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_behavior: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure snowflake_procedure} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the procedure. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#database Procedure#database}
        :param name: Specifies the identifier for the procedure; does not have to be unique for the schema in which the procedure is created. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#name Procedure#name}
        :param return_type: The return type of the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_type Procedure#return_type}
        :param schema: The schema in which to create the procedure. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#schema Procedure#schema}
        :param statement: Specifies the code used to create the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#statement Procedure#statement}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#arguments Procedure#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#comment Procedure#comment}
        :param execute_as: Sets execution context. Allowed values are CALLER and OWNER (consult a proper section in the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-procedure#id1>`_). For more information see `caller's rights and owner's rights <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#execute_as Procedure#execute_as}
        :param handler: The handler method for Java / Python procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#handler Procedure#handler}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#id Procedure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: Imports for Java / Python procedures. For Java this a list of jar files, for Python this is a list of Python files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#imports Procedure#imports}
        :param language: Specifies the language of the stored procedure code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#language Procedure#language}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#null_input_behavior Procedure#null_input_behavior}
        :param packages: List of package imports to use for Java / Python procedures. For Java, package imports should be of the form: package_name:version_number, where package_name is snowflake_domain:package. For Python use it should be: ('numpy','pandas','xgboost==1.5.0'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#packages Procedure#packages}
        :param return_behavior: Specifies the behavior of the function when returning results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_behavior Procedure#return_behavior}
        :param runtime_version: Required for Python procedures. Specifies Python runtime version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#runtime_version Procedure#runtime_version}
        :param secure: Specifies that the procedure is secure. For more information about secure procedures, see Protecting Sensitive Information with Secure UDFs and Stored Procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#secure Procedure#secure}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9987cca8b445cddeff76d27d8c792f688bc8e92ee1b896b860b0fa51f14ff8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProcedureConfig(
            database=database,
            name=name,
            return_type=return_type,
            schema=schema,
            statement=statement,
            arguments=arguments,
            comment=comment,
            execute_as=execute_as,
            handler=handler,
            id=id,
            imports=imports,
            language=language,
            null_input_behavior=null_input_behavior,
            packages=packages,
            return_behavior=return_behavior,
            runtime_version=runtime_version,
            secure=secure,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Procedure resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Procedure to import.
        :param import_from_id: The id of the existing Procedure that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Procedure to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e16813566d0354f979c60c7621afd1aed1d0133ce0f9ff29a2e3806648d0b9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f551de5ce61230c81d600f7b801e3cb7c86ddaf813bae8f9b1cecae77d8a8085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetExecuteAs")
    def reset_execute_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteAs", []))

    @jsii.member(jsii_name="resetHandler")
    def reset_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandler", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImports")
    def reset_imports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImports", []))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetNullInputBehavior")
    def reset_null_input_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullInputBehavior", []))

    @jsii.member(jsii_name="resetPackages")
    def reset_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackages", []))

    @jsii.member(jsii_name="resetReturnBehavior")
    def reset_return_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnBehavior", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @jsii.member(jsii_name="resetSecure")
    def reset_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecure", []))

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
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> "ProcedureArgumentsList":
        return typing.cast("ProcedureArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureArguments"]]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="executeAsInput")
    def execute_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executeAsInput"))

    @builtins.property
    @jsii.member(jsii_name="handlerInput")
    def handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handlerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importsInput")
    def imports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "importsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullInputBehaviorInput")
    def null_input_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nullInputBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="packagesInput")
    def packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packagesInput"))

    @builtins.property
    @jsii.member(jsii_name="returnBehaviorInput")
    def return_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="secureInput")
    def secure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureInput"))

    @builtins.property
    @jsii.member(jsii_name="statementInput")
    def statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a5042d617b7357761bb18447e8499a71762761de20f1fb9eaddfa7f2e9890a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c816f95eb66fac7e742e16ae8159a7db152369ce4eccaf9e21f3158b5cb4f1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executeAs")
    def execute_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executeAs"))

    @execute_as.setter
    def execute_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39fd112214bec71e2afbab1a320c9fc7ec84117d2f3c73943fe0144f71ed82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48a2bbca602431b6df7f85c15ab6663a64a15c2274e22ce5c672dbcdab3b761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e5b3b13cf1311a9ee172d65d7990fe3cad2403570ced58ac4572763812de57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imports")
    def imports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imports"))

    @imports.setter
    def imports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909c1e0dd9f00fbc61a8602e290adbde6681ddad4cb17d3eec6e85fa6f687881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a28cdf4745a8f54328ee961adb59a2dbdda670815070d2ed11fd5548b69cd8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b197f6ae29938aba6b168c0b1154d201d1d06e65a81ff5951793e40f07396d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112c0e194907e062fe70531d6837af853d7b507f516a144f754797aa4263a2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packages"))

    @packages.setter
    def packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9620379941a9eebaab0fc33d69d3ee7abe9f5d6f73cbc2576d3dcf62ac85d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnBehavior")
    def return_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnBehavior"))

    @return_behavior.setter
    def return_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1561be22c225a688cdcdbe3b019aa402ffb08713653751b24c2277b34603582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b169431d6712e84c14c3dece7627e57ab15f5f52a1354f7365ad0b06196ca2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300fc5075eef395de86ccff2a0195533801df41873537d46edb9d7ddd9915660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995f819c09f7713106e5afb8e8abe22bce97c9685cdb25f35d3c02bbcc92af7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secure")
    def secure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secure"))

    @secure.setter
    def secure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2df0b6afe51d4cc5327e9f4c445787becdec0f2fc2c7376acff8bdcf176a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5152cc7a0814ff4df3efa32864f419e00110656f996e4ffb1e7b935d000feef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedure.ProcedureArguments",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class ProcedureArguments:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: The argument name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#name Procedure#name}
        :param type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#type Procedure#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652550d16952704b961c487e4484ac2ba5ffe2277b5b2e737b05f8971821d762)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The argument name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#name Procedure#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The argument type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#type Procedure#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedure.ProcedureArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7588a066eb906c3168c9f6951ca33ae4f06306b65d850859bf862dc7c05ef20c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238c0572f99d78b066a3d30f6b7b615c3f13761a7fb157e3fd82fa4f5423b8f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec38f51c14e787f8ed92d5b801dde415a99634e1227b15dfba01e8f82459fe7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0b0d6e919220158257cb74687c48288fcdd148f48d4d33ca54e520a3807ff76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29f3dc3ce373f2add7d53f0fcea0f5c5baac048cee2f582231dc2c55169c611f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4116476a1f4df9dabe3913a0fc55dcc21f986e44b10e5da8e91a07423c7be65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedure.ProcedureArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef653b5c94d1b2d33b33e781e62b013e8a877e36f6cb5501688de170da22965)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044096e126ad1f280b8c8cab339f151ce1edcc678500948178065d7af682b1bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e751c6a16cae29d125534a1bbb46a4e8270a5256e6e2113a425c9cb6f3c72b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fd44ecdbfdbd9317d70e9c21f545dfc1e3c766a46d9b9b791a3196d4c66a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedure.ProcedureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "name": "name",
        "return_type": "returnType",
        "schema": "schema",
        "statement": "statement",
        "arguments": "arguments",
        "comment": "comment",
        "execute_as": "executeAs",
        "handler": "handler",
        "id": "id",
        "imports": "imports",
        "language": "language",
        "null_input_behavior": "nullInputBehavior",
        "packages": "packages",
        "return_behavior": "returnBehavior",
        "runtime_version": "runtimeVersion",
        "secure": "secure",
    },
)
class ProcedureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        statement: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        execute_as: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_behavior: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the procedure. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#database Procedure#database}
        :param name: Specifies the identifier for the procedure; does not have to be unique for the schema in which the procedure is created. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#name Procedure#name}
        :param return_type: The return type of the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_type Procedure#return_type}
        :param schema: The schema in which to create the procedure. Don't use the | character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#schema Procedure#schema}
        :param statement: Specifies the code used to create the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#statement Procedure#statement}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#arguments Procedure#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#comment Procedure#comment}
        :param execute_as: Sets execution context. Allowed values are CALLER and OWNER (consult a proper section in the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-procedure#id1>`_). For more information see `caller's rights and owner's rights <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#execute_as Procedure#execute_as}
        :param handler: The handler method for Java / Python procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#handler Procedure#handler}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#id Procedure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: Imports for Java / Python procedures. For Java this a list of jar files, for Python this is a list of Python files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#imports Procedure#imports}
        :param language: Specifies the language of the stored procedure code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#language Procedure#language}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#null_input_behavior Procedure#null_input_behavior}
        :param packages: List of package imports to use for Java / Python procedures. For Java, package imports should be of the form: package_name:version_number, where package_name is snowflake_domain:package. For Python use it should be: ('numpy','pandas','xgboost==1.5.0'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#packages Procedure#packages}
        :param return_behavior: Specifies the behavior of the function when returning results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_behavior Procedure#return_behavior}
        :param runtime_version: Required for Python procedures. Specifies Python runtime version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#runtime_version Procedure#runtime_version}
        :param secure: Specifies that the procedure is secure. For more information about secure procedures, see Protecting Sensitive Information with Secure UDFs and Stored Procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#secure Procedure#secure}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0181f7795a616ef15a26e405e01f7be9c86c4e0cbaa07a313ef4938c818f2b0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument execute_as", value=execute_as, expected_type=type_hints["execute_as"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument imports", value=imports, expected_type=type_hints["imports"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument null_input_behavior", value=null_input_behavior, expected_type=type_hints["null_input_behavior"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument return_behavior", value=return_behavior, expected_type=type_hints["return_behavior"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument secure", value=secure, expected_type=type_hints["secure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "return_type": return_type,
            "schema": schema,
            "statement": statement,
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
        if arguments is not None:
            self._values["arguments"] = arguments
        if comment is not None:
            self._values["comment"] = comment
        if execute_as is not None:
            self._values["execute_as"] = execute_as
        if handler is not None:
            self._values["handler"] = handler
        if id is not None:
            self._values["id"] = id
        if imports is not None:
            self._values["imports"] = imports
        if language is not None:
            self._values["language"] = language
        if null_input_behavior is not None:
            self._values["null_input_behavior"] = null_input_behavior
        if packages is not None:
            self._values["packages"] = packages
        if return_behavior is not None:
            self._values["return_behavior"] = return_behavior
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if secure is not None:
            self._values["secure"] = secure

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
    def database(self) -> builtins.str:
        '''The database in which to create the procedure. Don't use the | character.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#database Procedure#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the procedure;

        does not have to be unique for the schema in which the procedure is created. Don't use the | character.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#name Procedure#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''The return type of the procedure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_type Procedure#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the procedure. Don't use the | character.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#schema Procedure#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement(self) -> builtins.str:
        '''Specifies the code used to create the procedure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#statement Procedure#statement}
        '''
        result = self._values.get("statement")
        assert result is not None, "Required property 'statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#arguments Procedure#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the procedure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#comment Procedure#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_as(self) -> typing.Optional[builtins.str]:
        '''Sets execution context.

        Allowed values are CALLER and OWNER (consult a proper section in the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-procedure#id1>`_). For more information see `caller's rights and owner's rights <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#execute_as Procedure#execute_as}
        '''
        result = self._values.get("execute_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''The handler method for Java / Python procedures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#handler Procedure#handler}
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#id Procedure#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Imports for Java / Python procedures.

        For Java this a list of jar files, for Python this is a list of Python files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#imports Procedure#imports}
        '''
        result = self._values.get("imports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''Specifies the language of the stored procedure code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#language Procedure#language}
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the procedure when called with null inputs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#null_input_behavior Procedure#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of package imports to use for Java / Python procedures.

        For Java, package imports should be of the form: package_name:version_number, where package_name is snowflake_domain:package. For Python use it should be: ('numpy','pandas','xgboost==1.5.0').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#packages Procedure#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def return_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when returning results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#return_behavior Procedure#return_behavior}
        '''
        result = self._values.get("return_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''Required for Python procedures. Specifies Python runtime version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#runtime_version Procedure#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the procedure is secure.

        For more information about secure procedures, see Protecting Sensitive Information with Secure UDFs and Stored Procedures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/0.100.0/docs/resources/procedure#secure Procedure#secure}
        '''
        result = self._values.get("secure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Procedure",
    "ProcedureArguments",
    "ProcedureArgumentsList",
    "ProcedureArgumentsOutputReference",
    "ProcedureConfig",
]

publication.publish()

def _typecheckingstub__9e9987cca8b445cddeff76d27d8c792f688bc8e92ee1b896b860b0fa51f14ff8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    statement: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    execute_as: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_behavior: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__1e16813566d0354f979c60c7621afd1aed1d0133ce0f9ff29a2e3806648d0b9a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f551de5ce61230c81d600f7b801e3cb7c86ddaf813bae8f9b1cecae77d8a8085(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a5042d617b7357761bb18447e8499a71762761de20f1fb9eaddfa7f2e9890a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c816f95eb66fac7e742e16ae8159a7db152369ce4eccaf9e21f3158b5cb4f1c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39fd112214bec71e2afbab1a320c9fc7ec84117d2f3c73943fe0144f71ed82b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48a2bbca602431b6df7f85c15ab6663a64a15c2274e22ce5c672dbcdab3b761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e5b3b13cf1311a9ee172d65d7990fe3cad2403570ced58ac4572763812de57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909c1e0dd9f00fbc61a8602e290adbde6681ddad4cb17d3eec6e85fa6f687881(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a28cdf4745a8f54328ee961adb59a2dbdda670815070d2ed11fd5548b69cd8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b197f6ae29938aba6b168c0b1154d201d1d06e65a81ff5951793e40f07396d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112c0e194907e062fe70531d6837af853d7b507f516a144f754797aa4263a2c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9620379941a9eebaab0fc33d69d3ee7abe9f5d6f73cbc2576d3dcf62ac85d5b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1561be22c225a688cdcdbe3b019aa402ffb08713653751b24c2277b34603582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b169431d6712e84c14c3dece7627e57ab15f5f52a1354f7365ad0b06196ca2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300fc5075eef395de86ccff2a0195533801df41873537d46edb9d7ddd9915660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995f819c09f7713106e5afb8e8abe22bce97c9685cdb25f35d3c02bbcc92af7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2df0b6afe51d4cc5327e9f4c445787becdec0f2fc2c7376acff8bdcf176a5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5152cc7a0814ff4df3efa32864f419e00110656f996e4ffb1e7b935d000feef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652550d16952704b961c487e4484ac2ba5ffe2277b5b2e737b05f8971821d762(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7588a066eb906c3168c9f6951ca33ae4f06306b65d850859bf862dc7c05ef20c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238c0572f99d78b066a3d30f6b7b615c3f13761a7fb157e3fd82fa4f5423b8f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec38f51c14e787f8ed92d5b801dde415a99634e1227b15dfba01e8f82459fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b0d6e919220158257cb74687c48288fcdd148f48d4d33ca54e520a3807ff76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f3dc3ce373f2add7d53f0fcea0f5c5baac048cee2f582231dc2c55169c611f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4116476a1f4df9dabe3913a0fc55dcc21f986e44b10e5da8e91a07423c7be65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef653b5c94d1b2d33b33e781e62b013e8a877e36f6cb5501688de170da22965(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044096e126ad1f280b8c8cab339f151ce1edcc678500948178065d7af682b1bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e751c6a16cae29d125534a1bbb46a4e8270a5256e6e2113a425c9cb6f3c72b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fd44ecdbfdbd9317d70e9c21f545dfc1e3c766a46d9b9b791a3196d4c66a56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0181f7795a616ef15a26e405e01f7be9c86c4e0cbaa07a313ef4938c818f2b0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    statement: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    execute_as: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_behavior: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
