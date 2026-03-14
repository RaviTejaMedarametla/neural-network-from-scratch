"""Auto-generated deterministic design points for hardware sweeps."""

from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class DesignPoint:
    name: str
    mac_units: int
    frequency_ghz: float
    bandwidth_gbps: float
    sram_kb: int
    voltage_v: float

def score_point(p: DesignPoint, model_flops: float, model_bytes: float) -> dict:
    peak_ops = p.mac_units * p.frequency_ghz * 2e9
    bw = p.bandwidth_gbps * 1e9 / 8.0
    t_compute = model_flops / max(peak_ops, 1.0)
    t_mem = model_bytes / max(bw, 1.0)
    latency = max(t_compute, t_mem)
    energy = model_flops * (0.4e-12 * (p.voltage_v/0.8)**2) + model_bytes * (3.2e-12 * (p.voltage_v/0.8)**2)
    throughput = 1.0 / max(latency, 1e-12)
    return {"latency_s": latency, "energy_j": energy, "throughput": throughput}

def point_0() -> DesignPoint:
    return DesignPoint("point_0", mac_units=128, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=128, voltage_v=0.65)

def point_1() -> DesignPoint:
    return DesignPoint("point_1", mac_units=160, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=192, voltage_v=0.68)

def point_2() -> DesignPoint:
    return DesignPoint("point_2", mac_units=192, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=256, voltage_v=0.71)

def point_3() -> DesignPoint:
    return DesignPoint("point_3", mac_units=224, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=320, voltage_v=0.74)

def point_4() -> DesignPoint:
    return DesignPoint("point_4", mac_units=256, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=384, voltage_v=0.77)

def point_5() -> DesignPoint:
    return DesignPoint("point_5", mac_units=288, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=448, voltage_v=0.80)

def point_6() -> DesignPoint:
    return DesignPoint("point_6", mac_units=320, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=512, voltage_v=0.83)

def point_7() -> DesignPoint:
    return DesignPoint("point_7", mac_units=352, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=576, voltage_v=0.86)

def point_8() -> DesignPoint:
    return DesignPoint("point_8", mac_units=384, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=640, voltage_v=0.89)

def point_9() -> DesignPoint:
    return DesignPoint("point_9", mac_units=416, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=704, voltage_v=0.92)

def point_10() -> DesignPoint:
    return DesignPoint("point_10", mac_units=448, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=768, voltage_v=0.65)

def point_11() -> DesignPoint:
    return DesignPoint("point_11", mac_units=480, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=832, voltage_v=0.68)

def point_12() -> DesignPoint:
    return DesignPoint("point_12", mac_units=512, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=896, voltage_v=0.71)

def point_13() -> DesignPoint:
    return DesignPoint("point_13", mac_units=544, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=960, voltage_v=0.74)

def point_14() -> DesignPoint:
    return DesignPoint("point_14", mac_units=576, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.77)

def point_15() -> DesignPoint:
    return DesignPoint("point_15", mac_units=608, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.80)

def point_16() -> DesignPoint:
    return DesignPoint("point_16", mac_units=640, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=128, voltage_v=0.83)

def point_17() -> DesignPoint:
    return DesignPoint("point_17", mac_units=672, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=192, voltage_v=0.86)

def point_18() -> DesignPoint:
    return DesignPoint("point_18", mac_units=704, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=256, voltage_v=0.89)

def point_19() -> DesignPoint:
    return DesignPoint("point_19", mac_units=736, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=320, voltage_v=0.92)

def point_20() -> DesignPoint:
    return DesignPoint("point_20", mac_units=768, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=384, voltage_v=0.65)

def point_21() -> DesignPoint:
    return DesignPoint("point_21", mac_units=800, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=448, voltage_v=0.68)

def point_22() -> DesignPoint:
    return DesignPoint("point_22", mac_units=832, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=512, voltage_v=0.71)

def point_23() -> DesignPoint:
    return DesignPoint("point_23", mac_units=864, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=576, voltage_v=0.74)

def point_24() -> DesignPoint:
    return DesignPoint("point_24", mac_units=896, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=640, voltage_v=0.77)

def point_25() -> DesignPoint:
    return DesignPoint("point_25", mac_units=928, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=704, voltage_v=0.80)

def point_26() -> DesignPoint:
    return DesignPoint("point_26", mac_units=960, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=768, voltage_v=0.83)

def point_27() -> DesignPoint:
    return DesignPoint("point_27", mac_units=992, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=832, voltage_v=0.86)

def point_28() -> DesignPoint:
    return DesignPoint("point_28", mac_units=1024, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=896, voltage_v=0.89)

def point_29() -> DesignPoint:
    return DesignPoint("point_29", mac_units=1056, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=960, voltage_v=0.92)

def point_30() -> DesignPoint:
    return DesignPoint("point_30", mac_units=1088, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.65)

def point_31() -> DesignPoint:
    return DesignPoint("point_31", mac_units=1120, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.68)

def point_32() -> DesignPoint:
    return DesignPoint("point_32", mac_units=128, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=128, voltage_v=0.71)

def point_33() -> DesignPoint:
    return DesignPoint("point_33", mac_units=160, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=192, voltage_v=0.74)

def point_34() -> DesignPoint:
    return DesignPoint("point_34", mac_units=192, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=256, voltage_v=0.77)

def point_35() -> DesignPoint:
    return DesignPoint("point_35", mac_units=224, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=320, voltage_v=0.80)

def point_36() -> DesignPoint:
    return DesignPoint("point_36", mac_units=256, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=384, voltage_v=0.83)

def point_37() -> DesignPoint:
    return DesignPoint("point_37", mac_units=288, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=448, voltage_v=0.86)

def point_38() -> DesignPoint:
    return DesignPoint("point_38", mac_units=320, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=512, voltage_v=0.89)

def point_39() -> DesignPoint:
    return DesignPoint("point_39", mac_units=352, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=576, voltage_v=0.92)

def point_40() -> DesignPoint:
    return DesignPoint("point_40", mac_units=384, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=640, voltage_v=0.65)

def point_41() -> DesignPoint:
    return DesignPoint("point_41", mac_units=416, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=704, voltage_v=0.68)

def point_42() -> DesignPoint:
    return DesignPoint("point_42", mac_units=448, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=768, voltage_v=0.71)

def point_43() -> DesignPoint:
    return DesignPoint("point_43", mac_units=480, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=832, voltage_v=0.74)

def point_44() -> DesignPoint:
    return DesignPoint("point_44", mac_units=512, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=896, voltage_v=0.77)

def point_45() -> DesignPoint:
    return DesignPoint("point_45", mac_units=544, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=960, voltage_v=0.80)

def point_46() -> DesignPoint:
    return DesignPoint("point_46", mac_units=576, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.83)

def point_47() -> DesignPoint:
    return DesignPoint("point_47", mac_units=608, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.86)

def point_48() -> DesignPoint:
    return DesignPoint("point_48", mac_units=640, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=128, voltage_v=0.89)

def point_49() -> DesignPoint:
    return DesignPoint("point_49", mac_units=672, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=192, voltage_v=0.92)

def point_50() -> DesignPoint:
    return DesignPoint("point_50", mac_units=704, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=256, voltage_v=0.65)

def point_51() -> DesignPoint:
    return DesignPoint("point_51", mac_units=736, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=320, voltage_v=0.68)

def point_52() -> DesignPoint:
    return DesignPoint("point_52", mac_units=768, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=384, voltage_v=0.71)

def point_53() -> DesignPoint:
    return DesignPoint("point_53", mac_units=800, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=448, voltage_v=0.74)

def point_54() -> DesignPoint:
    return DesignPoint("point_54", mac_units=832, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=512, voltage_v=0.77)

def point_55() -> DesignPoint:
    return DesignPoint("point_55", mac_units=864, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=576, voltage_v=0.80)

def point_56() -> DesignPoint:
    return DesignPoint("point_56", mac_units=896, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=640, voltage_v=0.83)

def point_57() -> DesignPoint:
    return DesignPoint("point_57", mac_units=928, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=704, voltage_v=0.86)

def point_58() -> DesignPoint:
    return DesignPoint("point_58", mac_units=960, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=768, voltage_v=0.89)

def point_59() -> DesignPoint:
    return DesignPoint("point_59", mac_units=992, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=832, voltage_v=0.92)

def point_60() -> DesignPoint:
    return DesignPoint("point_60", mac_units=1024, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=896, voltage_v=0.65)

def point_61() -> DesignPoint:
    return DesignPoint("point_61", mac_units=1056, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=960, voltage_v=0.68)

def point_62() -> DesignPoint:
    return DesignPoint("point_62", mac_units=1088, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.71)

def point_63() -> DesignPoint:
    return DesignPoint("point_63", mac_units=1120, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.74)

def point_64() -> DesignPoint:
    return DesignPoint("point_64", mac_units=128, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=128, voltage_v=0.77)

def point_65() -> DesignPoint:
    return DesignPoint("point_65", mac_units=160, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=192, voltage_v=0.80)

def point_66() -> DesignPoint:
    return DesignPoint("point_66", mac_units=192, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=256, voltage_v=0.83)

def point_67() -> DesignPoint:
    return DesignPoint("point_67", mac_units=224, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=320, voltage_v=0.86)

def point_68() -> DesignPoint:
    return DesignPoint("point_68", mac_units=256, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=384, voltage_v=0.89)

def point_69() -> DesignPoint:
    return DesignPoint("point_69", mac_units=288, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=448, voltage_v=0.92)

def point_70() -> DesignPoint:
    return DesignPoint("point_70", mac_units=320, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=512, voltage_v=0.65)

def point_71() -> DesignPoint:
    return DesignPoint("point_71", mac_units=352, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=576, voltage_v=0.68)

def point_72() -> DesignPoint:
    return DesignPoint("point_72", mac_units=384, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=640, voltage_v=0.71)

def point_73() -> DesignPoint:
    return DesignPoint("point_73", mac_units=416, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=704, voltage_v=0.74)

def point_74() -> DesignPoint:
    return DesignPoint("point_74", mac_units=448, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=768, voltage_v=0.77)

def point_75() -> DesignPoint:
    return DesignPoint("point_75", mac_units=480, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=832, voltage_v=0.80)

def point_76() -> DesignPoint:
    return DesignPoint("point_76", mac_units=512, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=896, voltage_v=0.83)

def point_77() -> DesignPoint:
    return DesignPoint("point_77", mac_units=544, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=960, voltage_v=0.86)

def point_78() -> DesignPoint:
    return DesignPoint("point_78", mac_units=576, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.89)

def point_79() -> DesignPoint:
    return DesignPoint("point_79", mac_units=608, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.92)

def point_80() -> DesignPoint:
    return DesignPoint("point_80", mac_units=640, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=128, voltage_v=0.65)

def point_81() -> DesignPoint:
    return DesignPoint("point_81", mac_units=672, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=192, voltage_v=0.68)

def point_82() -> DesignPoint:
    return DesignPoint("point_82", mac_units=704, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=256, voltage_v=0.71)

def point_83() -> DesignPoint:
    return DesignPoint("point_83", mac_units=736, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=320, voltage_v=0.74)

def point_84() -> DesignPoint:
    return DesignPoint("point_84", mac_units=768, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=384, voltage_v=0.77)

def point_85() -> DesignPoint:
    return DesignPoint("point_85", mac_units=800, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=448, voltage_v=0.80)

def point_86() -> DesignPoint:
    return DesignPoint("point_86", mac_units=832, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=512, voltage_v=0.83)

def point_87() -> DesignPoint:
    return DesignPoint("point_87", mac_units=864, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=576, voltage_v=0.86)

def point_88() -> DesignPoint:
    return DesignPoint("point_88", mac_units=896, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=640, voltage_v=0.89)

def point_89() -> DesignPoint:
    return DesignPoint("point_89", mac_units=928, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=704, voltage_v=0.92)

def point_90() -> DesignPoint:
    return DesignPoint("point_90", mac_units=960, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=768, voltage_v=0.65)

def point_91() -> DesignPoint:
    return DesignPoint("point_91", mac_units=992, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=832, voltage_v=0.68)

def point_92() -> DesignPoint:
    return DesignPoint("point_92", mac_units=1024, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=896, voltage_v=0.71)

def point_93() -> DesignPoint:
    return DesignPoint("point_93", mac_units=1056, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=960, voltage_v=0.74)

def point_94() -> DesignPoint:
    return DesignPoint("point_94", mac_units=1088, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.77)

def point_95() -> DesignPoint:
    return DesignPoint("point_95", mac_units=1120, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.80)

def point_96() -> DesignPoint:
    return DesignPoint("point_96", mac_units=128, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=128, voltage_v=0.83)

def point_97() -> DesignPoint:
    return DesignPoint("point_97", mac_units=160, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=192, voltage_v=0.86)

def point_98() -> DesignPoint:
    return DesignPoint("point_98", mac_units=192, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=256, voltage_v=0.89)

def point_99() -> DesignPoint:
    return DesignPoint("point_99", mac_units=224, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=320, voltage_v=0.92)

def point_100() -> DesignPoint:
    return DesignPoint("point_100", mac_units=256, frequency_ghz=0.600, bandwidth_gbps=128, sram_kb=384, voltage_v=0.65)

def point_101() -> DesignPoint:
    return DesignPoint("point_101", mac_units=288, frequency_ghz=0.650, bandwidth_gbps=144, sram_kb=448, voltage_v=0.68)

def point_102() -> DesignPoint:
    return DesignPoint("point_102", mac_units=320, frequency_ghz=0.700, bandwidth_gbps=160, sram_kb=512, voltage_v=0.71)

def point_103() -> DesignPoint:
    return DesignPoint("point_103", mac_units=352, frequency_ghz=0.750, bandwidth_gbps=176, sram_kb=576, voltage_v=0.74)

