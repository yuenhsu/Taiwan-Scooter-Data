# Taiwan-Scooter-Data
Python script for scraping electricity scooter subsidy data from Taiwan government websites, cleaning collected data, and analysis. 

## Project
### Purpose
The repository is for my research on *The Effect of Government Subsidy Program on Consumer Behaviours: A Case Study of Electric Scooters in Taiwan*. To improve air quality and recude emissions, Taiwan government started providing subsidy to encourage consumers to adopt electric scooter, over gasoline ones. 

I want to use data from administration to examine whether electric scooter sales increased after the policy is implemented and whether high subsidy amount correlated with more electric scooter purchase. While the data is available online, I had difficulty extracting the information in desired format (monthly number by city). 

The scripts are for automating the data collection process and exporting the results for analysis and visualisation.

### Data Source
* [Subsidy Results](https://www.lev.org.tw/subsidy/result.aspx) from Low Emission Vehicle by the Ministry of Economic Affairs
* [Subsidy Results](https://mobile.epa.gov.tw/LowPoll/TwostrokeStatistics.aspx?Type=O) from Environmental Protection Administration

## Getting Started
### Optional: Virtualenv
I also use [virtualenv](http://www.virtualenv.org) to isolate the environment for the project.

```bash
$ pip install virtualenv #install
$ mkdir ~/Desktop/Scooter #create project folder
$ touch moea.py #create python script
$ virtualenv venv #create virtual environment 
$ source venv/bin/activate #activate virtual environment
```

### Install: ChromeDriver
Download ChromeDriver from [Choromium](https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/), unzip the file and move it to `/usr/local/bin` (mac os). 
```bash
$ mv ~/Downloads/chromedriver /usr/local/bin
```

### Install: Selenium
I use [pip](https://pip.pypa.io/) and install the library with Terminal. 
```bash
$ pip install selenium
```
Alternatively, you can download the source distribution from [PyPI](https://pypi.org/project/selenium/#files).

## Script
### moea
![moea graph](https://raw.githubusercontent.com/yuenhsu/Taiwan-Scooter-Data/master/image/moea_graph.png)


