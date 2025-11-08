# Chocolatey package version checking and packing of package
# Written by Hadrien Dussuel

import os
import subprocess
import json
import urllib.request
import hashlib
import zipfile
import pathlib
import shutil
import functions as func
import glob

# Routine de vérification et de paquetage automatique en fonction de la version connue sur le site de Chocolatey
packages = os.listdir('src/')
print(packages)

for p in packages:
    print("Checking -> " + p)
    # versionPublished = subprocess.getoutput('choco search -r --pre ' + p).split('|')[1]
    versionLocalData = func.GetLocalData(p)
    versionLocal = versionLocalData["version"].strip()

    if not os.path.exists('packed/'):
        os.makedirs('packed/')

    if not os.path.exists("packed/" + p + "." + versionLocal + ".nupkg"):
        print("Packing -> " + p + " | " + versionLocal)

        # Create the temp directory
        if not os.path.isdir("tmp/"):
            os.mkdir("tmp")

        # Calculate checksums      
        urllib.request.urlretrieve(versionLocalData["url"], "tmp/tmpfile")  # DEBUG
        checksum = func.GetFileChecksum("tmp/tmpfile") 

        # Loading source files
        fileNuspec = func.GetFileContent("src/" + p + "/" + p + ".nuspec")
        fileInstall = func.GetFileContent("src/" + p + "/tools/chocolateyinstall.ps1")

        # Replace variables
        fileNuspec = fileNuspec.replace("{{version}}", versionLocal)
        fileInstall = fileInstall.replace("{{checksum}}", checksum).replace("{{url}}", versionLocalData["url"])

        if not os.path.isdir("tmp/tools"):
            os.mkdir("tmp/tools")

        func.WriteFileContent("tmp/" + p + ".nuspec", fileNuspec)
        func.WriteFileContent("tmp/tools/chocolateyinstall.ps1", fileInstall)

        # Execute the packing
        choco = subprocess.Popen(["choco", "pack"], cwd="tmp/")
        choco.wait()

        # Locate the produced nupkg (Chocolatey may normalize version 4.1.0.0 -> 4.1.0)
        nupkgs = glob.glob(f"tmp/{p}*.nupkg")
        if not nupkgs:
            raise FileNotFoundError(f"No package file found for {p} in tmp/. Expected version {versionLocal}")
        pkg_path = max(nupkgs, key=os.path.getmtime)  # latest if multiple
        dest_path = os.path.join("packed", os.path.basename(pkg_path))
        shutil.move(pkg_path, dest_path)
        print(f"Moved -> {dest_path}")

        # Clean up temp directory
        shutil.rmtree('tmp/')

