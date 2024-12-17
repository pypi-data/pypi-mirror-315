import importlib.metadata
from packaging import version
import subprocess
import os
import sys
import logging
import requests
import re
import threading
import time

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    fmt="\33[34m[%(levelname)s] %(asctime)s:\33[0m %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)

class PackageUpdater:
    def __init__(self, default_package='pip-start'):
        self.default_package = default_package
        self.script_name = os.path.abspath(__file__)
        self.update_threads = {}
        self.stop_events = {}  # Add stop events for threads

    def get_python_executable(self):
        full_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        possible_execs = [
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            f"py -{sys.version_info.major}.{sys.version_info.minor}",
            f"python{full_version}",
            f"py -{full_version}",
            "python",
            "py"
        ]
        for exec_name in possible_execs:
            try:
                result = subprocess.run(
                    [exec_name, "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                version_match = re.search(r'Python (\d+\.\d+\.\d+)', result.stdout)
                if version_match and version_match.group(1) == full_version:
                    return exec_name
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        logger.warning(f"Could not find exact version match. Falling back to {sys.executable}")
        return sys.executable

    def update_pkg(self, package_name=None):
        pkg = package_name or self.default_package
        logger.info(f"Updating {pkg}...")
        python_exec = self.get_python_executable()
        update_cmd = [python_exec, "-m", "pip", "install", "--upgrade", pkg]
        result = subprocess.run(update_cmd, capture_output=True, text=True)
        logger.info(f"Update process stdout: {result.stdout}")
        
        if result.returncode != 0:
            logger.error(f"Error during update: {result.stderr}")  # Log stderr only on error
        else:
            logger.info(f"{pkg} successfully updated.")

        if pkg == self.default_package:
            logger.info("Attempting to restart the application...")
            self.restart()

    def check_version(self, package_name=None, auto_update=False,
                      check_interval=86400, background=True, daemon=True):
        pkg = package_name or self.default_package

        def check_and_update():
            try:
                self.stop_events[pkg] = threading.Event()  # Create stop event for this thread
                while not self.stop_events[pkg].is_set():  # Check stop event
                    try:
                        installed_version = importlib.metadata.version(pkg)
                        logger.info(f"Installed version of {pkg}: {installed_version}")
                    except importlib.metadata.PackageNotFoundError:
                        logger.error(f"Package {pkg} not found.")
                        return False

                    try:
                        response = requests.get(f"https://pypi.org/pypi/{pkg}/json")
                        response.raise_for_status()
                        data = response.json()
                        latest_version = data['info']['version']
                        logger.info(f"Latest version of {pkg}: {latest_version}")
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Error fetching versions of {pkg} from PyPI: {e}")
                        return False

                    if version.parse(installed_version) < version.parse(latest_version):
                        logger.warning(f"{pkg} is ready for an update.")
                        if auto_update:
                            logger.warning(f"Auto-update flag set. Updating {pkg}")
                            self.update_pkg(pkg)
                            return True
                        logger.info(f"Update available for {pkg}. Current: {installed_version}, Latest: {latest_version}")
                        return True

                    logger.info(f"{pkg} is up to date.")
                    time.sleep(check_interval)
            except Exception as e:
                logger.error(f"Unexpected error in background update check for {pkg}: {e}")

        if background:
            thread = threading.Thread(target=check_and_update, daemon=daemon)
            thread.start()
            self.update_threads[pkg] = thread
            return False
        return check_and_update()

    def restart(self):
        logger.info("Restarting the application...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    def stop_background_checks(self, package_name=None):
        if package_name:
            if package_name in self.stop_events:
                self.stop_events[package_name].set()  # Signal the thread to stop
                del self.update_threads[package_name]
        else:
            for event in self.stop_events.values():
                event.set()  # Signal all threads to stop
            self.update_threads.clear()

def main():
    """
    Main function to demonstrate usage.
    """
    updater = PackageUpdater()
    
    # Check and update pip-start
    update_needed = updater.check_version("pip-start", auto_update=True)
    
    if update_needed:
        logger.info("pip-start has been updated.")
    else:
        logger.info("pip-start is up to date.")

if __name__ == '__main__':
    main()