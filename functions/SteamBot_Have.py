from selenium import webdriver
from time import sleep
from re import findall
from pymongo import MongoClient
from .InfoDb import InfoDb

class SteamBot_Have:

    def __init__ (self,url_steam):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        url_drive = executable_path=r"./../../driver/chromedriver.exe"
        
        self.url_steam = url_steam
        self.driver = webdriver.Chrome(url_drive)
        self.links = []

        db = InfoDb()
        url = f"mongodb+srv://{db.getUsername()}:{db.getPassword()}@cluster0.nth3w.mongodb.net/{db.getDbName()}?retryWrites=true&w=majority"
        
        self.connect = MongoClient(url,27017)

        self.db = self.connect[db.getDbName()]   
        self.links_db = self.db.links


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
        # steamlink_have = open("text\steamlink_have.txt","w")
        
        index = 0
        for link in self.links:
            result = self.links_db.find_one({"link": link})
            
            index += 1
            if(result == None):
                link_info = {
                    "link" : link,
                    "verified" : 0
                }
                link_id = self.links_db.insert_one(link_info).inserted_id

            print(index)

        # steamlink_have.close()
    
    def CloseBrowser(self):
        self.driver.close()