import asyncio
import multiprocessing
import os
from multiprocessing import cpu_count, get_context, Pool
from core.Sender import Sender, Settings
from Config import FirebaseConfig
from utlis import re_initialized_auth


def run_worker(args):
    asyncio.run(process_apps(args))

async def worker_sender(config, data, method="reset"):
    process_name = multiprocessing.current_process().name
    print(f"Process {process_name} is working on {config}")
    auth = re_initialized_auth(config)
    await Settings(data_csv_path=data, authentication=auth, config=config).sending(method=method)

async def process_apps(args):
    worker, config_path, data_file = args
    await asyncio.gather(worker(config_path, data_file))

def start_process():
    print('Starting', multiprocessing.current_process().name)

def run_parallel(worker, apps_path, data_path):
    cores = cpu_count() - 14
    spawntype = 'fork'
    args_list = []

    total_projects = os.listdir(apps_path)
    total_data = os.listdir(data_path)

    for ID_RUN in range(0, len(total_projects)):
        config_path = os.path.join(apps_path, total_projects[ID_RUN])
        data_file = os.path.join(data_path, total_data[ID_RUN])
        args_list.append((worker, config_path, data_file))

    with get_context(spawntype).Pool(processes=cores, initializer=start_process) as p:
        results = []
        for args in args_list:
            result = p.apply_async(run_worker, (args,))
            results.append(result)

        p.close()

        p.join()

        for result in results:
            result.get()

if __name__ == '__main__':
    apps_path = "./apps"  # Replace with your actual path
    data_path = "./Data"  # Replace with your actual path

    run_parallel(worker_sender, apps_path, data_path)