def point_104() -> DesignPoint:
    return DesignPoint("point_104", mac_units=384, frequency_ghz=0.800, bandwidth_gbps=192, sram_kb=640, voltage_v=0.77)

def point_105() -> DesignPoint:
    return DesignPoint("point_105", mac_units=416, frequency_ghz=0.850, bandwidth_gbps=208, sram_kb=704, voltage_v=0.80)

def point_106() -> DesignPoint:
    return DesignPoint("point_106", mac_units=448, frequency_ghz=0.900, bandwidth_gbps=224, sram_kb=768, voltage_v=0.83)

def point_107() -> DesignPoint:
    return DesignPoint("point_107", mac_units=480, frequency_ghz=0.950, bandwidth_gbps=240, sram_kb=832, voltage_v=0.86)

def point_108() -> DesignPoint:
    return DesignPoint("point_108", mac_units=512, frequency_ghz=1.000, bandwidth_gbps=256, sram_kb=896, voltage_v=0.89)

def point_109() -> DesignPoint:
    return DesignPoint("point_109", mac_units=544, frequency_ghz=1.050, bandwidth_gbps=272, sram_kb=960, voltage_v=0.92)

def point_110() -> DesignPoint:
    return DesignPoint("point_110", mac_units=576, frequency_ghz=1.100, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.65)

def point_111() -> DesignPoint:
    return DesignPoint("point_111", mac_units=608, frequency_ghz=1.150, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.68)

def point_112() -> DesignPoint:
    return DesignPoint("point_112", mac_units=640, frequency_ghz=1.200, bandwidth_gbps=320, sram_kb=128, voltage_v=0.71)

def point_113() -> DesignPoint:
    return DesignPoint("point_113", mac_units=672, frequency_ghz=1.250, bandwidth_gbps=336, sram_kb=192, voltage_v=0.74)

def point_114() -> DesignPoint:
    return DesignPoint("point_114", mac_units=704, frequency_ghz=1.300, bandwidth_gbps=352, sram_kb=256, voltage_v=0.77)

def point_115() -> DesignPoint:
    return DesignPoint("point_115", mac_units=736, frequency_ghz=1.350, bandwidth_gbps=368, sram_kb=320, voltage_v=0.80)

def point_116() -> DesignPoint:
    return DesignPoint("point_116", mac_units=768, frequency_ghz=1.400, bandwidth_gbps=384, sram_kb=384, voltage_v=0.83)

def point_117() -> DesignPoint:
    return DesignPoint("point_117", mac_units=800, frequency_ghz=1.450, bandwidth_gbps=400, sram_kb=448, voltage_v=0.86)

def point_118() -> DesignPoint:
    return DesignPoint("point_118", mac_units=832, frequency_ghz=1.500, bandwidth_gbps=416, sram_kb=512, voltage_v=0.89)

def point_119() -> DesignPoint:
    return DesignPoint("point_119", mac_units=864, frequency_ghz=1.550, bandwidth_gbps=432, sram_kb=576, voltage_v=0.92)

def point_120() -> DesignPoint:
    return DesignPoint("point_120", mac_units=896, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=640, voltage_v=0.65)

def point_121() -> DesignPoint:
    return DesignPoint("point_121", mac_units=928, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=704, voltage_v=0.68)

def point_122() -> DesignPoint:
    return DesignPoint("point_122", mac_units=960, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=768, voltage_v=0.71)

def point_123() -> DesignPoint:
    return DesignPoint("point_123", mac_units=992, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=832, voltage_v=0.74)

def point_124() -> DesignPoint:
    return DesignPoint("point_124", mac_units=1024, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=896, voltage_v=0.77)

def point_125() -> DesignPoint:
    return DesignPoint("point_125", mac_units=1056, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=960, voltage_v=0.80)

def point_126() -> DesignPoint:
    return DesignPoint("point_126", mac_units=1088, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.83)

def point_127() -> DesignPoint:
    return DesignPoint("point_127", mac_units=1120, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.86)

def point_128() -> DesignPoint:
    return DesignPoint("point_128", mac_units=128, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=128, voltage_v=0.89)

def point_129() -> DesignPoint:
    return DesignPoint("point_129", mac_units=160, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=192, voltage_v=0.92)

def point_130() -> DesignPoint:
    return DesignPoint("point_130", mac_units=192, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=256, voltage_v=0.65)

def point_131() -> DesignPoint:
    return DesignPoint("point_131", mac_units=224, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=320, voltage_v=0.68)

def point_132() -> DesignPoint:
    return DesignPoint("point_132", mac_units=256, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=384, voltage_v=0.71)

def point_133() -> DesignPoint:
    return DesignPoint("point_133", mac_units=288, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=448, voltage_v=0.74)

def point_134() -> DesignPoint:
    return DesignPoint("point_134", mac_units=320, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=512, voltage_v=0.77)

def point_135() -> DesignPoint:
    return DesignPoint("point_135", mac_units=352, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=576, voltage_v=0.80)

def point_136() -> DesignPoint:
    return DesignPoint("point_136", mac_units=384, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=640, voltage_v=0.83)

def point_137() -> DesignPoint:
    return DesignPoint("point_137", mac_units=416, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=704, voltage_v=0.86)

def point_138() -> DesignPoint:
    return DesignPoint("point_138", mac_units=448, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=768, voltage_v=0.89)

def point_139() -> DesignPoint:
    return DesignPoint("point_139", mac_units=480, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=832, voltage_v=0.92)

def point_140() -> DesignPoint:
    return DesignPoint("point_140", mac_units=512, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=896, voltage_v=0.65)

def point_141() -> DesignPoint:
    return DesignPoint("point_141", mac_units=544, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=960, voltage_v=0.68)

def point_142() -> DesignPoint:
    return DesignPoint("point_142", mac_units=576, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.71)

def point_143() -> DesignPoint:
    return DesignPoint("point_143", mac_units=608, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.74)

def point_144() -> DesignPoint:
    return DesignPoint("point_144", mac_units=640, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=128, voltage_v=0.77)

def point_145() -> DesignPoint:
    return DesignPoint("point_145", mac_units=672, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=192, voltage_v=0.80)

def point_146() -> DesignPoint:
    return DesignPoint("point_146", mac_units=704, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=256, voltage_v=0.83)

def point_147() -> DesignPoint:
    return DesignPoint("point_147", mac_units=736, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=320, voltage_v=0.86)

def point_148() -> DesignPoint:
    return DesignPoint("point_148", mac_units=768, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=384, voltage_v=0.89)

def point_149() -> DesignPoint:
    return DesignPoint("point_149", mac_units=800, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=448, voltage_v=0.92)

def point_150() -> DesignPoint:
    return DesignPoint("point_150", mac_units=832, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=512, voltage_v=0.65)

def point_151() -> DesignPoint:
    return DesignPoint("point_151", mac_units=864, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=576, voltage_v=0.68)

def point_152() -> DesignPoint:
    return DesignPoint("point_152", mac_units=896, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=640, voltage_v=0.71)

def point_153() -> DesignPoint:
    return DesignPoint("point_153", mac_units=928, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=704, voltage_v=0.74)

def point_154() -> DesignPoint:
    return DesignPoint("point_154", mac_units=960, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=768, voltage_v=0.77)

def point_155() -> DesignPoint:
    return DesignPoint("point_155", mac_units=992, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=832, voltage_v=0.80)

def point_156() -> DesignPoint:
    return DesignPoint("point_156", mac_units=1024, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=896, voltage_v=0.83)

def point_157() -> DesignPoint:
    return DesignPoint("point_157", mac_units=1056, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=960, voltage_v=0.86)

def point_158() -> DesignPoint:
    return DesignPoint("point_158", mac_units=1088, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.89)

def point_159() -> DesignPoint:
    return DesignPoint("point_159", mac_units=1120, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.92)

def point_160() -> DesignPoint:
    return DesignPoint("point_160", mac_units=128, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=128, voltage_v=0.65)

def point_161() -> DesignPoint:
    return DesignPoint("point_161", mac_units=160, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=192, voltage_v=0.68)

def point_162() -> DesignPoint:
    return DesignPoint("point_162", mac_units=192, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=256, voltage_v=0.71)

def point_163() -> DesignPoint:
    return DesignPoint("point_163", mac_units=224, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=320, voltage_v=0.74)

def point_164() -> DesignPoint:
    return DesignPoint("point_164", mac_units=256, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=384, voltage_v=0.77)

def point_165() -> DesignPoint:
    return DesignPoint("point_165", mac_units=288, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=448, voltage_v=0.80)

def point_166() -> DesignPoint:
    return DesignPoint("point_166", mac_units=320, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=512, voltage_v=0.83)

def point_167() -> DesignPoint:
    return DesignPoint("point_167", mac_units=352, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=576, voltage_v=0.86)

def point_168() -> DesignPoint:
    return DesignPoint("point_168", mac_units=384, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=640, voltage_v=0.89)

def point_169() -> DesignPoint:
    return DesignPoint("point_169", mac_units=416, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=704, voltage_v=0.92)

def point_170() -> DesignPoint:
    return DesignPoint("point_170", mac_units=448, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=768, voltage_v=0.65)

def point_171() -> DesignPoint:
    return DesignPoint("point_171", mac_units=480, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=832, voltage_v=0.68)

def point_172() -> DesignPoint:
    return DesignPoint("point_172", mac_units=512, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=896, voltage_v=0.71)

def point_173() -> DesignPoint:
    return DesignPoint("point_173", mac_units=544, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=960, voltage_v=0.74)

def point_174() -> DesignPoint:
    return DesignPoint("point_174", mac_units=576, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.77)

def point_175() -> DesignPoint:
    return DesignPoint("point_175", mac_units=608, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.80)

def point_176() -> DesignPoint:
    return DesignPoint("point_176", mac_units=640, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=128, voltage_v=0.83)

def point_177() -> DesignPoint:
    return DesignPoint("point_177", mac_units=672, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=192, voltage_v=0.86)

def point_178() -> DesignPoint:
    return DesignPoint("point_178", mac_units=704, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=256, voltage_v=0.89)

def point_179() -> DesignPoint:
    return DesignPoint("point_179", mac_units=736, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=320, voltage_v=0.92)

def point_180() -> DesignPoint:
    return DesignPoint("point_180", mac_units=768, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=384, voltage_v=0.65)

def point_181() -> DesignPoint:
    return DesignPoint("point_181", mac_units=800, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=448, voltage_v=0.68)

def point_182() -> DesignPoint:
    return DesignPoint("point_182", mac_units=832, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=512, voltage_v=0.71)

def point_183() -> DesignPoint:
    return DesignPoint("point_183", mac_units=864, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=576, voltage_v=0.74)

def point_184() -> DesignPoint:
    return DesignPoint("point_184", mac_units=896, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=640, voltage_v=0.77)

def point_185() -> DesignPoint:
    return DesignPoint("point_185", mac_units=928, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=704, voltage_v=0.80)

def point_186() -> DesignPoint:
    return DesignPoint("point_186", mac_units=960, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=768, voltage_v=0.83)

def point_187() -> DesignPoint:
    return DesignPoint("point_187", mac_units=992, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=832, voltage_v=0.86)

def point_188() -> DesignPoint:
    return DesignPoint("point_188", mac_units=1024, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=896, voltage_v=0.89)

def point_189() -> DesignPoint:
    return DesignPoint("point_189", mac_units=1056, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=960, voltage_v=0.92)

def point_190() -> DesignPoint:
    return DesignPoint("point_190", mac_units=1088, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.65)

def point_191() -> DesignPoint:
    return DesignPoint("point_191", mac_units=1120, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.68)

def point_192() -> DesignPoint:
    return DesignPoint("point_192", mac_units=128, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=128, voltage_v=0.71)

def point_193() -> DesignPoint:
    return DesignPoint("point_193", mac_units=160, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=192, voltage_v=0.74)

def point_194() -> DesignPoint:
    return DesignPoint("point_194", mac_units=192, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=256, voltage_v=0.77)

def point_195() -> DesignPoint:
    return DesignPoint("point_195", mac_units=224, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=320, voltage_v=0.80)

def point_196() -> DesignPoint:
    return DesignPoint("point_196", mac_units=256, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=384, voltage_v=0.83)

def point_197() -> DesignPoint:
    return DesignPoint("point_197", mac_units=288, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=448, voltage_v=0.86)

def point_198() -> DesignPoint:
    return DesignPoint("point_198", mac_units=320, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=512, voltage_v=0.89)

def point_199() -> DesignPoint:
    return DesignPoint("point_199", mac_units=352, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=576, voltage_v=0.92)

def point_200() -> DesignPoint:
    return DesignPoint("point_200", mac_units=384, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=640, voltage_v=0.65)

def point_201() -> DesignPoint:
    return DesignPoint("point_201", mac_units=416, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=704, voltage_v=0.68)

def point_202() -> DesignPoint:
    return DesignPoint("point_202", mac_units=448, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=768, voltage_v=0.71)

def point_203() -> DesignPoint:
    return DesignPoint("point_203", mac_units=480, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=832, voltage_v=0.74)

def point_204() -> DesignPoint:
    return DesignPoint("point_204", mac_units=512, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=896, voltage_v=0.77)

def point_205() -> DesignPoint:
    return DesignPoint("point_205", mac_units=544, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=960, voltage_v=0.80)

def point_206() -> DesignPoint:
    return DesignPoint("point_206", mac_units=576, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.83)

def point_207() -> DesignPoint:
    return DesignPoint("point_207", mac_units=608, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.86)

def point_208() -> DesignPoint:
    return DesignPoint("point_208", mac_units=640, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=128, voltage_v=0.89)

def point_209() -> DesignPoint:
    return DesignPoint("point_209", mac_units=672, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=192, voltage_v=0.92)

def point_210() -> DesignPoint:
    return DesignPoint("point_210", mac_units=704, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=256, voltage_v=0.65)

def point_211() -> DesignPoint:
    return DesignPoint("point_211", mac_units=736, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=320, voltage_v=0.68)

