from selenium import webdriver
from time import sleep
import re

class OpenGameLink:
    
    def __init__ (self,url_game):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        url_drive = executable_path=r"./../../driver/chromedriver.exe"
        
        self.driver = webdriver.Chrome(url_drive)
        self.url_game = url_game
        self.agecheck = False
        
    def OpenBrowser(self):
        self.driver.get(self.url_game)
    
    def CloseBrowser(self):
        self.driver.close()
        
    def VerifyLink(self):
        palavra = re.search(r"agecheck",self.url_game)
        if(palavra):
            self.agecheck = True
        
        
        
# url_game = "https://store.steampowered.com/agecheck/app/208650/"
url_game = "https://store.steampowered.com/app/239200"
openGame = OpenGameLink(url_game)
openGame.OpenBrowser()
openGame.VerifyLink()
sleep(3)
openGame.CloseBrowser()