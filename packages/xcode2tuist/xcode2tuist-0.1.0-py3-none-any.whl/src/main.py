"""
CLI tool to convert an Xcode project (.xcodeproj) file to a Tuist configuration.
"""

import os
import uuid
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
import json

from pbxproj import XcodeProject, PBXKey
from pbxproj.pbxsections import *
from pbxproj.pbxextensions import TreeType
import traceback
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure rich console
console = Console()


@dataclass
class ConversionConfig:
    """Configuration for the conversion process."""

    input_path: Path
    output_path: Path
    verbose: bool = False


class PBXToTuistConverter:
    def __init__(self, config: ConversionConfig):
        """
        Initializes the converter with the path to the Xcode project.

        Args:
            config (ConversionConfig): Configuration for the conversion process
        """
        self.config = config
        self.xcode_project_path = self._validate_input_path(config.input_path)
        self.output_path = self._validate_output_path(config.output_path)
        self.xcode_project = XcodeProject.load(str(self.xcode_project_path))
        self.tuist_data: Dict[str, List[Any]] = {"projects": [], "workspaces": []}

    def _validate_input_path(self, path: Path) -> Path:
        """Validates and returns the proper input path."""
        if path.is_dir():
            path = path / "project.pbxproj"
        if not path.is_file():
            raise FileNotFoundError(f"Project file not found at path: {path}")
        return path

    def _validate_output_path(self, path: Path) -> Path:
        """Validates and creates output directory if needed."""
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _analyze_pbxproj_capabilities(self):
        """
        This method analyzes the pbxproj library capabilities
        """
        console.print("\n--- pbxproj library analysis ---")
        console.print("- Identified project object id:", self.xcode_project.rootObject)
        console.print("- Available TreeTypes", TreeType.options())
        console.print("\n")

    def _extract_project_settings(self):
        """Extracts general project settings."""
        project_object = self.xcode_project.objects[self.xcode_project.rootObject]
        project = {}
        project["name"] = self.xcode_project._pbxproj_path.split("/")[-2]
        project["organizationalName"] = project_object.get("organizationName", "")
        project["targets"] = []  # Initialize targets list

        # Handle build configurations
        project["build_configurations"] = self._extract_build_configurations(
            configuration_list_id=project_object.get("buildConfigurationList", None)
        )
        self.tuist_data["projects"] = [project]  # Store as single project

    def _extract_target_settings(self, target):
        """Extracts target settings and adds them to the project's targets list."""
        target_data = {}
        target_data["name"] = target.name
        target_data["product"] = target.productType
        target_data["bundleId"] = target.productName
        target_data["destinations"] = target.productType
        target_data["dependencies"] = []
        target_data["sources"] = []
        target_data["resources"] = []
        target_data["copy_files"] = []
        target_data["headers"] = []
        target_data["frameworks"] = []

        # Handle build configurations
        target_data["build_configurations"] = self._extract_build_configurations(
            configuration_list_id=target.buildConfigurationList, target=target
        )
        # Add build phases
        if hasattr(target, "buildPhases"):
            target_data["build_phases"] = self._extract_build_phases(
                build_phases_ids=target.buildPhases, target=target
            )
        if hasattr(target, "dependencies"):
            for dep_id in target.dependencies:
                dep = self.xcode_project.objects[dep_id]
                target_data["dependencies"].append(self._extract_dependency(dep))

        if hasattr(target, "packageProductDependencies"):
            for dep_id in target.packageProductDependencies:
                dep = self.xcode_project.objects[dep_id]
                target_data["dependencies"].append(
                    self._extract_package_dependency(dep)
                )

        for build_phase_id in target.buildPhases:
            build_phase = self.xcode_project.objects[build_phase_id]
            if isinstance(build_phase, PBXSourcesBuildPhase):
                for build_file_id in build_phase.files:
                    build_file = self.xcode_project.objects[build_file_id]
                    file_ref = self.xcode_project.objects[build_file.fileRef]
                    relative_path = self._get_relative_path(file_ref)
                    target_data["sources"].append(
                        {
                            "path": relative_path,
                        }
                    )
                continue
            if isinstance(build_phase, PBXResourcesBuildPhase):
                for build_file_id in build_phase.files:
                    build_file = self.xcode_project.objects[build_file_id]
                    file_ref = self.xcode_project.objects[build_file.fileRef]
                    relative_path = self._get_relative_path(file_ref)
                    target_data["resources"].append(
                        {
                            "path": relative_path,
                        }
                    )
                continue
            if isinstance(build_phase, PBXCopyFilesBuildPhase):
                for build_file_id in build_phase.files:
                    build_file = self.xcode_project.objects[build_file_id]
                    file_ref = self.xcode_project.objects[build_file.fileRef]
                    relative_path = self._get_relative_path(file_ref)
                    target_data["copy_files"].append(
                        {
                            "path": relative_path,
                            "destination": build_phase.dstPath,
                            "subfolder": build_phase.dstSubfolderSpec,
                        }
                    )
                continue
            if isinstance(build_phase, PBXHeadersBuildPhase):
                for build_file_id in build_phase.files:
                    build_file = self.xcode_project.objects[build_file_id]
                    file_ref = self.xcode_project.objects[build_file.fileRef]
                    relative_path = self._get_relative_path(file_ref)
                    target_data["headers"].append(
                        {
                            "path": relative_path,
                        }
                    )
                continue
            if isinstance(build_phase, PBXFrameworksBuildPhase):
                for build_file_id in build_phase.files:
                    build_file = self.xcode_project.objects[build_file_id]
                    if hasattr(build_file, "fileRef"):
                        file_ref = self.xcode_project.objects[build_file.fileRef]
                        relative_path = self._get_relative_path(file_ref)
                        target_data["frameworks"].append(
                            {
                                "path": relative_path,
                                "is_weak": build_file.get("settings", {}).get(
                                    "ATTRIBUTES"
                                )
                                == "Weak",
                            }
                        )
                    if hasattr(build_file, "productRef"):
                        product_ref = self.xcode_project.objects[build_file.productRef]
                        target_data["frameworks"].append(
                            {
                                "name": product_ref.productName,
                                "is_package": True,
                            }
                        )

        # Add target to the project's targets list instead of creating a new project
        self.tuist_data["projects"][0]["targets"].append(target_data)

    def _get_relative_path(self, file_ref):
        """
        Calculates the relative path of a file reference.
        """
        if file_ref.sourceTree == "<group>":
            # If the source tree is <group>, the path is relative to the parent group.
            parent_group = self._find_parent_group(file_ref)
            if parent_group:
                # Build the path from the root to the parent group
                path_from_root = self._build_path_from_root(parent_group)
                # Combine it with the file ref's path
                return os.path.join(path_from_root, file_ref.get("path", ""))
            else:
                # If no parent group is found, use the file ref's path directly
                return file_ref.get("path", "")
        elif file_ref.sourceTree == "SOURCE_ROOT":
            # If the source tree is SOURCE_ROOT, the path is relative to the project's root
            return file_ref.get("path", "")
        else:
            # Handle other source trees as needed
            return file_ref.get("path", "")

    def _find_parent_group(self, file_ref):
        """
        Finds the parent group of a file reference.
        """
        for group in self.xcode_project.objects.get_objects_in_section("PBXGroup"):
            if file_ref.get_id() in group.children:
                return group
        return None

    def _build_path_from_root(self, group):
        """
        Builds the path from the project root to the given group.
        """
        path_components = []
        while group and group.isa == "PBXGroup":
            if hasattr(group, "path"):
                path_components.insert(0, group.path)
            group = self._find_parent_group(group)
        if not path_components:
            return ""
        return os.path.join(*path_components)

    def _extract_dependency(self, dep: PBXTargetDependency) -> dict:
        """
        Extracts a project dependency dictionary from PBXTargetDependency object
        :param dep: PBXTargetDependency object to be extracted from.
        :return: A dictionary with the extracted dependency information.
        """
        dep_data = {}
        if hasattr(dep, "target"):
            dep_target = self.xcode_project.objects[dep.target]
            dep_data["type"] = "target"
            dep_data["name"] = dep_target.name
        if hasattr(dep, "targetProxy"):
            dep_proxy = self.xcode_project.objects[dep.targetProxy]
            container_proxy = self.xcode_project.objects[dep_proxy.containerPortal]
            dep_data["type"] = "project"
            dep_data["target"] = dep_proxy.remoteInfo
            if hasattr(container_proxy, "path"):
                dep_data["path"] = container_proxy.path
        return dep_data

    def _extract_package_dependency(self, dep: XCSwiftPackageProductDependency) -> dict:
        """
        Extracts a swift package product dependency dictionary from XCSwiftPackageProductDependency object
        :param dep: XCSwiftPackageProductDependency object to be extracted from.
        :return: A dictionary with the extracted dependency information.
        """
        dep_data = {}
        if hasattr(dep, "package"):
            dep_package = self.xcode_project.objects[dep.package]
            dep_data["type"] = "package"
            dep_data["name"] = dep.productName
            dep_data["url"] = dep_package.repositoryURL
            dep_data["requirement"] = dep_package.requirement
        return dep_data

    def _extract_build_phases(self, build_phases_ids, target) -> list:
        """
        Extracts a build phases array from an array of PBXGenericBuildPhase objects
        :param build_phases_ids: Array of PBXGenericBuildPhase objects.
        :param target: parent Target.
        :return: A list of build phases.
        """
        phases = []
        for build_phase_id in build_phases_ids:
            build_phase = self.xcode_project.objects[build_phase_id]
            if isinstance(build_phase, PBXShellScriptBuildPhase):
                phases.append(self._extract_run_script(build_phase, target))
            if isinstance(build_phase, PBXCopyFilesBuildPhase):
                phases.append(self._extract_copy_files(build_phase, target))
        return phases

    def _extract_run_script(self, build_phase, target) -> dict:
        """
        Extracts a build phase run script from PBXShellScriptBuildPhase objects
        :param build_phase: PBXShellScriptBuildPhase object to be extracted from.
        :param target: parent Target.
        :return: A dictionary with the extracted build phase information.
        """
        phase_info = {}
        phase_info["type"] = "run_script"
        phase_info["name"] = build_phase.get("name", "Run Script")
        phase_info["shell_script"] = build_phase.shellScript
        phase_info["shell_path"] = build_phase.shellPath
        phase_info["input_paths"] = build_phase.inputPaths
        phase_info["output_paths"] = build_phase.outputPaths
        phase_info["runOnlyForDeploymentPostprocessing"] = (
            build_phase.runOnlyForDeploymentPostprocessing
        )
        return phase_info

    def _extract_copy_files(self, build_phase, target) -> dict:
        """
        Extracts a build phase copy files from PBXCopyFilesBuildPhase objects
        :param build_phase: PBXCopyFilesBuildPhase object to be extracted from.
        :param target: parent Target.
        :return: A dictionary with the extracted build phase information.
        """
        phase_info = {}
        phase_info["type"] = "copy_files"
        phase_info["name"] = build_phase.get("name", "Copy Files")
        phase_info["destination"] = build_phase.dstPath
        phase_info["subfolder"] = build_phase.dstSubfolderSpec
        return phase_info

    def _extract_build_configurations(self, configuration_list_id, target=None) -> list:
        """
         Extracts a build configurations array from an XCConfigurationList object
        :param configuration_list_id: A XCConfigurationList object id.
        :param target: parent Target.
        :return: A list of configuration objects.
        """
        if not configuration_list_id:
            return []

        config_list = self.xcode_project.objects[configuration_list_id]
        configurations = []
        for config_id in config_list.buildConfigurations:
            config = self.xcode_project.objects[config_id]
            config_data = {
                "name": config.name,
                "settings": config.buildSettings,
            }

            # Look for the xconfig file
            if "baseConfigurationReference" in config:
                xconfig_file = self.xcode_project.objects[
                    config.baseConfigurationReference
                ]
                config_data["xconfig_file"] = {
                    "path": xconfig_file.path,
                    "tree": xconfig_file.sourceTree,
                }
            configurations.append(config_data)

        return configurations

    def convert_to_tuist(self) -> None:
        """
        Performs the conversion to Tuist configuration files.
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing project capabilities...", total=None)
            self._analyze_pbxproj_capabilities()

            progress.update(task, description="Extracting project settings...")
            self._extract_project_settings()

            progress.update(task, description="Processing targets...")
            for target in self.xcode_project.objects.get_targets():
                self._extract_target_settings(target)

            progress.update(task, description="Generating Tuist files...")
            self._generate_tuist_files()

    def _generate_tuist_files(self) -> None:
        """Generates Tuist configuration files in the output directory."""
        try:
            # Create Project.swift - now we only have one project
            project = self.tuist_data["projects"][0]
            print("[cyan]Project data:[/cyan]")
            print(project)
            project_swift_content = self._generate_project_swift(project)
            project_swift_path = self.output_path / "Project.swift"
            project_swift_path.write_text(project_swift_content)

            # Create Tuist.swift
            tuist_swift_content = """import ProjectDescription

