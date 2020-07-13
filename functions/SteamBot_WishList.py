from selenium import webdriver
from time import sleep
from re import findall

class SteamBot_WishList:
    
    def __init__ (self,url_steam_wishlist):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        
        url_drive = executable_path=r"./../../driver/chromedriver.exe"
        self.driver = webdriver.Chrome(url_drive)
        self.url_steam_wishlist = url_steam_wishlist
        self.links = []
        
    def OpenBrowser(self):
        self.driver.get(self.url_steam_wishlist)
    
    def CloseBrowser(self):
        self.driver.close()
        
    def GetLinks(self):
        pre = self.driver.find_element_by_xpath("//pre").text

        appids = findall(r"[0-9]+.:",pre)
        for appid in appids:
            appid_ = findall(r"[0-9]+",appid)[0]
            link = f"https://store.steampowered.com/app/{appid_}"
            self.links.append(link)
       
        # doc = self.driver.page_source
        
        
            
    def SaveLinks(self):
        steamlink_wishList = open("text\steamlink_wishlist.txt","a+")
        
        for link in self.links:
            steamlink_wishList.writelines(f"\n{link}")
            
        steamlink_wishList.close()