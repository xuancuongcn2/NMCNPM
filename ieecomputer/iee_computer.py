import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def write_json(data, filename):
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def write_csv(data, filename):
    with open(filename, 'w', newline='',encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
  ##Trình duyệt web la Firefox
  driver = webdriver.Firefox()

  ##ngày tháng năm bắt đầu lấy các sự kiện 
  start_date = '2024-03-01'

  ## đường link sau sẽ lấy tất các các sự kiện tecnical
  url = f"https://www.computer.org/conferences/calendar?queryState=%7B%22eventType%22:%22Technical%20Conference%22,%22numPages%22:1,%22startDate%22:%22{start_date}%22%7D"
  driver.get(url)
  time.sleep(20)
  elements = driver.find_elements(By.CSS_SELECTOR, "event-list-item")

  data = []
  for element in elements:
    conference_name_tag = element.find_element(By.CSS_SELECTOR, "h2")
    conference_name = conference_name_tag.text

    event_tag = element.find_element(By.CLASS_NAME, "tw-mt-4")
    event_span_tags = event_tag.find_elements(By.CSS_SELECTOR, "span")

    attendence_type = event_span_tags[0].text
    event_type = event_span_tags[1].text

    location_date_tags = element.find_element(By.CLASS_NAME, "tw-gap-4")
    spans = location_date_tags.find_elements(By.CSS_SELECTOR, "span")
    start_date = spans[0].text
    end_date = spans[1].text
    address = spans[2].text

    sponsor_tags = element.find_elements(By.CSS_SELECTOR, "li")
    sponsors = []
    for sp in sponsor_tags:
      sponsors.append(sp.text)

    try:
      map_tag = element.find_element(By.CSS_SELECTOR, "img")
      map = map_tag.get_attribute("src")
    except NoSuchElementException:
      map = ""
    try:
      website_tag = element.find_element(By.CLASS_NAME, "tw-text-gray-800")
      website = website_tag.get_attribute("href")
    except NoSuchElementException:
      website = ""
    data.append({"conference_name":conference_name,"event_type":event_type,"attendence_type":attendence_type,"start_date":start_date,"end_date":end_date, "address": address, "sponsors": sponsors,"map":map,"website":website})
    
  driver.quit()

  write_json(data,"ieecomputer.json")
  write_csv(data,"ieecomputer.csv")
