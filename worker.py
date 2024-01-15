import asyncio
import multiprocessing
from core.Sender import Sender, Settings
from Config import FirebaseConfig
from parser import load_json_into_dictionary
import os
from utlis import re_initialized_auth
async def worker_sender(config, data, method="reset"):
    process_name = multiprocessing.current_process().name
    print(f"Process {process_name} is working on {config}")
    auth = re_initialized_auth(config)
    await Settings(data_csv_path=data, authentication=auth,config=config).sending(method=method)

async def process_apps(worker, data_path, apps_path):
    tasks = []

    total_projects = os.listdir(apps_path)
    total_data = os.listdir(data_path)

    for project, data_file in zip(total_projects, total_data):
        config_path = os.path.join(apps_path, project)
        data_path = os.path.join(data_path, data_file)
        task = worker(config_path, data_path)
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    apps_path = "./apps"  # Replace with your actual path
    data_path = "./data"  # Replace with your actual path

    loop.run_until_complete(process_apps(worker_sender, data_path, apps_path))