def point_212() -> DesignPoint:
    return DesignPoint("point_212", mac_units=768, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=384, voltage_v=0.71)

def point_213() -> DesignPoint:
    return DesignPoint("point_213", mac_units=800, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=448, voltage_v=0.74)

def point_214() -> DesignPoint:
    return DesignPoint("point_214", mac_units=832, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=512, voltage_v=0.77)

def point_215() -> DesignPoint:
    return DesignPoint("point_215", mac_units=864, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=576, voltage_v=0.80)

def point_216() -> DesignPoint:
    return DesignPoint("point_216", mac_units=896, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=640, voltage_v=0.83)

def point_217() -> DesignPoint:
    return DesignPoint("point_217", mac_units=928, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=704, voltage_v=0.86)

def point_218() -> DesignPoint:
    return DesignPoint("point_218", mac_units=960, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=768, voltage_v=0.89)

def point_219() -> DesignPoint:
    return DesignPoint("point_219", mac_units=992, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=832, voltage_v=0.92)

def point_220() -> DesignPoint:
    return DesignPoint("point_220", mac_units=1024, frequency_ghz=0.600, bandwidth_gbps=128, sram_kb=896, voltage_v=0.65)

def point_221() -> DesignPoint:
    return DesignPoint("point_221", mac_units=1056, frequency_ghz=0.650, bandwidth_gbps=144, sram_kb=960, voltage_v=0.68)

def point_222() -> DesignPoint:
    return DesignPoint("point_222", mac_units=1088, frequency_ghz=0.700, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.71)

def point_223() -> DesignPoint:
    return DesignPoint("point_223", mac_units=1120, frequency_ghz=0.750, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.74)

def point_224() -> DesignPoint:
    return DesignPoint("point_224", mac_units=128, frequency_ghz=0.800, bandwidth_gbps=192, sram_kb=128, voltage_v=0.77)

def point_225() -> DesignPoint:
    return DesignPoint("point_225", mac_units=160, frequency_ghz=0.850, bandwidth_gbps=208, sram_kb=192, voltage_v=0.80)

def point_226() -> DesignPoint:
    return DesignPoint("point_226", mac_units=192, frequency_ghz=0.900, bandwidth_gbps=224, sram_kb=256, voltage_v=0.83)

def point_227() -> DesignPoint:
    return DesignPoint("point_227", mac_units=224, frequency_ghz=0.950, bandwidth_gbps=240, sram_kb=320, voltage_v=0.86)

def point_228() -> DesignPoint:
    return DesignPoint("point_228", mac_units=256, frequency_ghz=1.000, bandwidth_gbps=256, sram_kb=384, voltage_v=0.89)

def point_229() -> DesignPoint:
    return DesignPoint("point_229", mac_units=288, frequency_ghz=1.050, bandwidth_gbps=272, sram_kb=448, voltage_v=0.92)

def point_230() -> DesignPoint:
    return DesignPoint("point_230", mac_units=320, frequency_ghz=1.100, bandwidth_gbps=288, sram_kb=512, voltage_v=0.65)

def point_231() -> DesignPoint:
    return DesignPoint("point_231", mac_units=352, frequency_ghz=1.150, bandwidth_gbps=304, sram_kb=576, voltage_v=0.68)

def point_232() -> DesignPoint:
    return DesignPoint("point_232", mac_units=384, frequency_ghz=1.200, bandwidth_gbps=320, sram_kb=640, voltage_v=0.71)

def point_233() -> DesignPoint:
    return DesignPoint("point_233", mac_units=416, frequency_ghz=1.250, bandwidth_gbps=336, sram_kb=704, voltage_v=0.74)

def point_234() -> DesignPoint:
    return DesignPoint("point_234", mac_units=448, frequency_ghz=1.300, bandwidth_gbps=352, sram_kb=768, voltage_v=0.77)

def point_235() -> DesignPoint:
    return DesignPoint("point_235", mac_units=480, frequency_ghz=1.350, bandwidth_gbps=368, sram_kb=832, voltage_v=0.80)

def point_236() -> DesignPoint:
    return DesignPoint("point_236", mac_units=512, frequency_ghz=1.400, bandwidth_gbps=384, sram_kb=896, voltage_v=0.83)

def point_237() -> DesignPoint:
    return DesignPoint("point_237", mac_units=544, frequency_ghz=1.450, bandwidth_gbps=400, sram_kb=960, voltage_v=0.86)

def point_238() -> DesignPoint:
    return DesignPoint("point_238", mac_units=576, frequency_ghz=1.500, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.89)

def point_239() -> DesignPoint:
    return DesignPoint("point_239", mac_units=608, frequency_ghz=1.550, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.92)

def point_240() -> DesignPoint:
    return DesignPoint("point_240", mac_units=640, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=128, voltage_v=0.65)

def point_241() -> DesignPoint:
    return DesignPoint("point_241", mac_units=672, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=192, voltage_v=0.68)

def point_242() -> DesignPoint:
    return DesignPoint("point_242", mac_units=704, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=256, voltage_v=0.71)

def point_243() -> DesignPoint:
    return DesignPoint("point_243", mac_units=736, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=320, voltage_v=0.74)

def point_244() -> DesignPoint:
    return DesignPoint("point_244", mac_units=768, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=384, voltage_v=0.77)

def point_245() -> DesignPoint:
    return DesignPoint("point_245", mac_units=800, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=448, voltage_v=0.80)

def point_246() -> DesignPoint:
    return DesignPoint("point_246", mac_units=832, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=512, voltage_v=0.83)

def point_247() -> DesignPoint:
    return DesignPoint("point_247", mac_units=864, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=576, voltage_v=0.86)

def point_248() -> DesignPoint:
    return DesignPoint("point_248", mac_units=896, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=640, voltage_v=0.89)

def point_249() -> DesignPoint:
    return DesignPoint("point_249", mac_units=928, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=704, voltage_v=0.92)

def point_250() -> DesignPoint:
    return DesignPoint("point_250", mac_units=960, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=768, voltage_v=0.65)

def point_251() -> DesignPoint:
    return DesignPoint("point_251", mac_units=992, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=832, voltage_v=0.68)

def point_252() -> DesignPoint:
    return DesignPoint("point_252", mac_units=1024, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=896, voltage_v=0.71)

def point_253() -> DesignPoint:
    return DesignPoint("point_253", mac_units=1056, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=960, voltage_v=0.74)

def point_254() -> DesignPoint:
    return DesignPoint("point_254", mac_units=1088, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.77)

def point_255() -> DesignPoint:
    return DesignPoint("point_255", mac_units=1120, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.80)

def point_256() -> DesignPoint:
    return DesignPoint("point_256", mac_units=128, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=128, voltage_v=0.83)

def point_257() -> DesignPoint:
    return DesignPoint("point_257", mac_units=160, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=192, voltage_v=0.86)

def point_258() -> DesignPoint:
    return DesignPoint("point_258", mac_units=192, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=256, voltage_v=0.89)

def point_259() -> DesignPoint:
    return DesignPoint("point_259", mac_units=224, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=320, voltage_v=0.92)

def point_260() -> DesignPoint:
    return DesignPoint("point_260", mac_units=256, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=384, voltage_v=0.65)

def point_261() -> DesignPoint:
    return DesignPoint("point_261", mac_units=288, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=448, voltage_v=0.68)

def point_262() -> DesignPoint:
    return DesignPoint("point_262", mac_units=320, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=512, voltage_v=0.71)

def point_263() -> DesignPoint:
    return DesignPoint("point_263", mac_units=352, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=576, voltage_v=0.74)

def point_264() -> DesignPoint:
    return DesignPoint("point_264", mac_units=384, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=640, voltage_v=0.77)

def point_265() -> DesignPoint:
    return DesignPoint("point_265", mac_units=416, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=704, voltage_v=0.80)

def point_266() -> DesignPoint:
    return DesignPoint("point_266", mac_units=448, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=768, voltage_v=0.83)

def point_267() -> DesignPoint:
    return DesignPoint("point_267", mac_units=480, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=832, voltage_v=0.86)

def point_268() -> DesignPoint:
    return DesignPoint("point_268", mac_units=512, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=896, voltage_v=0.89)

def point_269() -> DesignPoint:
    return DesignPoint("point_269", mac_units=544, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=960, voltage_v=0.92)

def point_270() -> DesignPoint:
    return DesignPoint("point_270", mac_units=576, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.65)

def point_271() -> DesignPoint:
    return DesignPoint("point_271", mac_units=608, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.68)

def point_272() -> DesignPoint:
    return DesignPoint("point_272", mac_units=640, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=128, voltage_v=0.71)

def point_273() -> DesignPoint:
    return DesignPoint("point_273", mac_units=672, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=192, voltage_v=0.74)

def point_274() -> DesignPoint:
    return DesignPoint("point_274", mac_units=704, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=256, voltage_v=0.77)

def point_275() -> DesignPoint:
    return DesignPoint("point_275", mac_units=736, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=320, voltage_v=0.80)

def point_276() -> DesignPoint:
    return DesignPoint("point_276", mac_units=768, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=384, voltage_v=0.83)

def point_277() -> DesignPoint:
    return DesignPoint("point_277", mac_units=800, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=448, voltage_v=0.86)

def point_278() -> DesignPoint:
    return DesignPoint("point_278", mac_units=832, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=512, voltage_v=0.89)

def point_279() -> DesignPoint:
    return DesignPoint("point_279", mac_units=864, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=576, voltage_v=0.92)

def point_280() -> DesignPoint:
    return DesignPoint("point_280", mac_units=896, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=640, voltage_v=0.65)

def point_281() -> DesignPoint:
    return DesignPoint("point_281", mac_units=928, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=704, voltage_v=0.68)

def point_282() -> DesignPoint:
    return DesignPoint("point_282", mac_units=960, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=768, voltage_v=0.71)

def point_283() -> DesignPoint:
    return DesignPoint("point_283", mac_units=992, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=832, voltage_v=0.74)

def point_284() -> DesignPoint:
    return DesignPoint("point_284", mac_units=1024, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=896, voltage_v=0.77)

def point_285() -> DesignPoint:
    return DesignPoint("point_285", mac_units=1056, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=960, voltage_v=0.80)

def point_286() -> DesignPoint:
    return DesignPoint("point_286", mac_units=1088, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.83)

def point_287() -> DesignPoint:
    return DesignPoint("point_287", mac_units=1120, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.86)

def point_288() -> DesignPoint:
    return DesignPoint("point_288", mac_units=128, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=128, voltage_v=0.89)

def point_289() -> DesignPoint:
    return DesignPoint("point_289", mac_units=160, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=192, voltage_v=0.92)

def point_290() -> DesignPoint:
    return DesignPoint("point_290", mac_units=192, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=256, voltage_v=0.65)

def point_291() -> DesignPoint:
    return DesignPoint("point_291", mac_units=224, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=320, voltage_v=0.68)

def point_292() -> DesignPoint:
    return DesignPoint("point_292", mac_units=256, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=384, voltage_v=0.71)

def point_293() -> DesignPoint:
    return DesignPoint("point_293", mac_units=288, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=448, voltage_v=0.74)

def point_294() -> DesignPoint:
    return DesignPoint("point_294", mac_units=320, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=512, voltage_v=0.77)

def point_295() -> DesignPoint:
    return DesignPoint("point_295", mac_units=352, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=576, voltage_v=0.80)

def point_296() -> DesignPoint:
    return DesignPoint("point_296", mac_units=384, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=640, voltage_v=0.83)

def point_297() -> DesignPoint:
    return DesignPoint("point_297", mac_units=416, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=704, voltage_v=0.86)

def point_298() -> DesignPoint:
    return DesignPoint("point_298", mac_units=448, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=768, voltage_v=0.89)

def point_299() -> DesignPoint:
    return DesignPoint("point_299", mac_units=480, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=832, voltage_v=0.92)

def point_300() -> DesignPoint:
    return DesignPoint("point_300", mac_units=512, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=896, voltage_v=0.65)

def point_301() -> DesignPoint:
    return DesignPoint("point_301", mac_units=544, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=960, voltage_v=0.68)

def point_302() -> DesignPoint:
    return DesignPoint("point_302", mac_units=576, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.71)

def point_303() -> DesignPoint:
    return DesignPoint("point_303", mac_units=608, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.74)

def point_304() -> DesignPoint:
    return DesignPoint("point_304", mac_units=640, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=128, voltage_v=0.77)

def point_305() -> DesignPoint:
    return DesignPoint("point_305", mac_units=672, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=192, voltage_v=0.80)

def point_306() -> DesignPoint:
    return DesignPoint("point_306", mac_units=704, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=256, voltage_v=0.83)

def point_307() -> DesignPoint:
    return DesignPoint("point_307", mac_units=736, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=320, voltage_v=0.86)

def point_308() -> DesignPoint:
    return DesignPoint("point_308", mac_units=768, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=384, voltage_v=0.89)

def point_309() -> DesignPoint:
    return DesignPoint("point_309", mac_units=800, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=448, voltage_v=0.92)

def point_310() -> DesignPoint:
    return DesignPoint("point_310", mac_units=832, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=512, voltage_v=0.65)

def point_311() -> DesignPoint:
    return DesignPoint("point_311", mac_units=864, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=576, voltage_v=0.68)

def point_312() -> DesignPoint:
    return DesignPoint("point_312", mac_units=896, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=640, voltage_v=0.71)

def point_313() -> DesignPoint:
    return DesignPoint("point_313", mac_units=928, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=704, voltage_v=0.74)

def point_314() -> DesignPoint:
    return DesignPoint("point_314", mac_units=960, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=768, voltage_v=0.77)

def point_315() -> DesignPoint:
    return DesignPoint("point_315", mac_units=992, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=832, voltage_v=0.80)

def point_316() -> DesignPoint:
    return DesignPoint("point_316", mac_units=1024, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=896, voltage_v=0.83)

