from selenium import webdriver
from selenium.webdriver.support.select import Select
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
        self.game_name = ""
        self.requirements = ""
        self.game_dlc = False
        
    def OpenBrowser(self):
        self.driver.get(self.url_game)
    
    def CloseBrowser(self):
        self.driver.close()
        
    def VerifyLink(self):
        palavra = re.search(r"agecheck",self.url_game)
        if(palavra):
            self.agecheck = True

    def SetAge(self):
        if(self.agecheck == True):
            ageDay = self.driver.find_element_by_name("ageDay")
            selectAgeDay = Select(ageDay)
            selectAgeDay.select_by_value("10")
            
            ageMonth = self.driver.find_element_by_name("ageMonth")
            selectAgeMonth = Select(ageMonth)
            selectAgeMonth.select_by_value("March")
            
            ageYear = self.driver.find_element_by_name("ageYear")
            selectAgeYear = Select(ageYear)
            selectAgeYear.select_by_value("2000")
            
            acessToPage = self.driver.find_element_by_xpath("//a[@class='btnv6_blue_hoverfade btn_medium']")
            acessToPage.click()
            
            #Cookies 
            """
            {
                lastagecheckage:"1-0-2000"
            }
            """
          
    def GetInfo(self):
        self.SetAge()
        sleep(1)
        self.game_name = self.driver.find_element_by_class_name("apphub_AppName").text

        try:
            gameIsDlc = self.driver.find_element_by_xpath("//div[@class='game_area_bubble game_area_dlc_bubble ']")
            self.game_dlc = True
        except:
            self.game_dlc = False
        
        self.requirements = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_rightCol']/ul/ul[@class='bb_ul']").text
        
    def SaveInfo(self):
        OpenGameLinkInfo = open("opengamelinkinfo.txt","w")
        
        OpenGameLinkInfo.writelines(self.game_name+"\n")
        OpenGameLinkInfo.writelines("\n")
        OpenGameLinkInfo.writelines(self.requirements+"\n")
        OpenGameLinkInfo.writelines("\n")
        OpenGameLinkInfo.writelines(f"DLC : {self.game_dlc}")
        
        OpenGameLinkInfo.close()
        
        
url_game = "https://store.steampowered.com/agecheck/app/208650/"
#game agecheck
# url_game = "https://store.steampowered.com/app/239200"
#game
# url_game = "https://store.steampowered.com/app/1248434"
#dlc
openGame = OpenGameLink(url_game)
openGame.OpenBrowser()
openGame.VerifyLink()
openGame.GetInfo()
openGame.SaveInfo()
sleep(3)
openGame.CloseBrowser()