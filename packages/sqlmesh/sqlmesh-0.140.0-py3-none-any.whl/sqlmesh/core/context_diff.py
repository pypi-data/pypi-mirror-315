"""
# ContextDiff

ContextDiff encapsulates the differences between two environments. The two environments can be the local
environment and a remote environment, or two remote environments. ContextDiff is an important part of
SQLMesh. SQLMesh plans use ContextDiff to determine what nodes were changed between two environments.
The SQLMesh CLI diff command uses ContextDiff to determine what to visualize.

When creating a ContextDiff object, SQLMesh will compare the snapshots from one environment with those of
another remote environment and determine if nodes have been added, removed, or modified.
"""

from __future__ import annotations

import logging
import sys
import typing as t
from difflib import ndiff
from functools import cached_property
from sqlmesh.core import constants as c
from sqlmesh.core.snapshot import Snapshot, SnapshotId, SnapshotTableInfo
from sqlmesh.utils.errors import SQLMeshError
from sqlmesh.utils.pydantic import PydanticModel


if sys.version_info >= (3, 12):
    from importlib import metadata
else:
    import importlib_metadata as metadata  # type: ignore


if t.TYPE_CHECKING:
    from sqlmesh.core.state_sync import StateReader

IGNORED_PACKAGES = {"sqlmesh", "sqlglot"}

logger = logging.getLogger(__name__)


