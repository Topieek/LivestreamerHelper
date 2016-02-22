from tkinter import *
from tkinter import messagebox
import requests, json, os, configparser

class LivestreamerHelper:

    def __init__(self):
        print("LivestreamerHelper v1.1")
        self.streamerList = []
        self.currentGame = ""
        self.refreshed = False
        self.root = Tk()
        self.root.title("LivestreamerHelper v1.1")
        
        self.upperFrame = Frame(self.root)
        self.bottomFrame = Frame(self.root)
	
        self.leftFrame = Frame(self.bottomFrame)
        self.rightFrame = Frame(self.bottomFrame)
        
        self.upperFrame.pack(side = TOP)
        self.bottomFrame.pack(side = BOTTOM)

        self.leftButtonFrame = Frame(self.upperFrame)
        self.leftButtonFrame.pack(side=LEFT)
        
        self.rightButtonFrame = Frame(self.upperFrame)
        self.rightButtonFrame.pack(side=RIGHT)
        
        self.leftFrame.pack(side = LEFT)
        self.rightFrame.pack(side = RIGHT)
        
        if os.path.isfile("LivestreamerHelper.ini") and os.access("LivestreamerHelper.ini", os.R_OK):
            self.iniExists = True
        else:
            with open("LivestreamerHelper.ini", "w+") as out:
                out.write("[settings]\n")
                out.write("amountStreamers=1000\n")
                out.write("amountGames=25\n")
                self.iniExists = True
             
        if self.iniExists == True:
            self.configFile = configparser.ConfigParser()
            self.configFile.read("LivestreamerHelper.ini")
            self.configAmountStreamers = self.configFile.get("settings","amountStreamers")
            self.configAmountGames = self.configFile.get("settings","amountGames")
        
        refreshButton = Button(self.leftButtonFrame, text="Refresh", command=self.refresh, width=20)
        refreshButton.pack()
        
        configButton = Button(self.rightButtonFrame, text="Configuration", command=self.config, width=20)
        configButton.pack()
	
        self.listbox = Listbox(self.leftFrame, selectmode=SINGLE,width=50,height=25)
        url_games = "https://api.twitch.tv/kraken/games/top?limit="+self.configAmountGames

        games = requests.get(url_games).json()

        for key, item in enumerate(games['top']):
            name = item['game']['name']
            game_id = str(item['game']['_id'])
            self.listbox.insert(END, name)
            self.listbox.bind("<<ListboxSelect>>", self.game_selected)
        
        self.listbox.pack()
        
        self.streams = Listbox(self.rightFrame, selectmode=SINGLE,width=150,height=25)
        self.streams.insert(END, "Please select a game first...")
        self.streams.pack()
        
        mainloop()
	
    def game_selected(self, event):
        self.streamerList = []
        selectedGame = self.listbox.get(self.listbox.curselection())
        selectedGame = selectedGame.replace(" ", "+")
        self.currentGame = selectedGame
        self.streams.delete(0, END)

        url_streamers = "https://api.twitch.tv/kraken/streams?limit="+self.configAmountStreamers+"&game="
        url = url_streamers + selectedGame
        
        streamers = requests.get(url).json()
        
        for skey, sitem in enumerate(streamers['streams']):
            channelname = sitem['channel']['name']
            viewers = str(sitem['viewers'])
            self.streamerList.append(channelname)
            
            self.streams.insert(END, channelname + " (" + viewers + " viewers) ")
            self.streams.bind("<Double-1>", self.streamer_selected)
        
    def streamer_selected(self, event):
        selection = self.streams.curselection()[0]
        selectedChannel = self.streamerList[selection]
        
        os.system("start /wait cmd /c livestreamer http://twitch.tv/" + selectedChannel + " source")
        
    def refresh(self):
        if self.currentGame == "":
            return False
            
        self.streams.delete(0, END)

        url_streamers = "https://api.twitch.tv/kraken/streams?limit="+self.configAmountStreamers+"&game="
        url = url_streamers + self.currentGame
        streamers = requests.get(url).json()
        
        for skey, sitem in enumerate(streamers['streams']):
            channelname = sitem['channel']['name']
            viewers = str(sitem['viewers'])
            self.streamerList.append(channelname)
            
            self.streams.insert(END, channelname + " (" + viewers + " viewers) ")
            self.streams.bind("<Double-1>", self.streamer_selected)
            
    def config(self):
        self.confTk = Tk()
        self.confTk.title("LivestreamerHelper Configuration")
        
        self.amountGamesLabel = Label(self.confTk, text="Amount of listed games:").grid(row=0)
        self.amountGamesInput = Entry(self.confTk)
        self.amountGamesInput.insert(END, self.configAmountGames)
        self.amountGamesInput.grid(row=0,column=1)
        
        self.amountStreamersLabel = Label(self.confTk, text="Amount of listed streamers:").grid(row=1,ipady=10)
        self.amountStreamersInput = Entry(self.confTk)
        self.amountStreamersInput.insert(END, self.configAmountStreamers)
        self.amountStreamersInput.grid(row=1,column=1)
        
        self.saveButton = Button(self.confTk, text="Save!", command=self.config_save, width=20).grid(row=2,columnspan=2)
        
    def config_save(self):
        self.configFile.set("settings", "amountStreamers", self.amountStreamersInput.get())
        self.configFile.set("settings", "amountGames", self.amountGamesInput.get())
        with open("LivestreamerHelper.ini", "w") as iniFile:
            self.configFile.write(iniFile)
            messagebox.showinfo("Saved!", "Your settings have been saved. Some settings will apply after the next restart!")
            self.confTk.destroy()
            
if __name__ == "__main__":
    app = LivestreamerHelper()
