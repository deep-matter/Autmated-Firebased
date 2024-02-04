import asyncio
import multiprocessing
from core.Sender import Sender, Settings
import os
from Helper.utlis import re_initialized_auth

async def worker_sender(config, data, method="reset"):
    process_name = multiprocessing.current_process().name
    print(f"Process {process_name} is working on {config}")
    auth = re_initialized_auth(config)
    await Settings(data_csv_path=data, authentication=auth,config=config).sending(method=method)

async def process_apps(worker, data_path, apps_path):
    tasks = []

    total_projects = os.listdir(apps_path)
    total_data = os.listdir(data_path)
    print(total_data)

    for ID_RUN in range(0,len(total_projects)):
        config_path = "./apps/" + total_projects[ID_RUN]
        data_file = "./Data/" +  total_data[ID_RUN]
        task = worker(config_path, data_file)
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    apps_path = "./apps"  # Replace with your actual path
    data_path = "./data"  # Replace with your actual path

    loop.run_until_complete(process_apps(worker_sender, data_path, apps_path))