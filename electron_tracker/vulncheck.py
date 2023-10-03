import semver
import re
from .logger import *

PATCHED_VERSIONS = {
    "cve_2023_4863": ["22.3.24", "24.8.3", "25.8.1", "26.2.1"],
    "cve_2023_5217": ["22.3.25", "24.8.5", "25.8.4", "26.2.4"]
}


def is_patched(cve: str, electron_version: str) -> bool:
    """
    Uses Semantic Versioning to compare patching status

    PARAMETERS
    ----------

    cve: str - CVE number, either with dashes or underscores, aka "cve_2023_4683"
    electron_version: str - Raw electron version
    """
    try:
        cve_key = cve.lower().replace("-","_")
        cleaned_version = re.sub("[\^~]", "", electron_version)
        if not semver.Version.is_valid(cleaned_version):
            warn(f"Invalid Semantic version: {cleaned_version}")
            return False
        version = semver.Version.parse(cleaned_version)
        if electron_version in PATCHED_VERSIONS[cve_key]:
            return True
        else:
            patched_versions = [semver.Version.parse(v) for v in PATCHED_VERSIONS[cve_key]]
            patched_major = [v for v in patched_versions if v.major == version.major]
            if patched_major:
                return version.compare(patched_major[0]) >= 0
            else:
                return False
    except KeyError:
        return False
        
