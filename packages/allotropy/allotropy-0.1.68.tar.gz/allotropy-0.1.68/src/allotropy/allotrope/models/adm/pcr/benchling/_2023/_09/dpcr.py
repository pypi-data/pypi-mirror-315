# generated by datamodel-codegen:
#   filename:  dpcr.schema.json
#   timestamp: 2024-11-20T16:32:39+00:00

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from allotropy.allotrope.models.shared.definitions.custom import (
    TQuantityValueDegreeCelsius,
    TQuantityValueMicroliter,
    TQuantityValueNumber,
    TQuantityValueNumberPerMicroliter,
    TQuantityValueSecondTime,
    TQuantityValueUnitless,
)
from allotropy.allotrope.models.shared.definitions.definitions import (
    TDatacubeData,
    TDatacubeStructure,
    TDateTimeValue,
    TQuantityValue,
    TStringValue,
)


class ExperimentType(Enum):
    dPCR_experiment = "dPCR experiment"


class ContainerType(Enum):
    reactor = "reactor"
    controlled_lab_reactor = "controlled lab reactor"
    tube = "tube"
    well_plate = "well plate"
    differential_scanning_calorimetry_pan = "differential scanning calorimetry pan"
    qPCR_reaction_block = "qPCR reaction block"
    vial_rack = "vial rack"
    pan = "pan"
    reservoir = "reservoir"
    array_card_block = "array card block"
    capillary = "capillary"
    disintegration_apparatus_basket = "disintegration apparatus basket"
    jar = "jar"
    container = "container"
    tray = "tray"
    basket = "basket"
    cell_holder = "cell holder"


@dataclass(kw_only=True)
class DataSourceDocumentItem:
    data_source_identifier: TStringValue | None = None
    data_source_feature: TStringValue | None = None


@dataclass(kw_only=True)
class DataSourceAggregateDocument:
    data_source_document: list[DataSourceDocumentItem] | None = None


@dataclass(kw_only=True)
class DeviceSystemDocument:
    device_identifier: TStringValue
    asset_management_identifier: TStringValue | None = None
    model_number: TStringValue | None = None
    device_serial_number: TStringValue | None = None
    firmware_version: TStringValue | None = None
    description: TStringValue | None = None
    brand_name: TStringValue | None = None
    product_manufacturer: TStringValue | None = None


@dataclass(kw_only=True)
class DataSystemDocument:
    data_system_instance_identifier: TStringValue | None = None
    file_name: TStringValue | None = None
    UNC_path: TStringValue | None = None
    software_name: TStringValue | None = None
    software_version: TStringValue | None = None
    ASM_converter_name: TStringValue | None = None
    ASM_converter_version: TStringValue | None = None


@dataclass(kw_only=True)
class ErrorDocumentItem:
    error: TStringValue
    error_feature: TStringValue | None = None


@dataclass(kw_only=True)
class ErrorAggregateDocument:
    error_document: list[ErrorDocumentItem]


@dataclass(kw_only=True)
class SampleDocument:
    sample_identifier: TStringValue
    batch_identifier: TStringValue | None = None
    sample_role_type: TStringValue | None = None
    well_location_identifier: TStringValue | None = None
    well_plate_identifier: TStringValue | None = None


@dataclass(kw_only=True)
class DeviceControlDocumentItem:
    device_type: TStringValue
    device_identifier: TStringValue | None = None
    detection_type: TStringValue | None = None
    measurement_method_identifier: TStringValue | None = None
    total_cycle_number_setting: TQuantityValueNumber | None = None
    denaturing_temperature_setting: TQuantityValueDegreeCelsius | None = None
    denaturing_time_setting: TQuantityValueSecondTime | None = None
    annealing_temperature_setting: TQuantityValueDegreeCelsius | None = None
    annealing_time_setting: TQuantityValueSecondTime | None = None
    extension_temperature_setting: TQuantityValueDegreeCelsius | None = None
    extension_time_setting: TQuantityValueSecondTime | None = None
    PCR_detection_chemistry: TStringValue | None = None
    reporter_dye_setting: TStringValue | None = None
    quencher_dye_setting: TStringValue | None = None
    passive_reference_dye_setting: TStringValue | None = None


