from selenium import webdriver
import csv

class city():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def collect(self):

        # open wikipedia page
        self.driver.get(
            "https://en.wikipedia.org/wiki/List_of_administrative_divisions_of_Taiwan"
        )

        # find table
        table = self.driver.find_elements_by_xpath(
            '//*[@id="mw-content-text"]/div/table/tbody/tr'
        )

        results = []

        # extract data from table
        for row in range(len(table)):

            # english name
            english = self.driver.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/table/tbody/tr['
                + str(row + 1)
                + "]/td[4]"
            )
            
            # mandarin name
            mandarin = self.driver.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/table/tbody/tr['
                + str(row + 1)
                + "]/td[5]"
            )
            entry = [mandarin.text, english.text]
            results.append(entry)

        with open("output/city_name.text", "w") as f:
            for r in results:
                f.write(",".join(r) + "\n")


bot = city()
bot.collect()