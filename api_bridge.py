from fastapi import FastAPI
from datetime import datetime
import system_checks as sc
import network_checks as nc
import disk_checks as dc
import platform

app = FastAPI()


@app.get("/health")
def get_system_status():
    # 1. Define the variable first
    disk_target = ["C:\\"] if platform.system() == "Windows" else ["/"]

    # 2. Run the checks
    cpu = sc.check_cpu_load()
    net = nc.check_connectivity()
    disk = dc.check_disk_usage(disk_target)  # Pass the defined variable

    return {
        "cpu_usage": cpu,
        "network_ok": net,
        "disk_info": disk,
        "timestamp": datetime.now().strftime("%I:%M:%S %p")
    }


@app.get("/speedtest")
def run_speedtest():
    # Regular 'def' (not async) is better here for blocking speedtests
    return nc.get_speed_results()