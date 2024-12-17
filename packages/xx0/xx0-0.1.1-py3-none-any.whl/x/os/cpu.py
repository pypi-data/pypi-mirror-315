import os

import platform


def num() -> int:
    """获取 CPU 数量"""
    return os.cpu_count() or 0  # 返回 CPU 数量，如果无法获取则返回 0


class CPUInfo:
    """CPU 信息类"""

    def __init__(self):
        self.cpu数量 = os.cpu_count() or 0  # 获取 CPU 数量
        self.cpu名称 = platform.processor() or "无法获取 CPU 名称"  # 获取 CPU 名称
        self.架构 = platform.architecture()[0]  # 获取系统架构
        self.操作系统 = platform.system()  # 获取操作系统
        self.版本 = platform.release()  # 获取操作系统版本
        self.详细版本 = platform.version()  # 获取操作系统详细版本
        self.逻辑核心数量 = os.cpu_count() or 0  # 获取逻辑核心数量
        self.物理核心数量 = self._get_physical_cores()  # 获取物理核心数量
        self.频率 = self._get_cpu_frequency()  # 获取 CPU 频率

    def _get_physical_cores(self) -> int:
        """获取物理核心数量"""
        try:
            # 通过读取 /proc/cpuinfo 文件来获取物理核心数量（仅适用于类 Unix 系统）
            with open('/proc/cpuinfo', 'r') as f:
                return len(set(line.split(":")[1].strip() for line in f if "core id" in line))
        except Exception:
            return 0  # 如果无法获取，返回 0

    def _get_cpu_frequency(self) -> str:
        """获取 CPU 频率"""
        try:
            # 通过读取 /proc/cpuinfo 文件来获取 CPU 频率（仅适用于类 Unix 系统）
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if "cpu MHz" in line:
                        return line.split(":")[1].strip() + " MHz"
            return "无法获取频率"
        except Exception:
            return "无法获取频率"

    # 添加注释以描述 CPUInfo 类的功能
    # CPUInfo 类用于获取和存储有关 CPU 的详细信息，包括数量、名称、架构、操作系统及其版本。
    # 该类的实例可以通过 __str__ 和 __repr__ 方法以易读的格式输出其信息。
    def __str__(self):
        return (f"CPU 名称: {self.cpu名称}\n"
                f"架构: {self.架构}\n"
                f"操作系统: {self.操作系统}\n"
                f"版本: {self.版本}\n"
                f"详细版本: {self.详细版本}\n"
                f"逻辑核心数量: {self.逻辑核心数量}\n"
                f"物理核心数量: {self.物理核心数量}\n"
                f"频率: {self.频率}")

    def __repr__(self):
        return self.__str__()


def info() -> CPUInfo:
    """获取详细的 CPU 信息"""
    return CPUInfo()
