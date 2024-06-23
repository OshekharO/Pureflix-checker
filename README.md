PureFlix Checker

A Python script to check PureFlix login credentials.

**Usage**

1. Create a file named `accounts.txt` with your login credentials in the format `email:password` one per line.
2. Run the script using `python main.py`.
3. The script will check each credential and write the valid ones to a file named `hits.txt`.

**Note**

* This script uses a third-party authentication service, Applicaster, to handle login requests.
* The URL used in this script is subject to change, so please check the PureFlix website for the latest URL.
* This script is for educational purposes only and should not be used for malicious activities.

**Requirements**

* Python 3.x
* `requests` library
