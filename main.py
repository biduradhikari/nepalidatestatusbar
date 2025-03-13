import rumps
import pandas as pd
import json
from datetime import datetime

# Nepali Unicode numbers
nepali_numbers = {
    0: '०', 1: '१', 2: '२', 3: '३', 4: '४',
    5: '५', 6: '६', 7: '७', 8: '८', 9: '९'
}

# Nepali Unicode months
nepali_months = {
    1: 'बैशाख', 2: 'जेष्ठ', 3: 'आषाढ', 4: 'श्रावण',
    5: 'भदौ', 6: 'असोज', 7: 'कार्तिक', 8: 'मंसिर',
    9: 'पुस', 10: 'माघ', 11: 'फाल्गुण', 12: 'चैत्र'
}

# Load data from JSON
with open("datesdb.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

def convert_to_nepali(number):
    return ''.join(nepali_numbers[int(digit)] for digit in str(number))

class DateStatusBarApp(rumps.App):
    def __init__(self):
        super(DateStatusBarApp, self).__init__("Date")
        self.df = df
        self.current_date = None
        self.menu = ["Update Date"]
        self.add_sidebar_menu()
        self.update_date()
        self.timer = rumps.Timer(self.refresh_date, 60)
        self.timer.start()

    def add_sidebar_menu(self):
        self.menu.add(rumps.MenuItem("About", callback=self.show_about))

    def show_about(self, _):
        rumps.alert("Nepali Calendar Menubar", "Version 1.2\nbiduradhikari@gmail.com\n\nhttps://github.com/biduradhikari/nepalidatestatusbar")

    @rumps.clicked("Update Date")
    def update_date(self, _=None):
        self.title = self.get_nepali_date()

    def refresh_date(self, _):
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            self.update_date()

    def get_nepali_date(self):
        today = datetime.now()
        today_month, today_day, today_year = today.month, today.day, today.year
        self.current_date = today.strftime("%Y-%m-%d")

        nepali_date_row = self.df[
            (self.df['EnglishMonth'] == today_month) &
            (self.df['EnglishDay'] == today_day) &
            (self.df['EnglishYear'] == today_year)
        ]

        if not nepali_date_row.empty:
            nepali_date = nepali_date_row.iloc[0]
            nepali_month = nepali_months[int(nepali_date['NepaliMonth'])]
            nepali_day = convert_to_nepali(nepali_date['NepaliDay'])
            nepali_year = convert_to_nepali(nepali_date['NepaliYear'])
            return f"{nepali_month} {nepali_day}, {nepali_year}"
        else:
            return "Date not found"

if __name__ == "__main__":
    app = DateStatusBarApp()
    app.run()