@dataclass(kw_only=True)
class DeviceControlAggregateDocument:
    device_control_document: list[DeviceControlDocumentItem]


@dataclass(kw_only=True)
class DataProcessingDocument:
    flourescence_intensity_threshold_setting: TQuantityValueUnitless | None = None
    reference_DNA_description: TStringValue | None = None
    reference_DNA_copy_number_setting: TQuantityValueNumber | None = None


@dataclass(kw_only=True)
class ProcessedDataDocumentItem:
    number_concentration: TQuantityValueNumberPerMicroliter
    positive_partition_count: TQuantityValueNumber
    data_processing_document: DataProcessingDocument | None = None
    negative_partition_count: TQuantityValueNumber | None = None
    confidence_interval__95__: TQuantityValueNumber | None = None


@dataclass(kw_only=True)
class ProcessedDataAggregateDocument:
    processed_data_document: list[ProcessedDataDocumentItem]


@dataclass(kw_only=True)
class CalculatedDataDocumentItem:
    calculated_data_identifier: TStringValue | None = None
    data_source_aggregate_document: DataSourceAggregateDocument | None = None
    data_processing_document: DataProcessingDocument | None = None
    calculated_data_name: TStringValue | None = None
    calculated_data_description: TStringValue | None = None
    calculated_datum: TQuantityValue | None = None


@dataclass(kw_only=True)
class TCalculatedDataAggregateDocument:
    calculated_data_document: list[CalculatedDataDocumentItem] | None = None


@dataclass(kw_only=True)
class ReporterDyeDataCube:
    label: str | None = None
    cube_structure: TDatacubeStructure | None = None
    data: TDatacubeData | None = None


@dataclass(kw_only=True)
class PassiveReferenceDyeDataCube:
    label: str | None = None
    cube_structure: TDatacubeStructure | None = None
    data: TDatacubeData | None = None


@dataclass(kw_only=True)
class MeasurementDocumentItem:
    measurement_identifier: TStringValue
    measurement_time: TDateTimeValue
    target_DNA_description: TStringValue
    sample_document: SampleDocument
    device_control_aggregate_document: DeviceControlAggregateDocument
    total_partition_count: TQuantityValueNumber
    processed_data_aggregate_document: ProcessedDataAggregateDocument
    error_aggregate_document: ErrorAggregateDocument | None = None
    reporter_dye_data_cube: ReporterDyeDataCube | None = None
    passive_reference_dye_data_cube: PassiveReferenceDyeDataCube | None = None


@dataclass(kw_only=True)
class MeasurementAggregateDocument:
    plate_well_count: TQuantityValueNumber
    measurement_document: list[MeasurementDocumentItem]
    analytical_method_identifier: TStringValue | None = None
    experimental_data_identifier: TStringValue | None = None
    experiment_type: ExperimentType | None = None
    container_type: ContainerType | None = None
    well_volume: TQuantityValueMicroliter | None = None
    error_aggregate_document: ErrorAggregateDocument | None = None


@dataclass(kw_only=True)
class DPCRDocumentItem:
    measurement_aggregate_document: MeasurementAggregateDocument
    analyst: TStringValue | None = None
    submitter: TStringValue | None = None
    calculated_data_aggregate_document: TCalculatedDataAggregateDocument | None = None


@dataclass(kw_only=True)
class DPCRAggregateDocument:
    device_system_document: DeviceSystemDocument
    dPCR_document: list[DPCRDocumentItem]
    data_system_document: DataSystemDocument | None = None
    calculated_data_aggregate_document: TCalculatedDataAggregateDocument | None = None


@dataclass(kw_only=True)
class Model:
    manifest: str = (
        "http://purl.allotrope.org/manifests/pcr/BENCHLING/2023/09/dpcr.manifest"
    )
    dPCR_aggregate_document: DPCRAggregateDocument | None = None