let tuist = Tuist()
"""
            tuist_swift_path = self.output_path / "Tuist.swift"
            tuist_swift_path.write_text(tuist_swift_content)

            # Create Tuist/Package.swift if there are package dependencies
            has_package_deps = any(
                any(d["type"] == "package" for d in target.get("dependencies", []))
                for project in self.tuist_data["projects"]
                for target in project.get("targets", [])
            )

            if has_package_deps:
                package_dir = self.output_path / "Tuist"
                package_dir.mkdir(exist_ok=True)

                package_swift_content = """// swift-tools-version: 5.9
import PackageDescription

#if TUIST
    import ProjectDescription

    let packageSettings = PackageSettings(
        productTypes: [:]
    )
#endif

let package = Package(
    name: "Dependencies",
    dependencies: []  // TODO: Add package dependencies
)
"""
                package_swift_path = package_dir / "Package.swift"
                package_swift_path.write_text(package_swift_content)

            console.print("[green]Successfully generated Tuist configuration!")
            console.print(f"Output directory: {self.output_path}")

            # Print generated files
            console.print("\nGenerated files:")
            console.print(f"- {project_swift_path}")
            console.print(f"- {tuist_swift_path}")
            if has_package_deps:
                console.print(f"- {package_swift_path}")

        except Exception as e:
            console.print(f"[red]Error generating Tuist files:[/red] {str(e)}")
            raise

    def _generate_project_swift(self, project_data: Dict[str, Any]) -> str:
        """
        Generates the contents of Project.swift file.

        Args:
            project_data: Dictionary containing project configuration
        Returns:
            String containing the Project.swift file contents
        """
        targets_str = []

        for target in project_data.get("targets", []):
            # Convert sources to Tuist format
            sources = [f'"{s["path"]}"' for s in target.get("sources", [])]
            sources_str = (
                f"[\n            {','.join(sources)}\n        ]" if sources else "[]"
            )

            # Convert resources to Tuist format
            resources = [f'"{r["path"]}"' for r in target.get("resources", [])]
            resources_str = (
                f"[\n            {','.join(resources)}\n        ]"
                if resources
                else "[]"
            )

            # Convert dependencies to Tuist format
            dependencies = []
            for dep in target.get("dependencies", []):
                if dep["type"] == "target":
                    dependencies.append(f'.target(name: "{dep["name"]}")')
                elif dep["type"] == "package":
                    dependencies.append(f'.external(name: "{dep["name"]}")')

            dependencies_str = (
                f"[\n            {','.join(dependencies)}\n        ]"
                if dependencies
                else "[]"
            )

            # Generate target configuration
            target_str = f"""        .target(
                name: "{target["name"]}",
                destinations: [.iOS],
                product: {self._convert_product_type(target.get("product"))},
                bundleId: "{target.get("bundleId", "io.tuist." + target["name"])}",
                infoPlist: .default,
                sources: {sources_str},
                resources: {resources_str},
                dependencies: {dependencies_str}
            )"""
            targets_str.append(target_str)

        # Generate Project.swift content
        project_swift = f"""import ProjectDescription

