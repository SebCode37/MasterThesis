# Thesis: A flicker in the dark. Exploring MEV in the Ethereum Ecosystem </h1>

My data is available for download [here](https://drive.google.com/drive/folders/1_J6eKtyw1vxG_27ZU0DUhYFJgEEGbTKF?usp=sharing). If you have any questions, code missing, no access pls do not hesitate to shoot me a quick email s.wunderlich[at]hotmail[dot]com.

**Code**

This repository contains:

1. A script adapted from Weintraub et al. to fetch MEV Data. With (minor) adjustments.[MEV Script (Weintraub et al.)]
   - utils.py (sleep parameter >10 for Coingecko prices and fixes for Python utility error)
   - FlashbotsAnalysis.ipynb (environmental variable fix, updated range to 2023, get all mev not only mev via flashbots) 
   - add FlashbotsScraper

2. Code for scraping the Zeromev API [ZeromevScraper]
3. Visualizing the data using Python and Pandas. This script generates monthly MEV type absolute values, USD values, and detects outlier blocks.[CreatePlots]
4. A simple script for determining the end of month, corresponding blocknumber [BlocknumberStartMonth]

**Datasets**

The datasets included in this repository are:

1. Data from Flashbots in Pan mev-inspect Script for Blocks 14,444,725 - 16,700,000
   - `sandwich_results.json`
   - `arbitrage_results.json`
   - `liquidation_results.json`
2. Data from ZeroMev scraped for Blocks 14,444,725 - 16,700,000
   - `ZeroMevBlock14444725:16.700.000`
3. A table detailing the months and dates corresponding to the ZeroMev data.[Data]

**API Links:**

https://blocks.flashbots.net/

https://data.zeromev.org/docs/





## Quick Start to run Weintraub et al. Script 

A container with all the dependencies can be pulled from Docker hub (see below)

Depeding on your architecture (amd/arm) you might need to rebuild!

To run the container, please install docker and run:
**pls check your systems capabilities and adjust accordingly**

``` shell
docker pull sebpet1337/0x:readyfetch
docker run --name naughtynakamoto -m 16g --memory-swap="24g" -p 8888:8888 -it readyfetch

```

Afterwards, start an instance of MongoDB inside the container:

``` shell
mkdir -p /data/db && mongod --fork --logpath /var/log/mongod.log
```


To run the MEV measurement scripts, simply run inside the container the following commands:

**Quicknode RPC connection to a fully synched Ethereum archive node is provided - can change to own (watch limits!) 
BCCM desperately needs one, I recommend to setup Erigon ;)
in  ```PROVIDER``` in ```data-collection/mev/utils/settings.py``` !!**

``` shell
# Run the sandwich measurement script
cd /root/data-collection/mev/sandwiches
python3 sandwiches.py <BLOCK_RANGE_START>:<BLOCK_RANGE_END> # For exmaple: python3 sandwiches.py 15900000:15901000

# Run the arbitrage measurement script
cd /root/data-collection/mev/arbitrage
python3 arbitrage.py <BLOCK_RANGE_START>:<BLOCK_RANGE_END> # For exmaple: python3 arbitrage.py 11706655:11706655

# Run the liquidation measurement script
cd /root/data-collection/mev/liquidation
python3 liquidation.py <BLOCK_RANGE_START>:<BLOCK_RANGE_END> # For exmaple: python3 liquidation.py 11181773:11181773


Download new price data from Coingecko Api and save to prices.json
-> Already done and up to date till March 8th 2023 
# change if you want to update prices, however, if manually imported prices.json no need

cd /root/data-collection/mev/utils
change Settings.py 
set Update_Prices = True 

```

**Download & Import the flashbots blocks into MongoDB by running inside the container the following commands:**
-> need to update via Flashbots API. Watch out! 18GB

``` shell
cd /root/data-collection/flashbots
python3 import_flashbots_data.py
```


**To run the analysis, please launch the Jupyter notebook server inside the container using the following commands and then open up http://localhost:8888 on your browser:**
Watch out! Extremly memory heavy, I had to use 32cpu /70 mem

``` shell
cd /root/analysis
jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password=''
```




