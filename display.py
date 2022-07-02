import os.path
import tkinter as tk

import pandas
from PIL import ImageTk, Image

from weather_data import Weather


# Class to handle what is displayed on screen

class Display:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Weather App')
        # Bind return to update display
        self.window.bind('<Return>', self.update_weather_display)

        self.canvas = tk.Canvas(self.window, width=400, height=400, bg='skyblue')
        self.canvas.pack()
        self.zip_code_entry = ''
        self.weather_image = ''

    def initial_display(self):
        # Intiial data
        zip_code_label = tk.Label(text="Enter a USA Zip Code", font=('Arial', 20), bg='skyblue')
        self.canvas.create_window(200, 150, window=zip_code_label)

        self.zip_code_entry = tk.Entry(self.window)
        self.canvas.create_window(200, 200, window=self.zip_code_entry)

        zip_code_entry_button = tk.Button(text='Get Current Weather', command=self.update_weather_display)
        self.canvas.create_window(200, 250, window=zip_code_entry_button)

        # Check for csv file, if existing set default value for zip code to saved value
        if os.path.isfile('last_location.csv'):
            data = pandas.read_csv('last_location.csv')
            previous_zip_code = data.at[0, 'Zip Code']
            self.zip_code_entry.insert(0, previous_zip_code)

        self.window.mainloop()

        try:
            update_last_location()
        except NameError:
            pass

    # Update display once a zip code is entered, grabs data from Weather class
    def update_weather_display(self, event=None):
        global zip_code
        zip_code = self.zip_code_entry.get()
        try:
            weather = Weather(zip_code)
        except KeyError:
            self.canvas.delete('all')
            error_label = tk.Label(self.window, text="Please Enter a Valid Zip Code", font=('Arial', 20),
                                   bg='skyblue', fg='red')
            self.canvas.create_window(200, 350, window=error_label)
            self.initial_display()
        self.canvas.delete("all")
        location = weather.name
        image_location = weather.update_weather_status(weather.weather_code)
        temp = f"{round(weather.current_temp)}°F"
        description = weather.weather_description
        location_label = tk.Label(self.window, text=location, font=('Arial', 20), bg='skyblue')
        self.canvas.create_window(200, 50, window=location_label)
        self.weather_image = ImageTk.PhotoImage(Image.open(image_location))
        self.canvas.create_image(200, 100, image=self.weather_image)
        temp_label = tk.Label(self.window, text=temp, font=('Arial', 20), bg='skyblue')
        self.canvas.create_window(200, 150, window=temp_label)
        description_label = tk.Label(self.window, text=description, font=('Arial', 20), bg='skyblue')
        self.canvas.create_window(200, 200, window=description_label)
        self.zip_code_entry = tk.Entry(self.window)
        self.canvas.create_window(200, 250, window=self.zip_code_entry)
        zip_code_entry_button = tk.Button(text='Get Current Weather at New Location',
                                          command=self.update_weather_display)
        self.canvas.create_window(200, 300, window=zip_code_entry_button)
        self.canvas.update()


# Updates .csv file with most recent location
def update_last_location():
    last_location = pandas.DataFrame({'Zip Code': zip_code}, index=[1])
    last_location.to_csv('last_location.csv')
