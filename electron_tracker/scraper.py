import requests
import json
from bs4 import BeautifulSoup
from .logger import *

def has_package_json(html: str) -> str:
    """
    Determines whether a given HTML document has a link to `package.json`
    
    Returns the found URI, None if not found
    
    PARAMETERS
    ----------
    
    html: str - Text response of a HTTP request
    """
    soup = BeautifulSoup(html, features="html.parser")
    clean_links = [l for l in soup.find_all("a") if "href" in l.attrs] 
    package_links = [a["href"] for a in soup.find_all("a") if "href" in a.attrs and "package.json" in a["href"]]
    if len(package_links) > 0:
        return package_links[0]
    
    return None

def search_package_json(repo_url: str) -> str:
    """
    Attempt to identify where package.json lives in the repo, if in fact it lives there.
    
    Returns the URL to the package.json
    
    PARAMETERS
    ----------
    repo_url: str - URL to the base repo
    
    """
    info(f"Getting repo: {repo_url}")
    repo_res = requests.get(repo_url)
    if repo_res.status_code == 200:
        info(f"Successfully retrieved repo: {repo_url}")
        found_package_json = has_package_json(repo_res.text)
        # If it's package.json, we're done
        if found_package_json:
            info(f"Found package.json at {repo_url}")
            return "https://" + repo_url.split("/")[2] + found_package_json
        # Otherwise, we go through each likely dir
        else:
            warn(f"Package.json not found at root of {repo_url}; trying directories")
            soup = BeautifulSoup(repo_res.text, features="html.parser") 
            # Look for tree links, but we have to (for sanity) stay in main branches. Sorry, Signal
            clean_links = [l for l in soup.find_all("a") if "href" in l.attrs] 
            links = [l["href"] for l in clean_links if "tree/main" in l["href"] or "tree/master" in l["href"]]
            for l in links:
                url = l if "https://" in l else "https://" + repo_url.split("/")[2] + l
                info(f"Trying {url}")
                file_res = requests.get(url).text
                if has_package_json(file_res):
                    info(f"Found package.json in {url}")
                    return url 
            else:
                crit("Could not find package.json in first-level-subdirs")                 
    else:
        crit(f"Could not connect to {repo_url}")
    
    return None

def get_electron_version(package_json_url: str) -> str:
    info(f"Getting {package_json_url}")
    package_res = requests.get(package_json_url)
    if package_res.status_code == 200:
        try:
            package_json_data = json.loads("".join(package_res.json()["payload"]["blob"]["rawLines"]))
        except json.JSONDecodeError:
            crit(f"Could not retrieve electron version from f{package_json_url}")
            return None
        except KeyError:
            crit(f"Could not extract raw lines from f{package_json_url}")
            return None

        for k in ["devDependencies", "dependencies"]:
            if k in package_json_data.keys():
                test_deps = package_json_data[k]
                if "electron" in test_deps.keys():
                    return package_json_data[k]["electron"]
        return None
    else:
        crit(f"Could not retrieve package.json {package_json_url}")
        return None
