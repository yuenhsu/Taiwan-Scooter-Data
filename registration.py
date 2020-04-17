from selenium import webdriver
import csv
import pandas as pd

class reg():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def collect(self):

        # open search result page
        self.driver.get(
            "https://stat.thb.gov.tw/hb01/webMain.aspx?sys=220&ym=10101&ymt=10902&kind=21&type=1&funid=1110008&cycle=1&outmode=0&compmode=0&outkind=1&fld26=1&cod01=1&cod03=1&codspc1=1,22,&rdm=R113476"
        )

        header = self.driver.find_elements_by_xpath('/html/body/form/table[2]/tbody/tr[2]/th')
        col_list = [i.text for i in header]

        results = []


        table = self.driver.find_elements_by_xpath('/html/body/form/table[2]/tbody/tr')

        for c in range(len(table)):
            if c < 2: continue
            row = self.driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[' + str(c+1) + ']')
            yr_mo = row.find_element_by_tag_name('th').text

            if len(yr_mo) == 8:
                yr = str(int(yr_mo[:3]) + 1911)
                mo = yr_mo[5:6]

            else:
                yr = str(int(yr_mo[:3]) + 1911)
                mo = yr_mo[5:7]


            for count in range(len(row.find_elements_by_tag_name('td'))):
                fuel = self.driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/th[' + str(count+2)+']').text[:2]
                city = self.driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/th[' + str(count+2)+']').text[5:]
                reg_count = row.find_element_by_xpath('td['+str(count+1)+']').text
                entry = {"time": yr+'/'+mo+'/1', "fuel": fuel,"city":city, "registration": reg_count}
                results.append(entry)

        data = pd.DataFrame(data = results)
        gas = data[data['fuel']=='汽油'].rename(columns={'registration':'gas_reg'}).drop(columns='fuel')
        elec = data[data['fuel']!='汽油'].rename(columns={'registration':'elec_reg'}).drop(columns='fuel')
        data_wide = gas.merge(elec, on=['time','city'])
        data_wide.to_csv("output/registration_wide.csv", index=False)


        with open("output/registration.csv", "w", newline="") as file:

            writer = csv.DictWriter(file, fieldnames=["time", "fuel", "city", "registration"])
            writer.writeheader()

            for r in results:
                writer.writerow(r)
            file.close()


bot = reg()
bot.collect()