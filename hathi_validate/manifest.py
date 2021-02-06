import collections
import os
import typing
from typing import Set, List

PackageManifest = \
    collections.namedtuple("PackageManifest", ("source", "item_types"))


class PackageManifestDirector:

    def __init__(self) -> None:
        self._packages: typing.List["PackageManifestBuilder"] = []

    #     self.source = source

    def build_manifest(self) -> typing.List["PackageManifestBuilder"]:
        return self._packages

    def add_package(self, path: str) -> "PackageManifestBuilder":
        package = PackageManifestBuilder(path)
        self._packages.append(package)
        return package


class PackageManifestBuilder:
    def __init__(self, source: str) -> None:
        self._files: typing.Dict[str, Set[str]] = collections.defaultdict(set)
        self.source = source

    def add_file(self, file: str) -> None:
        base_name = os.path.basename(file)
        _, ext = os.path.splitext(base_name)
        self._files[ext].add(file)

    @property
    def files(self) -> typing.Dict[str, Set[str]]:
        return dict(self._files)


def get_report_as_str(manifest: List[PackageManifestBuilder],
                      width: int) -> str:

    line_sep = "=" * width
    title = "Manifest"
    header = f"{line_sep}" \
             f"\n{title}" \
             f"\n{line_sep}"

    item_messages = []

    for item in manifest:
        item_source = item.source

        component_messages = []
        for ext, files in sorted(item.files.items()):
            component_messages.append(f" * {ext}: {len(files)} file(s)")
        component_messages_text = "\n".join(component_messages)
        item_message = f"{item_source}" \
                       f"\n{component_messages_text}" \
                       f"\n"
        item_messages.append(item_message)

    item_messages_text = "\n".join(item_messages)

    report = f"{header}" \
             f"\n" \
             f"\n{item_messages_text}" \
             f"\n{line_sep}"
    return report
