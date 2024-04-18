import requests
import yaml
import json
import csv

def write_yml(data,filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file)

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def write_csv(data, filename):
    with open(filename, "w", newline='') as file:
      writer = csv.writer(file)
      # Ghi header
      writer.writerow(["Title", "Description", "Sub", "Rank", "DBLP", "Year", "ID", "Link", "Abstract Deadline", "Deadline", "Timezone", "Date", "Place"])
      # Ghi dữ liệu từ YAML vào CSV
      for conference in data:
          title = conference["title"]
          description = conference["description"]
          sub = conference["sub"]
          rank = conference["rank"]
          dblp = conference["dblp"]
          confs = conference["confs"]
          for conf in confs:
              year = conf["year"]
              conf_id = conf["id"]
              link = conf["link"]
              timeline = conf["timeline"][0]  # Lấy timeline đầu tiên trong trường hợp có nhiều timeline
              abstract_deadline = timeline.get("abstract_deadline", "")
              deadline = timeline.get("deadline", "")
              timezone = conf["timezone"]
              date = conf["date"]
              place = conf["place"]
              writer.writerow([title, description, sub, rank, dblp, year, conf_id, link, abstract_deadline, deadline, timezone, date, place])


if __name__ == "__main__":
  # URL chứa dữ liệu YAML
  url = "https://ccfddl.github.io/conference/allconf.yml"

  # Tải nội dung từ URL
  response = requests.get(url)
  if response.status_code == 200:
    data = response.text

    # chuyển nội dung sang object
    yaml_data = yaml.safe_load(data)

    write_yml(yaml_data,"allconf.yml")
    write_json(yaml_data,"allconf.json")
    write_csv(yaml_data,"allconf.csv")


