#  Attae Firebase Automation

Automated Tool for Firebase Sending Emails. This documentation outlines the usage and functionality of each function.

## Table of Contents

- [Installation](#installation)
- [Setup Data](#setup-data)
- [Usage](#usage)
- [Cost Sending](#cost-sending)


#### Features added 

1. parallel run multi projects
2. handling the unsend the Emails into the Caching 
3. Split the data into Batches 

## Installation

To install the tool and create a virtual environment to run the main script, follow these steps:

### Steps to run the Firebase Sender tool:

1. Initialize the environment:

    ```bash
    python -m venv Firebase
    ```

2. Activate the environment:

    ```bash
    source Firebase/Scripts/activate.bat
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Setup Data

To insert data into the tool, store the CSV Excel file containing email/password data in the [Data](/Data) folder.

### Notation Setting in Firebase Platform

To store data in the Firebase Realtime Database, follow these steps:

1. Create an instance of the Realtime Database.

2. Overwrite the permissions of data to read and write by setting the following to **true** in your Firebase project's rules:

    ```yaml
    {
      "rules": {
        ".read": true,
        ".write": true
      }
    }
    ```

3. In the `Credential.py` file, add your own database link. Append `/user` to the end of the link:

```bash
"databaseURL": "https://add-user-e98e9-default-rtdb.firebaseio.com/users",
```


### Config file 
the new the update in the application we need on to set the config into Config.txt 

and select the option to parser the Files into apps.json 


```YAML
"apiKey": "AIzaSyDtQPBX8qQZ22xyNCaAANg02XDM_bfN0uk",
"authDomain": "add-user-e98e9.firebaseapp.com",
"projectId": "add-user-e98e9",
"databaseURL": "https://add-user-e98e9-default-rtdb.firebaseio.com/users",
"storageBucket": "add-user-e98e9.appspot.com",
"messagingSenderId": "858288259676",
"appId": "1:858288259676:web:52354ec6f2a90f13581c99",
"measurementId": "G-D0WPTFDN0K"
```


#### Usage-run

to run the tool follow the Command :

```bash 
python main.py
```

