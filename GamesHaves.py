from functions.SteamBot_Have import SteamBot_Have
from functions.OpenGameLink import OpenGameLink

urls_games_steam = open("text/steamlink_have.txt","r")

# url_steam = "https://steamcommunity.com/id/ahsj4/games/?tab=all&sort=name"
# steam = SteamBot_Have(url_steam)
# steam.OpenBrowser()
# steam.GetLink()
# steam.CountLinks()
# steam.SaveLinks()
# steam.CloseBrowser()

# i = 1
# for url_game_steam in urls_games_steam:
#     openGame = OpenGameLink(url_game_steam,1)
#     openGame.OpenBrowser()
#     print(f"Index:0{i} Link: {url_game_steam}")
#     openGame.VerifyLink()
#     openGame.GetInfo()
#     openGame.ParseInfoSpace()
#     openGame.SaveInfo()
#     openGame.CloseBrowser()
#     i+=1
    
url_game = "https://store.steampowered.com/app/57300"
openGame = OpenGameLink(url_game,1)
openGame.OpenBrowser()
openGame.VerifyLink()
openGame.GetInfo()
openGame.ParseInfoSpace()
openGame.SaveInfo()
openGame.CloseBrowser()