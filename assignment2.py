
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(executable_path='/Users/Brennan/Desktop/Classes/BIA-660/hw2/chromedriver')


driver.get("http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='S'&season=2018&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts=1520372225716")
assert 'Stats' in driver.title

time.sleep(3)
element = Select(driver.find_element_by_id('sp_hitting_season'))
element.select_by_visible_text('2015')

time.sleep(3)
element = Select(driver.find_element_by_id('sp_hitting_game_type'))
element.select_by_visible_text('Regular Season')

time.sleep(3)
driver.find_element_by_xpath('//*[@id="sp_hitting-0"]/fieldset[5]/label[1]').click()

time.sleep(3)
"""get table for a loop"""


def morePages():
#    currentPage = driver.find_element_by_xpath('//input[@class="paginationWidget-page"]').get_attribute('value')
    lastPage = driver.find_element_by_xpath('//button[@class="paginationWidget-last"]').get_attribute('text')
    print(currentPage + "should be 1")
    print(lastPage + "should be 26")
#    if (currentPage != lastPage):
#        print("True")
#    else: 
#        print("False")
#
#morePages()

table = driver.find_element_by_xpath('//table[@class="stats_table data_grid"]')
time.sleep(3)
for row in table.find_elements_by_xpath(".//tbody"):
    print([td.text for td in row.find_elements_by_xpath(".//td[@class='dg-team_abbrev']")], [td.text for td in row.find_elements_by_xpath(".//td[@class='dg-hr']")])

lastPage = driver.find_element_by_xpath('//button[@class="paginationWidget-last"]')
print(type(lastPage))
    

    
    
    
    