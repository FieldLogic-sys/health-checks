from fastapi import FastAPI
from datetime import datetime
import system_checks as sc
import network_checks as nc
import disk_checks as dc
import platform
import shutil

app = FastAPI()


@app.get("/health")
def get_system_status():
    # Fix: Ensure this variable is defined correctly
    disk_target = ["C:\\"] if platform.system() == "Windows" else ["/"]

    cpu = sc.check_cpu_load()
    net = nc.check_connectivity()
    # Fix: Ensure we are passing 'disk_target' here
    disk_issues = dc.check_disk_usage(disk_target)

    # Format the disk information for the dashboard
    if not disk_issues:
        # If there are no issues, grab the free space to display a healthy status
        du = shutil.disk_usage(disk_target[0])
        percent_free = 100 * du.free / du.total
        gigabytes_free = du.free / 2**30
        disk_info = f"OK ({percent_free:.1f}% / {gigabytes_free:.1f} GB free)"
    else:
        disk_info = "Issues: " + ", ".join(disk_issues)

    return {
        "cpu_usage": cpu,
        "network_ok": net,
        "disk_info": disk_info,
        "timestamp": datetime.now().strftime("%I:%M:%S %p")
    }


@app.get("/speedtest")
def run_speedtest():
    # Use regular 'def' to let FastAPI handle the threading for the heavy speedtest
    return nc.get_speed_results()
