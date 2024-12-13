from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from .utils import get_version_from_config, load_configfile
import yaml


class SnkConfigError(Exception):
    """
    Base class for all SNK config exceptions.
    """

class InvalidSnkConfigError(SnkConfigError, ValueError):
    """
    Thrown if the given SNK config appears to have an invalid format.
    """

class MissingSnkConfigError(SnkConfigError, FileNotFoundError):
    """
    Thrown if the given SNK config file cannot be found.
    """

@dataclass
class SnkConfig:
    """
    A dataclass for storing Snakemake workflow configuration.

    Attributes:
      art (str, optional): The art to display in the CLI. Defaults to None.
      logo (str, optional): The logo to display in the CLI. Defaults to None.
      tagline (str): The tagline to display in the CLI. Defaults to "A Snakemake workflow CLI generated with Snk".
      font (str): The font size for the CLI. Defaults to "small".
      version (Optional[str], optional): The version of the workflow. Defaults to None.
      conda (bool): Whether to use conda for managing environments. Defaults to True.
      resources (List[Path]): List of paths to additional resources. Defaults to an empty list.
      symlink_resources (bool): Whether to symlink resources instead of copying them. Defaults to False.
      skip_missing (bool): Whether to skip missing CLI options. Defaults to False.
      additional_snakemake_args (List[str]): List of additional Snakemake command-line arguments. Defaults to an empty list.
      commands (List[str]): List of subcommands to include in the CLI. Defaults to ["run", "script", "env", "profile", "info", "config"].
      snakefile (Optional[Path]): Path to the Snakefile. Defaults to None.
      configfile (Optional[Path]): Path to the config file. Defaults to None.
      min_snk_cli_version (Optional[str]): Minimum version of the SNK CLI required to run the workflow. Defaults to None.
      cli (dict): Dictionary of CLI options and their values. Defaults to an empty dictionary.
      _snk_config_path (Path): The path to the SNK config file. Defaults to None.

    Methods:
      from_path(snk_config_path: Path) -> SnkConfig:
        Load and validate Snk config from file.

      from_workflow_dir(workflow_dir_path: Path, create_if_not_exists: bool = False) -> SnkConfig:
        Load and validate SNK config from workflow directory.

      validate_resources(resources: List[Path]) -> None:
        Validate resources.

      add_resources(resources: List[Path], workflow_dir_path: Path = None) -> None:
        Add resources to the SNK config.

      to_yaml(path: Path) -> None:
        Write SNK config to YAML file.

      save() -> None:
        Save SNK config.
    """

    art: str = None
    logo: str = None
    tagline: str = "A Snakemake workflow CLI generated with Snk"
    font: str = "small"
    version: Optional[str] = None
    conda: bool = True
    resources: List[Path] = field(default_factory=list)
    symlink_resources: bool = False
    skip_missing: bool = False # skip any missing cli options (i.e. those not in the snk file)
    additional_snakemake_args: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=lambda: ["run", "script", "env", "profile", "info", "config"])
    snakefile: Optional[Path] = None
    configfile: Optional[Path] = None
    min_snk_cli_version: Optional[str] = None
    cli: dict = field(default_factory=dict)
    _snk_config_path: Path = None

    @classmethod
    def from_path(cls, snk_config_path: Path):
        """
        Load and validate Snk config from file.
        Args:
          snk_config_path (Path): Path to the SNK config file.
        Returns:
          SnkConfig: A SnkConfig object.
        Raises:
          FileNotFoundError: If the SNK config file is not found.
        Examples:
          >>> SnkConfig.from_path(Path("snk.yaml"))
          SnkConfig(art=None, logo=None, tagline='A Snakemake workflow CLI generated with Snk', font='small', resources=[], annotations={}, symlink_resources=False, _snk_config_path=PosixPath('snk.yaml'))
        """
        if not snk_config_path.exists():
            raise MissingSnkConfigError(
                f"Could not find SNK config file: {snk_config_path}"
            ) from FileNotFoundError
        # raise error if file is empty
        if snk_config_path.stat().st_size == 0:
            raise InvalidSnkConfigError(f"SNK config file is empty: {snk_config_path}") from ValueError

        snk_config_dict = load_configfile(snk_config_path)
        snk_config_dict["version"] = get_version_from_config(snk_config_path, snk_config_dict)
        if "annotations" in snk_config_dict:
            # TODO: remove annotations in the future
            snk_config_dict["cli"] = snk_config_dict["annotations"]
            del snk_config_dict["annotations"]
        if "conda_required" in snk_config_dict:
            # TODO: remove conda_required in the future
            snk_config_dict["conda"] = snk_config_dict["conda_required"]
            del snk_config_dict["conda_required"]
        # print warning about any invalid keys
        fields = set(cls.__dict__["__dataclass_fields__"])
        invalid_config_keys = set(snk_config_dict.keys()) - fields
        if invalid_config_keys:
            import warnings
            warnings.warn(f"invalid keys in `snk.yaml` file: {invalid_config_keys}.")
        # filer out any invalid keys
        snk_config_dict = {k: v for k, v in snk_config_dict.items() if k in fields}
        snk_config = cls(**snk_config_dict)
        snk_config.resources = [
            snk_config_path.parent / resource for resource in snk_config.resources
        ]
        snk_config.validate_resources(snk_config.resources)
        snk_config._snk_config_path = snk_config_path
        snk_config.snakefile = Path(snk_config.snakefile) if snk_config.snakefile else None
        snk_config.configfile = Path(snk_config.configfile) if snk_config.configfile else None
        return snk_config
  
    @classmethod
    def from_workflow_dir(
        cls, workflow_dir_path: Path, create_if_not_exists: bool = False
    ):
        """
        Load and validate SNK config from workflow directory.
        Args:
          workflow_dir_path (Path): Path to the workflow directory.
          create_if_not_exists (bool): Whether to create a SNK config file if one does not exist.
        Returns:
          SnkConfig: A SnkConfig object.
        Raises:
          FileNotFoundError: If the SNK config file is not found.
        Examples:
          >>> SnkConfig.from_workflow_dir(Path("workflow"))
          SnkConfig(art=None, logo=None, tagline='A Snakemake workflow CLI generated with Snk', font='small', resources=[], annotations={}, symlink_resources=False, _snk_config_path=PosixPath('workflow/snk.yaml'))
        """
        if (workflow_dir_path / "snk.yaml").exists():
            return cls.from_path(workflow_dir_path / "snk.yaml")
        elif (workflow_dir_path / ".snk").exists():
            import warnings

            warnings.warn(
                "Use of .snk will be deprecated in the future. Please use snk.yaml instead.",
                DeprecationWarning,
            )
            return cls.from_path(workflow_dir_path / ".snk")
        elif create_if_not_exists:
            snk_config = cls(_snk_config_path=workflow_dir_path / "snk.yaml")
            return snk_config
        else:
            raise FileNotFoundError(
                f"Could not find SNK config file in workflow directory: {workflow_dir_path}"
            )

    def validate_resources(self, resources):
        """
        Validate resources.
        Args:
          resources (List[Path]): List of resources to validate.
        Raises:
          FileNotFoundError: If a resource is not found.
        Notes:
          This function does not modify the resources list.
        Examples:
          >>> SnkConfig.validate_resources([Path("resource1.txt"), Path("resource2.txt")])
        """
        for resource in resources:
            if not resource.exists():
                raise FileNotFoundError(f"Could not find resource: {resource}")

    def add_resources(self, resources: List[Path], workflow_dir_path: Path = None):
        """
        Add resources to the SNK config.
        Args:
          resources (List[Path]): List of resources to add.
          workflow_dir_path (Path): Path to the workflow directory.
        Returns:
          None
        Side Effects:
          Adds the resources to the SNK config.
        Examples:
          >>> snk_config = SnkConfig()
          >>> snk_config.add_resources([Path("resource1.txt"), Path("resource2.txt")], Path("workflow"))
        """
        processed = []
        for resource in resources:
            if workflow_dir_path and not resource.is_absolute():
                resource = workflow_dir_path / resource
            processed.append(resource)
        self.validate_resources(processed)
        self.resources.extend(processed)

    def to_yaml(self, path: Path) -> None:
        """
        Write SNK config to YAML file.
        Args:
          path (Path): Path to write the YAML file to.
        Returns:
          None
        Side Effects:
          Writes the SNK config to the specified path.
        Examples:
          >>> snk_config = SnkConfig()
          >>> snk_config.to_yaml(Path("snk.yaml"))
        """
        config_dict = {k: v for k, v in vars(self).items() if not k.startswith("_")}
        def convert_paths(data):
            if isinstance(data, dict):
                return {key: convert_paths(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_paths(item) for item in data]
            elif isinstance(data, Path):
                return str(data)
            return data
        
        config_dict = convert_paths(config_dict)

        with open(path, "w") as f:
            yaml.dump(config_dict, f)

    def save(self) -> None:
        """
        Save SNK config.
        Args:
          path (Path): Path to write the YAML file to.
        Returns:
          None
        Side Effects:
          Writes the SNK config to the path specified by _snk_config_path.
        Examples:
          >>> snk_config = SnkConfig()
          >>> snk_config.save()
        """
        self.to_yaml(self._snk_config_path)


def get_config_from_workflow_dir(workflow_dir_path: Path):
    """
    Get the config file from a workflow directory.
    Args:
      workflow_dir_path (Path): Path to the workflow directory.
    Returns:
      Path: Path to the config file, or None if not found.
    Examples:
      >>> get_config_from_workflow_dir(Path("workflow"))
      PosixPath('workflow/config.yaml')
    """
    for path in [
        Path("config") / "config.yaml",
        Path("config") / "config.yml",
        "config.yaml",
        "config.yml",
    ]:
        if (workflow_dir_path / path).exists():
            return workflow_dir_path / path
    return None


def load_workflow_snakemake_config(workflow_dir_path: Path):
    """
    Load the Snakemake config from a workflow directory.
    Args:
      workflow_dir_path (Path): Path to the workflow directory.
    Returns:
      dict: The Snakemake config.
    Examples:
      >>> load_workflow_snakemake_config(Path("workflow"))
      {'inputs': {'data': 'data.txt'}, 'outputs': {'results': 'results.txt'}}
    """
    workflow_config_path = get_config_from_workflow_dir(workflow_dir_path)
    if not workflow_config_path or not workflow_config_path.exists():
        return {}
    return load_configfile(workflow_config_path)
