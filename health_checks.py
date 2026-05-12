import network_checks as nc
import system_checks as sc
import disk_checks as dc
import platform
import sys


def main():
    # Define exit codes
    EXIT_SUCCESS = 0
    EXIT_CPU_LOAD_HIGH = 2
    EXIT_NO_NETWORK = 3
    EXIT_DISK_ISSUE = 4
    EXIT_GENERAL_ERROR = 255  # A catch-all (for now)
    """A dictionary is used for better error checking and readability."""

    checks = {
        "cpu_load": (
            lambda: sc.check_cpu_load(),
            EXIT_CPU_LOAD_HIGH,
            "CPU load to high.",
        ),
        "network": (
            lambda: nc.check_connectivity(),
            EXIT_NO_NETWORK,
            "No working network",
        ),
        "speed": (
            lambda: nc.get_speed_results(),
            EXIT_GENERAL_ERROR,
            "Internet speed not available",
        ),
        "disk_usage": (
            lambda: dc.check_disk_usage(disks_to_check),
            EXIT_DISK_ISSUE,
            "Disk usage issues detected",
        ),
    }
    everything_ok = True

    # Determine disks to check based on OS
    disks_to_check = ["/"] if platform.system() == "Linux" else ["C:\\\\"]

    for check_name, (check_func, exit_code, msg) in checks.items():
        try:
            result = check_func()
            # Check if the result is None or False (indicating failure)
            if result is None or result is False:
                print(msg)
                everything_ok = False
            elif isinstance(result, list):
                for issue in result:
                    print(issue)
                everything_ok = False
            else:
                # If the result is not None or False, it's likely a success
                # No output needed as the return statements should give the needed information
                if check_name == "cpu_load":
                    print(f"CPU load: {result}%")
                elif check_name == "disk_usage":
                    print(f"Disk usage: {result}")

        except Exception as e:
            print(f"Error checking {check_name}: {e}")
            everything_ok = False
            sys.exit(EXIT_GENERAL_ERROR)

    if everything_ok:
        print("Everything is okay")
        sys.exit(EXIT_SUCCESS)
    else:
        for check_name, (check_func, exit_code, msg) in checks.items():
            if check_func() is not None and check_name != "speed":
                if check_name == "cpu_load":
                    sys.exit(EXIT_CPU_LOAD_HIGH)
                elif check_name == "network":
                    sys.exit(EXIT_NO_NETWORK)
                elif check_name == "disk_usage":
                    sys.exit(EXIT_DISK_ISSUE)
                else:  # Default to general error if the check isn't specifically handled
                    sys.exit(EXIT_GENERAL_ERROR)


if __name__ == "__main__":
    main()
