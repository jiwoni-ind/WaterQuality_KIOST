#%%
from selenium import webdriver

driver = webdriver.Chrome('C:\\Users\\jwkim\\chromedriver_win32\\chromedriver.exe')
driver.get('https://www.nifs.go.kr/femo/data_obs.femo')
# driver.close()