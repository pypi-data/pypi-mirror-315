# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Parser for Ascend CANN profiling data."""
import os
import glob
from typing import Dict, Optional

import numpy as np

from mindspore import log as logger
from mindspore.profiler.analysis.parser.base_parser import BaseParser
from mindspore.profiler.common.file_manager import FileManager
from mindspore.profiler.common.ascend_msprof_exporter import AscendMsprofExporter


class AscendMsprofParser(BaseParser):
    """Parser for MindSpore profiling data on Ascend platform."""

    _MSPROF_TIMELINE_FILE_PATTERN = ["msprof_[0-9]*.json", "msprof_slice_*.json"]
    _OP_SUMMARY_FILE_PATTERN = "op_summary_*.csv"

    def __init__(self, next_parser: Optional[BaseParser] = None, **kwargs):
        """Initialize AscendMsprofParser."""
        super().__init__(next_parser)
        self._kwargs = kwargs
        self._msprof_profile_output_path = self._kwargs.get(
            "msprof_profile_output_path"
        )
        self.op_summary = None
        self.op_summary_headers = None
        self.msprof_timeline = []

    def _parse(self, data=None) -> Dict:
        """Parse profiling data and update the input dictionary.

        Args:
            data (Dict, optional): Input data dictionary. Defaults to None.

        Returns:
            Dict: Updated data with op_summary, headers and timeline information.
        """
        if data is None:
            data = {}
        AscendMsprofExporter(**self._kwargs).export()
        self._parse_op_summary()
        self._parse_msprof_timeline()
        data.update(
            {
                "op_summary": self.op_summary,
                "op_summary_headers": self.op_summary_headers,
                "msprof_timeline": self.msprof_timeline,
            }
        )
        return data

    def _parse_op_summary(self):
        """Parse operation summary data from CSV files.

        Raises:
            RuntimeError: If no op summary files are found or read file failed.
        """
        file_path_list = glob.glob(
            os.path.join(
                self._msprof_profile_output_path, self._OP_SUMMARY_FILE_PATTERN
            )
        )
        if not file_path_list:
            logger.error(
                f"Failed to find op_summary_*.csv in directory: {self._msprof_profile_output_path}"
            )
            return

        for file_path in file_path_list:
            csv_data_np, self.op_summary_headers = FileManager.read_csv_file_as_numpy(
                file_path=file_path, extern_headers=["Step ID"]
            )
            if self.op_summary is None:
                self.op_summary = csv_data_np
            else:
                self.op_summary = np.concatenate([self.op_summary, csv_data_np], axis=0)

    def _parse_msprof_timeline(self) -> None:
        """Parse msprof timeline data from JSON files.

        Raises:
            RuntimeError: If no msprof JSON files are found in the specified directory.
        """
        file_path_list = []
        for pattern in self._MSPROF_TIMELINE_FILE_PATTERN:
            file_path_list.extend(glob.glob(os.path.join(self._msprof_profile_output_path, pattern)))

        if not file_path_list:
            raise RuntimeError(
                f"Failed to find msprof JSON files in directory: {self._msprof_profile_output_path}"
            )
        for file_path in file_path_list:
            self._process_timeline_file(file_path)
        if not self.msprof_timeline:
            logger.error(
                "Failed to collect msprof timeline data"
            )

    def _process_timeline_file(self, file_path: str) -> None:
        """Process a single timeline JSON file.

        Args:
            file_path (str): Path to the JSON file to process.
        """
        try:
            timeline_data = FileManager.read_json_file(file_path)
            if timeline_data:
                self.msprof_timeline.extend(timeline_data)
            else:
                logger.warning(
                    f"Msporf timeline data in {file_path} is empty."
                )
        except RuntimeError as err:
            logger.error(
                f"Failed to read file: {file_path}. Error: {str(err)}"
            )