class ContextDiff(PydanticModel):
    """ContextDiff is an object representing the difference between two environments.

    The two environments can be the local environment and a remote environment, or two remote
    environments.
    """

    environment: str
    """The environment to diff."""
    is_new_environment: bool
    """Whether the target environment is new."""
    is_unfinalized_environment: bool
    """Whether the currently stored environment record is in unfinalized state."""
    normalize_environment_name: bool
    """Whether the environment name should be normalized."""
    create_from: str
    """The name of the environment the target environment will be created from if new."""
    create_from_env_exists: bool
    """Whether the create_from environment already exists at plan time."""
    added: t.Set[SnapshotId]
    """New nodes."""
    removed_snapshots: t.Dict[SnapshotId, SnapshotTableInfo]
    """Deleted nodes."""
    modified_snapshots: t.Dict[str, t.Tuple[Snapshot, Snapshot]]
    """Modified snapshots."""
    snapshots: t.Dict[SnapshotId, Snapshot]
    """Merged snapshots."""
    new_snapshots: t.Dict[SnapshotId, Snapshot]
    """New snapshots."""
    previous_plan_id: t.Optional[str]
    """Previous plan id."""
    previously_promoted_snapshot_ids: t.Set[SnapshotId]
    """Snapshot IDs that were promoted by the previous plan."""
    previous_finalized_snapshots: t.Optional[t.List[SnapshotTableInfo]]
    """Snapshots from the previous finalized state."""
    previous_requirements: t.Dict[str, str] = {}
    """Previous requirements."""
    provided_requirements: t.Dict[str, str] = {}
    """Requirements from lock file."""

    @classmethod
    def create(
        cls,
        environment: str,
        snapshots: t.Dict[str, Snapshot],
        create_from: str,
        state_reader: StateReader,
        ensure_finalized_snapshots: bool = False,
        requirements: t.Optional[t.Dict[str, str]] = None,
    ) -> ContextDiff:
        """Create a ContextDiff object.

        Args:
            environment: The remote environment to diff.
            snapshots: The snapshots of the current environment.
            create_from: The environment to create the target environment from if it
                doesn't exist.
            state_reader: StateReader to access the remote environment to diff.
            ensure_finalized_snapshots: Whether to compare against snapshots from the latest finalized
                environment state, or to use whatever snapshots are in the current environment state even if
                the environment is not finalized.
            requirements: Fixed requirements to build the context diff with.

        Returns:
            The ContextDiff object.
        """
        environment = environment.lower()
        env = state_reader.get_environment(environment)

        create_from_env_exists = False
        if env is None or env.expired:
            env = state_reader.get_environment(create_from.lower())

            if not env and create_from != c.PROD:
                logger.warning(
                    f"The environment name '{create_from}' was passed to the `plan` command's `--create-from` argument, but '{create_from}' does not exist. Initializing new environment '{environment}' from scratch."
                )

            is_new_environment = True
            create_from_env_exists = env is not None
            previously_promoted_snapshot_ids = set()
        else:
            is_new_environment = False
            previously_promoted_snapshot_ids = {s.snapshot_id for s in env.promoted_snapshots}

        environment_snapshot_infos = []
        if env:
            environment_snapshot_infos = (
                env.snapshots
                if not ensure_finalized_snapshots
                else env.finalized_or_current_snapshots
            )
        remote_snapshot_name_to_info = {
            snapshot_info.name: snapshot_info for snapshot_info in environment_snapshot_infos
        }
        removed = {
            snapshot_table_info.snapshot_id: snapshot_table_info
            for snapshot_table_info in environment_snapshot_infos
            if snapshot_table_info.name not in snapshots
        }
        added = {
            snapshot.snapshot_id
            for snapshot in snapshots.values()
            if snapshot.name not in remote_snapshot_name_to_info
        }
        modified_snapshot_name_to_snapshot_info = {
            snapshot.name: remote_snapshot_name_to_info[snapshot.name]
            for snapshot in snapshots.values()
            if snapshot.snapshot_id not in added
            and snapshot.fingerprint != remote_snapshot_name_to_info[snapshot.name].fingerprint
        }

        stored = state_reader.get_snapshots(
            [*snapshots.values(), *modified_snapshot_name_to_snapshot_info.values()]
        )

        merged_snapshots = {}
        modified_snapshots = {}
        new_snapshots = {}

        for snapshot in snapshots.values():
            s_id = snapshot.snapshot_id
            modified_snapshot_info = modified_snapshot_name_to_snapshot_info.get(snapshot.name)
            existing_snapshot = stored.get(s_id)

            if modified_snapshot_info and snapshot.node_type != modified_snapshot_info.node_type:
                added.add(snapshot.snapshot_id)
                removed[modified_snapshot_info.snapshot_id] = modified_snapshot_info
                modified_snapshot_name_to_snapshot_info.pop(snapshot.name)
            elif existing_snapshot:
                # Keep the original node instance to preserve the query cache.
                existing_snapshot.node = snapshot.node

                merged_snapshots[s_id] = existing_snapshot.copy()
                if modified_snapshot_info:
                    modified_snapshots[s_id.name] = (
                        existing_snapshot,
                        stored[modified_snapshot_info.snapshot_id],
                    )
            else:
                snapshot = snapshot.copy()
                merged_snapshots[s_id] = snapshot
                new_snapshots[snapshot.snapshot_id] = snapshot
                if modified_snapshot_info:
                    snapshot.previous_versions = modified_snapshot_info.all_versions
                    modified_snapshots[s_id.name] = (
                        snapshot,
                        stored[modified_snapshot_info.snapshot_id],
                    )

        return ContextDiff(
            environment=environment,
            is_new_environment=is_new_environment,
            is_unfinalized_environment=bool(env and not env.finalized_ts),
            normalize_environment_name=is_new_environment or bool(env and env.normalize_name),
            create_from=create_from,
            create_from_env_exists=create_from_env_exists,
            added=added,
            removed_snapshots=removed,
            modified_snapshots=modified_snapshots,
            snapshots=merged_snapshots,
            new_snapshots=new_snapshots,
            previous_plan_id=env.plan_id if env and not is_new_environment else None,
            previously_promoted_snapshot_ids=previously_promoted_snapshot_ids,
            previous_finalized_snapshots=env.previous_finalized_snapshots if env else None,
            previous_requirements=env.requirements if env else {},
            provided_requirements=requirements,
        )

    @classmethod
    def create_no_diff(cls, environment: str, state_reader: StateReader) -> ContextDiff:
        """Create a no-op ContextDiff object.

        Args:
            environment: The target environment.
            state_reader: StateReader to access the remote environment record.

        Returns:
            The ContextDiff object.
        """
        env = state_reader.get_environment(environment.lower())
        if not env:
            raise SQLMeshError(f"Environment '{environment}' must exist for this operation.")

        snapshots = state_reader.get_snapshots(env.snapshots)

        return ContextDiff(
            environment=env.name,
            is_new_environment=False,
            is_unfinalized_environment=False,
            normalize_environment_name=env.normalize_name,
            create_from="",
            create_from_env_exists=False,
            added=set(),
            removed_snapshots={},
            modified_snapshots={},
            snapshots=snapshots,
            new_snapshots={},
            previous_plan_id=env.plan_id,
            previously_promoted_snapshot_ids={s.snapshot_id for s in env.promoted_snapshots},
            previous_finalized_snapshots=env.previous_finalized_snapshots,
            previous_requirements=env.requirements,
            provided_requirements=env.requirements,
        )

    @property
    def has_changes(self) -> bool:
        return (
            self.has_snapshot_changes
            or self.is_new_environment
            or self.is_unfinalized_environment
            or self.has_requirement_changes
        )

    @property
    def has_requirement_changes(self) -> bool:
        return self.previous_requirements != self.requirements

    @property
    def has_snapshot_changes(self) -> bool:
        return bool(self.added or self.removed_snapshots or self.modified_snapshots)

    @property
    def added_materialized_snapshot_ids(self) -> t.Set[SnapshotId]:
        """Returns the set of added internal snapshot ids."""
        return {
            s_id
            for s_id in self.added
            if self.snapshots[s_id].model_kind_name
            and self.snapshots[s_id].model_kind_name.is_materialized  # type: ignore
        }

    @property
    def promotable_snapshot_ids(self) -> t.Set[SnapshotId]:
        """The set of snapshot ids that have to be promoted in the target environment."""
        return {
            *self.previously_promoted_snapshot_ids,
            *self.added,
            *self.current_modified_snapshot_ids,
        } - set(self.removed_snapshots)

    @property
    def unpromoted_models(self) -> t.Set[SnapshotId]:
        """The set of snapshot IDs that have not yet been promoted in the target environment."""
        return set(self.snapshots) - self.previously_promoted_snapshot_ids

    @property
    def current_modified_snapshot_ids(self) -> t.Set[SnapshotId]:
        return {current.snapshot_id for current, _ in self.modified_snapshots.values()}

    @cached_property
    def snapshots_by_name(self) -> t.Dict[str, Snapshot]:
        return {x.name: x for x in self.snapshots.values()}

    @cached_property
    def requirements(self) -> t.Dict[str, str]:
        requirements = self.provided_requirements.copy()
        distributions = metadata.packages_distributions()

        for snapshot in self.snapshots.values():
            if snapshot.is_model:
                for executable in snapshot.model.python_env.values():
                    if executable.kind == "import":
                        try:
                            start = "from " if executable.payload.startswith("from ") else "import "
                            lib = executable.payload.split(start)[1].split()[0].split(".")[0]
                            if lib in distributions:
                                for dist in distributions[lib]:
                                    if dist not in requirements and dist not in IGNORED_PACKAGES:
                                        requirements[dist] = metadata.version(dist)
                        except metadata.PackageNotFoundError:
                            logger.warning("Failed to find package for %s", lib)
        return requirements

    def requirements_diff(self) -> str:
        return "\n".join(
            ndiff(
                [
                    f"{k}=={self.previous_requirements[k]}"
                    for k in sorted(self.previous_requirements)
                ],
                [f"{k}=={self.requirements[k]}" for k in sorted(self.requirements)],
            )
        )

    @property
    def environment_snapshots(self) -> t.List[SnapshotTableInfo]:
        """Returns current snapshots in the environment."""
        return [
            *self.removed_snapshots.values(),
            *(old.table_info for _, old in self.modified_snapshots.values()),
            *[
                s.table_info
                for s_id, s in self.snapshots.items()
                if s_id not in self.added and s.name not in self.modified_snapshots
            ],
        ]

    def directly_modified(self, name: str) -> bool:
        """Returns whether or not a node was directly modified in this context.

        Args:
            name: The snapshot name to check.

        Returns:
            Whether or not the node was directly modified.
        """

        if name not in self.modified_snapshots:
            return False

        current, previous = self.modified_snapshots[name]
        return current.fingerprint.data_hash != previous.fingerprint.data_hash

    def indirectly_modified(self, name: str) -> bool:
        """Returns whether or not a node was indirectly modified in this context.

        Args:
            name: The snapshot name to check.

        Returns:
            Whether or not the node was indirectly modified.
        """

        if name not in self.modified_snapshots:
            return False

        current, previous = self.modified_snapshots[name]
        return (
            current.fingerprint.data_hash == previous.fingerprint.data_hash
            and current.fingerprint.parent_data_hash != previous.fingerprint.parent_data_hash
        )

    def metadata_updated(self, name: str) -> bool:
        """Returns whether or not the given node's metadata has been updated.

        Args:
            name: The node to check.

        Returns:
            Whether or not the node's metadata has been updated.
        """

        if name not in self.modified_snapshots:
            return False

        current, previous = self.modified_snapshots[name]
        return current.fingerprint.metadata_hash != previous.fingerprint.metadata_hash

    def text_diff(self, name: str) -> str:
        """Finds the difference of a node between the current and remote environment.

        Args:
            name: The Snapshot name.

        Returns:
            A unified text diff of the node.
        """
        if name not in self.snapshots_by_name:
            raise SQLMeshError(f"`{name}` does not exist.")
        if name not in self.modified_snapshots:
            return ""

        new, old = self.modified_snapshots[name]
        try:
            return old.node.text_diff(new.node)
        except SQLMeshError as e:
            logger.warning("Failed to diff model '%s': %s", name, str(e))
            return ""
