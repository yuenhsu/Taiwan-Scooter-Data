from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import csv

class MOEA_bot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def collect(self):
        self.driver.get("https://www.lev.org.tw/subsidy/result.aspx")
        sleep(2)

        # select table instead of chart
        table_select = self.driver.find_element_by_xpath('//*[@id="rblType_1"]')
        table_select.click()

        # choose beginning year 2012
        str_yr_opt = self.driver.find_element_by_xpath(
            '//*[@id="ssStartYear"]/option[9]'
        )
        str_yr_opt.click()

        # choose beginning month September
        str_mo_opt = self.driver.find_element_by_xpath('//*[@id="ssStartM"]/option[9]')
        str_mo_opt.click()

        results = []

        # loop through every city in the dropdown menu
        for c in range(
            len(Select(self.driver.find_element_by_xpath('//*[@id="ddlCity"]')).options)
        ):
            # skip if c is 0, nationwide
            if c == 0: continue

            # locate element and select
            city = Select(self.driver.find_element_by_xpath('//*[@id="ddlCity"]'))
            city.select_by_index(c)

            #locate search button and click
            search_btn = self.driver.find_element_by_xpath('//*[@id="btSel"]')
            search_btn.click()

            sleep(2)

            #iterate rows in search results
            for row in self.driver.find_elements_by_xpath(
                '//*[@id="plType1"]/table/tbody/tr'
            ):
                #iterate cells in each row
                tdata = [td.text for td in row.find_elements_by_tag_name("td")]
                if len(tdata) == 2:
                    if tdata[0] != "合計":
                        entry = {
                            "city": self.driver.find_element_by_xpath(
                                '//*[@id="spanCity"]'
                            ).text,
                            "time": tdata[0] + "/1",
                            "moea_app": tdata[1],
                        }
                        results.append(entry)
                    else:
                        continue
                else:
                    continue

            # print statement after the loop is done
            print(
                self.driver.find_element_by_xpath('//*[@id="spanCity"]').text,
                "done!",
            )
                
            sleep(2)


        with open("output/moea.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=["city", "time", "moea_app"]
            )
            writer.writeheader()
            for r in results:
                writer.writerow(r)

bot = MOEA_bot()
bot.collect()