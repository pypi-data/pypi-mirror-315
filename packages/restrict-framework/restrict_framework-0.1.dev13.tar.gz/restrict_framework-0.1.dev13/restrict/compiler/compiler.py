from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Literal, Type

from .parsers.ast import FileGraph
from ..types.base import TRUE, _Boolean, DataType, Empty


class JsonProvider(ABC):
    @abstractmethod
    def json(self) -> Any:  # pragma: nocover
        pass


class JsonException(Exception, JsonProvider):
    pass


class JsonWarning(Warning, JsonProvider):
    pass


class MissingPrefixError(Exception):
    def __init__(self, entry, resource):
        super().__init__(entry, resource)


class ValidationError(JsonException):
    def __init__(self, field_name: str, message: str):
        super().__init__(field_name, message)

    @property
    def field_name(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]

    def rescope(self, prefix: str):
        return ValidationError(f"{prefix}.{self.field_name}", self.message)

    def json(self):
        return {
            "pointer": f"/{self.field_name}",
            "title": "validation error",
            "detail": self.message,
        }

    def __eq__(self, other):
        return other.__class__ is ValidationError and other.args == self.args


class ResourceExceptionGroup(Exception):
    def __init__(
        self,
        exceptions: Sequence[JsonException],
        warnings: Sequence[JsonWarning],
    ):
        super().__init__(exceptions, warnings)

    @property
    def exceptions(self):
        return self.args[0]

    @property
    def warnings(self):
        return self.args[1]

    def json(self):
        return {
            "errors": [e.json() for e in self.exceptions],
            "warnings": [e.json() for e in self.warnings],
        }


class MissingFieldError(JsonException):
    def __init__(self, field_name: str, resource_name: str):
        super().__init__(field_name, resource_name)

    @property
    def field_name(self) -> str:
        return self.args[0]

    @property
    def resource_name(self) -> str:
        return self.args[1]

    def json(self):
        return {
            "pointer": f"/{self.field_name}",
            "title": "missing field",
            "detail": f"{self.field_name} is a required field for {self.resource_name}",
        }

    def __eq__(self, other):
        return other.__class__ is MissingFieldError and other.args == self.args


@dataclass
class WritableDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_optional: bool
    is_hidden: bool
    validator: Callable[[ResourceInstance], _Boolean]
    create_effect: Callable[[dict], DataType] | None = None
    create_rule: Callable[[dict], _Boolean] | None = None

    @property
    def is_required(self):
        return self.is_required_input

    @property
    def is_required_input(self):
        return not self.is_optional

    def to_schema(self) -> dict:
        return self.type.default().schema_type | {
            "readOnly": False,
        }

    def to_instance_field(self, inst: ResourceInstance) -> WritableDataField:
        return WritableDataField(inst, self)


@dataclass
class ReadonlyDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_optional: bool
    is_hidden: bool
    validator: Callable[[ResourceInstance], _Boolean]
    create_effect: Callable[[dict], DataType] | None = None

    @property
    def is_required(self):
        return not self.is_optional

    @property
    def is_required_input(self):
        return False

    def to_schema(self) -> dict:
        return self.type.default().schema_type | {
            "readOnly": True,
        }

    def to_instance_field(self, inst: ResourceInstance) -> ReadonlyDataField:
        return ReadonlyDataField(inst, self)


@dataclass
class ComputedDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_hidden: bool
    computation: Callable[[ResourceInstance], DataType]

    @property
    def is_required(self):
        return True

    @property
    def is_required_input(self):
        return False

    def to_schema(self) -> dict:
        return self.type.default().schema_type | {
            "readOnly": True,
        }

    def to_instance_field(self, inst: ResourceInstance) -> ComputedDataField:
        return ComputedDataField(inst, self)


@dataclass
class DncFieldDef:
    owner: ResourceDefinition
    name: str
    multiplicity: int | Literal["*"]
    type: ResourceDefinition
    is_optional: bool
    is_hidden: bool
    create_effect: Callable[[dict], ResourceInstance] | None = None
    create_rule: Callable[[dict], _Boolean] | None = None

    @property
    def is_required(self):
        return self.is_required_input

    @property
    def is_required_input(self):
        return not self.is_optional

    def to_schema(self) -> dict:
        return self.type.to_schema() | {
            "readOnly": False,
        }

    def to_instance_field(self, res: ResourceInstance) -> DncField:
        return DncField(res, self)


