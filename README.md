# Taiwan-Scooter-Data
Python script for scraping electricity scooter subsidy data from Taiwan government websites, cleaning collected data, and analysis. 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge&.svg)](https://github.com/psf/black)

## Project
### Purpose
The repository is for my research on *The Effect of Government Subsidy Program on Consumer Behaviours: A Case Study of Electric Scooters in Taiwan*. To improve air quality and recude emissions, Taiwan government started providing subsidy to encourage consumers to adopt electric scooter, over gasoline ones. 

I want to use data from administration to examine whether electric scooter sales increased after the policy is implemented and whether high subsidy amount correlated with more electric scooter purchase. While the data is available online, I had difficulty extracting the information in desired format (monthly number by city). 

The scripts are for automating the data collection process and exporting the results for analysis and visualisation.

### Data Source
* [Subsidy Results](https://www.lev.org.tw/subsidy/result.aspx) from Low Emission Vehicle by the Ministry of Economic Affairs
* [Subsidy Results](https://mobile.epa.gov.tw/LowPoll/TwostrokeStatistics.aspx?Type=O) from Environmental Protection Administration

## Getting Started
Python is required for running the scripts. In addition, some common libraries, such as `csv`, `time`, and `calendar`, are used. 
```bash
$ pip install <library>
```
### Optional: Virtualenv
I use [virtualenv](http://www.virtualenv.org) to isolate the environment for the project. However, this is not required to run the script.

```bash
$ pip install virtualenv #install
$ mkdir ~/Desktop/Scooter #create project folder
$ touch moea.py #create python script
$ virtualenv venv #create virtual environment 
$ source venv/bin/activate #activate virtual environment
```

### Install: ChromeDriver
Download ChromeDriver from [Choromium](https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/), unzip the file and move it from `~/Downloads/chromedriver` to `/usr/local/bin` (mac os) with the following command.
```bash
$ mv ~/Downloads/chromedriver /usr/local/bin
```

### Install: Selenium
I use [pip](https://pip.pypa.io/) and install the library with Terminal. 
```bash
$ pip install selenium
```
Alternatively, you can download the source distribution from [PyPI](https://pypi.org/project/selenium/#files).

## Usage
### [moea.py](https://github.com/yuenhsu/Taiwan-Scooter-Data/blob/master/moea.py)
![moea graph](https://raw.githubusercontent.com/yuenhsu/Taiwan-Scooter-Data/master/image/moea_graph.png)

[moea.py](https://github.com/yuenhsu/Taiwan-Scooter-Data/blob/master/moea.py) script automates the process of collecting [subsidy application information](https://www.lev.org.tw/subsidy/result.aspx) from MOEA. As shown in graph, the script 1) selects table for output format, 2) iterates through cities, 3) chooses beginning year and month, and 4) clicks research. Once the result is available, iterate through the output HTML table to collect information. After gathering information from all cities, export data to csv file.

### [epa.py](https://github.com/yuenhsu/Taiwan-Scooter-Data/blob/master/epa.py)
![moea graph](https://raw.githubusercontent.com/yuenhsu/Taiwan-Scooter-Data/master/image/epa_graph.png)

[epa.py](https://github.com/yuenhsu/Taiwan-Scooter-Data/blob/master/epa.py) collects [subsidy information](https://mobile.epa.gov.tw/LowPoll/TwostrokeStatistics.aspx?Type=O) from EPA. Starting from beginning date and end date datepickers, the script continues to click `<`, the previous month button, until it reaches August 2015, which is when the policy was implemented. Once done, iterate through three types of subsidy and export data to csv.





