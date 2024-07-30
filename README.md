# Platinum Upsell

## Table of Contents
1. [Project Description](#project-description)
2. [Installation](#installation)
3. [Usage](#usage)
    - [Script 1](#script-1)
    - [Script 2](#script-2)
    - [Script 3](#script-3)
4. [License](#license)

## Project Description
A series of scripts using the warframe.market API to find items with high resell value and automatically populating your account with buy orders for them

## Installation

```bash
git clone https://github.com/ChinmayKhachane/PlatinumArbitrage.git
cd PlatinumArbitrage
pip install -r requirements.txt
```

## Usage

###script-1

To get the top buy and sell orders for an item. Enter the proper item name for the keyword

```bash
python get_orders.py --keyword [KEYWORD]
```

###script-2

To find profitable items under a specific class use the following

```bash
python finddiff.py --min_value [MIN_VALUE] --max_cost [MAX_VALUE] --keyword KEYWORD [KEYWORD ...]
```
-
