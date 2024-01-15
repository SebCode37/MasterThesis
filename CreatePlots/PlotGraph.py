import utils
from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as mcm

# Example usage:
config_file = 'config.json'
config_loader = utils.ConfigLoader(config_file)
drop_configs = config_loader.load_config()
genericData = config_loader.getGenericData()

def draw_line_graphs_from_csv_1():
    # Read data from CSV file using pandas
    data = pd.read_csv(genericData.customOutputFile)

    # Create line graph for USD Value Data
    plt.figure(figsize=(20, 10))
    grouped_usd_data = data.groupby('MEV Type')
    colors = mcm.tab20  # Get the 'tab20' colormap
    for i, (mev_type, group) in enumerate(grouped_usd_data):
        plt.plot(group['Month'], group['USD Value Data'], label=mev_type, color=colors(i / len(grouped_usd_data)))
        plt.fill_between(group['Month'], group['USD Value Data'], color=colors(i / len(grouped_usd_data)), alpha=0.4)

    # Find the index of "September 22" in the 'Month' column
    september_index = data[data['Month'] == 'Sept-22'].index[0]//3

    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('USD Value Data')
    plt.title('USD Value Data Over Months')
    plt.legend()
    plt.gca().get_yaxis().set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plt.savefig('custom_usd_value_data_fill.png')

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
    plt.savefig('custom_absolute_number_fill.png')

def draw_line_graphs_from_csv():
    # Read data from CSV file using pandas
    data = pd.read_csv(genericData.customOutputFile)

    # Create line graph for USD Value Data
    plt.figure(figsize=(20, 10))
    grouped_usd_data = data.groupby('MEV Type')
    for mev_type, group in grouped_usd_data:
        plt.plot(group['Month'], group['USD Value Data'], label=mev_type)
    # Find the index of "September 22" in the 'Month' column
    september_index = data[data['Month'] == 'Sept-22'].index[0]//3

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
    plt.savefig('custom_usd_value_data.png')

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
    plt.savefig('custom_absolute_number.png')

def draw_comparison_line_graphs():
    # Read data from CSV file using pandas
    data = pd.read_csv(genericData.comparisionFile)

    # Plot comparison line graph for Absolute Number
    plt.figure(figsize=(20, 10))
    # Find the index of "September 22" in the 'Month' column
    september_index = data[data['Month'] == 'Sept-22'].index[0]

    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.plot(data['Month'], data['Absolute Number1'], label='Absolute Number 1')
    plt.plot(data['Month'], data['Absolute Number2'], label='Absolute Number 2')
    plt.xlabel('Month')
    plt.ylabel('Absolute Number')
    plt.title('Comparison of Absolute Number 1 and 2')
    plt.legend()
    plt.savefig('Comparision_absolute_number_comparison.png')

    # Plot comparison line graph for USD Value Data
    plt.figure(figsize=(20, 10))
    # Add a dotted line at September 15 (September 22 midpoint)
    plt.axvline(x=september_index+0.5, linestyle='dotted', color='red', linewidth=2)

    plt.plot(data['Month'], data['USD Value Data1'], label='USD Value Data 1')
    plt.plot(data['Month'], data['USD Value Data2'], label='USD Value Data 2')
    plt.xlabel('Month')
    plt.ylabel('USD Value Data')
    plt.title('Comparison of USD Value Data 1 and 2')
    plt.legend()
    plt.savefig('Comparision_Custom_usd_value_data_comparison.png')



def drawPlots():
    draw_line_graphs_from_csv()
    draw_line_graphs_from_csv_1()
    draw_comparison_line_graphs()

if __name__ == '__main__':
    drawPlots()
