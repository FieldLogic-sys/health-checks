import shutil
import psutil
import platform
import os
import time

from shared_checks import check_disk_usage  # Import from shared_checks
# import win32api

try:
    import win32api
    import win32con
except ImportError:
    win32api = None


def check_reboot():
    """Checks if a reboot is pending on Windows."""
    if platform.system() == "Windows":
        if win32api:  # Check if win32api is available
            try:
                return win32api.GetSystemMetrics(win32con.SM_SHUTTINGDOWN) != 0
            except Exception as e:  # Catch potential errors with GetSystemMetrics
                print(f"Error checking Windows reboot status: {e}")
                return False
        else:
            print("win32api module not available on this system.")
            return False
    return False


def check_disk_usage(disks=["C:\\"], min_gb=2, min_percent=10):
    """
    Checks disk usage of specified disks or partitions on Windows.

    Args:
        disks (list): A list of disks or partitions to check (default: ["C:\\"]).
        min_gb (float): Minimum free space in gigabytes required.
        min_percent (float): Minimum percentage of free space required.

    Returns:
        list: A list of messages indicating disk usage issues, or an empty list if all okay.
    """
    issues = []
    for disk in disks:
        du = shutil.disk_usage(disk)
        percent_free = 100 * du.free / du.total
        gigabytes_free = du.free / 2**30

        if gigabytes_free < min_gb:
            issues.append(
                f"Disk {disk} has less than {min_gb:.2f} GB free ({gigabytes_free:.2f} GB available)."
            )
        if percent_free < min_percent:
            issues.append(
                f"Disk {disk} has less than {min_percent:.2f}% free space ({percent_free:.2f}% available)."
            )
    return issues  # Disk usage is within limits


def check_cpu_load(threshold=75, interval=15):
    """
    Checks the average CPU load over a specified interval on Windows.

    Args:
        threshold (float): Maximum allowed CPU load percentage (default: 75).
        interval (int): Time interval (in seconds) to calculate average load (default: 1).

    Returns:
        str: A message indicating the CPU load status, or None if it's okay.
    """
    cpu_percent = psutil.cpu_percent(interval=interval)
    if cpu_percent > threshold:
        return (
            f"CPU load is {cpu_percent:.2f}%, exceeding the threshold of {threshold}%"
        )
    else:
        return f"CPU load is {cpu_percent:.2f}% within the threshold of {threshold}"  # here


def check_uptime():
    """Returns the system uptime in seconds on Windows."""
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - boot_time

    days = uptime_seconds // (24 * 60 * 60)
    hours = (uptime_seconds % (24 * 60 * 60)) // (60 * 60)
    minutes = (uptime_seconds % (60 * 60)) // 60
    seconds = round(uptime_seconds % 60, 2)

    uptime_str = f"As of {time.strftime('%Y-%m-%d %H:%M:%S')}, system has been running for {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    # print(uptime_str)
    return uptime_seconds, uptime_str


# if __name__ == "__main__":
# print(check_reboot())
# print(check_disk_usage())
# print(check_cpu_load())
# print(check_uptime())
