import platform
import subprocess
import requests
import platform
import subprocess
import time


API_KEY = ""


def get_os_version():
    """Get a clean OS version."""
    try:
        result = subprocess.run(
            ["lsb_release", "-ds"], stdout=subprocess.PIPE, text=True, check=True
        )
        return result.stdout.strip().strip('"')  # Clean version string
    except FileNotFoundError:
        return "Unknown Version"


def gather_system_info():
    """Collect basic system information."""
    system_info = {
        "os": platform.system(),  # e.g., 'Linux', 'Windows', 'Darwin'
        "os_version": get_os_version(),  # Clean OS version
        "kernel_version": platform.release(),  # Kernel version
        "architecture": platform.architecture()[0]  # e.g., '64bit'
    }

    # Example: List installed packages (Linux-specific, adjust for other OSes)
    try:
        result = subprocess.run(
            ["dpkg", "--get-selections"], stdout=subprocess.PIPE, text=True, check=True
        )
        system_info["installed_packages"] = result.stdout.splitlines()
    except FileNotFoundError:
        system_info["installed_packages"] = ["Package manager not supported"]

    return system_info


def search_cves(software_name, version):
    """Search for CVEs matching the software and version."""
    api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={software_name}+{version}"
    headers = {"apiKey": API_KEY}
    retries = 3
    for attempt in range(retries):
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get("vulnerabilities", [])
        elif response.status_code == 403:
            print("Access denied. Check your API key or rate limits.")
            return []
        elif response.status_code == 429:  # Too Many Requests
            print("Rate limit reached. Retrying...")
            time.sleep(10)  # Wait before retrying
        else:
            print(f"Error querying CVE database: {response.status_code}")
            return []
    print("Failed to query the CVE database after multiple attempts.")
    return []


def scan_for_cves():
    """Scan the system for known CVEs."""
    system_info = gather_system_info()
    print(f"System Info: {system_info['os']} {system_info['os_version']}")

    vulnerabilities = []
    for package in system_info.get("installed_packages", []):
        package_name, _, package_version = package.partition("\t")
        cves = search_cves(package_name, package_version)
        if cves:
            vulnerabilities.append((package_name, package_version, cves))

    # Report vulnerabilities
    if vulnerabilities:
        for package, version, cves in vulnerabilities:
            print(f"Vulnerabilities for {package} ({version}):")
            for cve in cves:
                print(
                    f"- {cve['cve']['CVE_data_meta']['ID']}: {cve['cve']['description']['description_data'][0]['value']}")
    else:
        print("No known vulnerabilities found.")
