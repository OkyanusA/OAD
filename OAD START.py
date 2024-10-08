import os
import subprocess
import time

class OADStart:
    def __init__(self):
        self.oad_exe_path = r"C:\OAD ANAHTAR YAZILIMI\OAD.exe"

    def start_oad(self):
        while True:
            if os.path.exists(self.oad_exe_path):
                subprocess.Popen(self.oad_exe_path, shell=True)
                break
            time.sleep(1)

if __name__ == "__main__":
    oad_start = OADStart()
    oad_start.start_oad()