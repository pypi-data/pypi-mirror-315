import os
import shutil

# Define tasks in order
tasks = ['CE', 'DTAN', 'DTCT', 'DTF', 'DTS1', 'DTS7', 'DTV', 'ST1', 'ST2']

# Source and destination directory
source_directory = 'testeo'
destination_directory = 'destino_testeo'

# Get the list of files in the source directory
files = os.listdir(source_directory)

# Sort the files by creation date
files.sort(key=lambda x: os.path.getmtime(os.path.join(source_directory, x)))

# Initialize subject and task counter
subject_counter = 1
task_counter = 0

for file in files:
    # Increment task counter
    task_counter += 1

    # If we have gone through all tasks, increment subject counter and reset task counter
    if task_counter > len(tasks):
        subject_counter += 1
        task_counter = 1

    # Create the name of the destination directory
    directory_name = f'OpenBCISession_Sub-CTR{subject_counter:03d}_ses_V0_tak_{tasks[task_counter-1]}_eeg'

    # Create the destination directory if it does not exist
    os.makedirs(os.path.join(destination_directory, directory_name), exist_ok=True)

    # Create the new name of the file
    if "BrainFlow-RAW" in file:
        new_name = f'BrainFlow-RAW_Sub-CTR{subject_counter:03d}_ses_V0_taw'
    elif "OpenBCI-RAW" in file:
        new_name = f'OpenBCI-RAW-2023-10-23_11-04-32.txt'  # Ask this
    else:
        new_name = file

    # Move and rename the file to the destination directory
    shutil.move(os.path.join(source_directory, file), os.path.join(destination_directory, directory_name, new_name))
