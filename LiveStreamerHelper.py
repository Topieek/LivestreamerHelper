from tkinter import *
from tkinter import ttk
from collections import OrderedDict
import requests, json, os

class App:
	def __init__(self):
		print("INITIALIZING")
	
		self.root = Tk()
		self.root.title("Livestreamer helper")
		self.tree = ttk.Treeview(self.root)

		self.tree["columns"]=("one","two")
		self.tree.column("one", width=500)
		self.tree.column("two", width=100)
		self.tree.heading("one", text="Streamer")
		self.tree.heading("two", text="Viewers")

		url_games = "https://api.twitch.tv/kraken/games/top?limit=25"
		url_streamers = "https://api.twitch.tv/kraken/streams?game="

		response = requests.get(url_games)

		if(response.status_code == requests.codes.ok):

			games = response.json(object_pairs_hook = OrderedDict)
			for key, item in enumerate(games['top']):
				name = item['game']['name']
				game_viewers = item['viewers']
				url_name = item['game']['name']
				url_name = url_name.replace(" ", "+")
				game_id = str(item['game']['_id'])
				self.tree.insert("", "end", game_id, text=name, values=("", game_viewers))
				streamers = requests.get(url_streamers + url_name)
				
				streamers_json = streamers.json(object_pairs_hook = OrderedDict)
				
				for skey, sitem in enumerate(streamers_json['streams']):
					streamer_name = sitem['channel']['name']
					streamer_viewers = str(sitem['viewers'])
					print("STREAMER: " + streamer_name + "; VIEWERS: " + streamer_viewers)
					self.tree.insert(game_id, "end", text="",values=(streamer_name, streamer_viewers))
					self.tree.bind("<Double-1>", self.OnDoubleClick)
					
				print("GAME '" + name + "' INITIALIZED")
			print("INITIALIZING FINISHED")
			self.tree.pack()
			self.root.mainloop()
			
	def OnDoubleClick(self, event):
		item = self.tree.selection()[0]
		selected = self.tree.item(item,"values")[0]
		os.system("livestreamer http://twitch.tv/" + selected + " source")
		
if __name__ == "__main__":
    app = App()