def point_317() -> DesignPoint:
    return DesignPoint("point_317", mac_units=1056, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=960, voltage_v=0.86)

def point_318() -> DesignPoint:
    return DesignPoint("point_318", mac_units=1088, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.89)

def point_319() -> DesignPoint:
    return DesignPoint("point_319", mac_units=1120, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.92)

def point_320() -> DesignPoint:
    return DesignPoint("point_320", mac_units=128, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=128, voltage_v=0.65)

def point_321() -> DesignPoint:
    return DesignPoint("point_321", mac_units=160, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=192, voltage_v=0.68)

def point_322() -> DesignPoint:
    return DesignPoint("point_322", mac_units=192, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=256, voltage_v=0.71)

def point_323() -> DesignPoint:
    return DesignPoint("point_323", mac_units=224, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=320, voltage_v=0.74)

def point_324() -> DesignPoint:
    return DesignPoint("point_324", mac_units=256, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=384, voltage_v=0.77)

def point_325() -> DesignPoint:
    return DesignPoint("point_325", mac_units=288, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=448, voltage_v=0.80)

def point_326() -> DesignPoint:
    return DesignPoint("point_326", mac_units=320, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=512, voltage_v=0.83)

def point_327() -> DesignPoint:
    return DesignPoint("point_327", mac_units=352, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=576, voltage_v=0.86)

def point_328() -> DesignPoint:
    return DesignPoint("point_328", mac_units=384, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=640, voltage_v=0.89)

def point_329() -> DesignPoint:
    return DesignPoint("point_329", mac_units=416, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=704, voltage_v=0.92)

def point_330() -> DesignPoint:
    return DesignPoint("point_330", mac_units=448, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=768, voltage_v=0.65)

def point_331() -> DesignPoint:
    return DesignPoint("point_331", mac_units=480, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=832, voltage_v=0.68)

def point_332() -> DesignPoint:
    return DesignPoint("point_332", mac_units=512, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=896, voltage_v=0.71)

def point_333() -> DesignPoint:
    return DesignPoint("point_333", mac_units=544, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=960, voltage_v=0.74)

def point_334() -> DesignPoint:
    return DesignPoint("point_334", mac_units=576, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.77)

def point_335() -> DesignPoint:
    return DesignPoint("point_335", mac_units=608, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.80)

def point_336() -> DesignPoint:
    return DesignPoint("point_336", mac_units=640, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=128, voltage_v=0.83)

def point_337() -> DesignPoint:
    return DesignPoint("point_337", mac_units=672, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=192, voltage_v=0.86)

def point_338() -> DesignPoint:
    return DesignPoint("point_338", mac_units=704, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=256, voltage_v=0.89)

def point_339() -> DesignPoint:
    return DesignPoint("point_339", mac_units=736, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=320, voltage_v=0.92)

def point_340() -> DesignPoint:
    return DesignPoint("point_340", mac_units=768, frequency_ghz=0.600, bandwidth_gbps=128, sram_kb=384, voltage_v=0.65)

def point_341() -> DesignPoint:
    return DesignPoint("point_341", mac_units=800, frequency_ghz=0.650, bandwidth_gbps=144, sram_kb=448, voltage_v=0.68)

def point_342() -> DesignPoint:
    return DesignPoint("point_342", mac_units=832, frequency_ghz=0.700, bandwidth_gbps=160, sram_kb=512, voltage_v=0.71)

def point_343() -> DesignPoint:
    return DesignPoint("point_343", mac_units=864, frequency_ghz=0.750, bandwidth_gbps=176, sram_kb=576, voltage_v=0.74)

def point_344() -> DesignPoint:
    return DesignPoint("point_344", mac_units=896, frequency_ghz=0.800, bandwidth_gbps=192, sram_kb=640, voltage_v=0.77)

def point_345() -> DesignPoint:
    return DesignPoint("point_345", mac_units=928, frequency_ghz=0.850, bandwidth_gbps=208, sram_kb=704, voltage_v=0.80)

def point_346() -> DesignPoint:
    return DesignPoint("point_346", mac_units=960, frequency_ghz=0.900, bandwidth_gbps=224, sram_kb=768, voltage_v=0.83)

def point_347() -> DesignPoint:
    return DesignPoint("point_347", mac_units=992, frequency_ghz=0.950, bandwidth_gbps=240, sram_kb=832, voltage_v=0.86)

def point_348() -> DesignPoint:
    return DesignPoint("point_348", mac_units=1024, frequency_ghz=1.000, bandwidth_gbps=256, sram_kb=896, voltage_v=0.89)

def point_349() -> DesignPoint:
    return DesignPoint("point_349", mac_units=1056, frequency_ghz=1.050, bandwidth_gbps=272, sram_kb=960, voltage_v=0.92)

def point_350() -> DesignPoint:
    return DesignPoint("point_350", mac_units=1088, frequency_ghz=1.100, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.65)

def point_351() -> DesignPoint:
    return DesignPoint("point_351", mac_units=1120, frequency_ghz=1.150, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.68)

def point_352() -> DesignPoint:
    return DesignPoint("point_352", mac_units=128, frequency_ghz=1.200, bandwidth_gbps=320, sram_kb=128, voltage_v=0.71)

def point_353() -> DesignPoint:
    return DesignPoint("point_353", mac_units=160, frequency_ghz=1.250, bandwidth_gbps=336, sram_kb=192, voltage_v=0.74)

def point_354() -> DesignPoint:
    return DesignPoint("point_354", mac_units=192, frequency_ghz=1.300, bandwidth_gbps=352, sram_kb=256, voltage_v=0.77)

def point_355() -> DesignPoint:
    return DesignPoint("point_355", mac_units=224, frequency_ghz=1.350, bandwidth_gbps=368, sram_kb=320, voltage_v=0.80)

def point_356() -> DesignPoint:
    return DesignPoint("point_356", mac_units=256, frequency_ghz=1.400, bandwidth_gbps=384, sram_kb=384, voltage_v=0.83)

def point_357() -> DesignPoint:
    return DesignPoint("point_357", mac_units=288, frequency_ghz=1.450, bandwidth_gbps=400, sram_kb=448, voltage_v=0.86)

def point_358() -> DesignPoint:
    return DesignPoint("point_358", mac_units=320, frequency_ghz=1.500, bandwidth_gbps=416, sram_kb=512, voltage_v=0.89)

def point_359() -> DesignPoint:
    return DesignPoint("point_359", mac_units=352, frequency_ghz=1.550, bandwidth_gbps=432, sram_kb=576, voltage_v=0.92)

def point_360() -> DesignPoint:
    return DesignPoint("point_360", mac_units=384, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=640, voltage_v=0.65)

def point_361() -> DesignPoint:
    return DesignPoint("point_361", mac_units=416, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=704, voltage_v=0.68)

def point_362() -> DesignPoint:
    return DesignPoint("point_362", mac_units=448, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=768, voltage_v=0.71)

def point_363() -> DesignPoint:
    return DesignPoint("point_363", mac_units=480, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=832, voltage_v=0.74)

def point_364() -> DesignPoint:
    return DesignPoint("point_364", mac_units=512, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=896, voltage_v=0.77)

def point_365() -> DesignPoint:
    return DesignPoint("point_365", mac_units=544, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=960, voltage_v=0.80)

def point_366() -> DesignPoint:
    return DesignPoint("point_366", mac_units=576, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.83)

def point_367() -> DesignPoint:
    return DesignPoint("point_367", mac_units=608, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.86)

def point_368() -> DesignPoint:
    return DesignPoint("point_368", mac_units=640, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=128, voltage_v=0.89)

def point_369() -> DesignPoint:
    return DesignPoint("point_369", mac_units=672, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=192, voltage_v=0.92)

def point_370() -> DesignPoint:
    return DesignPoint("point_370", mac_units=704, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=256, voltage_v=0.65)

def point_371() -> DesignPoint:
    return DesignPoint("point_371", mac_units=736, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=320, voltage_v=0.68)

def point_372() -> DesignPoint:
    return DesignPoint("point_372", mac_units=768, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=384, voltage_v=0.71)

def point_373() -> DesignPoint:
    return DesignPoint("point_373", mac_units=800, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=448, voltage_v=0.74)

def point_374() -> DesignPoint:
    return DesignPoint("point_374", mac_units=832, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=512, voltage_v=0.77)

def point_375() -> DesignPoint:
    return DesignPoint("point_375", mac_units=864, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=576, voltage_v=0.80)

def point_376() -> DesignPoint:
    return DesignPoint("point_376", mac_units=896, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=640, voltage_v=0.83)

def point_377() -> DesignPoint:
    return DesignPoint("point_377", mac_units=928, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=704, voltage_v=0.86)

def point_378() -> DesignPoint:
    return DesignPoint("point_378", mac_units=960, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=768, voltage_v=0.89)

def point_379() -> DesignPoint:
    return DesignPoint("point_379", mac_units=992, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=832, voltage_v=0.92)

def point_380() -> DesignPoint:
    return DesignPoint("point_380", mac_units=1024, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=896, voltage_v=0.65)

def point_381() -> DesignPoint:
    return DesignPoint("point_381", mac_units=1056, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=960, voltage_v=0.68)

def point_382() -> DesignPoint:
    return DesignPoint("point_382", mac_units=1088, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.71)

def point_383() -> DesignPoint:
    return DesignPoint("point_383", mac_units=1120, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.74)

def point_384() -> DesignPoint:
    return DesignPoint("point_384", mac_units=128, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=128, voltage_v=0.77)

def point_385() -> DesignPoint:
    return DesignPoint("point_385", mac_units=160, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=192, voltage_v=0.80)

def point_386() -> DesignPoint:
    return DesignPoint("point_386", mac_units=192, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=256, voltage_v=0.83)

def point_387() -> DesignPoint:
    return DesignPoint("point_387", mac_units=224, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=320, voltage_v=0.86)

def point_388() -> DesignPoint:
    return DesignPoint("point_388", mac_units=256, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=384, voltage_v=0.89)

def point_389() -> DesignPoint:
    return DesignPoint("point_389", mac_units=288, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=448, voltage_v=0.92)

def point_390() -> DesignPoint:
    return DesignPoint("point_390", mac_units=320, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=512, voltage_v=0.65)

def point_391() -> DesignPoint:
    return DesignPoint("point_391", mac_units=352, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=576, voltage_v=0.68)

def point_392() -> DesignPoint:
    return DesignPoint("point_392", mac_units=384, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=640, voltage_v=0.71)

def point_393() -> DesignPoint:
    return DesignPoint("point_393", mac_units=416, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=704, voltage_v=0.74)

def point_394() -> DesignPoint:
    return DesignPoint("point_394", mac_units=448, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=768, voltage_v=0.77)

def point_395() -> DesignPoint:
    return DesignPoint("point_395", mac_units=480, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=832, voltage_v=0.80)

def point_396() -> DesignPoint:
    return DesignPoint("point_396", mac_units=512, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=896, voltage_v=0.83)

def point_397() -> DesignPoint:
    return DesignPoint("point_397", mac_units=544, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=960, voltage_v=0.86)

def point_398() -> DesignPoint:
    return DesignPoint("point_398", mac_units=576, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.89)

def point_399() -> DesignPoint:
    return DesignPoint("point_399", mac_units=608, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.92)

def point_400() -> DesignPoint:
    return DesignPoint("point_400", mac_units=640, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=128, voltage_v=0.65)

def point_401() -> DesignPoint:
    return DesignPoint("point_401", mac_units=672, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=192, voltage_v=0.68)

def point_402() -> DesignPoint:
    return DesignPoint("point_402", mac_units=704, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=256, voltage_v=0.71)

def point_403() -> DesignPoint:
    return DesignPoint("point_403", mac_units=736, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=320, voltage_v=0.74)

def point_404() -> DesignPoint:
    return DesignPoint("point_404", mac_units=768, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=384, voltage_v=0.77)

def point_405() -> DesignPoint:
    return DesignPoint("point_405", mac_units=800, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=448, voltage_v=0.80)

def point_406() -> DesignPoint:
    return DesignPoint("point_406", mac_units=832, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=512, voltage_v=0.83)

def point_407() -> DesignPoint:
    return DesignPoint("point_407", mac_units=864, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=576, voltage_v=0.86)

def point_408() -> DesignPoint:
    return DesignPoint("point_408", mac_units=896, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=640, voltage_v=0.89)

def point_409() -> DesignPoint:
    return DesignPoint("point_409", mac_units=928, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=704, voltage_v=0.92)

def point_410() -> DesignPoint:
    return DesignPoint("point_410", mac_units=960, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=768, voltage_v=0.65)

def point_411() -> DesignPoint:
    return DesignPoint("point_411", mac_units=992, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=832, voltage_v=0.68)

def point_412() -> DesignPoint:
    return DesignPoint("point_412", mac_units=1024, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=896, voltage_v=0.71)

def point_413() -> DesignPoint:
    return DesignPoint("point_413", mac_units=1056, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=960, voltage_v=0.74)

def point_414() -> DesignPoint:
    return DesignPoint("point_414", mac_units=1088, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.77)

def point_415() -> DesignPoint:
    return DesignPoint("point_415", mac_units=1120, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.80)

def point_416() -> DesignPoint:
    return DesignPoint("point_416", mac_units=128, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=128, voltage_v=0.83)

def point_417() -> DesignPoint:
    return DesignPoint("point_417", mac_units=160, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=192, voltage_v=0.86)

def point_418() -> DesignPoint:
    return DesignPoint("point_418", mac_units=192, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=256, voltage_v=0.89)

def point_419() -> DesignPoint:
    return DesignPoint("point_419", mac_units=224, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=320, voltage_v=0.92)

def point_420() -> DesignPoint:
    return DesignPoint("point_420", mac_units=256, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=384, voltage_v=0.65)

def point_421() -> DesignPoint:
    return DesignPoint("point_421", mac_units=288, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=448, voltage_v=0.68)

