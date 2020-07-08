from selenium import webdriver
from time import sleep
from re import findall

class SteamBot_Have:
    
    def __init__ (self,url_steam):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        url_drive = executable_path=r"./../../driver/chromedriver.exe"
        
        self.url_steam = url_steam
        self.driver = webdriver.Chrome(url_drive)
        # self.right_click = ActionChains(self.driver)
        self.links = []
        
    def OpenBrowser(self):
        self.driver.get(self.url_steam)

    def GetLink(self):
        sleep(1.5)
        doc = self.driver.page_source
        regex="htt.+store.+/app/[0-9]+"
        self.links = findall(rf"{regex}",doc)

    def CountLinks(self):
        print(len(self.links))
    
    def SaveLinks(self):
        steamlink_have = open("steamlink_have.txt","w")
        
        for link in self.links:
            steamlink_have.write(link+"\n")
            
        steamlink_have.close()
    
    def CloseBrowser(self):
        self.driver.close()