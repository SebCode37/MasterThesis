import os
import re
import json
import utils
import csv
import numpy as np
from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as mcm
import warnings

# Set the warning filter to "ignore" to hide all runtime warnings
warnings.filterwarnings("ignore")

protocolFile = 'ProtocolData.csv'

# Example usage:
config_file = 'config.json'
config_loader = utils.ConfigLoader(config_file)
drop_configs = config_loader.load_config()
genericData = config_loader.getGenericData()

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Construct the complete folder path
folder_name = genericData.folderName
folder_path = os.path.join(parent_directory, folder_name)
protocolDict = {}


def draw_line_graphs_from_csv_1():
    # Read data from CSV file using pandas
    data = pd.read_csv(genericData.outputFiles)

    # Create line graph for USD Value Data
    plt.figure(figsize=(20, 10))
    grouped_usd_data = data.groupby('MEV Type')
    colors = mcm.tab20  # Get the 'tab20' colormap
    for i, (mev_type, group) in enumerate(grouped_usd_data):
        plt.plot(group['Month'], group['USD Value Data'], label=mev_type, color=colors(i / len(grouped_usd_data)))
        plt.fill_between(group['Month'], group['USD Value Data'], color=colors(i / len(grouped_usd_data)), alpha=0.4)

    # Find the index of "September 22" in the 'Month' column
    september_index = data[data['Month'] == 'September 22'].index[0]//3

    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('USD Value Data')
    plt.title('USD Value Data Over Months')
    plt.legend()
    plt.gca().get_yaxis().set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plt.savefig('usd_value_data_fill.png')

    # Create line graph for Absolute Number
    plt.figure(figsize=(20, 10))
    grouped_abs_data = data.groupby('MEV Type')
    colors = mcm.tab20  # Get the 'tab20' colormap
    for i, (mev_type, group) in enumerate(grouped_abs_data):
        plt.plot(group['Month'], group['Absolute Number'], label=mev_type, color=colors(i / len(grouped_abs_data)))
        plt.fill_between(group['Month'], group['Absolute Number'], color=colors(i / len(grouped_abs_data)), alpha=0.4)
    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('Absolute Number')
    plt.title('Absolute Number Over Months')
    plt.legend()
    plt.gca().get_yaxis().set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plt.savefig('absolute_number_fill.png')
def draw_line_graphs_from_csv():
    # Read data from CSV file using pandas
    data = pd.read_csv(genericData.outputFiles)

    # Create line graph for USD Value Data
    plt.figure(figsize=(20, 10))
    grouped_usd_data = data.groupby('MEV Type')
    for mev_type, group in grouped_usd_data:
        plt.plot(group['Month'], group['USD Value Data'], label=mev_type)
    # Find the index of "September 22" in the 'Month' column
    september_index = data[data['Month'] == 'September 22'].index[0]//3

    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('USD Value Data')
    plt.title('USD Value Data Over Months')
    plt.legend()
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticks(plt.gca().get_yticks())
    plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
    # plt.gca().get_yaxis().set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plt.savefig('usd_value_data.png')

    # Create line graph for Absolute Number
    plt.figure(figsize=(20, 10))
    grouped_abs_data = data.groupby('MEV Type')
    for mev_type, group in grouped_abs_data:
        plt.plot(group['Month'], group['Absolute Number'], label=mev_type)
        # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index + 0.5, linestyle='dotted', color='red', linewidth=2)
    plt.xlabel('Month')
    plt.ylabel('Absolute Number')
    plt.title('Absolute Number Over Months')
    plt.legend()
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticks(plt.gca().get_yticks())
    plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
    # plt.gca().get_yaxis().set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plt.savefig('absolute_number.png')