def point_422() -> DesignPoint:
    return DesignPoint("point_422", mac_units=320, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=512, voltage_v=0.71)

def point_423() -> DesignPoint:
    return DesignPoint("point_423", mac_units=352, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=576, voltage_v=0.74)

def point_424() -> DesignPoint:
    return DesignPoint("point_424", mac_units=384, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=640, voltage_v=0.77)

def point_425() -> DesignPoint:
    return DesignPoint("point_425", mac_units=416, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=704, voltage_v=0.80)

def point_426() -> DesignPoint:
    return DesignPoint("point_426", mac_units=448, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=768, voltage_v=0.83)

def point_427() -> DesignPoint:
    return DesignPoint("point_427", mac_units=480, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=832, voltage_v=0.86)

def point_428() -> DesignPoint:
    return DesignPoint("point_428", mac_units=512, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=896, voltage_v=0.89)

def point_429() -> DesignPoint:
    return DesignPoint("point_429", mac_units=544, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=960, voltage_v=0.92)

def point_430() -> DesignPoint:
    return DesignPoint("point_430", mac_units=576, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.65)

def point_431() -> DesignPoint:
    return DesignPoint("point_431", mac_units=608, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.68)

def point_432() -> DesignPoint:
    return DesignPoint("point_432", mac_units=640, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=128, voltage_v=0.71)

def point_433() -> DesignPoint:
    return DesignPoint("point_433", mac_units=672, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=192, voltage_v=0.74)

def point_434() -> DesignPoint:
    return DesignPoint("point_434", mac_units=704, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=256, voltage_v=0.77)

def point_435() -> DesignPoint:
    return DesignPoint("point_435", mac_units=736, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=320, voltage_v=0.80)

def point_436() -> DesignPoint:
    return DesignPoint("point_436", mac_units=768, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=384, voltage_v=0.83)

def point_437() -> DesignPoint:
    return DesignPoint("point_437", mac_units=800, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=448, voltage_v=0.86)

def point_438() -> DesignPoint:
    return DesignPoint("point_438", mac_units=832, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=512, voltage_v=0.89)

def point_439() -> DesignPoint:
    return DesignPoint("point_439", mac_units=864, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=576, voltage_v=0.92)

def point_440() -> DesignPoint:
    return DesignPoint("point_440", mac_units=896, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=640, voltage_v=0.65)

def point_441() -> DesignPoint:
    return DesignPoint("point_441", mac_units=928, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=704, voltage_v=0.68)

def point_442() -> DesignPoint:
    return DesignPoint("point_442", mac_units=960, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=768, voltage_v=0.71)

def point_443() -> DesignPoint:
    return DesignPoint("point_443", mac_units=992, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=832, voltage_v=0.74)

def point_444() -> DesignPoint:
    return DesignPoint("point_444", mac_units=1024, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=896, voltage_v=0.77)

def point_445() -> DesignPoint:
    return DesignPoint("point_445", mac_units=1056, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=960, voltage_v=0.80)

def point_446() -> DesignPoint:
    return DesignPoint("point_446", mac_units=1088, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.83)

def point_447() -> DesignPoint:
    return DesignPoint("point_447", mac_units=1120, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.86)

def point_448() -> DesignPoint:
    return DesignPoint("point_448", mac_units=128, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=128, voltage_v=0.89)

def point_449() -> DesignPoint:
    return DesignPoint("point_449", mac_units=160, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=192, voltage_v=0.92)

def point_450() -> DesignPoint:
    return DesignPoint("point_450", mac_units=192, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=256, voltage_v=0.65)

def point_451() -> DesignPoint:
    return DesignPoint("point_451", mac_units=224, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=320, voltage_v=0.68)

def point_452() -> DesignPoint:
    return DesignPoint("point_452", mac_units=256, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=384, voltage_v=0.71)

def point_453() -> DesignPoint:
    return DesignPoint("point_453", mac_units=288, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=448, voltage_v=0.74)

def point_454() -> DesignPoint:
    return DesignPoint("point_454", mac_units=320, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=512, voltage_v=0.77)

def point_455() -> DesignPoint:
    return DesignPoint("point_455", mac_units=352, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=576, voltage_v=0.80)

def point_456() -> DesignPoint:
    return DesignPoint("point_456", mac_units=384, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=640, voltage_v=0.83)

def point_457() -> DesignPoint:
    return DesignPoint("point_457", mac_units=416, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=704, voltage_v=0.86)

def point_458() -> DesignPoint:
    return DesignPoint("point_458", mac_units=448, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=768, voltage_v=0.89)

def point_459() -> DesignPoint:
    return DesignPoint("point_459", mac_units=480, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=832, voltage_v=0.92)

def point_460() -> DesignPoint:
    return DesignPoint("point_460", mac_units=512, frequency_ghz=0.600, bandwidth_gbps=128, sram_kb=896, voltage_v=0.65)

def point_461() -> DesignPoint:
    return DesignPoint("point_461", mac_units=544, frequency_ghz=0.650, bandwidth_gbps=144, sram_kb=960, voltage_v=0.68)

def point_462() -> DesignPoint:
    return DesignPoint("point_462", mac_units=576, frequency_ghz=0.700, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.71)

def point_463() -> DesignPoint:
    return DesignPoint("point_463", mac_units=608, frequency_ghz=0.750, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.74)

def point_464() -> DesignPoint:
    return DesignPoint("point_464", mac_units=640, frequency_ghz=0.800, bandwidth_gbps=192, sram_kb=128, voltage_v=0.77)

def point_465() -> DesignPoint:
    return DesignPoint("point_465", mac_units=672, frequency_ghz=0.850, bandwidth_gbps=208, sram_kb=192, voltage_v=0.80)

def point_466() -> DesignPoint:
    return DesignPoint("point_466", mac_units=704, frequency_ghz=0.900, bandwidth_gbps=224, sram_kb=256, voltage_v=0.83)

def point_467() -> DesignPoint:
    return DesignPoint("point_467", mac_units=736, frequency_ghz=0.950, bandwidth_gbps=240, sram_kb=320, voltage_v=0.86)

def point_468() -> DesignPoint:
    return DesignPoint("point_468", mac_units=768, frequency_ghz=1.000, bandwidth_gbps=256, sram_kb=384, voltage_v=0.89)

def point_469() -> DesignPoint:
    return DesignPoint("point_469", mac_units=800, frequency_ghz=1.050, bandwidth_gbps=272, sram_kb=448, voltage_v=0.92)

def point_470() -> DesignPoint:
    return DesignPoint("point_470", mac_units=832, frequency_ghz=1.100, bandwidth_gbps=288, sram_kb=512, voltage_v=0.65)

def point_471() -> DesignPoint:
    return DesignPoint("point_471", mac_units=864, frequency_ghz=1.150, bandwidth_gbps=304, sram_kb=576, voltage_v=0.68)

def point_472() -> DesignPoint:
    return DesignPoint("point_472", mac_units=896, frequency_ghz=1.200, bandwidth_gbps=320, sram_kb=640, voltage_v=0.71)

def point_473() -> DesignPoint:
    return DesignPoint("point_473", mac_units=928, frequency_ghz=1.250, bandwidth_gbps=336, sram_kb=704, voltage_v=0.74)

def point_474() -> DesignPoint:
    return DesignPoint("point_474", mac_units=960, frequency_ghz=1.300, bandwidth_gbps=352, sram_kb=768, voltage_v=0.77)

def point_475() -> DesignPoint:
    return DesignPoint("point_475", mac_units=992, frequency_ghz=1.350, bandwidth_gbps=368, sram_kb=832, voltage_v=0.80)

def point_476() -> DesignPoint:
    return DesignPoint("point_476", mac_units=1024, frequency_ghz=1.400, bandwidth_gbps=384, sram_kb=896, voltage_v=0.83)

def point_477() -> DesignPoint:
    return DesignPoint("point_477", mac_units=1056, frequency_ghz=1.450, bandwidth_gbps=400, sram_kb=960, voltage_v=0.86)

def point_478() -> DesignPoint:
    return DesignPoint("point_478", mac_units=1088, frequency_ghz=1.500, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.89)

def point_479() -> DesignPoint:
    return DesignPoint("point_479", mac_units=1120, frequency_ghz=1.550, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.92)

def point_480() -> DesignPoint:
    return DesignPoint("point_480", mac_units=128, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=128, voltage_v=0.65)

def point_481() -> DesignPoint:
    return DesignPoint("point_481", mac_units=160, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=192, voltage_v=0.68)

def point_482() -> DesignPoint:
    return DesignPoint("point_482", mac_units=192, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=256, voltage_v=0.71)

def point_483() -> DesignPoint:
    return DesignPoint("point_483", mac_units=224, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=320, voltage_v=0.74)

def point_484() -> DesignPoint:
    return DesignPoint("point_484", mac_units=256, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=384, voltage_v=0.77)

def point_485() -> DesignPoint:
    return DesignPoint("point_485", mac_units=288, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=448, voltage_v=0.80)

def point_486() -> DesignPoint:
    return DesignPoint("point_486", mac_units=320, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=512, voltage_v=0.83)

def point_487() -> DesignPoint:
    return DesignPoint("point_487", mac_units=352, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=576, voltage_v=0.86)

def point_488() -> DesignPoint:
    return DesignPoint("point_488", mac_units=384, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=640, voltage_v=0.89)

def point_489() -> DesignPoint:
    return DesignPoint("point_489", mac_units=416, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=704, voltage_v=0.92)

def point_490() -> DesignPoint:
    return DesignPoint("point_490", mac_units=448, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=768, voltage_v=0.65)

def point_491() -> DesignPoint:
    return DesignPoint("point_491", mac_units=480, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=832, voltage_v=0.68)

def point_492() -> DesignPoint:
    return DesignPoint("point_492", mac_units=512, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=896, voltage_v=0.71)

def point_493() -> DesignPoint:
    return DesignPoint("point_493", mac_units=544, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=960, voltage_v=0.74)

def point_494() -> DesignPoint:
    return DesignPoint("point_494", mac_units=576, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.77)

def point_495() -> DesignPoint:
    return DesignPoint("point_495", mac_units=608, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.80)

def point_496() -> DesignPoint:
    return DesignPoint("point_496", mac_units=640, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=128, voltage_v=0.83)

def point_497() -> DesignPoint:
    return DesignPoint("point_497", mac_units=672, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=192, voltage_v=0.86)

def point_498() -> DesignPoint:
    return DesignPoint("point_498", mac_units=704, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=256, voltage_v=0.89)

def point_499() -> DesignPoint:
    return DesignPoint("point_499", mac_units=736, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=320, voltage_v=0.92)

def point_500() -> DesignPoint:
    return DesignPoint("point_500", mac_units=768, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=384, voltage_v=0.65)

def point_501() -> DesignPoint:
    return DesignPoint("point_501", mac_units=800, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=448, voltage_v=0.68)

def point_502() -> DesignPoint:
    return DesignPoint("point_502", mac_units=832, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=512, voltage_v=0.71)

def point_503() -> DesignPoint:
    return DesignPoint("point_503", mac_units=864, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=576, voltage_v=0.74)

def point_504() -> DesignPoint:
    return DesignPoint("point_504", mac_units=896, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=640, voltage_v=0.77)

def point_505() -> DesignPoint:
    return DesignPoint("point_505", mac_units=928, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=704, voltage_v=0.80)

def point_506() -> DesignPoint:
    return DesignPoint("point_506", mac_units=960, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=768, voltage_v=0.83)

def point_507() -> DesignPoint:
    return DesignPoint("point_507", mac_units=992, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=832, voltage_v=0.86)

def point_508() -> DesignPoint:
    return DesignPoint("point_508", mac_units=1024, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=896, voltage_v=0.89)

def point_509() -> DesignPoint:
    return DesignPoint("point_509", mac_units=1056, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=960, voltage_v=0.92)

def point_510() -> DesignPoint:
    return DesignPoint("point_510", mac_units=1088, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.65)

def point_511() -> DesignPoint:
    return DesignPoint("point_511", mac_units=1120, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.68)

def point_512() -> DesignPoint:
    return DesignPoint("point_512", mac_units=128, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=128, voltage_v=0.71)

def point_513() -> DesignPoint:
    return DesignPoint("point_513", mac_units=160, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=192, voltage_v=0.74)

def point_514() -> DesignPoint:
    return DesignPoint("point_514", mac_units=192, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=256, voltage_v=0.77)

def point_515() -> DesignPoint:
    return DesignPoint("point_515", mac_units=224, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=320, voltage_v=0.80)

def point_516() -> DesignPoint:
    return DesignPoint("point_516", mac_units=256, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=384, voltage_v=0.83)

def point_517() -> DesignPoint:
    return DesignPoint("point_517", mac_units=288, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=448, voltage_v=0.86)

def point_518() -> DesignPoint:
    return DesignPoint("point_518", mac_units=320, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=512, voltage_v=0.89)

def point_519() -> DesignPoint:
    return DesignPoint("point_519", mac_units=352, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=576, voltage_v=0.92)

def point_520() -> DesignPoint:
    return DesignPoint("point_520", mac_units=384, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=640, voltage_v=0.65)

def point_521() -> DesignPoint:
    return DesignPoint("point_521", mac_units=416, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=704, voltage_v=0.68)

def point_522() -> DesignPoint:
    return DesignPoint("point_522", mac_units=448, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=768, voltage_v=0.71)

def point_523() -> DesignPoint:
    return DesignPoint("point_523", mac_units=480, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=832, voltage_v=0.74)

def point_524() -> DesignPoint:
    return DesignPoint("point_524", mac_units=512, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=896, voltage_v=0.77)

def point_525() -> DesignPoint:
    return DesignPoint("point_525", mac_units=544, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=960, voltage_v=0.80)

def point_526() -> DesignPoint:
    return DesignPoint("point_526", mac_units=576, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.83)

