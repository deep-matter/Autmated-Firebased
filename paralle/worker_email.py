import os 
import sys
current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, target_dir)

import asyncio
import multiprocessing
from core.Manager import create_users_in_firebase
from Helper.utlis import re_initialized_auth
 

async def worker_emails(config, data, method="reset"):
    process_name = multiprocessing.current_process().name
    print(f"Process {process_name} is working on {config} and {data}")
    auth = re_initialized_auth(config)
    await create_users_in_firebase(data_csv=data, auth=auth,config=config)

async def process_apps_emails(worker, data_path, apps_path):
    tasks = []

    total_projects = os.listdir(apps_path)
    total_data = os.listdir(data_path)
    print(total_data)

    for ID_RUN in range(0,len(total_projects)):
        config_path = "apps/" + total_projects[ID_RUN]
        print(config_path)
        data_file = "Data/" +  total_data[ID_RUN]
        print(data_file)
        task = worker(config_path, data_file)
        tasks.append(task)
        

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    apps_path = "../apps"  # Replace with your actual path
    data_path = "../Data"  # Replace with your actual path

    loop.run_until_complete(process_apps_emails(worker_emails, data_path, apps_path))