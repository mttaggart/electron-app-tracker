# Electron Vulnerability Tracker

This Notebook tracks known [Electron](https://electronjs.org) apps for vulnerabilities. This knowledge is valuable given the frequent release of vulns in the browser technologies that comprise Electron, although these apps often fly under the radar for remediation.

## Methodology

The original list of apps was sourced from [Electron's own site](https://electron.js.org/apps), and has been amended with community support since then.

This script both sources from and dynamically updates the CSV (and JSON) files holding the app info. If an app has a repo associated, then the repo is queried, using `requests` and `BeautifulSoup` for parsing. We're avoiding the GitHub API to avoid rate limiting. Each repo is then examined for `package.json` files. If none is found in the repo root, immediate subdirectories are queries. For sanity, we only query immediate subdirs and we only query `main` and `master` branches. That means some apps will be missed in the scrape due to using version branches that are ahead of `main`.

If a `package.json` file is found, it is analyzed for the presence of `electron` as a dependency. This version is then tested against known-patched versions of Electron for each listed vulnerability. If the semantic version is equal or greater, we show `patched` for that vuln; otherwise, we show `vulnerable`. Each scrape is timestamped, so new data will update existing data.

## Contributing 

Contributing is easy! Simply open a Pull Request updating `electron_apps.csv` with a `manual` access type. Please provide evidence of the versions of the apps you're updating. And thank you for helping with the effort!
