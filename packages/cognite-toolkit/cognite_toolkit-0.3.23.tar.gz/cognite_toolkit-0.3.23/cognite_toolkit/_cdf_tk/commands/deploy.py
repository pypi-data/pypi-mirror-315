from __future__ import annotations

import re
import traceback
from graphlib import TopologicalSorter
from pathlib import Path
from typing import Any

from cognite.client.data_classes._base import T_CogniteResourceList
from cognite.client.exceptions import CogniteAPIError, CogniteDuplicatedError
from rich import print
from rich.panel import Panel

from cognite_toolkit._cdf_tk.commands._base import ToolkitCommand
from cognite_toolkit._cdf_tk.commands.clean import CleanCommand
from cognite_toolkit._cdf_tk.constants import (
    _RUNNING_IN_BROWSER,
    BUILD_ENVIRONMENT_FILE,
    TABLE_FORMATS,
)
from cognite_toolkit._cdf_tk.data_classes import (
    BuildEnvironment,
    DatapointDeployResult,
    DeployResult,
    DeployResults,
    ResourceContainerDeployResult,
    ResourceDeployResult,
    UploadDeployResult,
)
from cognite_toolkit._cdf_tk.exceptions import (
    ResourceCreationError,
    ResourceUpdateError,
    ToolkitDeployResourceError,
    ToolkitFileNotFoundError,
    ToolkitNotADirectoryError,
)
from cognite_toolkit._cdf_tk.loaders import (
    DataLoader,
    Loader,
    RawDatabaseLoader,
    ResourceContainerLoader,
    ResourceLoader,
)
from cognite_toolkit._cdf_tk.tk_warnings.other import (
    LowSeverityWarning,
    MediumSeverityWarning,
    ToolkitDependenciesIncludedWarning,
)
from cognite_toolkit._cdf_tk.utils import (
    CDFToolConfig,
    read_yaml_file,
    to_diff,
)

from ._utils import _print_ids_or_length, _remove_duplicates


