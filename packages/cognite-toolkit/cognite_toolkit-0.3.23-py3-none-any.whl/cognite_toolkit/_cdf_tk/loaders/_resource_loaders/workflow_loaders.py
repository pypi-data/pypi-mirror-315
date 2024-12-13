# Copyright 2023 Cognite AS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import json
from collections.abc import Hashable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any, final

from cognite.client.data_classes import (
    ClientCredentials,
    Workflow,
    WorkflowList,
    WorkflowTrigger,
    WorkflowTriggerList,
    WorkflowTriggerUpsert,
    WorkflowTriggerUpsertList,
    WorkflowUpsert,
    WorkflowUpsertList,
    WorkflowVersion,
    WorkflowVersionId,
    WorkflowVersionList,
    WorkflowVersionUpsert,
    WorkflowVersionUpsertList,
)
from cognite.client.data_classes.capabilities import (
    Capability,
    WorkflowOrchestrationAcl,
)
from cognite.client.exceptions import CogniteNotFoundError
from cognite.client.utils.useful_types import SequenceNotStr
from rich import print

from cognite_toolkit._cdf_tk._parameters import ANY_INT, ANY_STR, ParameterSpec, ParameterSpecSet
from cognite_toolkit._cdf_tk.client import ToolkitClient
from cognite_toolkit._cdf_tk.exceptions import (
    ToolkitRequiredValueError,
)
from cognite_toolkit._cdf_tk.loaders._base_loaders import ResourceLoader
from cognite_toolkit._cdf_tk.tk_warnings import LowSeverityWarning
from cognite_toolkit._cdf_tk.utils import (
    CDFToolConfig,
)

from .auth_loaders import GroupAllScopedLoader
from .data_organization_loaders import DataSetsLoader
from .function_loaders import FunctionLoader
from .transformation_loaders import TransformationLoader