def point_527() -> DesignPoint:
    return DesignPoint("point_527", mac_units=608, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.86)

def point_528() -> DesignPoint:
    return DesignPoint("point_528", mac_units=640, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=128, voltage_v=0.89)

def point_529() -> DesignPoint:
    return DesignPoint("point_529", mac_units=672, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=192, voltage_v=0.92)

def point_530() -> DesignPoint:
    return DesignPoint("point_530", mac_units=704, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=256, voltage_v=0.65)

def point_531() -> DesignPoint:
    return DesignPoint("point_531", mac_units=736, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=320, voltage_v=0.68)

def point_532() -> DesignPoint:
    return DesignPoint("point_532", mac_units=768, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=384, voltage_v=0.71)

def point_533() -> DesignPoint:
    return DesignPoint("point_533", mac_units=800, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=448, voltage_v=0.74)

def point_534() -> DesignPoint:
    return DesignPoint("point_534", mac_units=832, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=512, voltage_v=0.77)

def point_535() -> DesignPoint:
    return DesignPoint("point_535", mac_units=864, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=576, voltage_v=0.80)

def point_536() -> DesignPoint:
    return DesignPoint("point_536", mac_units=896, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=640, voltage_v=0.83)

def point_537() -> DesignPoint:
    return DesignPoint("point_537", mac_units=928, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=704, voltage_v=0.86)

def point_538() -> DesignPoint:
    return DesignPoint("point_538", mac_units=960, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=768, voltage_v=0.89)

def point_539() -> DesignPoint:
    return DesignPoint("point_539", mac_units=992, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=832, voltage_v=0.92)

def point_540() -> DesignPoint:
    return DesignPoint("point_540", mac_units=1024, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=896, voltage_v=0.65)

def point_541() -> DesignPoint:
    return DesignPoint("point_541", mac_units=1056, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=960, voltage_v=0.68)

def point_542() -> DesignPoint:
    return DesignPoint("point_542", mac_units=1088, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.71)

def point_543() -> DesignPoint:
    return DesignPoint("point_543", mac_units=1120, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.74)

def point_544() -> DesignPoint:
    return DesignPoint("point_544", mac_units=128, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=128, voltage_v=0.77)

def point_545() -> DesignPoint:
    return DesignPoint("point_545", mac_units=160, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=192, voltage_v=0.80)

def point_546() -> DesignPoint:
    return DesignPoint("point_546", mac_units=192, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=256, voltage_v=0.83)

def point_547() -> DesignPoint:
    return DesignPoint("point_547", mac_units=224, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=320, voltage_v=0.86)

def point_548() -> DesignPoint:
    return DesignPoint("point_548", mac_units=256, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=384, voltage_v=0.89)

def point_549() -> DesignPoint:
    return DesignPoint("point_549", mac_units=288, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=448, voltage_v=0.92)

def point_550() -> DesignPoint:
    return DesignPoint("point_550", mac_units=320, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=512, voltage_v=0.65)

def point_551() -> DesignPoint:
    return DesignPoint("point_551", mac_units=352, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=576, voltage_v=0.68)

def point_552() -> DesignPoint:
    return DesignPoint("point_552", mac_units=384, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=640, voltage_v=0.71)

def point_553() -> DesignPoint:
    return DesignPoint("point_553", mac_units=416, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=704, voltage_v=0.74)

def point_554() -> DesignPoint:
    return DesignPoint("point_554", mac_units=448, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=768, voltage_v=0.77)

def point_555() -> DesignPoint:
    return DesignPoint("point_555", mac_units=480, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=832, voltage_v=0.80)

def point_556() -> DesignPoint:
    return DesignPoint("point_556", mac_units=512, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=896, voltage_v=0.83)

def point_557() -> DesignPoint:
    return DesignPoint("point_557", mac_units=544, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=960, voltage_v=0.86)

def point_558() -> DesignPoint:
    return DesignPoint("point_558", mac_units=576, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.89)

def point_559() -> DesignPoint:
    return DesignPoint("point_559", mac_units=608, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.92)

def point_560() -> DesignPoint:
    return DesignPoint("point_560", mac_units=640, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=128, voltage_v=0.65)

def point_561() -> DesignPoint:
    return DesignPoint("point_561", mac_units=672, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=192, voltage_v=0.68)

def point_562() -> DesignPoint:
    return DesignPoint("point_562", mac_units=704, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=256, voltage_v=0.71)

def point_563() -> DesignPoint:
    return DesignPoint("point_563", mac_units=736, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=320, voltage_v=0.74)

def point_564() -> DesignPoint:
    return DesignPoint("point_564", mac_units=768, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=384, voltage_v=0.77)

def point_565() -> DesignPoint:
    return DesignPoint("point_565", mac_units=800, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=448, voltage_v=0.80)

def point_566() -> DesignPoint:
    return DesignPoint("point_566", mac_units=832, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=512, voltage_v=0.83)

def point_567() -> DesignPoint:
    return DesignPoint("point_567", mac_units=864, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=576, voltage_v=0.86)

def point_568() -> DesignPoint:
    return DesignPoint("point_568", mac_units=896, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=640, voltage_v=0.89)

def point_569() -> DesignPoint:
    return DesignPoint("point_569", mac_units=928, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=704, voltage_v=0.92)

def point_570() -> DesignPoint:
    return DesignPoint("point_570", mac_units=960, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=768, voltage_v=0.65)

def point_571() -> DesignPoint:
    return DesignPoint("point_571", mac_units=992, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=832, voltage_v=0.68)

def point_572() -> DesignPoint:
    return DesignPoint("point_572", mac_units=1024, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=896, voltage_v=0.71)

def point_573() -> DesignPoint:
    return DesignPoint("point_573", mac_units=1056, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=960, voltage_v=0.74)

def point_574() -> DesignPoint:
    return DesignPoint("point_574", mac_units=1088, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.77)

def point_575() -> DesignPoint:
    return DesignPoint("point_575", mac_units=1120, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.80)

def point_576() -> DesignPoint:
    return DesignPoint("point_576", mac_units=128, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=128, voltage_v=0.83)

def point_577() -> DesignPoint:
    return DesignPoint("point_577", mac_units=160, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=192, voltage_v=0.86)

def point_578() -> DesignPoint:
    return DesignPoint("point_578", mac_units=192, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=256, voltage_v=0.89)

def point_579() -> DesignPoint:
    return DesignPoint("point_579", mac_units=224, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=320, voltage_v=0.92)

def point_580() -> DesignPoint:
    return DesignPoint("point_580", mac_units=256, frequency_ghz=0.600, bandwidth_gbps=128, sram_kb=384, voltage_v=0.65)

def point_581() -> DesignPoint:
    return DesignPoint("point_581", mac_units=288, frequency_ghz=0.650, bandwidth_gbps=144, sram_kb=448, voltage_v=0.68)

def point_582() -> DesignPoint:
    return DesignPoint("point_582", mac_units=320, frequency_ghz=0.700, bandwidth_gbps=160, sram_kb=512, voltage_v=0.71)

def point_583() -> DesignPoint:
    return DesignPoint("point_583", mac_units=352, frequency_ghz=0.750, bandwidth_gbps=176, sram_kb=576, voltage_v=0.74)

def point_584() -> DesignPoint:
    return DesignPoint("point_584", mac_units=384, frequency_ghz=0.800, bandwidth_gbps=192, sram_kb=640, voltage_v=0.77)

def point_585() -> DesignPoint:
    return DesignPoint("point_585", mac_units=416, frequency_ghz=0.850, bandwidth_gbps=208, sram_kb=704, voltage_v=0.80)

def point_586() -> DesignPoint:
    return DesignPoint("point_586", mac_units=448, frequency_ghz=0.900, bandwidth_gbps=224, sram_kb=768, voltage_v=0.83)

def point_587() -> DesignPoint:
    return DesignPoint("point_587", mac_units=480, frequency_ghz=0.950, bandwidth_gbps=240, sram_kb=832, voltage_v=0.86)

def point_588() -> DesignPoint:
    return DesignPoint("point_588", mac_units=512, frequency_ghz=1.000, bandwidth_gbps=256, sram_kb=896, voltage_v=0.89)

def point_589() -> DesignPoint:
    return DesignPoint("point_589", mac_units=544, frequency_ghz=1.050, bandwidth_gbps=272, sram_kb=960, voltage_v=0.92)

def point_590() -> DesignPoint:
    return DesignPoint("point_590", mac_units=576, frequency_ghz=1.100, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.65)

def point_591() -> DesignPoint:
    return DesignPoint("point_591", mac_units=608, frequency_ghz=1.150, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.68)

def point_592() -> DesignPoint:
    return DesignPoint("point_592", mac_units=640, frequency_ghz=1.200, bandwidth_gbps=320, sram_kb=128, voltage_v=0.71)

def point_593() -> DesignPoint:
    return DesignPoint("point_593", mac_units=672, frequency_ghz=1.250, bandwidth_gbps=336, sram_kb=192, voltage_v=0.74)

def point_594() -> DesignPoint:
    return DesignPoint("point_594", mac_units=704, frequency_ghz=1.300, bandwidth_gbps=352, sram_kb=256, voltage_v=0.77)

def point_595() -> DesignPoint:
    return DesignPoint("point_595", mac_units=736, frequency_ghz=1.350, bandwidth_gbps=368, sram_kb=320, voltage_v=0.80)

def point_596() -> DesignPoint:
    return DesignPoint("point_596", mac_units=768, frequency_ghz=1.400, bandwidth_gbps=384, sram_kb=384, voltage_v=0.83)

def point_597() -> DesignPoint:
    return DesignPoint("point_597", mac_units=800, frequency_ghz=1.450, bandwidth_gbps=400, sram_kb=448, voltage_v=0.86)

def point_598() -> DesignPoint:
    return DesignPoint("point_598", mac_units=832, frequency_ghz=1.500, bandwidth_gbps=416, sram_kb=512, voltage_v=0.89)

def point_599() -> DesignPoint:
    return DesignPoint("point_599", mac_units=864, frequency_ghz=1.550, bandwidth_gbps=432, sram_kb=576, voltage_v=0.92)

def point_600() -> DesignPoint:
    return DesignPoint("point_600", mac_units=896, frequency_ghz=0.600, bandwidth_gbps=64, sram_kb=640, voltage_v=0.65)

def point_601() -> DesignPoint:
    return DesignPoint("point_601", mac_units=928, frequency_ghz=0.650, bandwidth_gbps=80, sram_kb=704, voltage_v=0.68)

def point_602() -> DesignPoint:
    return DesignPoint("point_602", mac_units=960, frequency_ghz=0.700, bandwidth_gbps=96, sram_kb=768, voltage_v=0.71)

def point_603() -> DesignPoint:
    return DesignPoint("point_603", mac_units=992, frequency_ghz=0.750, bandwidth_gbps=112, sram_kb=832, voltage_v=0.74)

def point_604() -> DesignPoint:
    return DesignPoint("point_604", mac_units=1024, frequency_ghz=0.800, bandwidth_gbps=128, sram_kb=896, voltage_v=0.77)

def point_605() -> DesignPoint:
    return DesignPoint("point_605", mac_units=1056, frequency_ghz=0.850, bandwidth_gbps=144, sram_kb=960, voltage_v=0.80)

def point_606() -> DesignPoint:
    return DesignPoint("point_606", mac_units=1088, frequency_ghz=0.900, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.83)

def point_607() -> DesignPoint:
    return DesignPoint("point_607", mac_units=1120, frequency_ghz=0.950, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.86)

def point_608() -> DesignPoint:
    return DesignPoint("point_608", mac_units=128, frequency_ghz=1.000, bandwidth_gbps=192, sram_kb=128, voltage_v=0.89)

def point_609() -> DesignPoint:
    return DesignPoint("point_609", mac_units=160, frequency_ghz=1.050, bandwidth_gbps=208, sram_kb=192, voltage_v=0.92)

def point_610() -> DesignPoint:
    return DesignPoint("point_610", mac_units=192, frequency_ghz=1.100, bandwidth_gbps=224, sram_kb=256, voltage_v=0.65)

def point_611() -> DesignPoint:
    return DesignPoint("point_611", mac_units=224, frequency_ghz=1.150, bandwidth_gbps=240, sram_kb=320, voltage_v=0.68)

def point_612() -> DesignPoint:
    return DesignPoint("point_612", mac_units=256, frequency_ghz=1.200, bandwidth_gbps=256, sram_kb=384, voltage_v=0.71)

def point_613() -> DesignPoint:
    return DesignPoint("point_613", mac_units=288, frequency_ghz=1.250, bandwidth_gbps=272, sram_kb=448, voltage_v=0.74)

def point_614() -> DesignPoint:
    return DesignPoint("point_614", mac_units=320, frequency_ghz=1.300, bandwidth_gbps=288, sram_kb=512, voltage_v=0.77)

def point_615() -> DesignPoint:
    return DesignPoint("point_615", mac_units=352, frequency_ghz=1.350, bandwidth_gbps=304, sram_kb=576, voltage_v=0.80)

def point_616() -> DesignPoint:
    return DesignPoint("point_616", mac_units=384, frequency_ghz=1.400, bandwidth_gbps=320, sram_kb=640, voltage_v=0.83)

def point_617() -> DesignPoint:
    return DesignPoint("point_617", mac_units=416, frequency_ghz=1.450, bandwidth_gbps=336, sram_kb=704, voltage_v=0.86)

def point_618() -> DesignPoint:
    return DesignPoint("point_618", mac_units=448, frequency_ghz=1.500, bandwidth_gbps=352, sram_kb=768, voltage_v=0.89)

def point_619() -> DesignPoint:
    return DesignPoint("point_619", mac_units=480, frequency_ghz=1.550, bandwidth_gbps=368, sram_kb=832, voltage_v=0.92)

def point_620() -> DesignPoint:
    return DesignPoint("point_620", mac_units=512, frequency_ghz=0.600, bandwidth_gbps=384, sram_kb=896, voltage_v=0.65)

