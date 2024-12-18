from __future__ import annotations

from types import SimpleNamespace

import module_qc_tools as mqt
import pytest
from module_qc_tools.measurements.adc_calibration import run
from module_qc_tools.utils.misc import (
    load_config,
)
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr


@pytest.fixture()
def config_emulator():
    return load_config(
        mqt.data / "configs" / "emulator_merged_vmux.json", test_type="ADC_CALIBRATION"
    )


@pytest.fixture()
def hardware(config_emulator):
    return SimpleNamespace(
        ps=power_supply(config_emulator["power_supply"]),
        yr=yarr(config_emulator["yarr"]),
    )


def test_issue114(config_emulator, hardware):
    layer = "L1"

    hardware.ps.set(v=config_emulator["v_max"], i=config_emulator["i_config"][layer])

    data = run(config_emulator, hardware.ps, hardware.yr, layer, False)
    metadata = data[0].get_meta_data()

    assert "ChipConfigs" in metadata
    assert "RD53B" in metadata["ChipConfigs"]
    assert "GlobalConfig" in metadata["ChipConfigs"]["RD53B"]
    assert "InjVcalRange" in metadata["ChipConfigs"]["RD53B"]["GlobalConfig"]
