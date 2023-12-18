# Firebase Automation

Automated Tool for Firebase Sending Emails. This documentation outlines the usage and functionality of each function.

## Table of Contents

- [Installation](#installation)
- [Setup Data](#setup-data)
- [Usage](#usage)
- [Cost Sending](#cost-sending)

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

Note: To get the Credential Config of the Project, follow the steps in the project settings and copy the JSON to `Creditials.py`.

```python

Creditials = {
    "apiKey": "AIzaSyDtQPBX8qQZ22xyNCaAANg02XDM_bfN0uk",
    "authDomain": "add-user-e98e9.firebaseapp.com",
    "projectId": "add-user-e98e9",
    "databaseURL": "https://add-user-e98e9-default-rtdb.firebaseio.com/users",
    "storageBucket": "add-user-e98e9.appspot.com",
    "messagingSenderId": "858288259676",
    "appId": "1:858288259676:web:52354ec6f2a90f13581c99",
    "measurementId": "G-D0WPTFDN0K"
}
```


#### Usage-run

to run the tool follow the Command :

```bash 
python main.py
```

##### How to use 

when the Tool Lunch there two options so far Version 1.1 

* Options :

    1. Insert the Data into Firebase Users 

        **Note** : here you have to Provide the Path of you data .CSV format stored in **Folder DATA**

    2. Send Email with Reset Password Method to set reset

        **Note** : here you have to give the method send ***for now only we have **reset** as Method to set in option 2 ***
      
    3. Exiting from tool Press CTRL + C
    
       **Note** : to exit from the Tool use CTRL + C

#### Cost-Sending

##### Accounts per project

| Account type              | Limit           |
|---------------------------|-----------------|
| Anonymous user accounts   | 100 million     |
| Registered user accounts  | Unlimited       |

##### Reset Password Method

Here, the table shows how much to send per account for three projects:

| Project                  | Reset Password Limit  |
|--------------------------|-----------------------|
| Project 1                | 150        |
| Project 2                | 150        |
| Project 3                | 150        |

**Send Total = 450 Emails**

###### Email Sending Limits

The quotas listed in this section scale with the size of their respective projects.

| Operation                   | Spark Plan Limit   | 
|-----------------------------|--------------------|
| Address verification emails | 1000 emails/day    | 
| Address change emails       | 1000 emails/day    | 
| Password reset emails       | 150 emails/day     | 
| Email link sign-in emails   | 5 emails/day      | 