def point_621() -> DesignPoint:
    return DesignPoint("point_621", mac_units=544, frequency_ghz=0.650, bandwidth_gbps=400, sram_kb=960, voltage_v=0.68)

def point_622() -> DesignPoint:
    return DesignPoint("point_622", mac_units=576, frequency_ghz=0.700, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.71)

def point_623() -> DesignPoint:
    return DesignPoint("point_623", mac_units=608, frequency_ghz=0.750, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.74)

def point_624() -> DesignPoint:
    return DesignPoint("point_624", mac_units=640, frequency_ghz=0.800, bandwidth_gbps=64, sram_kb=128, voltage_v=0.77)

def point_625() -> DesignPoint:
    return DesignPoint("point_625", mac_units=672, frequency_ghz=0.850, bandwidth_gbps=80, sram_kb=192, voltage_v=0.80)

def point_626() -> DesignPoint:
    return DesignPoint("point_626", mac_units=704, frequency_ghz=0.900, bandwidth_gbps=96, sram_kb=256, voltage_v=0.83)

def point_627() -> DesignPoint:
    return DesignPoint("point_627", mac_units=736, frequency_ghz=0.950, bandwidth_gbps=112, sram_kb=320, voltage_v=0.86)

def point_628() -> DesignPoint:
    return DesignPoint("point_628", mac_units=768, frequency_ghz=1.000, bandwidth_gbps=128, sram_kb=384, voltage_v=0.89)

def point_629() -> DesignPoint:
    return DesignPoint("point_629", mac_units=800, frequency_ghz=1.050, bandwidth_gbps=144, sram_kb=448, voltage_v=0.92)

def point_630() -> DesignPoint:
    return DesignPoint("point_630", mac_units=832, frequency_ghz=1.100, bandwidth_gbps=160, sram_kb=512, voltage_v=0.65)

def point_631() -> DesignPoint:
    return DesignPoint("point_631", mac_units=864, frequency_ghz=1.150, bandwidth_gbps=176, sram_kb=576, voltage_v=0.68)

def point_632() -> DesignPoint:
    return DesignPoint("point_632", mac_units=896, frequency_ghz=1.200, bandwidth_gbps=192, sram_kb=640, voltage_v=0.71)

def point_633() -> DesignPoint:
    return DesignPoint("point_633", mac_units=928, frequency_ghz=1.250, bandwidth_gbps=208, sram_kb=704, voltage_v=0.74)

def point_634() -> DesignPoint:
    return DesignPoint("point_634", mac_units=960, frequency_ghz=1.300, bandwidth_gbps=224, sram_kb=768, voltage_v=0.77)

def point_635() -> DesignPoint:
    return DesignPoint("point_635", mac_units=992, frequency_ghz=1.350, bandwidth_gbps=240, sram_kb=832, voltage_v=0.80)

def point_636() -> DesignPoint:
    return DesignPoint("point_636", mac_units=1024, frequency_ghz=1.400, bandwidth_gbps=256, sram_kb=896, voltage_v=0.83)

def point_637() -> DesignPoint:
    return DesignPoint("point_637", mac_units=1056, frequency_ghz=1.450, bandwidth_gbps=272, sram_kb=960, voltage_v=0.86)

def point_638() -> DesignPoint:
    return DesignPoint("point_638", mac_units=1088, frequency_ghz=1.500, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.89)

def point_639() -> DesignPoint:
    return DesignPoint("point_639", mac_units=1120, frequency_ghz=1.550, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.92)

def point_640() -> DesignPoint:
    return DesignPoint("point_640", mac_units=128, frequency_ghz=0.600, bandwidth_gbps=320, sram_kb=128, voltage_v=0.65)

def point_641() -> DesignPoint:
    return DesignPoint("point_641", mac_units=160, frequency_ghz=0.650, bandwidth_gbps=336, sram_kb=192, voltage_v=0.68)

def point_642() -> DesignPoint:
    return DesignPoint("point_642", mac_units=192, frequency_ghz=0.700, bandwidth_gbps=352, sram_kb=256, voltage_v=0.71)

def point_643() -> DesignPoint:
    return DesignPoint("point_643", mac_units=224, frequency_ghz=0.750, bandwidth_gbps=368, sram_kb=320, voltage_v=0.74)

def point_644() -> DesignPoint:
    return DesignPoint("point_644", mac_units=256, frequency_ghz=0.800, bandwidth_gbps=384, sram_kb=384, voltage_v=0.77)

def point_645() -> DesignPoint:
    return DesignPoint("point_645", mac_units=288, frequency_ghz=0.850, bandwidth_gbps=400, sram_kb=448, voltage_v=0.80)

def point_646() -> DesignPoint:
    return DesignPoint("point_646", mac_units=320, frequency_ghz=0.900, bandwidth_gbps=416, sram_kb=512, voltage_v=0.83)

def point_647() -> DesignPoint:
    return DesignPoint("point_647", mac_units=352, frequency_ghz=0.950, bandwidth_gbps=432, sram_kb=576, voltage_v=0.86)

def point_648() -> DesignPoint:
    return DesignPoint("point_648", mac_units=384, frequency_ghz=1.000, bandwidth_gbps=64, sram_kb=640, voltage_v=0.89)

def point_649() -> DesignPoint:
    return DesignPoint("point_649", mac_units=416, frequency_ghz=1.050, bandwidth_gbps=80, sram_kb=704, voltage_v=0.92)

def point_650() -> DesignPoint:
    return DesignPoint("point_650", mac_units=448, frequency_ghz=1.100, bandwidth_gbps=96, sram_kb=768, voltage_v=0.65)

def point_651() -> DesignPoint:
    return DesignPoint("point_651", mac_units=480, frequency_ghz=1.150, bandwidth_gbps=112, sram_kb=832, voltage_v=0.68)

def point_652() -> DesignPoint:
    return DesignPoint("point_652", mac_units=512, frequency_ghz=1.200, bandwidth_gbps=128, sram_kb=896, voltage_v=0.71)

def point_653() -> DesignPoint:
    return DesignPoint("point_653", mac_units=544, frequency_ghz=1.250, bandwidth_gbps=144, sram_kb=960, voltage_v=0.74)

def point_654() -> DesignPoint:
    return DesignPoint("point_654", mac_units=576, frequency_ghz=1.300, bandwidth_gbps=160, sram_kb=1024, voltage_v=0.77)

def point_655() -> DesignPoint:
    return DesignPoint("point_655", mac_units=608, frequency_ghz=1.350, bandwidth_gbps=176, sram_kb=1088, voltage_v=0.80)

def point_656() -> DesignPoint:
    return DesignPoint("point_656", mac_units=640, frequency_ghz=1.400, bandwidth_gbps=192, sram_kb=128, voltage_v=0.83)

def point_657() -> DesignPoint:
    return DesignPoint("point_657", mac_units=672, frequency_ghz=1.450, bandwidth_gbps=208, sram_kb=192, voltage_v=0.86)

def point_658() -> DesignPoint:
    return DesignPoint("point_658", mac_units=704, frequency_ghz=1.500, bandwidth_gbps=224, sram_kb=256, voltage_v=0.89)

def point_659() -> DesignPoint:
    return DesignPoint("point_659", mac_units=736, frequency_ghz=1.550, bandwidth_gbps=240, sram_kb=320, voltage_v=0.92)

def point_660() -> DesignPoint:
    return DesignPoint("point_660", mac_units=768, frequency_ghz=0.600, bandwidth_gbps=256, sram_kb=384, voltage_v=0.65)

def point_661() -> DesignPoint:
    return DesignPoint("point_661", mac_units=800, frequency_ghz=0.650, bandwidth_gbps=272, sram_kb=448, voltage_v=0.68)

def point_662() -> DesignPoint:
    return DesignPoint("point_662", mac_units=832, frequency_ghz=0.700, bandwidth_gbps=288, sram_kb=512, voltage_v=0.71)

def point_663() -> DesignPoint:
    return DesignPoint("point_663", mac_units=864, frequency_ghz=0.750, bandwidth_gbps=304, sram_kb=576, voltage_v=0.74)

def point_664() -> DesignPoint:
    return DesignPoint("point_664", mac_units=896, frequency_ghz=0.800, bandwidth_gbps=320, sram_kb=640, voltage_v=0.77)

def point_665() -> DesignPoint:
    return DesignPoint("point_665", mac_units=928, frequency_ghz=0.850, bandwidth_gbps=336, sram_kb=704, voltage_v=0.80)

def point_666() -> DesignPoint:
    return DesignPoint("point_666", mac_units=960, frequency_ghz=0.900, bandwidth_gbps=352, sram_kb=768, voltage_v=0.83)

def point_667() -> DesignPoint:
    return DesignPoint("point_667", mac_units=992, frequency_ghz=0.950, bandwidth_gbps=368, sram_kb=832, voltage_v=0.86)

def point_668() -> DesignPoint:
    return DesignPoint("point_668", mac_units=1024, frequency_ghz=1.000, bandwidth_gbps=384, sram_kb=896, voltage_v=0.89)

def point_669() -> DesignPoint:
    return DesignPoint("point_669", mac_units=1056, frequency_ghz=1.050, bandwidth_gbps=400, sram_kb=960, voltage_v=0.92)

def point_670() -> DesignPoint:
    return DesignPoint("point_670", mac_units=1088, frequency_ghz=1.100, bandwidth_gbps=416, sram_kb=1024, voltage_v=0.65)

def point_671() -> DesignPoint:
    return DesignPoint("point_671", mac_units=1120, frequency_ghz=1.150, bandwidth_gbps=432, sram_kb=1088, voltage_v=0.68)

def point_672() -> DesignPoint:
    return DesignPoint("point_672", mac_units=128, frequency_ghz=1.200, bandwidth_gbps=64, sram_kb=128, voltage_v=0.71)

def point_673() -> DesignPoint:
    return DesignPoint("point_673", mac_units=160, frequency_ghz=1.250, bandwidth_gbps=80, sram_kb=192, voltage_v=0.74)

def point_674() -> DesignPoint:
    return DesignPoint("point_674", mac_units=192, frequency_ghz=1.300, bandwidth_gbps=96, sram_kb=256, voltage_v=0.77)

def point_675() -> DesignPoint:
    return DesignPoint("point_675", mac_units=224, frequency_ghz=1.350, bandwidth_gbps=112, sram_kb=320, voltage_v=0.80)

def point_676() -> DesignPoint:
    return DesignPoint("point_676", mac_units=256, frequency_ghz=1.400, bandwidth_gbps=128, sram_kb=384, voltage_v=0.83)

def point_677() -> DesignPoint:
    return DesignPoint("point_677", mac_units=288, frequency_ghz=1.450, bandwidth_gbps=144, sram_kb=448, voltage_v=0.86)

def point_678() -> DesignPoint:
    return DesignPoint("point_678", mac_units=320, frequency_ghz=1.500, bandwidth_gbps=160, sram_kb=512, voltage_v=0.89)

def point_679() -> DesignPoint:
    return DesignPoint("point_679", mac_units=352, frequency_ghz=1.550, bandwidth_gbps=176, sram_kb=576, voltage_v=0.92)

def point_680() -> DesignPoint:
    return DesignPoint("point_680", mac_units=384, frequency_ghz=0.600, bandwidth_gbps=192, sram_kb=640, voltage_v=0.65)

def point_681() -> DesignPoint:
    return DesignPoint("point_681", mac_units=416, frequency_ghz=0.650, bandwidth_gbps=208, sram_kb=704, voltage_v=0.68)

def point_682() -> DesignPoint:
    return DesignPoint("point_682", mac_units=448, frequency_ghz=0.700, bandwidth_gbps=224, sram_kb=768, voltage_v=0.71)

def point_683() -> DesignPoint:
    return DesignPoint("point_683", mac_units=480, frequency_ghz=0.750, bandwidth_gbps=240, sram_kb=832, voltage_v=0.74)

def point_684() -> DesignPoint:
    return DesignPoint("point_684", mac_units=512, frequency_ghz=0.800, bandwidth_gbps=256, sram_kb=896, voltage_v=0.77)

def point_685() -> DesignPoint:
    return DesignPoint("point_685", mac_units=544, frequency_ghz=0.850, bandwidth_gbps=272, sram_kb=960, voltage_v=0.80)

def point_686() -> DesignPoint:
    return DesignPoint("point_686", mac_units=576, frequency_ghz=0.900, bandwidth_gbps=288, sram_kb=1024, voltage_v=0.83)

def point_687() -> DesignPoint:
    return DesignPoint("point_687", mac_units=608, frequency_ghz=0.950, bandwidth_gbps=304, sram_kb=1088, voltage_v=0.86)

def point_688() -> DesignPoint:
    return DesignPoint("point_688", mac_units=640, frequency_ghz=1.000, bandwidth_gbps=320, sram_kb=128, voltage_v=0.89)

def point_689() -> DesignPoint:
    return DesignPoint("point_689", mac_units=672, frequency_ghz=1.050, bandwidth_gbps=336, sram_kb=192, voltage_v=0.92)

def point_690() -> DesignPoint:
    return DesignPoint("point_690", mac_units=704, frequency_ghz=1.100, bandwidth_gbps=352, sram_kb=256, voltage_v=0.65)

def point_691() -> DesignPoint:
    return DesignPoint("point_691", mac_units=736, frequency_ghz=1.150, bandwidth_gbps=368, sram_kb=320, voltage_v=0.68)

def point_692() -> DesignPoint:
    return DesignPoint("point_692", mac_units=768, frequency_ghz=1.200, bandwidth_gbps=384, sram_kb=384, voltage_v=0.71)

def point_693() -> DesignPoint:
    return DesignPoint("point_693", mac_units=800, frequency_ghz=1.250, bandwidth_gbps=400, sram_kb=448, voltage_v=0.74)

