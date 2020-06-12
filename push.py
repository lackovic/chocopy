# Chocolatey package version checking and packing of package
# Written by Hadrien Dussuel
# Before to run this script for the first time, register your API key on Chocolatey.
# Find the API KEY here: https://chocolatey.org/account
# Then enter this command as admin: 
# choco setapikey -k yourAPIkey -s https://push.chocolatey.org/

import os
import subprocess
import glob

def RunVerbose(command):
    print('Running ' + command)
    output = subprocess.getoutput(command)
    print(output)
    return
    
packageNames = os.listdir('src/')
print("Pushing packages = " + str(packageNames))

for packageName in packageNames:
    print("\nChecking versions for " + packageName)
    remoteVersions = subprocess.getoutput('choco list --all -r ' + packageName).split('\n')
    print("Remote versions = " + str(remoteVersions))

    files = glob.glob("packed\\" + packageName + "*.nupkg")

    for f in files:

        versionFound = False
        localVersion = f.replace("packed\\" + packageName + ".", "").replace(".nupkg", "")

        for v in remoteVersions:
            remoteVersion = v.split("|")[1]
            if(remoteVersion == localVersion):
                versionFound = True
                print("\nLocal version " + localVersion + " is already published, skipping")

        if not versionFound:
            print("\nLocal version " + localVersion + " is not published")
            print("Pushing version " + localVersion + " for " + packageName)
            RunVerbose('choco push ' + f)
            RunVerbose('git add src\\' + packageName + '\\latest.json')
            RunVerbose('git commit -m \"' + packageName + '|' + localVersion + '\"')