class DeployCommand(ToolkitCommand):
    def __init__(self, print_warning: bool = True, skip_tracking: bool = False, silent: bool = False) -> None:
        super().__init__(print_warning, skip_tracking, silent)
        self._clean_command = CleanCommand(print_warning, skip_tracking=True)

    def execute(
        self,
        ToolGlobals: CDFToolConfig,
        build_dir: Path,
        build_env_name: str | None,
        dry_run: bool,
        drop: bool,
        drop_data: bool,
        force_update: bool,
        include: list[str],
        verbose: bool,
    ) -> None:
        if not build_dir.is_dir():
            raise ToolkitNotADirectoryError(
                "The build directory does not exists. Did you forget to run `cdf-tk build` first?"
            )
        build_environment_file_path = build_dir / BUILD_ENVIRONMENT_FILE
        if not build_environment_file_path.is_file():
            raise ToolkitFileNotFoundError(
                f"Could not find build environment file '{BUILD_ENVIRONMENT_FILE}' in '{build_dir}'. "
                "Did you forget to run `cdf-tk build` first?"
            )

        deploy_state = BuildEnvironment.load(read_yaml_file(build_environment_file_path), build_env_name, "deploy")

        deploy_state.set_environment_variables()

        errors = deploy_state.check_source_files_changed()
        for error in errors:
            self.warn(error)
        if errors:
            raise ToolkitDeployResourceError(
                "One or more source files have been modified since the last build. Please rebuild the project."
            )
        environment_vars = ""
        if not _RUNNING_IN_BROWSER:
            environment_vars = f"\n\nConnected to {ToolGlobals.as_string()}"

        verb = "Checking" if dry_run else "Deploying"

        print(
            Panel(
                f"[bold]{verb}[/]resource files from {build_dir} directory." f"{environment_vars}",
                expand=False,
            )
        )

        selected_loaders = self._clean_command.get_selected_loaders(
            build_dir, deploy_state.read_resource_folders, include
        )

        results = DeployResults([], "deploy", dry_run=dry_run)

        ordered_loaders: list[type[Loader]] = []
        should_include: list[type[Loader]] = []
        # The topological sort can include loaders that are not selected, so we need to check for that.
        for loader_cls in TopologicalSorter(selected_loaders).static_order():
            if loader_cls in selected_loaders:
                ordered_loaders.append(loader_cls)
            elif (build_dir / loader_cls.folder_name).is_dir():
                should_include.append(loader_cls)
            # Otherwise, it is not in the build directory and not selected, so we skip it.
            # There should be a warning in the build step if it is missing.
        if should_include:
            self.warn(ToolkitDependenciesIncludedWarning(list({item.folder_name for item in should_include})))

        result: DeployResult | None
        if drop or drop_data:
            # Drop has to be done in the reverse order of deploy.
            if drop and drop_data:
                print(Panel("[bold] Cleaning resources as --drop and --drop-data are passed[/]"))
            elif drop:
                print(Panel("[bold] Cleaning resources as --drop is passed[/]"))
            elif drop_data:
                print(Panel("[bold] Cleaning resources as --drop-data is passed[/]"))

            for loader_cls in reversed(ordered_loaders):
                if not issubclass(loader_cls, ResourceLoader):
                    continue
                loader: ResourceLoader = loader_cls.create_loader(ToolGlobals, build_dir)
                result = self._clean_command.clean_resources(
                    loader,
                    ToolGlobals,
                    drop=drop,
                    dry_run=dry_run,
                    drop_data=drop_data,
                    verbose=verbose,
                )
                if result:
                    results[result.name] = result
            print("[bold]...cleaning complete![/]")

        if drop or drop_data:
            print(Panel("[bold]DEPLOYING resources...[/]"))

        for loader_cls in ordered_loaders:
            loader_instance = loader_cls.create_loader(ToolGlobals, build_dir)
            result = self.deploy_resources(
                loader_instance,
                ToolGlobals=ToolGlobals,
                state=deploy_state,
                dry_run=dry_run,
                has_done_drop=drop,
                has_dropped_data=drop_data,
                force_update=force_update,
                verbose=verbose,
            )
            if result:
                results[result.name] = result
            if verbose:
                print("")  # Extra newline

        if results.has_counts:
            print(results.counts_table())
        if results.has_uploads:
            print(results.uploads_table())

    def deploy_resources(
        self,
        loader: Loader,
        ToolGlobals: CDFToolConfig,
        state: BuildEnvironment,
        dry_run: bool = False,
        has_done_drop: bool = False,
        has_dropped_data: bool = False,
        force_update: bool = False,
        verbose: bool = False,
    ) -> DeployResult | None:
        if isinstance(loader, ResourceLoader):
            return self._deploy_resources(
                loader, ToolGlobals, state, dry_run, has_done_drop, has_dropped_data, force_update, verbose
            )
        elif isinstance(loader, DataLoader):
            return self._deploy_data(loader, ToolGlobals, state, dry_run, verbose)
        else:
            raise ValueError(f"Unsupported loader type {type(loader)}.")

    def _deploy_resources(
        self,
        loader: ResourceLoader,
        ToolGlobals: CDFToolConfig,
        state: BuildEnvironment,
        dry_run: bool = False,
        has_done_drop: bool = False,
        has_dropped_data: bool = False,
        force_update: bool = False,
        verbose: bool = False,
    ) -> ResourceDeployResult | None:
        filepaths = loader.find_files()

        for read_module in state.read_modules:
            if resource_dir := read_module.resource_dir_path(loader.folder_name):
                # As of 05/11/24, Asset support csv and parquet files in addition to YAML.
                # These table formats are not built, i.e., no variable replacement is done,
                # so we load them directly from the source module.
                filepaths.extend(loader.find_files(resource_dir, include_formats=TABLE_FORMATS))

        if not filepaths:
            # Skipping silently as this is not an error.
            return None

        def sort_key(p: Path) -> int:
            if result := re.findall(r"^(\d+)", p.stem):
                return int(result[0])
            else:
                return len(filepaths)

        # In the build step, the resource files are prefixed a number that controls the order in which
        # the resources are deployed. The custom 'sort_key' here is to get a sort on integer instead of a default string
        # sort.
        filepaths = sorted(filepaths, key=sort_key)

        loaded_resources = self._load_files(loader, filepaths, ToolGlobals, skip_validation=dry_run)

        # Duplicates should be handled on the build step,
        # but in case any of them slip through, we do it here as well to
        # avoid an error.
        loaded_resources, duplicates = _remove_duplicates(loaded_resources, loader)

        if not loaded_resources:
            return ResourceDeployResult(name=loader.display_name)

        capabilities = loader.get_required_capability(loaded_resources, read_only=dry_run)
        if capabilities:
            ToolGlobals.verify_authorization(capabilities, action=f"deploy {loader.display_name}")

        nr_of_items = len(loaded_resources)
        if nr_of_items == 0:
            return ResourceDeployResult(name=loader.display_name)

        prefix = "Would deploy" if dry_run else "Deploying"
        print(f"[bold]{prefix} {nr_of_items} {loader.display_name} to CDF...[/]")
        # Moved here to avoid printing before the above message.
        if not isinstance(loader, RawDatabaseLoader):
            for duplicate in duplicates:
                self.warn(LowSeverityWarning(f"Skipping duplicate {loader.display_name} {duplicate}."))

        nr_of_created = nr_of_changed = nr_of_unchanged = 0
        to_create, to_update, unchanged = self.to_create_changed_unchanged_triple(loaded_resources, loader, verbose)
        if force_update:
            to_update.extend(unchanged)
            unchanged.clear()

        if dry_run:
            if (
                loader.support_drop
                and has_done_drop
                and (not isinstance(loader, ResourceContainerLoader) or has_dropped_data)
            ):
                # Means the resources will be deleted and not left unchanged or changed
                for item in unchanged:
                    # We cannot use extents as LoadableNodes cannot be extended.
                    to_create.append(item)
                for item in to_update:
                    to_create.append(item)
                unchanged.clear()
                to_update.clear()

            nr_of_unchanged += len(unchanged)
            nr_of_created += len(to_create)
            nr_of_changed += len(to_update)
        else:
            nr_of_unchanged += len(unchanged)

            if to_create:
                created = self._create_resources(to_create, loader)
                nr_of_created += created

            if to_update:
                updated = self._update_resources(to_update, loader)
                nr_of_changed += updated

        if verbose:
            self._verbose_print(to_create, to_update, unchanged, loader, dry_run)

        if isinstance(loader, ResourceContainerLoader):
            return ResourceContainerDeployResult(
                name=loader.display_name,
                created=nr_of_created,
                changed=nr_of_changed,
                unchanged=nr_of_unchanged,
                total=nr_of_items,
                item_name=loader.item_name,
            )
        else:
            return ResourceDeployResult(
                name=loader.display_name,
                created=nr_of_created,
                changed=nr_of_changed,
                unchanged=nr_of_unchanged,
                total=nr_of_items,
            )

    def to_create_changed_unchanged_triple(
        self,
        resources: T_CogniteResourceList,
        loader: ResourceLoader,
        verbose: bool = False,
    ) -> tuple[T_CogniteResourceList, T_CogniteResourceList, T_CogniteResourceList]:
        """Returns a triple of lists of resources that should be created, updated, and are unchanged."""
        resource_ids = loader.get_ids(resources)
        to_create, to_update, unchanged = (
            loader.list_write_cls([]),
            loader.list_write_cls([]),
            loader.list_write_cls([]),
        )
        try:
            cdf_resources = loader.retrieve(resource_ids)
        except CogniteAPIError as e:
            self.warn(
                MediumSeverityWarning(
                    f"Failed to retrieve {len(resource_ids)} of {loader.display_name}. Proceeding assuming not data in CDF. Error {e}."
                )
            )
            print(Panel(traceback.format_exc()))
            cdf_resource_by_id = {}
        else:
            cdf_resource_by_id = {loader.get_id(resource): resource for resource in cdf_resources}

        for item in resources:
            identifier = loader.get_id(item)
            cdf_resource = cdf_resource_by_id.get(identifier)
            local_dumped: dict[str, Any] = {}
            cdf_dumped: dict[str, Any] = {}
            are_equal = False
            if cdf_resource:
                try:
                    are_equal, local_dumped, cdf_dumped = loader.are_equal(item, cdf_resource, return_dumped=True)
                except CogniteAPIError as e:
                    self.warn(
                        MediumSeverityWarning(
                            f"Failed to compare {loader.display_name} {loader.get_id(item)} for equality. Proceeding assuming not data in CDF. Error {e}."
                        )
                    )
                    print(Panel(traceback.format_exc()))

            if are_equal:
                unchanged.append(item)
            elif cdf_resource:
                if verbose:
                    print(
                        Panel(
                            "\n".join(to_diff(cdf_dumped, local_dumped)),
                            title=f"{loader.display_name}: {identifier}",
                            expand=False,
                        )
                    )
                to_update.append(item)
            else:
                to_create.append(item)

        return to_create, to_update, unchanged

    def _verbose_print(
        self,
        to_create: T_CogniteResourceList,
        to_update: T_CogniteResourceList,
        unchanged: T_CogniteResourceList,
        loader: ResourceLoader,
        dry_run: bool,
    ) -> None:
        print_outs = []
        prefix = "Would have " if dry_run else ""
        if to_create:
            print_outs.append(f"{prefix}Created {_print_ids_or_length(loader.get_ids(to_create), limit=20)}")
        if to_update:
            print_outs.append(f"{prefix}Updated {_print_ids_or_length(loader.get_ids(to_update), limit=20)}")
        if unchanged:
            print_outs.append(
                f"{'Untouched' if dry_run else 'Unchanged'} {_print_ids_or_length(loader.get_ids(unchanged), limit=5)}"
            )
        prefix_message = f" {loader.display_name}: "
        if len(print_outs) == 1:
            print(f"{prefix_message}{print_outs[0]}")
        elif len(print_outs) == 2:
            print(f"{prefix_message}{print_outs[0]} and {print_outs[1]}")
        else:
            print(f"{prefix_message}{', '.join(print_outs[:-1])} and {print_outs[-1]}")

    def _create_resources(self, resources: T_CogniteResourceList, loader: ResourceLoader) -> int:
        try:
            created = loader.create(resources)
        except CogniteAPIError as e:
            if e.code == 409:
                self.warn(LowSeverityWarning("Resource(s) already exist(s), skipping creation."))
            else:
                # This must be printed as this if not rich filters out regex patterns from
                # the error message which typically contains the critical information.
                print(e)
                raise ResourceCreationError(f"Failed to create resource(s). Error: {e!s}.") from e
        except CogniteDuplicatedError as e:
            self.warn(
                LowSeverityWarning(
                    f"{len(e.duplicated)} out of {len(resources)} resource(s) already exist(s). {len(e.successful or [])} resource(s) created."
                )
            )
        else:
            return len(created) if created is not None else 0
        return 0

    def _update_resources(self, resources: T_CogniteResourceList, loader: ResourceLoader) -> int:
        try:
            updated = loader.update(resources)
        except CogniteAPIError as e:
            print(Panel(traceback.format_exc()))
            raise ResourceUpdateError(f"Failed to update resource(s). Error: {e!r}.") from e

        return len(updated)

    def _deploy_data(
        self,
        loader: DataLoader,
        ToolGlobals: CDFToolConfig,
        state: BuildEnvironment,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> UploadDeployResult:
        prefix = "Would upload" if dry_run else "Uploading"
        print(f"[bold]{prefix} {loader.display_name} files to CDF...[/]")

        datapoints = 0
        file_counts = 0
        for message, file_datapoints in loader.upload(state, ToolGlobals, dry_run):
            if verbose:
                print(message)
            datapoints += file_datapoints
            file_counts += 1

        if datapoints != 0:
            return DatapointDeployResult(
                loader.display_name, points=datapoints, uploaded=file_counts, item_name=loader.item_name
            )
        else:
            return UploadDeployResult(loader.display_name, uploaded=file_counts, item_name=loader.item_name)