def point_694() -> DesignPoint:
    return DesignPoint("point_694", mac_units=832, frequency_ghz=1.300, bandwidth_gbps=416, sram_kb=512, voltage_v=0.77)

def point_695() -> DesignPoint:
    return DesignPoint("point_695", mac_units=864, frequency_ghz=1.350, bandwidth_gbps=432, sram_kb=576, voltage_v=0.80)

def point_696() -> DesignPoint:
    return DesignPoint("point_696", mac_units=896, frequency_ghz=1.400, bandwidth_gbps=64, sram_kb=640, voltage_v=0.83)

def point_697() -> DesignPoint:
    return DesignPoint("point_697", mac_units=928, frequency_ghz=1.450, bandwidth_gbps=80, sram_kb=704, voltage_v=0.86)

def point_698() -> DesignPoint:
    return DesignPoint("point_698", mac_units=960, frequency_ghz=1.500, bandwidth_gbps=96, sram_kb=768, voltage_v=0.89)

def point_699() -> DesignPoint:
    return DesignPoint("point_699", mac_units=992, frequency_ghz=1.550, bandwidth_gbps=112, sram_kb=832, voltage_v=0.92)

def all_points() -> list[DesignPoint]:
    return [
        point_0(),
        point_1(),
        point_2(),
        point_3(),
        point_4(),
        point_5(),
        point_6(),
        point_7(),
        point_8(),
        point_9(),
        point_10(),
        point_11(),
        point_12(),
        point_13(),
        point_14(),
        point_15(),
        point_16(),
        point_17(),
        point_18(),
        point_19(),
        point_20(),
        point_21(),
        point_22(),
        point_23(),
        point_24(),
        point_25(),
        point_26(),
        point_27(),
        point_28(),
        point_29(),
        point_30(),
        point_31(),
        point_32(),
        point_33(),
        point_34(),
        point_35(),
        point_36(),
        point_37(),
        point_38(),
        point_39(),
        point_40(),
        point_41(),
        point_42(),
        point_43(),
        point_44(),
        point_45(),
        point_46(),
        point_47(),
        point_48(),
        point_49(),
        point_50(),
        point_51(),
        point_52(),
        point_53(),
        point_54(),
        point_55(),
        point_56(),
        point_57(),
        point_58(),
        point_59(),
        point_60(),
        point_61(),
        point_62(),
        point_63(),
        point_64(),
        point_65(),
        point_66(),
        point_67(),
        point_68(),
        point_69(),
        point_70(),
        point_71(),
        point_72(),
        point_73(),
        point_74(),
        point_75(),
        point_76(),
        point_77(),
        point_78(),
        point_79(),
        point_80(),
        point_81(),
        point_82(),
        point_83(),
        point_84(),
        point_85(),
        point_86(),
        point_87(),
        point_88(),
        point_89(),
        point_90(),
        point_91(),
        point_92(),
        point_93(),
        point_94(),
        point_95(),
        point_96(),
        point_97(),
        point_98(),
        point_99(),
        point_100(),
        point_101(),
        point_102(),
        point_103(),
        point_104(),
        point_105(),
        point_106(),
        point_107(),
        point_108(),
        point_109(),
        point_110(),
        point_111(),
        point_112(),
        point_113(),
        point_114(),
        point_115(),
        point_116(),
        point_117(),
        point_118(),
        point_119(),
        point_120(),
        point_121(),
        point_122(),
        point_123(),
        point_124(),
        point_125(),
        point_126(),
        point_127(),
        point_128(),
        point_129(),
        point_130(),
        point_131(),
        point_132(),
        point_133(),
        point_134(),
        point_135(),
        point_136(),
        point_137(),
        point_138(),
        point_139(),
        point_140(),
        point_141(),
        point_142(),
        point_143(),
        point_144(),
        point_145(),
        point_146(),
        point_147(),
        point_148(),
        point_149(),
        point_150(),
        point_151(),
        point_152(),
        point_153(),
        point_154(),
        point_155(),
        point_156(),
        point_157(),
        point_158(),
        point_159(),
        point_160(),
        point_161(),
        point_162(),
        point_163(),
        point_164(),
        point_165(),
        point_166(),
        point_167(),
        point_168(),
        point_169(),
        point_170(),
        point_171(),
        point_172(),
        point_173(),
        point_174(),
        point_175(),
        point_176(),
        point_177(),
        point_178(),
        point_179(),
        point_180(),
        point_181(),
        point_182(),
        point_183(),
        point_184(),
        point_185(),
        point_186(),
        point_187(),
        point_188(),
        point_189(),
        point_190(),
        point_191(),
        point_192(),
        point_193(),
        point_194(),
        point_195(),
        point_196(),
        point_197(),
        point_198(),
        point_199(),
        point_200(),
        point_201(),
        point_202(),
        point_203(),
        point_204(),
        point_205(),
        point_206(),
        point_207(),
        point_208(),
        point_209(),
        point_210(),
        point_211(),
        point_212(),
        point_213(),
        point_214(),
        point_215(),
        point_216(),
        point_217(),
        point_218(),
        point_219(),
        point_220(),
        point_221(),
        point_222(),
        point_223(),
        point_224(),
        point_225(),
        point_226(),
        point_227(),
        point_228(),
        point_229(),
        point_230(),
        point_231(),
        point_232(),
        point_233(),
        point_234(),
        point_235(),
        point_236(),
        point_237(),
        point_238(),
        point_239(),
        point_240(),
        point_241(),
        point_242(),
        point_243(),
        point_244(),
        point_245(),
        point_246(),
        point_247(),
        point_248(),
        point_249(),
        point_250(),
        point_251(),
        point_252(),
        point_253(),
        point_254(),
        point_255(),
        point_256(),
        point_257(),
        point_258(),
        point_259(),
        point_260(),
        point_261(),
        point_262(),
        point_263(),
        point_264(),
        point_265(),
        point_266(),
        point_267(),
        point_268(),
        point_269(),
        point_270(),
        point_271(),
        point_272(),
        point_273(),
        point_274(),
        point_275(),
        point_276(),
        point_277(),
        point_278(),
        point_279(),
        point_280(),
        point_281(),
        point_282(),
        point_283(),
        point_284(),
        point_285(),
        point_286(),
        point_287(),
        point_288(),
        point_289(),
        point_290(),
        point_291(),
        point_292(),
        point_293(),
        point_294(),
        point_295(),
        point_296(),
        point_297(),
        point_298(),
        point_299(),
        point_300(),
        point_301(),
        point_302(),
        point_303(),
        point_304(),
        point_305(),
        point_306(),
        point_307(),
        point_308(),
        point_309(),
        point_310(),
        point_311(),
        point_312(),
        point_313(),
        point_314(),
        point_315(),
        point_316(),
        point_317(),
        point_318(),
        point_319(),
        point_320(),
        point_321(),
        point_322(),
        point_323(),
        point_324(),
        point_325(),
        point_326(),
        point_327(),
        point_328(),
        point_329(),
        point_330(),
        point_331(),
        point_332(),
        point_333(),
        point_334(),
        point_335(),
        point_336(),
        point_337(),
        point_338(),
        point_339(),
        point_340(),
        point_341(),
        point_342(),
        point_343(),
        point_344(),
        point_345(),
        point_346(),
        point_347(),
        point_348(),
        point_349(),
        point_350(),
        point_351(),
        point_352(),
        point_353(),
        point_354(),
        point_355(),
        point_356(),
        point_357(),
        point_358(),
        point_359(),
        point_360(),
        point_361(),
        point_362(),
        point_363(),
        point_364(),
        point_365(),
        point_366(),
        point_367(),
        point_368(),
        point_369(),
        point_370(),
        point_371(),
        point_372(),
        point_373(),
        point_374(),
        point_375(),
        point_376(),
        point_377(),
        point_378(),
        point_379(),
        point_380(),
        point_381(),
        point_382(),
        point_383(),
        point_384(),
        point_385(),
        point_386(),
        point_387(),
        point_388(),
        point_389(),
        point_390(),
        point_391(),
        point_392(),
        point_393(),
        point_394(),
        point_395(),
        point_396(),
        point_397(),
        point_398(),
        point_399(),
        point_400(),
        point_401(),
        point_402(),
        point_403(),
        point_404(),
        point_405(),
        point_406(),
        point_407(),
        point_408(),
        point_409(),
        point_410(),
        point_411(),
        point_412(),
        point_413(),
        point_414(),
        point_415(),
        point_416(),
        point_417(),
        point_418(),
        point_419(),
        point_420(),
        point_421(),
        point_422(),
        point_423(),
        point_424(),
        point_425(),
        point_426(),
        point_427(),
        point_428(),
        point_429(),
        point_430(),
        point_431(),
        point_432(),
        point_433(),
        point_434(),
        point_435(),
        point_436(),
        point_437(),
        point_438(),
        point_439(),
        point_440(),
        point_441(),
        point_442(),
        point_443(),
        point_444(),
        point_445(),
        point_446(),
        point_447(),
        point_448(),
        point_449(),
        point_450(),
        point_451(),
        point_452(),
        point_453(),
        point_454(),
        point_455(),
        point_456(),
        point_457(),
        point_458(),
        point_459(),
        point_460(),
        point_461(),
        point_462(),
        point_463(),
        point_464(),
        point_465(),
        point_466(),
        point_467(),
        point_468(),
        point_469(),
        point_470(),
        point_471(),
        point_472(),
        point_473(),
        point_474(),
        point_475(),
        point_476(),
        point_477(),
        point_478(),
        point_479(),
        point_480(),
        point_481(),
        point_482(),
        point_483(),
        point_484(),
        point_485(),
        point_486(),
        point_487(),
        point_488(),
        point_489(),
        point_490(),
        point_491(),
        point_492(),
        point_493(),
        point_494(),
        point_495(),
        point_496(),
        point_497(),
        point_498(),
        point_499(),
        point_500(),
        point_501(),
        point_502(),
        point_503(),
        point_504(),
        point_505(),
        point_506(),
        point_507(),
        point_508(),
        point_509(),
        point_510(),
        point_511(),
        point_512(),
        point_513(),
        point_514(),
        point_515(),
        point_516(),
        point_517(),
        point_518(),
        point_519(),
        point_520(),
        point_521(),
        point_522(),
        point_523(),
        point_524(),
        point_525(),
        point_526(),
        point_527(),
        point_528(),
        point_529(),
        point_530(),
        point_531(),
        point_532(),
        point_533(),
        point_534(),
        point_535(),
        point_536(),
        point_537(),
        point_538(),
        point_539(),
        point_540(),
        point_541(),
        point_542(),
        point_543(),
        point_544(),
        point_545(),
        point_546(),
        point_547(),
        point_548(),
        point_549(),
        point_550(),
        point_551(),
        point_552(),
        point_553(),
        point_554(),
        point_555(),
        point_556(),
        point_557(),
        point_558(),
        point_559(),
        point_560(),
        point_561(),
        point_562(),
        point_563(),
        point_564(),
        point_565(),
        point_566(),
        point_567(),
        point_568(),
        point_569(),
        point_570(),
        point_571(),
        point_572(),
        point_573(),
        point_574(),
        point_575(),
        point_576(),
        point_577(),
        point_578(),
        point_579(),
        point_580(),
        point_581(),
        point_582(),
        point_583(),
        point_584(),
        point_585(),
        point_586(),
        point_587(),
        point_588(),
        point_589(),
        point_590(),
        point_591(),
        point_592(),
        point_593(),
        point_594(),
        point_595(),
        point_596(),
        point_597(),
        point_598(),
        point_599(),
        point_600(),
        point_601(),
        point_602(),
        point_603(),
        point_604(),
        point_605(),
        point_606(),
        point_607(),
        point_608(),
        point_609(),
        point_610(),
        point_611(),
        point_612(),
        point_613(),
        point_614(),
        point_615(),
        point_616(),
        point_617(),
        point_618(),
        point_619(),
        point_620(),
        point_621(),
        point_622(),
        point_623(),
        point_624(),
        point_625(),
        point_626(),
        point_627(),
        point_628(),
        point_629(),
        point_630(),
        point_631(),
        point_632(),
        point_633(),
        point_634(),
        point_635(),
        point_636(),
        point_637(),
        point_638(),
        point_639(),
        point_640(),
        point_641(),
        point_642(),
        point_643(),
        point_644(),
        point_645(),
        point_646(),
        point_647(),
        point_648(),
        point_649(),
        point_650(),
        point_651(),
        point_652(),
        point_653(),
        point_654(),
        point_655(),
        point_656(),
        point_657(),
        point_658(),
        point_659(),
        point_660(),
        point_661(),
        point_662(),
        point_663(),
        point_664(),
        point_665(),
        point_666(),
        point_667(),
        point_668(),
        point_669(),
        point_670(),
        point_671(),
        point_672(),
        point_673(),
        point_674(),
        point_675(),
        point_676(),
        point_677(),
        point_678(),
        point_679(),
        point_680(),
        point_681(),
        point_682(),
        point_683(),
        point_684(),
        point_685(),
        point_686(),
        point_687(),
        point_688(),
        point_689(),
        point_690(),
        point_691(),
        point_692(),
        point_693(),
        point_694(),
        point_695(),
        point_696(),
        point_697(),
        point_698(),
        point_699(),
    ]

def pareto_front(model_flops: float, model_bytes: float) -> list[tuple[DesignPoint, dict]]:
    pts = [(p, score_point(p, model_flops, model_bytes)) for p in all_points()]
    front = []
    for p, m in pts:
        dominated = False
        for p2, m2 in pts:
            if (m2["latency_s"] <= m["latency_s"] and m2["energy_j"] <= m["energy_j"] and (m2["latency_s"] < m["latency_s"] or m2["energy_j"] < m["energy_j"])):
                dominated = True
                break
        if not dominated:
            front.append((p,m))
    front.sort(key=lambda x: (x[1]["latency_s"], x[1]["energy_j"]))
    return front
