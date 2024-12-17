import os
import subprocess
from time import sleep
import uiautomator2 as u2


class U2:
    @staticmethod
    def connect(dev):
        devs = os.popen("adb devices").read()
        if dev not in devs:
            raise ValueError(f"{dev} 设备ADB离线 无法使用U2服务")

        d = None
        try:
            d = u2.connect(dev)
            if d(text="不可能真有这控价").exists: pass  # 诱发异常
        except Exception as e:
            print(f"{dev} U2服务启动失败，重新启动中")
            subprocess.run(f"adb -s {dev} shell /data/local/tmp/atx-agent server --stop")  # 停止服务
            subprocess.run(f"adb -s {dev} shell /data/local/tmp/atx-agent server -d")  # 启动服务
            sleep(3)
        finally:
            if not d:
                raise ValueError(f"{dev} 初始化U2失败")
            return d