class ResourceDefinition:
    fields: dict[
        str,
        WritableDataFieldDef
        | ReadonlyDataFieldDef
        | ComputedDataFieldDef
        | DncFieldDef,
    ]

    def __init__(self, name: str):
        self.name = name
        self.fields = {}

    def add_writable_data_field(
        self,
        name: str,
        type: type[DataType],
        is_optional: bool,
        is_hidden: bool,
        validator: Callable[[ResourceInstance], _Boolean],
    ):
        field = WritableDataFieldDef(
            self, name, type, is_optional, is_hidden, validator
        )
        self._add_field(field)

    def add_readonly_data_field(
        self,
        name: str,
        type: Type[DataType],
        is_optional: bool,
        is_hidden: bool,
        validator: Callable[[ResourceInstance], _Boolean],
    ):
        field = ReadonlyDataFieldDef(
            self, name, type, is_optional, is_hidden, validator
        )
        self._add_field(field)

    def add_computed_data_field(
        self,
        name: str,
        type: Type[DataType],
        is_hidden: bool,
        computation: Callable[[ResourceInstance], DataType],
    ):
        field = ComputedDataFieldDef(self, name, type, is_hidden, computation)
        self._add_field(field)

    def add_dnc_field(
        self,
        name: str,
        multiplicity: int | Literal["*"],
        type: ResourceDefinition,
        is_optional: bool,
        is_hidden: bool,
    ):
        field = DncFieldDef(
            self,
            name,
            multiplicity,
            type,
            is_optional,
            is_hidden,
        )
        self._add_field(field)

    def add_create_effect(self, field_name: str, effect: Callable[[dict], Any]):
        field = self.fields[field_name]
        if not isinstance(field, ComputedDataFieldDef):
            field.create_effect = effect

    def add_create_rule(
        self, field_name: str, rule: Callable[[dict], _Boolean]
    ):
        field = self.fields[field_name]
        if not isinstance(field, ComputedDataFieldDef) and not isinstance(
            field, ReadonlyDataFieldDef
        ):
            field.create_rule = rule

    def instantiate(self) -> ResourceInstance:
        return ResourceInstance(self)

    def to_schema(self) -> dict:
        schema = {"type": "object", "properties": {}, "required": []}
        defs = {}

        for name, field in self.fields.items():
            if field.is_hidden:
                continue
            if not isinstance(field, DncFieldDef):
                schema["properties"][name] = field.to_schema()
            else:
                schema["properties"][name] = {
                    "$ref": f"#/$defs/{field.type.name}",
                    "readOnly": False,
                }
                field_schema = field.type.to_schema()
                for field_name, field_def in field_schema["$defs"].items():
                    defs[field_name] = field_def
            if field.is_required_input:
                schema["required"].append(name)
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": f"#/$defs/{self.name}",
            "$defs": defs | {self.name: schema},
        }

    @staticmethod
    def default() -> ResourceInstance:
        return ResourceInstance(ResourceDefinition("EMPTY"))

    def _add_field(
        self,
        field: (
            WritableDataFieldDef
            | ReadonlyDataFieldDef
            | ComputedDataFieldDef
            | DncFieldDef
        ),
    ):
        if field.name in self.fields:
            raise KeyError(field.name, field)
        self.fields[field.name] = field


class WritableDataField:
    def __init__(self, res: ResourceInstance, field: WritableDataFieldDef):
        self.field = field
        self.resource = res

    @property
    def name(self):
        return self.field.name

    @property
    def is_required(self):
        return self.field.is_required

    @property
    def is_hidden(self):
        return self.field.is_hidden

    def initialize(self, lookup: dict):
        if self._create_allowed(lookup) and self.name in lookup:
            self.value = self.field.type(lookup[self.name])
        elif self.field.create_effect is not None:
            self.value = self.field.create_effect(lookup)

    def validate(self):
        self.field.validator(self.resource)

    def to_json(self):
        return self.value.json()

    def _create_allowed(self, lookup: dict):
        return (
            self.field.create_rule is None
            or self.field.create_rule(lookup) == TRUE
        )


