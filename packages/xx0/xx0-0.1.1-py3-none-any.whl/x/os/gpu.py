class GPU:
    """GPU 信息类"""

    def __init__(self):
        self.gpu数量 = self._get_gpu_count()  # 获取 GPU 数量
        self.gpu名称 = self._get_gpu_name()  # 获取 GPU 名称
        self.显存 = self._get_memory()  # 获取显存信息

    def _get_gpu_count(self) -> int:
        """获取 GPU 数量"""
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '-L'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return len(result.stdout.decode().strip().split('\n'))
            return 0
        except Exception:
            return 0  # 如果无法获取，返回 0

    def _get_gpu_name(self) -> str:
        """获取 GPU 名称"""
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return result.stdout.decode().strip().split('\n')[0]
            return "无法获取 GPU 名称"
        except Exception:
            return "无法获取 GPU 名称"

    def _get_memory(self) -> str:
        """获取显存信息"""
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return result.stdout.decode().strip().split('\n')[0]
            return "无法获取显存信息"
        except Exception:
            return "无法获取显存信息"

    def __str__(self):
        return (f"GPU 名称: {self.gpu名称}\n"
                f"GPU 数量: {self.gpu数量}\n"
                f"显存: {self.显存}")

    def __repr__(self):
        return self.__str__()