let project = Project(
    name: "{project_data.get("name", "TuistProject")}",
    organizationName: "{project_data.get("organizationalName", "")}",
    targets: [
{',\n'.join(targets_str)}
    ]
)
"""
        return project_swift

    def _convert_product_type(self, xcode_product_type: Optional[str]) -> str:
        """
        Converts Xcode product type to Tuist product type.

        Args:
            xcode_product_type: Xcode product type string
        Returns:
            Tuist product type string
        """
        product_type_mapping = {
            "com.apple.product-type.application": ".app",
            "com.apple.product-type.framework": ".framework",
            "com.apple.product-type.library.static": ".staticLibrary",
            "com.apple.product-type.bundle.unit-test": ".unitTests",
            "com.apple.product-type.bundle.ui-testing": ".uiTests",
            "com.apple.product-type.library.dynamic": ".dynamicLibrary",
            None: ".app",  # Default to .app if not specified
        }

        return product_type_mapping.get(xcode_product_type, ".app")


def parse_args() -> ConversionConfig:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Xcode project to Tuist configuration"
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to .xcodeproj file or directory",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Directory where Tuist files will be generated",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()
    return ConversionConfig(
        input_path=args.input_path,
        output_path=args.output_path,
        verbose=args.verbose,
    )


def main() -> None:
    """Main entry point for the CLI tool."""
    try:
        config = parse_args()
        if config.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        converter = PBXToTuistConverter(config)
        converter.convert_to_tuist()

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        logger.debug(
            f"Full traceback:\n{''.join(traceback.format_tb(e.__traceback__))}"
        )
        exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] An unexpected error occurred: {str(e)}")
        logger.debug(
            f"Full traceback:\n{''.join(traceback.format_tb(e.__traceback__))}"
        )
        exit(1)


if __name__ == "__main__":
    main()
