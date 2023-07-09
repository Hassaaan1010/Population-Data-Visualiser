import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
import csv

target = requests.get(
    "https://www.worldometers.info/world-population/population-by-country/"
)

soup = BeautifulSoup(target.text, "html.parser")

link_pattern = re.compile("/world-population/.*-population/")

country_matches = soup.find_all("a", attrs={"href": link_pattern})
country_populations = soup.find_all("td", attrs={"style": "font-weight: bold;"})
countries_data = []
for i in range(30):
    this_country = {
        "Name": country_matches[i].text,
        "Population": country_populations[i].text,
        "Country Data": f"https://www.worldometers.info{country_matches[i]['href']}",
    }
    countries_data.append(this_country)


x_axis = [i.text for i in country_matches[29::-1]]
y_axis = [int((i.text).replace(",", "")) for i in country_populations[29::-1]]
plt.bar(x_axis, y_axis)
plt.xticks(x_axis, rotation="vertical")
plt.title("Top 30 largest countries".title())
plt.xlabel("Country")
plt.ylabel("Population (in billions)")
plt.show()


with open(
    "SamplePopulationData.csv",
    "w",
    newline="",
) as file:
    fields = ["Name", "Population", "Country Data"]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(countries_data)
