# Chocolatey package version checking the latest version of packages
# Written by Hadrien Dussuel

import os
import json
import requests
import re
import functions

# Standard routine for package update
def PackageRoutine(name, urlVersion, regex, urlDownload):
    local = functions.GetLocalVersion(name)
    distant = functions.GetDistantVersion(urlVersion, regex)

    print("Checking -> " + name + " | " + local + " | " + distant)

    if(distant != local):
        url = urlDownload.replace("{{version}}", distant)
        print(name + " can be updated to " + distant + " with " + url)
        WriteVersionFile(name, distant, url)
        return True

    return False

# Write the new version in the JSON file
def WriteVersionFile(name, version, url):
    variables = { "name": name, "version": version, "url": url}
    file = "src/" + name + "/latest.json"

    if os.path.isdir("src/" + name) and os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(variables, f)

    return

# Running the routines
PackageRoutine("bulkrenameutility", "https://www.bulkrenameutility.co.uk/Download.php", r'(?<=<span class="text-muted">version\s)(\d{1,2}(\.\d{1,2})?(\.\d{1,2})?(\.\d{1,2})?)\s(?=<\/span>)', "https://www.s3.tgrmn.com/bru4/BRU_setup_{{version}}.exe")