class ReadonlyDataField:
    def __init__(self, res: ResourceInstance, field: ReadonlyDataFieldDef):
        self.field = field
        self.resource = res

    @property
    def name(self):
        return self.field.name

    @property
    def is_required(self):
        return self.field.is_required

    @property
    def is_hidden(self):
        return self.field.is_hidden

    def initialize(self, lookup: dict):
        if self.field.create_effect is None:
            raise RuntimeError(
                f"Expected create effect for {self.resource.name}#{self.name}"
            )
        self.value = self.field.create_effect(lookup)

    def validate(self):
        self.field.validator(self.resource)

    def to_json(self):
        return self.value.json()


class ComputedDataField:
    def __init__(self, res: ResourceInstance, field: ComputedDataFieldDef):
        self.field = field
        self.resource = res

    @property
    def name(self):
        return self.field.name

    @property
    def is_required(self):
        return self.field.is_required

    @property
    def is_hidden(self):
        return self.field.is_hidden

    def initialize(self, lookup: dict):
        pass

    def validate(self):
        pass

    def to_json(self):
        return self.field.computation(self.resource).json()


class DncField:
    def __init__(self, res: ResourceInstance, field: DncFieldDef):
        self.field = field
        self.resource = res

    @property
    def name(self):
        return self.field.name

    @property
    def is_required(self):
        return self.field.is_required

    @property
    def is_hidden(self):
        return self.field.is_hidden

    def initialize(self, lookup: dict):
        if self._create_allowed(lookup) and self.name in lookup:
            self.value = self.field.type.instantiate()
            try:
                self.value.initialize(lookup[self.name])
            except ResourceExceptionGroup as reg:
                self.errors = reg
        elif self.field.create_effect is not None:
            self.value = self.field.create_effect(lookup)
        else:
            value = self.field.type.instantiate()
            try:
                value.initialize({})
                self.value = value
            except ResourceExceptionGroup as reg:
                self.errors = reg

    def validate(self):
        if hasattr(self, "errors"):
            raise self.errors

    def to_json(self):
        if hasattr(self, "value") and isinstance(self.value, ResourceInstance):
            return self.value.to_json()

    def _create_allowed(self, lookup: dict):
        return (
            self.field.create_rule is None
            or self.field.create_rule(lookup) == TRUE
        )


class ResourceInstance:
    def __init__(self, resource_def: ResourceDefinition):
        self.resource_def = resource_def
        self.fields = {
            f.name: f.to_instance_field(self)
            for f in resource_def.fields.values()
        }

    @property
    def name(self):
        return self.resource_def.name

    def initialize(self, data: dict):
        for field in self.fields.values():
            field.initialize(data)
        missing_fields_errors = [
            MissingFieldError(field.name, self.resource_def.name)
            for field in self.fields.values()
            if not isinstance(field, ComputedDataField)
            and field.is_required
            and not hasattr(field, "value")
        ]
        if len(missing_fields_errors) > 0:
            raise ResourceExceptionGroup(missing_fields_errors, [])
        validation_errors = []
        for field in self.fields.values():
            try:
                field.validate()
            except ValidationError as ve:
                validation_errors.append(ve)
            except ResourceExceptionGroup as reg:
                for ex in reg.exceptions:
                    ex = ex.rescope(field.name)
                    validation_errors.append(ex)
        if len(validation_errors) > 0:
            raise ResourceExceptionGroup(validation_errors, [])

    def to_json(self):
        return {
            k: f.to_json() for k, f in self.fields.items() if not f.is_hidden
        }


class RestrictCompiler:
    def __init__(self, graph: FileGraph):
        self.graph = graph

    def compile(self) -> tuple[Sequence[ResourceDefinition]]:
        root = self.graph.root

        runnable_resources = []
        # for resource in root.resources:
        #     fields = []
        #     for entry in resource.data:
        #         if entry.resolved_prefix is None:
        #             raise MissingPrefixError(entry, resource)
        #         file = self.graph.files.get(entry.resolved_prefix)
        #         if file is None:
        #             raise MissingPrefixError(entry, resource)
        #         entry_type = file.get_data_type(entry.type)
        #         if entry_type is None:
        #             raise MissingTypeError(
        #                 entry.type,
        #                 entry.name,
        #                 entry.prefix,
        #                 entry.resolved_prefix,
        #                 root.path,
        #             )
        #         field = RunnableResourceField(
        #             entry.name, entry_type, lambda x: (TRUE, [])
        #         )
        #         fields.append(field)
        #     cls = type(resource.name, (RunnableResource,), {})
        #     runnable_resources.append(cls(fields))

        return (runnable_resources,)
