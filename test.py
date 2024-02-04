from numpy import euler_gamma
import pandas as pd
import os
def split_data(data_csv, n_splits):
    """
    Split data into n_splits chunks and save each part to a separate CSV file.
    """
    data_csv = pd.read_csv(data_csv)
    
    # Calculate the size of each chunk
    chunk_size = len(data_csv) // n_splits
    
    # Iterate over the number of splits
    for i in range(n_splits):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < n_splits - 1 else len(data_csv)
        
        # Extract the data for the current chunk
        data_part = data_csv[start_index:end_index]
        
        # Save the current chunk to a CSV file
        data_part.to_csv(f"Data/part_{i + 1}.csv", index=False)

if __name__ == "__main__":

#     data_csv = "./Data/test_data_5.csv"
#     data= "./Data"
#     partition_name = os.path.splitext(os.path.basename(data_csv))[0]
#     partition_name_ = os.path.splitext(os.path.basename(data_csv))[1]

#     if not os.path.exists(data +"/"+ partition_name):
#             os.makedirs(data +"/"+ partition_name, exist_ok=True)
# # Initializing five queues
#     print(partition_name_)

    for queue_index in range(1, 5):      
        if queue_index < 4 :
            print(queue_index)
            if queue_index == 3 :
                print("save")
        if queue_index == 4:
            print(queue_index)
        
