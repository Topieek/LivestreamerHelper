from tkinter import *
import requests, json, os

class LivestreamerHelper:

    def __init__(self):
        print("LivestreamerHelper v1.1")
        self.streamerList = []
        self.root = Tk()
        self.root.title("LivestreamerHelper v1.1")
        
        self.leftFrame = Frame(self.root)
        self.rightFrame = Frame(self.root)
        
        self.leftFrame.pack(side = LEFT)
        self.rightFrame.pack(side = RIGHT)
        
        self.listbox = Listbox(self.leftFrame, selectmode=SINGLE,width=50,height=25)
        url_games = "https://api.twitch.tv/kraken/games/top?limit=25"

        games = requests.get(url_games).json()

        for key, item in enumerate(games['top']):
            name = item['game']['name']
            game_id = str(item['game']['_id'])
            self.listbox.insert(END, name)
            self.listbox.bind("<<ListboxSelect>>", self.gameSelected)
        
        self.listbox.pack()
        
        self.streams = Listbox(self.rightFrame, selectmode=SINGLE,width=150,height=25)
        self.streams.insert(END, "Please select a game first...")
        self.streams.pack()
        
        mainloop()
	
    def gameSelected(self, event):
        selectedGame = self.listbox.get(self.listbox.curselection())
        selectedGame = selectedGame.replace(" ", "+")
        self.streams.delete(0, END)
        
        url_streamers = "https://api.twitch.tv/kraken/streams?limit=1000&game="
        url = url_streamers + selectedGame
        
        streamers = requests.get(url).json()
        
        for skey, sitem in enumerate(streamers['streams']):
            channelname = sitem['channel']['name']
            viewers = str(sitem['viewers'])
            self.streamerList.append(channelname)
            
            self.streams.insert(END, channelname + " (" + viewers + " viewers) ")
            self.streams.bind("<Double-1>", self.streamerSelected)
        
    def streamerSelected(self, event):
        selection = self.streams.curselection()[0]
        selectedChannel = self.streamerList[selection]
        
        os.system("start /wait cmd /c livestreamer http://twitch.tv/" + selectedChannel + " source")
        
if __name__ == "__main__":
    app = LivestreamerHelper()
