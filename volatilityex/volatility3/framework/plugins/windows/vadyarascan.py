# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#

import logging
from typing import Iterable, List, Tuple

from volatility3.framework import interfaces, renderers
from volatility3.framework.configuration import requirements
from volatility3.framework.renderers import format_hints
from volatility3.plugins import yarascan
from volatility3.plugins.windows import pslist

vollog = logging.getLogger(__name__)


class VadYaraScan(interfaces.plugins.PluginInterface):
    """Scans all the Virtual Address Descriptor memory maps using yara."""

    _required_framework_version = (2, 4, 0)
    _version = (1, 1, 1)

    @classmethod
    def get_requirements(cls) -> List[interfaces.configuration.RequirementInterface]:
        # create a list of requirements for vadyarascan
        vadyarascan_requirements = [
            requirements.ModuleRequirement(
                name="kernel",
                description="Windows kernel",
                architectures=["Intel32", "Intel64"],
            ),
            requirements.PluginRequirement(
                name="pslist", plugin=pslist.PsList, version=(2, 0, 0)
            ),
            requirements.VersionRequirement(
                name="yarascanner", component=yarascan.YaraScanner, version=(2, 0, 0)
            ),
            requirements.PluginRequirement(
                name="yarascan", plugin=yarascan.YaraScan, version=(2, 0, 0)
            ),
            requirements.ListRequirement(
                name="pid",
                element_type=int,
                description="Process IDs to include (all other processes are excluded)",
                optional=True,
            ),
        ]

        # get base yarascan requirements for command line options
        yarascan_requirements = yarascan.YaraScan.get_yarascan_option_requirements()

        # return the combined requirements
        return yarascan_requirements + vadyarascan_requirements

    def _generator(self):
        kernel = self.context.modules[self.config["kernel"]]

        rules = yarascan.YaraScan.process_yara_options(dict(self.config))

        filter_func = pslist.PsList.create_pid_filter(self.config.get("pid", None))

        sanity_check = 1024 * 1024 * 1024  # 1 GB

        for task in pslist.PsList.list_processes(
            context=self.context,
            layer_name=kernel.layer_name,
            symbol_table=kernel.symbol_table_name,
            filter_func=filter_func,
        ):
            layer_name = task.add_process_layer()
            layer = self.context.layers[layer_name]

            max_vad_size = 0
            vad_maps_to_scan = []

            for start, size in self.get_vad_maps(task):
                if size > sanity_check:
                    vollog.debug(
                        f"VAD at 0x{start:x} over sanity-check size, not scanning"
                    )
                    continue
                max_vad_size = max(max_vad_size, size)
                vad_maps_to_scan.append((start, size))

            if not vad_maps_to_scan:
                vollog.warning(
                    f"No VADs were found for task {task.UniqueProcessID}, not scanning"
                )
                continue

            scanner = yarascan.YaraScanner(rules=rules)
            scanner.chunk_size = max_vad_size

            # scan the VAD data (in one contiguous block) with the yarascanner
            for start, size in vad_maps_to_scan:
                for offset, rule_name, name, value in scanner(
                    layer.read(start, size, pad=True), start
                ):
                    yield 0, (
                        format_hints.Hex(offset),
                        task.UniqueProcessId,
                        rule_name,
                        name,
                        value,
                    )

    @staticmethod
    def get_vad_maps(
        task: interfaces.objects.ObjectInterface,
    ) -> Iterable[Tuple[int, int]]:
        """Creates a map of start/end addresses within a virtual address
        descriptor tree.

        Args:
            task: The EPROCESS object of which to traverse the vad tree

        Returns:
            An iterable of tuples containing start and size for each descriptor
        """
        vad_root = task.get_vad_root()
        for vad in vad_root.traverse():
            yield (vad.get_start(), vad.get_size())

    def run(self):
        return renderers.TreeGrid(
            [
                ("Offset", format_hints.Hex),
                ("PID", int),
                ("Rule", str),
                ("Component", str),
                ("Value", bytes),
            ],
            self._generator(),
        )