@final
class WorkflowLoader(ResourceLoader[str, WorkflowUpsert, Workflow, WorkflowUpsertList, WorkflowList]):
    folder_name = "workflows"
    filename_pattern = r"^.*Workflow$"
    resource_cls = Workflow
    resource_write_cls = WorkflowUpsert
    list_cls = WorkflowList
    list_write_cls = WorkflowUpsertList
    kind = "Workflow"
    dependencies = frozenset(
        {
            GroupAllScopedLoader,
            TransformationLoader,
            FunctionLoader,
            DataSetsLoader,
        }
    )
    _doc_base_url = "https://api-docs.cognite.com/20230101-beta/tag/"
    _doc_url = "Workflows/operation/CreateOrUpdateWorkflow"

    @property
    def display_name(self) -> str:
        return "workflows"

    @classmethod
    def get_required_capability(
        cls, items: WorkflowUpsertList | None, read_only: bool
    ) -> Capability | list[Capability]:
        if not items and items is not None:
            return []

        actions = (
            [WorkflowOrchestrationAcl.Action.Read]
            if read_only
            else [WorkflowOrchestrationAcl.Action.Read, WorkflowOrchestrationAcl.Action.Write]
        )

        return WorkflowOrchestrationAcl(
            actions,
            WorkflowOrchestrationAcl.Scope.All(),
        )

    @classmethod
    def get_id(cls, item: Workflow | WorkflowUpsert | dict) -> str:
        if isinstance(item, dict):
            return item["externalId"]
        if item.external_id is None:
            raise ToolkitRequiredValueError("Workflow must have external_id set.")
        return item.external_id

    @classmethod
    def dump_id(cls, id: str) -> dict[str, Any]:
        return {"externalId": id}

    def load_resource(
        self,
        resource: dict[str, Any] | list[dict[str, Any]],
        ToolGlobals: CDFToolConfig,
        skip_validation: bool,
        filepath: Path | None = None,
    ) -> WorkflowUpsertList:
        workflows: list[dict[str, Any]] = [resource] if isinstance(resource, dict) else resource
        for workflow in workflows:
            if "dataSetExternalId" in workflow:
                ds_external_id = workflow.pop("dataSetExternalId")
                workflow["dataSetId"] = ToolGlobals.verify_dataset(
                    ds_external_id, skip_validation, action="replace dataSetExternalId with dataSetId in workflow"
                )

        return WorkflowUpsertList.load(workflows)

    def retrieve(self, ids: SequenceNotStr[str]) -> WorkflowList:
        workflows = []
        for ext_id in ids:
            workflow = self.client.workflows.retrieve(external_id=ext_id)
            if workflow:
                workflows.append(workflow)
        return WorkflowList(workflows)

    def _upsert(self, items: WorkflowUpsert | WorkflowUpsertList) -> WorkflowList:
        upserts = [items] if isinstance(items, WorkflowUpsert) else items
        return WorkflowList([self.client.workflows.upsert(upsert) for upsert in upserts])

    def create(self, items: WorkflowUpsert | WorkflowUpsertList) -> WorkflowList:
        return self._upsert(items)

    def update(self, items: WorkflowUpsertList) -> WorkflowList:
        return self._upsert(items)

    def delete(self, ids: SequenceNotStr[str]) -> int:
        successes = 0
        for id_ in ids:
            try:
                self.client.workflows.delete(external_id=id_)
            except CogniteNotFoundError:
                print(f"  [bold yellow]WARNING:[/] Workflow {id_} does not exist, skipping delete.")
            else:
                successes += 1
        return successes

    def _iterate(
        self,
        data_set_external_id: str | None = None,
        space: str | None = None,
        parent_ids: list[Hashable] | None = None,
    ) -> Iterable[Workflow]:
        if data_set_external_id is None:
            yield from self.client.workflows.list(limit=-1)
            return
        data_set = self.client.data_sets.retrieve(external_id=data_set_external_id)
        if data_set is None:
            raise ToolkitRequiredValueError(f"DataSet {data_set_external_id!r} does not exist")
        for workflow in self.client.workflows.list(limit=-1):
            if workflow.data_set_id == data_set.id:
                yield workflow

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        spec.add(
            ParameterSpec(
                ("dataSetExternalId",),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=True,
            )
        )
        spec.discard(
            ParameterSpec(
                ("dataSetId",),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=True,
            )
        )
        return spec

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        """Returns all items that this item requires.

        For example, a TimeSeries requires a DataSet, so this method would return the
        DatasetLoader and identifier of that dataset.
        """
        if "dataSetExternalId" in item:
            yield DataSetsLoader, item["dataSetExternalId"]

    def _are_equal(
        self, local: WorkflowUpsert, cdf_resource: Workflow, return_dumped: bool = False
    ) -> bool | tuple[bool, dict[str, Any], dict[str, Any]]:
        local_dumped = local.dump()
        cdf_dumped = cdf_resource.as_write().dump()
        # Dry run
        if local_dumped.get("dataSetId") == -1 and "dataSetId" in cdf_dumped:
            local_dumped["dataSetId"] = cdf_dumped["dataSetId"]

        return self._return_are_equal(local_dumped, cdf_dumped, return_dumped)


