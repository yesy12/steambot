from functions.SteamBot_WishList import SteamBot_WishList
from functions.OpenGameLink import OpenGameLink
from time import sleep

# url_steam_wishlist = "https://store.steampowered.com/wishlist/profiles/76561198208574821/#sort=name"
# steam_wishList = SteamBot_WishList(url_steam_wishlist)
# steam_wishList.OpenBrowser()
# steam_wishList.GetLinks()
# steam_wishList.SaveLinks()
# steam_wishList.CloseBrowser()

urls_games_steam = open("text/steamlink_wishlist.txt","r")

for url_game_steam in urls_games_steam:
    if(url_game_steam != "\n"):
        print(url_game_steam)
        openGame = OpenGameLink(url_game_steam,0)
        openGame.OpenBrowser()
        openGame.VerifyLink()
        openGame.GetInfo()
        openGame.ParseInfoSpace()
        openGame.ParseInfoReview()
        openGame.SaveInfo()
        openGame.CloseBrowser()

# url_game = "https://store.steampowered.com/app/57300"
# openGame = OpenGameLink(url_game,0)
# openGame.OpenBrowser()
# openGame.VerifyLink()
# openGame.GetInfo()
# openGame.ParseInfoSpace()
# openGame.ParseInfoReview()
# openGame.SaveInfo()
# openGame.CloseBrowser()