import requests
import json
import time
import os

# API endpoint and parameters
base_url = "https://data.zeromev.org/v1/mevBlock"
start_block = 13916166
end_block = 14297758
count = 100
wait_time = 10  # seconds need to comply to rate limits

# Resume from the last successful block processed
resume_block = start_block

# Directory to save JSON files
save_directory = "/Users/seb/Desktop/Masterarbeit/Code/pythonProject"  # Replace with your desired directory path

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Loop through blocks in batches of 100
while resume_block < end_block:
    # Calculate the block range for the API call
    block_number = resume_block
    next_block_number = block_number + count - 1

    # Set the parameters for the API call
    params = {"block_number": block_number, "count": count}

    # Make the API call and get the response as JSON
    try:
        response = requests.get(base_url, params=params).json()
    except Exception as e:
        # Log the error and wait before retrying
        print(f"Error fetching blocks {block_number} to {next_block_number}: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(wait_time)
        continue

    # Check if the API call was successful
    if response:
        # Print the current range of blocks being fetched
        print(f"Fetching blocks {block_number} to {next_block_number}...")

        # Save the response data to a file
        filename = f"blocks_{block_number}_to_{next_block_number}.json"
        filepath = os.path.join(save_directory, filename)
        with open(filepath, "w") as f:
            json.dump(response, f)

        # Update the resume block
        resume_block = next_block_number + 1

        # Wait for the specified time before making the next API call
        time.sleep(wait_time)
    else:
        # If there was an error with the API call, print an error message
        print(f"Error fetching blocks {block_number} to {next_block_number}...")

    # Check if there are any existing files for the next block range
    next_filename = f"blocks_{resume_block}_to_{resume_block+count-1}.json"
    next_filepath = os.path.join(save_directory, next_filename)
    if os.path.exists(next_filepath):
        # If there are existing files, skip to the next block range
        print(f"Skipping blocks {block_number} to {next_block_number}...")
        resume_block = next_block_number + 1

print("Finished fetching all blocks.")
