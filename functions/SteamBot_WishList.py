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
        sleep(5)

        links_wishList = self.driver.find_elements_by_xpath("//div[@class='wishlist_row']/div[@class='content']/a[@class='title']")
    
        regex = "htt.+store.+/app/[0-9]+"
        
        for link_wishList in links_wishList:
            link = link_wishList.get_attribute("href")
            link = findall(rf"{regex}",link)[0]
            self.links.append(link)
            
    def SaveLinks(self):
        steamlink_wishList = open("text\steamlink_wishlist.txt","w")
        
        for link in self.links:
            steamlink_wishList.write(f"\n{link}")
            
        steamlink_wishList.close()