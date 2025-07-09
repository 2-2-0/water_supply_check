# wsc (water_supply_check) by 220 (E Castañeda)
# v1.0r - may 2025
# GPLv3 License - please credit where due

from requests_html import HTMLSession
from bs4 import BeautifulSoup

import datetime
import csv

# mz2
# 227 - Lindavista Vallejo

# mz3
# 2174 - Nueva Vallejo


# 613 - San Bartolo Atepehuacan
# 2166 - Nueva Industrial Vallejo

distribution_points = [
    ("227", "Lindavista Vallejo"),
    ("2174", "Nueva Vallejo"),
    ("2166", "Nueva Industrial Vallejo"),
    ("613", "San Bartolo Atepehuacan")
]

ROOT_URL = 'https://aguaentucolonia.sacmex.cdmx.gob.mx/#/search/'

CSV_PATH = "./"
CSV_FILENAME = "wst.csv"


session = HTMLSession ()


def fetchData (zip_code):
    global ROOT_URL
    global session

    url = ROOT_URL+zip_code
    print ("fetching {0}".format (url))
    r = session.get (url)
    r.html.render ()
    soup = BeautifulSoup (r.html.html, 'html.parser')

    message_section = soup.find (id="message-secction")
    hours_section = soup.find (id="hours-secction")

    return (message_section, hours_section)

def analyzeData (sections):
    m_section = sections [0]
    h_section = sections [1]

    if (m_section.p!=None):
        water_source = m_section.p.b.text
        water_schedule = h_section.div.div.find_all ("span") [2].text
        
    else:
        water_source = "Problemas de suministro"
        water_schedule = "Sin horario definido"
        
    return (water_source, water_schedule)

def currentTime ():
    return datetime.datetime.now ()

def main ():
    print ("water_supply_check, by 220")
    print (CSV_PATH+CSV_FILENAME)

    for distribution_point in distribution_points:
        data = fetchData (distribution_point [0])
        results = analyzeData (data)
        c_time = currentTime ()

        write_data = [
            [
                distribution_point [0], 
                distribution_point [1], 
                c_time,
                results [0],
                results [1]
            ]
        ]
        with open (CSV_PATH+CSV_FILENAME, 'a', newline='') as csv_file:
            writer = csv.writer (csv_file)
            writer.writerows (write_data)

if __name__ == "__main__":
    main ()