def get_file_numbers(filename):
    match = re.search(r'blocks_(\d+)_to_(\d+).json', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def find_missing_files(directory):
    files = os.listdir(directory)
    files.sort()

    missing_files = []
    expected_next_start = None
    expected_next_start_2 = None
    initialNum = 0
    endNum = 0
    count = 0

    for filename in files:
        start, end = get_file_numbers(filename)
        if count == 0:
            initialNum = start
            count = count +1
        if start is None or end is None:
            continue

        if expected_next_start is not None and (start != expected_next_start and start!=expected_next_start_2):
            missing_files.append(f"filefound blocks_{start}_to_{end}.json instead of blocks_{expected_next_start}_to_{expected_next_start +99 }.json")

        expected_next_start = end + 1
        expected_next_start_2 = end

    print("The data set have starting block {} and ending block {}".format(initialNum,expected_next_start))

    return missing_files

def get_files_in_range(directory, start_num, end_num):
    files = os.listdir(directory)
    json_files = []

    for filename in files:
        start, end = get_file_numbers(filename)
        if start is None or end is None:
            continue

        if start >= start_num and end <= end_num:
            json_files.append(filename)

    return json_files

def addProtocol(protocol):
    if protocol in protocolDict:
        protocolDict[protocol] += 1
    else:
        protocolDict[protocol] = 1


def getDataFromfile(json_file,profitMevSelector,mev_type,count,profit,profitArray,blockNumProfit):
    with open(json_file, 'r') as json_file:
        data = json.load(json_file)
        for block in data:
            protocol = block.get('protocol','empty')
            addProtocol(protocol)
            if block.get('mev_type') == mev_type:
                if block.get(profitMevSelector) != None:
                    profit += abs(block.get(profitMevSelector,0))
                    blockNumProfit.append(block.get("block_number"))
                    if mev_type=="sandwich":
                        profitArray.append(abs(block.get(profitMevSelector, 0)))
                    else:
                        profitArray.append(block.get(profitMevSelector, 0))
                count += 1
    return count,profit,profitArray,blockNumProfit


def checkIfblockValid(data):
    mevTypes = []
    profit = 0
    for i in range(len(data)):
        mevTypes.append(data[i]['types'])
    for i in range(len(data)):
        if data[i]['types'] == 'sandwich':
            profit = profit + data[i]['profit']
    return profit

def getSandwichData(json_file,profitMevSelector,count,profit,profitArray,blockNumProfit):
    blockToMevType = {}
    mevTypesToCheck = ['frontrun','backrun','sandwich']
    with open(json_file, 'r') as json_file:
        data = json.load(json_file)
        for block in data:
            protocol = block.get('protocol','empty')
            addProtocol(protocol)
            blockNumber = block.get('block_number')
            mevType = block.get('mev_type')
            if mevType in mevTypesToCheck:
                if block.get(profitMevSelector):
                    profit1 = abs(block.get(profitMevSelector,0))
                else:
                    profit1 = 0
                if blockNumber in blockToMevType:
                    data ={
                        "types":mevType,
                        "profit": profit1
                    }
                    blockToMevType[blockNumber].append(data)
                else:
                    data ={
                        "types":mevType,
                        "profit": profit1
                    }
                    blockToMevType[blockNumber] = [data]

    for key in blockToMevType.keys():
        blockData = blockToMevType[key]
        pro = checkIfblockValid(blockData)
        count = count+1
        profit = profit + pro
        blockNumProfit.append(key)
        profitArray.append(pro)

    return count,profit,profitArray,blockNumProfit



def count_data_for_mev_type(json_files, mev_type,profitMevSelector):
    count = 0
    profit = 0
    profitArray = []
    blockNumProfit = []

    for file in json_files:
        json_file = os.path.join(folder_path, file)
        if mev_type == "sandwich":
            count, profit, profitArray, blockNumProfit = getSandwichData(json_file,profitMevSelector,count,profit,profitArray,blockNumProfit)
        else:
            count, profit, profitArray, blockNumProfit = getDataFromfile(json_file,profitMevSelector,mev_type,count,profit,profitArray,blockNumProfit)

    return count,profit,profitArray,blockNumProfit

def getOutliersPerMonth(profitDataArray,blockNumProfit):
    outlier_threshold =1
    outlier_indices = []
    updatedBlockNumprofit =[]
    profitDataArr = np.array(profitDataArray)
    mean = np.mean(profitDataArr)
    std = np.std(profitDataArr)
    threshold = outlier_threshold * std

    for i, volume in enumerate(profitDataArr):
        if abs(volume - mean) > threshold:
            outlier_indices.append(profitDataArray[i])
            updatedBlockNumprofit.append(blockNumProfit[i])
    return outlier_indices,updatedBlockNumprofit

def process_monthly_drops():
    mev_types = genericData.mevTypes
    mev_type_selectors = genericData.mevTypesSelector
    outlierCsv = open(genericData.outlierCsv,'w',newline='')
    writerOutlier = csv.writer(outlierCsv)
    writerOutlier.writerow(['Month','Mev Type','BlockNumber','Outlier'])
    with open(genericData.outputFiles, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Month', 'MEV Type', 'Absolute Number','USD Value Data',])

        for drop_config in drop_configs:
            month = drop_config.month
            json_files = get_files_in_range(folder_path,drop_config.startdrop,drop_config.enddrop)
            for i in range(len(mev_types)):
                mev_type = mev_types[i]
                mev_type_selector = mev_type_selectors[i]
                block_count,profitData,profitDataArray,blockNumProfit = count_data_for_mev_type(json_files, mev_type,mev_type_selector)
                outlier_indices,updatedBlockNumprofit = getOutliersPerMonth(profitDataArray,blockNumProfit)
                for j in range(len(outlier_indices)):
                    writerOutlier.writerow([month,mev_type,updatedBlockNumprofit[j],outlier_indices[j]])
                writer.writerow([month, mev_type, block_count,profitData])
            print("Month {} mev_type data completed".format(month))

def checkMissingFiles():
    missing_files = find_missing_files(folder_path)
    if missing_files:
        print(f"Missing files ({len(missing_files)}):")
        for missing_file in missing_files:
            print(missing_file)
    else:
        print("No files are missing.")

def dumpProtocolData():
    data = protocolDict
    with open(protocolFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Key', 'Value'])  # Write header row

        for key, value in data.items():
            writer.writerow([key, value])

def plot_donut_chart():
    data = {}

    with open(protocolFile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            key, value = row
            data[key] = int(value)
    # Get the keys and values from the dictionary
    plt.clf()
    colorEncoding = {
        "uniswap2":'tomato',
        "multiple":'blue',
        "balancer1":'orange',
        "uniswap3":'mediumpurple',
        "curve":'yellow',
        "zerox":'red',
        "bancor":'cornflowerblue',
        "aave":'slateblue',
        "compoundv2":'limegreen'
    }
    colors = []
    for key in data.keys():
        colors.append(colorEncoding[key])

    labels = data.keys()
    values = data.values()

    filename = 'donut_chart.png'  # Specify the output file name

    # Plot the outer pie chart
    outer_colors = colors[:len(data)]  # Select colors for outer ring
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=outer_colors, radius=1.2, startangle=90)

    # Add a white circle at the center to create the donut hole
    center_circle = plt.Circle((0, 0), 0.8, color='white')
    plt.gca().add_artist(center_circle)

    # Set aspect ratio to equal for a circular donut chart
    plt.axis('equal')
    plt.title('Donut Chart')
    plt.legend()


    # Save the chart to a file
    plt.savefig(filename)


def dumpMonthlyData():
    process_monthly_drops()

def drawPlots():
    draw_line_graphs_from_csv()
    draw_line_graphs_from_csv_1()
    plot_donut_chart()


def runSimulation():
    checkMissingFiles()
    dumpMonthlyData()
    dumpProtocolData()
    drawPlots()

if __name__ == '__main__':
    runSimulation()
