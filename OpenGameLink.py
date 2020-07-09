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
        self.requirements_right = ""
        self.requirements_left = ""
        self.game_dlc = False
        
    def OpenBrowser(self):
        self.driver.get(self.url_game)
    
    def CloseBrowser(self):
        self.driver.close()
        
    def VerifyLink(self):
        palavra = re.search(r"agecheck",self.driver.current_url)
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
            
            self.agecheck = False
            #Cookies 
            """
            {
                lastagecheckage:"1-0-2000"
            }
            """
          
    def GetInfo(self):
        self.SetAge()
             
        regex = "h[a-z].+/app/[0-9]+/"
        while True:
            link_parser = re.findall(rf"{regex}",self.driver.current_url)
            if(self.url_game == link_parser[0]):
                break
        
        self.game_name = self.driver.find_element_by_class_name("apphub_AppName").text

        try:
            gameIsDlc = self.driver.find_element_by_xpath("//div[@class='game_area_bubble game_area_dlc_bubble ']")
            self.game_dlc = True
        except:
            self.game_dlc = False
        
        self.requirements_right = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_rightCol']/ul/ul[@class='bb_ul']").text
        self.requirements_left = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_leftCol']/ul/ul[@class='bb_ul']").text
        
    def SaveInfo(self):
        regex = "[0-9]+"
        name_file = re.findall(rf"{regex}",self.url_game)[0]
        OpenGameLinkInfo = open(f"text\{name_file}.txt","w",encoding="UTF-8")
        
        OpenGameLinkInfo.writelines(self.game_name+"\n")
        OpenGameLinkInfo.writelines("\n")
        OpenGameLinkInfo.writelines(self.requirements_left+"\n\n")
        OpenGameLinkInfo.writelines(self.requirements_right+"\n")
        OpenGameLinkInfo.writelines("\n")
        OpenGameLinkInfo.writelines(f"DLC : {self.game_dlc}")
        
        OpenGameLinkInfo.close()
        