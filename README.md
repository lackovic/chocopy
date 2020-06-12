# Chocopy

A [Chocolatey](https://chocolatey.org/) package update script written in Python forked from [dbkblk/chocolatey_packages](https://github.com/dbkblk/chocolatey_packages).

## Prerequisites

- Python version `3.x`

- Python `requests module`:

   ```powershell
   python -m pip install requests
   ```

- Register your [API key on Chocolatey](https://chocolatey.org/account) and then _run as administrator_:

   ```powershell
   choco setapikey -k <yourAPIkey> -s https://push.chocolatey.org/
   ```

## Running

1. To check whether there is a newer version available of any of the packages in this repo run:

   ```powershell
   .\check.py
   ```

1. To update `latest.json` with the latest version and create the files to be pushed in the `packed\` directory run:

   ```powershell
   .\pack.py
   ```

1. To publish the packed files to Chocolatey and commit `latest.json` run:

   ```powershell
   .\push.py
   ```
