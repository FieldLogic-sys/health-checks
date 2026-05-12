from fastapi import FastAPI
from datetime import datetime
import system_checks as sc
import network_checks as nc
import disk_checks as dc
import platform

app = FastAPI()


@app.get("/health")
def get_system_status():
    # Fix: Ensure this variable is defined correctly
    disk_target = ["C:\\"] if platform.system() == "Windows" else ["/"]

    cpu = sc.check_cpu_load()
    net = nc.check_connectivity()
    # Fix: Ensure we are passing 'disk_target' here
    disk = dc.check_disk_usage(disk_target)

    return {
        "cpu_usage": cpu,
        "network_ok": net,
        "disk_info": disk,
        "timestamp": datetime.now().strftime("%I:%M:%S %p")
    }


@app.get("/speedtest")
def run_speedtest():
    # Use regular 'def' to let FastAPI handle the threading for the heavy speedtest
    return nc.get_speed_results()