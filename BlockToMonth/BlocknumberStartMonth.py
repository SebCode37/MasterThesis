import requests
import calendar
import time

# Set the Etherscan API endpoint and your API key token
url = "https://api.etherscan.io/api"
api_key = "A1H66AV45BA8V4XN68HYV22U7WJG1CENW3"

# Get user input for the month and year
month, year = input("Enter the month and year (e.g. February 2022): ").split()

# Get the number of days in the specified month and year
num_days = calendar.monthrange(int(year), list(calendar.month_name).index(month))[1]

# Calculate the start and end timestamps for the specified month and year
start_timestamp = int(calendar.timegm(time.strptime(f"{month} 1 {year} 00:00:00", "%B %d %Y %H:%M:%S")))
end_timestamp = int(calendar.timegm(time.strptime(f"{month} {num_days} {year} 23:59:59", "%B %d %Y %H:%M:%S")))

# Make a request to the Etherscan API for the block number closest to the start timestamp
payload = {
    "module": "block",
    "action": "getblocknobytime",
    "timestamp": start_timestamp,
    "closest": "before",
    "apikey": api_key,
}
response = requests.get(url, params=payload).json()

# Print the block number and timestamp of the retrieved block
block_number = response["result"]
block_timestamp = int(requests.get(f"{url}?module=block&action=getblockreward&blockno={block_number}&apikey={api_key}").json()["result"]["timeStamp"])
print(f"The first block of {month} {year} is {block_number} and was mined on {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block_timestamp))}.")
