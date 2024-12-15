import subprocess


def list_packages(package_manager):
    if package_manager == 'apt':
        result = subprocess.run(
            ['apt-cache', 'search', '.'],
            capture_output=True,
            text=True
        )
    elif package_manager in ['yum', 'dnf']:
        result = subprocess.run(
            ['repoquery', '--all'],
            capture_output=True,
            text=True
        )
    elif package_manager == 'brew':
        result = subprocess.run(
            ['brew', 'search', '.'],
            capture_output=True,
            text=True
        )
    else:
        raise ValueError("ER1: Unsupported package manager for search")

    packages = result.stdout.splitlines()
    extracted_packages = []
    max_packages = 5
    k_packages = 0
    for line in packages:
        if not line.strip() or line.startswith("==>"):
            continue
        extracted_packages.append(line.split()[0])
        if k_packages >= max_packages:
            break
        k_packages += 1

    return extracted_packages


def get_package_info(package_manager, package_name):
    if package_manager == 'apt':
        cmd = ['apt-cache', 'show', package_name]
    elif package_manager in ['yum', 'dnf']:
        cmd = ['repoquery', '--info', package_name]
    elif package_manager == 'brew':
        cmd = ['brew', 'info', package_name]
    else:
        raise ValueError("ER: Unsupported package manager for info")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        # Parse the output based on the package manager
        if package_manager == 'brew':
            return parse_brew_info(output)
        elif package_manager in ['yum', 'dnf']:
            return parse_yum_info(output)
        elif package_manager == 'apt':
            return parse_apt_info(output)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def parse_brew_info(output):
    """Parses brew info output to extract license, website, and description."""
    info = {}
    lines = output.splitlines()
    info["license"] = "Unknown"
    info["website"] = "Unknown"
    info["description"] = "Unknown"

    for i, line in enumerate(lines):
        if i == 1:  # The description is usually on the second line
            info["description"] = line.strip()
        elif line.startswith("https://"):  # The website URL
            info["website"] = line.strip()
        elif line.startswith("License:"):  # The license information
            info["license"] = line.split(":", 1)[1].strip()

    # Ensure all keys are present even if some fields are missing
    return info



def parse_yum_info(output):
    """Parses yum repoquery --info output."""
    info = {}
    lines = output.splitlines()

    for line in lines:
        if line.startswith("License"):
            info["license"] = line.split(":", 1)[1].strip()
        elif line.startswith("URL"):
            info["website"] = line.split(":", 1)[1].strip()
        elif "Copyright" in line:
            info["copyright"] = line.strip()

    # Ensure all keys are present even if data is missing
    return {
        "license": info.get("license", "Unknown"),
        "copyright": info.get("copyright", "Unknown"),
        "website": info.get("website", "Unknown"),
    }


def parse_apt_info(output):
    """Parses apt-cache show output."""
    info = {}
    lines = output.splitlines()

    for line in lines:
        if line.startswith("License:") or "License" in line:
            info["license"] = line.split(":", 1)[1].strip()
        elif line.startswith("Homepage:"):
            info["website"] = line.split(":", 1)[1].strip()
        elif "Copyright" in line:
            info["copyright"] = line.strip()

    # Ensure all keys are present even if data is missing
    return {
        "license": info.get("license", "Unknown"),
        "copyright": info.get("copyright", "Unknown"),
        "website": info.get("website", "Unknown"),
    }