@final
class WorkflowVersionLoader(
    ResourceLoader[
        WorkflowVersionId, WorkflowVersionUpsert, WorkflowVersion, WorkflowVersionUpsertList, WorkflowVersionList
    ]
):
    folder_name = "workflows"
    filename_pattern = r"^.*WorkflowVersion$"
    resource_cls = WorkflowVersion
    resource_write_cls = WorkflowVersionUpsert
    list_cls = WorkflowVersionList
    list_write_cls = WorkflowVersionUpsertList
    kind = "WorkflowVersion"
    dependencies = frozenset({WorkflowLoader})
    parent_resource = frozenset({WorkflowLoader})

    _doc_base_url = "https://api-docs.cognite.com/20230101-beta/tag/"
    _doc_url = "Workflow-versions/operation/CreateOrUpdateWorkflowVersion"

    @property
    def display_name(self) -> str:
        return "workflow versions"

    @classmethod
    def get_required_capability(
        cls, items: WorkflowVersionUpsertList | None, read_only: bool
    ) -> Capability | list[Capability]:
        if not items and items is not None:
            return []

        actions = (
            [WorkflowOrchestrationAcl.Action.Read]
            if read_only
            else [WorkflowOrchestrationAcl.Action.Read, WorkflowOrchestrationAcl.Action.Write]
        )

        return WorkflowOrchestrationAcl(
            actions,
            WorkflowOrchestrationAcl.Scope.All(),
        )

    @classmethod
    def get_id(cls, item: WorkflowVersion | WorkflowVersionUpsert | dict) -> WorkflowVersionId:
        if isinstance(item, dict):
            if missing := tuple(k for k in {"workflowExternalId", "version"} if k not in item):
                # We need to raise a KeyError with all missing keys to get the correct error message.
                raise KeyError(*missing)
            return WorkflowVersionId(item["workflowExternalId"], item["version"])
        return item.as_id()

    @classmethod
    def dump_id(cls, id: WorkflowVersionId) -> dict[str, Any]:
        return id.dump()

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        if "workflowExternalId" in item:
            yield WorkflowLoader, item["workflowExternalId"]

    def retrieve(self, ids: SequenceNotStr[WorkflowVersionId]) -> WorkflowVersionList:
        return self.client.workflows.versions.list(list(ids))

    def _upsert(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        return WorkflowVersionList([self.client.workflows.versions.upsert(item) for item in items])

    def create(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        upserted = []
        for item in items:
            upserted.append(self.client.workflows.versions.upsert(item))
        return WorkflowVersionList(upserted)

    def update(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        updated = []
        for item in items:
            updated.append(self.client.workflows.versions.upsert(item))
        return WorkflowVersionList(updated)

    def delete(self, ids: SequenceNotStr[WorkflowVersionId]) -> int:
        successes = 0
        for id in ids:
            try:
                self.client.workflows.versions.delete(id)
            except CogniteNotFoundError:
                print(f"  [bold yellow]WARNING:[/] WorkflowVersion {id} does not exist, skipping delete.")
            else:
                successes += 1
        return successes

    def _iterate(
        self,
        data_set_external_id: str | None = None,
        space: str | None = None,
        parent_ids: list[Hashable] | None = None,
    ) -> Iterable[WorkflowVersion]:
        workflow_ids = [parent_id for parent_id in parent_ids if isinstance(parent_id, str)] if parent_ids else None
        return self.client.workflows.versions.list(limit=-1, workflow_version_ids=workflow_ids)  # type: ignore[arg-type]

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        # The Parameter class in the SDK class WorkflowVersion implementation is deviating from the API.
        # So we need to modify the spec to match the API.
        parameter_path = ("workflowDefinition", "tasks", ANY_INT, "parameters")
        length = len(parameter_path)
        for item in spec:
            if len(item.path) >= length + 1 and item.path[:length] == parameter_path[:length]:
                # Add extra ANY_STR layer
                # The spec class is immutable, so we use this trick to modify it.
                object.__setattr__(item, "path", item.path[:length] + (ANY_STR,) + item.path[length:])
        spec.add(ParameterSpec((*parameter_path, ANY_STR), frozenset({"dict"}), is_required=True, _is_nullable=False))
        # The depends on is implemented as a list of string in the SDK, but in the API spec it
        # is a list of objects with one 'externalId' field.
        spec.add(
            ParameterSpec(
                ("workflowDefinition", "tasks", ANY_INT, "dependsOn", ANY_INT, "externalId"),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=False,
            )
        )
        spec.add(
            ParameterSpec(
                ("workflowDefinition", "tasks", ANY_INT, "type"),
                frozenset({"str"}),
                is_required=True,
                _is_nullable=False,
            )
        )
        return spec


@final
class WorkflowTriggerLoader(
    ResourceLoader[str, WorkflowTriggerUpsert, WorkflowTrigger, WorkflowTriggerUpsertList, WorkflowTriggerList]
):
    folder_name = "workflows"
    filename_pattern = r"^.*WorkflowTrigger$"
    resource_cls = WorkflowTrigger
    resource_write_cls = WorkflowTriggerUpsert
    list_cls = WorkflowTriggerList
    list_write_cls = WorkflowTriggerUpsertList
    kind = "WorkflowTrigger"
    dependencies = frozenset({WorkflowLoader, WorkflowVersionLoader})
    parent_resource = frozenset({WorkflowLoader})

    _doc_url = "Workflow-triggers/operation/CreateOrUpdateTriggers"
    do_environment_variable_injection = True

    def __init__(self, client: ToolkitClient, build_dir: Path | None):
        super().__init__(client, build_dir)
        self._authentication_by_id: dict[str, ClientCredentials] = {}

    @property
    def display_name(self) -> str:
        return "workflow triggers"

    @classmethod
    def get_id(cls, item: WorkflowTriggerUpsert | WorkflowTrigger | dict) -> str:
        if isinstance(item, dict):
            return item["externalId"]
        return item.external_id

    @classmethod
    def dump_id(cls, id: str) -> dict[str, Any]:
        return {"externalId": id}

    @classmethod
    def get_required_capability(
        cls, items: WorkflowTriggerUpsertList | None, read_only: bool
    ) -> Capability | list[Capability]:
        if not items and items is not None:
            return []

        capability = (
            [WorkflowOrchestrationAcl.Action.Read]
            if read_only
            else [WorkflowOrchestrationAcl.Action.Read, WorkflowOrchestrationAcl.Action.Write]
        )

        return WorkflowOrchestrationAcl(
            capability,
            WorkflowOrchestrationAcl.Scope.All(),
        )

    def create(self, items: WorkflowTriggerUpsertList) -> WorkflowTriggerList:
        created = WorkflowTriggerList([])
        for item in items:
            credentials = self._authentication_by_id.get(item.external_id)
            created.append(self.client.workflows.triggers.upsert(item, credentials))
        return created

    def retrieve(self, ids: SequenceNotStr[str]) -> WorkflowTriggerList:
        all_triggers = self.client.workflows.triggers.list(limit=-1)
        lookup = set(ids)
        return WorkflowTriggerList([trigger for trigger in all_triggers if trigger.external_id in lookup])

    def update(self, items: WorkflowTriggerUpsertList) -> WorkflowTriggerList:
        exising = self.client.workflows.triggers.list(limit=-1)
        existing_lookup = {trigger.external_id: trigger for trigger in exising}
        updated = WorkflowTriggerList([])
        for item in items:
            if item.external_id in existing_lookup:
                self.client.workflows.triggers.delete(external_id=item.external_id)

            credentials = self._authentication_by_id.get(item.external_id)
            created = self.client.workflows.triggers.create(item, client_credentials=credentials)
            updated.append(created)
        return updated

    def delete(self, ids: SequenceNotStr[str]) -> int:
        successes = 0
        for id in ids:
            try:
                self.client.workflows.triggers.delete(external_id=id)
            except CogniteNotFoundError:
                LowSeverityWarning(f"WorkflowTrigger {id} does not exist, skipping delete.").print_warning()
            else:
                successes += 1
        return successes

    def _iterate(
        self,
        data_set_external_id: str | None = None,
        space: str | None = None,
        parent_ids: list[Hashable] | None = None,
    ) -> Iterable[WorkflowTrigger]:
        triggers = self.client.workflows.triggers.list(limit=-1)
        if parent_ids is not None:
            # Parent = Workflow
            workflow_ids = {parent_id for parent_id in parent_ids if isinstance(parent_id, str)}
            return (trigger for trigger in triggers if trigger.workflow_external_id in workflow_ids)
        return triggers

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        # Removed by the SDK
        spec.add(
            ParameterSpec(
                ("triggerRule", "triggerType"),
                frozenset({"str"}),
                is_required=True,
                _is_nullable=False,
            )
        )
        spec.add(
            ParameterSpec(
                ("authentication",),
                frozenset({"dict"}),
                is_required=True,
                _is_nullable=False,
            )
        )
        spec.add(
            ParameterSpec(
                ("authentication", "clientId"),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=False,
            )
        )
        spec.add(
            ParameterSpec(
                ("authentication", "clientSecret"),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=False,
            )
        )
        return spec

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        """Returns all items that this item requires."""
        if "workflowExternalId" in item:
            yield WorkflowLoader, item["workflowExternalId"]

            if "workflowVersion" in item:
                yield WorkflowVersionLoader, WorkflowVersionId(item["workflowExternalId"], item["workflowVersion"])

    def load_resource(
        self,
        resource: dict[str, Any] | list[dict[str, Any]],
        ToolGlobals: CDFToolConfig,
        skip_validation: bool,
        filepath: Path | None = None,
    ) -> WorkflowTriggerUpsertList:
        raw_list = resource if isinstance(resource, list) else [resource]
        loaded = WorkflowTriggerUpsertList([])
        for item in raw_list:
            if "data" in item and isinstance(item["data"], dict):
                item["data"] = json.dumps(item["data"])
            if "authentication" in item:
                raw_auth = item.pop("authentication")
                self._authentication_by_id[self.get_id(item)] = ClientCredentials._load(raw_auth)
            loaded.append(WorkflowTriggerUpsert.load(item))
        return loaded
