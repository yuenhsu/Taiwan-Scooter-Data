from selenium import webdriver
import csv
from time import sleep
from calendar import monthrange


class EPABot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open(self):
        self.driver.get(
            "https://mobile.epa.gov.tw/LowPoll/TwostrokeStatistics.aspx?Type=O"
        )

    def start(self):
        # for output
        results = []

        # click previous month on the start date table until the calendar is August 2015
        while (
            self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
            ).text
            != "2015年8月"
        ):
            prev_mo = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[1]/a'
            )
            prev_mo.click()
            sleep(1)

            # stop if it reaches August 2015
            if (
                self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                ).text
                == "2015年8月"
            ):
                break

        # click previous month on the end date table until it reaches August 2015
        while (
            self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
            ).text
            != "2015年8月"
        ):
            prev_mo = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[1]/a'
            )
            prev_mo.click()
            sleep(1)

            # stop if it reaches August 2015
            if (
                self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                ).text
                == "2015年8月"
            ):
                break

        # Loop until calendar reaches March 2020:
        while (
            self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
            ).text
            != "2020年3月"
        ):

            # specify year and month
            if (
                len(
                    self.driver.find_element_by_xpath(
                        '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                    ).text
                )
                == 7
            ):
                str_mo = self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                ).text
                yr = int(str_mo[:4])
                mo = int(str_mo[5:6])

            else:
                str_mo = self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                ).text
                yr = int(str_mo[:4])
                mo = int(str_mo[5:7])

            # get last day of the month from previous step knowing when to click next month
            last = monthrange(yr, mo)[1]

            str_date = []

            # check whether the first day is in the first row
            for d in self.driver.find_elements_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[3]/td'
            ):
                str_date.append(d.text)

            # if it is, click it
            if "1" in str_date:
                for d in self.driver.find_elements_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[3]/td'
                ):
                    if d.text == "1":
                        print("Start Date:", yr, "/", mo, "/", d.text)
                        d.find_element_by_tag_name("a").click()
                        sleep(2)
                        break

            # if it's not, find it in the second row and click it
            if "1" not in str_date:
                for d in self.driver.find_elements_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[4]/td'
                ):
                    if d.text == "1":
                        print("Start Date:", yr, "/", mo, "/", d.text)
                        d.find_element_by_tag_name("a").click()
                        sleep(2)
                        break

            # select last day of the month
            end_date = []

            # check whether the last day of the month is on the second to last row
            for d in self.driver.find_elements_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[7]/td'
            ):
                end_date.append(d.text)

            # if it is, click it
            if str(last) in end_date:
                for d in self.driver.find_elements_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[7]/td'
                ):
                    if d.text == str(last):
                        print("End Date:", yr, "/", mo, "/", d.text)
                        d.find_element_by_tag_name("a").click()
                        sleep(2)
                        break

            # if it's not, find it in the bottom row
            if str(last) not in end_date:
                for d in self.driver.find_elements_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[8]/td'
                ):
                    if d.text == str(last):
                        print("End Date:", yr, "/", mo, "/", d.text)
                        d.find_element_by_tag_name("a").click()
                        sleep(2)
                        break

            # loop through three subsidy types
            for sub in range(
                len(
                    self.driver.find_elements_by_xpath(
                        '//*[@id="ctl00_ContentPlaceHolder1_rbl_Kind"]/tbody/tr/td'
                    )
                )
            ):

                # specify current status to avoid stall reference exception
                current = self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_rbl_Kind"]/tbody/tr/td['
                    + str(sub + 1)
                    + "]"
                )

                # select subsidy type
                sub_select = current.find_element_by_tag_name("input")
                sub_select.click()

                # get sub name
                sub_name = current.find_element_by_tag_name("label").text

                # search botton
                search_btn = self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_ImageButton1"]'
                )
                search_btn.click()

                sleep(2)

                # extract content from results
                for row in self.driver.find_elements_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_gvData"]/tbody/tr'
                ):

                    # get elements from row
                    t = [td.text for td in row.find_elements_by_tag_name("td")]

                    # put data in a dictionary
                    if len(t) == 2:
                        if t[0] != "合計":

                            time = str(yr) + "/" + str(mo) + "/1"
                            entry = {
                                "time": time,
                                "type": sub_name,
                                "city": t[0],
                                "count": t[1],
                            }

                            results.append(entry)

                        else:
                            continue

                    elif len(t) == 6:
                        if t[0] != "合計":

                            time = str(yr) + "/" + str(mo) + "/1"
                            entry = {
                                "time": time,
                                "type": sub_name,
                                "city": t[0],
                                "epa_app": int(t[3]) + int(t[4]) + int(t[5]),
                            }

                            results.append(entry)

                        else:
                            continue
                    else:
                        continue

                print(str(yr) + "/" + str(mo) + "/1", sub_name, "Done.")
                sleep(1)

            # click next month on the beinning date table
            next_mo_str = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar1"]/tbody/tr[1]/td/table/tbody/tr/td[3]/a'
            )
            next_mo_str.click()

            sleep(2)

            # click next month on the ending date table
            next_mo_end = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[3]/a'
            )
            next_mo_end.click()

            sleep(2)

            # stop if reaches 2020/03
            if (
                self.driver.find_element_by_xpath(
                    '//*[@id="ctl00_ContentPlaceHolder1_Calendar2"]/tbody/tr[1]/td/table/tbody/tr/td[2]'
                ).text
                == "2020年3月"
            ):
                break

        # write csv file
        with open("output/epa.csv", "w", newline="") as file:

            writer = csv.DictWriter(file, fieldnames=["time", "type", "city", "epa_app"])
            writer.writeheader()

            for r in results:
                writer.writerow(r)
            file.close()


bot = EPABot()
bot.open()
bot.start()
