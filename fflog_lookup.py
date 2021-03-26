import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import re

def print_table_fflog(first_name, last_name, server):

    additional_jobs = ''
    
    ############### 
    # open driver #
    ###############
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    DRIVER_PATH = 'D:\ChromeDriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
    driver.implicitly_wait(10)
    driver.get(f"https://www.fflogs.com/character/na/{server}/{first_name}%20{last_name}")

    ########################################################################################################################

    ############
    # get data #
    ############

    # boss name
    boss_names = driver.find_elements_by_xpath('//div[contains(@style, "display:flex;flex-direction:row;align-items:center")]')

    # percentiles
    percentiles = driver.find_elements_by_xpath('//td[contains(@class, "rank-percent hist-cell")]')

    # icon of class
    pics = driver.find_elements_by_xpath('//td[contains(@class, "rank-percent hist-cell")]//img')

    # find r dps
    rdpses = driver.find_elements_by_xpath('//td[@class="rank-per-second verbose rdps"]')

    # find all star    
    all_stars = driver.find_elements_by_xpath('//td[@class="all-star-points verbose primary"]')

    # difficulty of raid
    difficulty = driver.find_element_by_xpath('//div[@class="best-perf-avg"]//span[@class="primary"]')

    ########################################################################################################################


    # intialize
    log_table = pd.DataFrame()

    b_names = []
    ptile = []
    job = []
    rDPS = []
    all_star = []
    diff = difficulty.text

    for boss in boss_names:
        b_names.append(boss.text)

    for p in percentiles:
        ptile.append(p.text)

    # choose pic, get class name, split by -, last element is class
    for pic in pics:
        job.append(pic.get_attribute('class').split('-')[-1])    

    for rdps in rdpses:
        rDPS.append(rdps.text)

    for astar in all_stars:
        all_star.append(astar.text)


    log_table['boss'] = b_names
    log_table['ptile'] = ptile

    # catch if did not clear full fight
    try:
        log_table['job'] = job
    except:
        additional_jobs = job

    log_table['rDPS'] = rDPS
    log_table['all_star'] = all_star

    # output
    print(first_name, last_name, ',', server, ',' , diff, additional_jobs)
    print()
    print(log_table)
    print('==========================================================')

    
def get_name_server(chat_msg):

    # split sentence
    temp = chat_msg.split('. ')

    # get first two words, firstname + lastname_Server
    temp2 = [line.split(' ')[:2] for line in temp]

    for item in temp2:
        # find server
        server_list = 'Behemoth|Excalibur|Exodus|Hyperion|Lamia|Leviathan|Ultros'
        p = re.compile(server_list)
        server = p.findall(item[1])

        # default server YOU are on
        # if no server, server = Famfrit
        if len(server) > 0:        
            # str name of server   
            server_name = server[0]
        else:
            server_name = 'Famfrit'


        item[1] = item[1].replace(server_name, '')
        item.append(server_name)
    
    return temp2   
  
########################################################################################################################  
# start here , paste in chat msg
chat_msg = input('insert chat:')
print('***************************************************')
print('***************************************************')

people_to_lookup = get_name_server(chat_msg)

for person in people_to_lookup:
    first_name = person[0]
    last_name = person[1]
    server = person[2]
    
    try:
        print_table_fflog(first_name, last_name, server)
    except:
        print('Error:', first_name, last_name, server)  

#######################################################################################################################
