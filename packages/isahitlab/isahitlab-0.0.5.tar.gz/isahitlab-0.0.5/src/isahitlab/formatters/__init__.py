# SPDX-FileCopyrightText: 2024-present Benjamin Piogé <benjamin@isahit.com>
#
# SPDX-License-Identifier: MIT
from typing import Dict
from isahitlab.domain.task import TaskCompatibilityMode
from isahitlab.domain.export import ExportFormat
from .lab_to_kili_formatter import LabToKiliFormatter
from .kili_to_lab_formatter import KiliToLabFormatter
from .lab_to_yolo_formatter import LabToYoloFormatter
from .base import BaseFormatter

def get_compatibility_formatter(from_mode : TaskCompatibilityMode, to_mode : TaskCompatibilityMode, project_configuration : Dict) -> BaseFormatter :
    """Factory"""
    if from_mode == "lab" and to_mode == "kili":
        return LabToKiliFormatter(project_configuration)
    if from_mode == "kili" and to_mode == "lab":
        return KiliToLabFormatter(project_configuration)
    
def get_export_formatter(from_format : ExportFormat, to_format : ExportFormat, project_configuration : Dict, options: Dict = {}) -> BaseFormatter :
    """Factory"""
    if from_format == "lab" and to_format == "kili":
        return LabToKiliFormatter(project_configuration, options)
    if from_format == "lab" and to_format == "yolo":
        return LabToYoloFormatter(project_configuration, options)
