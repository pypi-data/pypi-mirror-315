import subprocess


def cmd(command: str) -> str:
    """运行终端命令并返回输出"""
    try:
        # 使用subprocess.run执行命令，捕获标准输出和错误输出
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        if result.returncode == 0:
            # 如果命令成功执行，去除输出的空白字符并打印
            output = result.stdout.strip()
            print(output)
            return output  # 返回命令输出
        else:
            # 如果命令执行失败，返回错误信息
            return f"错误: {result.stderr.strip()}"  # 返回错误信息
    except Exception as e:
        # 捕获并返回异常信息
        return f"异常: {str(e)}"  # 返回异常信息


run = cmd
exec = cmd
