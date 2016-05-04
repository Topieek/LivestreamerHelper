from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


import openpyxl

from tkinter import *
from tkinter import filedialog

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from datetime import datetime

class Werkrooster:

    def __init__(self):
        self.root = Tk()
        self.root.title("Werkrooster -> Google Calendar")

        self.Frame = Frame(self.root)
        self.Frame.pack(side = TOP)


        self.Openfile = Button(self.Frame, text='Open rooster', command=self.askopenfile).pack()
        self.Submit = Button(self.Frame, text='Toevoegen aan Google Calendar', command=self.submit).pack()

        mainloop()

    def askopenfile(self):
        self.file = filedialog.askopenfilename(filetypes=[('Excelsheet','*.xlsx'), ('Excelsheet', '*.xls')], initialdir="../")
        print(self.file)

    def submit(self):
        wb = openpyxl.load_workbook(self.file)
        self.sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        werkdagen = []
        maximum = 100

        for i in range(1, maximum):
            if("Lanfrey Jansen" in self.sheet['A' + str(i)].value):
                self.row = str(i)
                break
            else:
                continue

        letters = ["B", "C", "D", "E", "F", "G", "H"]

        for letter in letters:
            if("FF008000" in self.sheet[letter + str(self.row)].fill.start_color.index):
                werkdagen.append({'date': self.sheet[letter + '2'].value.date(), 'time': str(self.sheet[letter + self.row].value)})

        for werkdag in werkdagen:
            datumStart = str(werkdag['date']) + "T"
            tijd = werkdag['time'].split("-")
            datumStart = datumStart + tijd[0] + ":00"
            datumEind = str(werkdag['date']) + "T"
            tijd = werkdag['time'].split("-")
            datumEind = datumEind + tijd[1] + ":00"

            SCOPES = 'https://www.googleapis.com/auth/calendar'
            store = file.Storage('Storage.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets("gc.json", SCOPES)
                creds = tools.run_flow(flow, store, flags) \
                    if flags else tools.run(flow, store)
            CAL = build('calendar', 'v3', http=creds.authorize(Http()))

            GMT_OFF = "+02:00"

            EVENT = {
                'summary': 'Werken van ' + tijd[0] + " tot " + tijd[1],
                'start': {'dateTime': datumStart + '%s' % GMT_OFF},
                'end': {'dateTime': datumEind + '%s' % GMT_OFF}
            }

            e = CAL.events().insert(calendarId='primary',
                    sendNotifications=False, body=EVENT).execute()

        #if("FF008000" in self.sheet['D' + self.row].fill.start_color.index):
        #    print(self.sheet['D1'].value)


if __name__ == "__main__":
    app = Werkrooster()