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

        # choose beginning year
        str_yr_opt = self.driver.find_element_by_xpath(
            '//*[@id="ssStartYear"]/option[12]'
        )
        str_yr_opt.click()

        # choose beginning month
        str_mo_opt = self.driver.find_element_by_xpath('//*[@id="ssStartM"]/option[1]')
        str_mo_opt.click()

        results = []

        # loop through every city in the dropdown menu
        for c in range(
            len(Select(self.driver.find_element_by_xpath('//*[@id="ddlCity"]')).options)
        ):
            #locate the element and select
            city = Select(self.driver.find_element_by_xpath('//*[@id="ddlCity"]'))
            city.select_by_index(c)

            # select scooter type
            for t in range(
                len(
                    Select(
                        self.driver.find_element_by_xpath('//*[@id="sslCar"]')
                    ).options
                )
            ):
                #locate the element and select
                scooter = Select(self.driver.find_element_by_xpath('//*[@id="sslCar"]'))
                scooter.select_by_index(t)

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
                                "type": self.driver.find_element_by_xpath(
                                    '//*[@id="spanCar"]'
                                ).text,
                                "time": tdata[0] + "/1",
                                "MOEA_Sub": tdata[1],
                            }
                            results.append(entry)
                        else:
                            continue
                    else:
                        continue

                print(
                    self.driver.find_element_by_xpath('//*[@id="spanCity"]').text,
                    self.driver.find_element_by_xpath('//*[@id="spanCar"]').text,
                    "done!",
                )
                
                sleep(2)


        with open("moea.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=["city", "type", "time", "moea_app"]
            )
            writer.writeheader()
            for r in results:
                writer.writerow(r)

bot = MOEA_bot()
bot.collect()