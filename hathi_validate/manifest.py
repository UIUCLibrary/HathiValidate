import collections
import os
import typing

PackageManifest = \
    collections.namedtuple("PackageManifest", ("source", "item_types"))


class PackageManifestDirector:

    def __init__(self) -> None:
        self._packages: typing.List[PackageManifest] = []

    #     self.source = source

    def build_manifest(self) -> typing.List[PackageManifest]:
        return self._packages

    def add_package(self, path):
        package = PackageManifestBuilder(path)
        self._packages.append(package)
        return package


class PackageManifestBuilder:
    def __init__(self, source):
        self._files: typing.Dict[str, set] = collections.defaultdict(set)
        self.source = source

    def add_file(self, file):
        base_namen = os.path.basename(file)
        _, ext = os.path.splitext(base_namen)
        self._files[ext].add(file)

    @property
    def files(self) -> typing.Dict[str, set]:
        return dict(self._files)


def get_report_as_str(manifest, width):
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
