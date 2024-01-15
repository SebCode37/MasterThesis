import json
import os
import time

import requests
from web3 import Web3


def get_coin_list():
    print("Getting list of coins from CoinGecko.com...")
    response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=true").json()
    coin_list = dict()
    for coin in response:
        if "ethereum" in coin["platforms"] and coin["platforms"]["ethereum"]:
            coin_list[Web3.toChecksumAddress(coin["platforms"]["ethereum"].lower())] = coin["id"]
    return coin_list


def get_prices():
    coin_list = get_coin_list()
    print("Fetching latest prices from CoinGecko.com...")
    from_timestamp = str(1392577232)  # Sun Feb 16 2014 19:00:32 GMT+0000
    to_timestamp = str(int(time.time()))
    prices = dict()
    if os.path.exists("prices.json"):
        with open("prices.json", "r") as f:
            prices = json.load(f)
    else:
        prices["eth_to_usd"] = requests.get(
            "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=usd&from=" + from_timestamp + "&to=" + to_timestamp).json()["prices"]

    for address in coin_list:
        if address not in prices:
            market_id = coin_list[address]
            print(address, market_id)
            try:
                response = requests.get(
                    "https://api.coingecko.com/api/v3/coins/" + market_id + "/market_chart/range?vs_currency=eth&from=" + from_timestamp + "&to=" + to_timestamp)
                prices[address] = response.json()["prices"]
                time.sleep(20)  # wait for 10 seconds before making the next API call
            except Exception as e:
                print(str(e) + ":", response.text)
                with open("prices.json", "w") as f:
                    json.dump(prices, f, indent=2)
                continue  # skip to the next coin in case of an error

    with open("prices.json", "w") as f:
        json.dump(prices, f, indent=2)

    print("Fetched prices for", len(prices), "coins.")
    return prices


if __name__ == '__main__':
    while True:
        try:
            get_prices()
            break  # exit the loop if all coins have been fetched successfully
        except Exception as e:
            print("Error occurred:", str(e))
            time.sleep(60)  # wait for 60 seconds before retrying
            continue  # retry fetching prices for all coins

