# Platinum Upsell

## Table of Contents
1. [Project Description](#project-description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)

## Project Description
A series of scripts using the warframe.market API to find items with high resell value and automatically populating your account with buy orders for them

## Installation

```bash
git clone https://github.com/ChinmayKhachane/PlatinumArbitrage.git
cd PlatinumArbitrage
pip install -r requirements.txt
```

Add your username and password to the following line in order to login to your account
```bash
headers = login("email", "password")
```

## Usage

Script 1

To get the top buy and sell orders for an item. Enter the proper item name for the keyword

```bash
python get_orders.py --keyword [KEYWORD]
```

Script 2

To find profitable items under a specific class use the following

```bash
python finddiff.py --min_value [MIN_VALUE] --max_value [MAX_VALUE] --keyword KEYWORD [KEYWORD ...]
```
-min_value: minimum margin for flip
-max_value: maximum cost for buying an item
-keyword: the keyword(s) that are in the item name (E.g. "Primed" for primed mods)

Script 3

Automatically populate your warframe.market account with orders found profitable in the previous script

```bash
python order_placing.py --min_value [MIN_VALUE] --max_value [MAX_VALUE] --keyword KEYWORD [KEYWORD ...]
```
-min_value: minimum margin for flip
-max_value: maximum cost for buying an item
-keyword: the keyword(s) that are in the item name (E.g. "Primed" for primed mods)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


