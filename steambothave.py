from selenium import webdriver
from time import sleep
from re import findall

class SteamBotHave:
    
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
        regex="[A-zi]{5}://[A-zi]{5}.[A-zi]{12}.[A-zi]{3}/app/[0-9]([0-9]|)([0-9]|)([0-9]|)([0-9]|)([0-9]|)([0-9]|)([0-9]|)"
        self.links = findall(rf"{regex}",doc)

    def CountLinks(self):
        print(len(self.links))
    
    def SaveLinks(self):
        
    
    def CloseBrowser(self):
        self.driver.close()
    
url_steam = "https://steamcommunity.com/id/ahsj4/games/?tab=all&sort=name"
steam = SteamBotHave(url_steam)
steam.OpenBrowser()
steam.GetLink()
steam.CountLinks()
steam.CloseBrowser()

url_steam = "https://steamcommunity.com/id/yesy12/games/?tab=all&sort=name"
steam2 = SteamBotHave(url_steam)
steam2.OpenBrowser()
steam2.GetLink()
steam2.CountLinks()
steam2.CloseBrowser()