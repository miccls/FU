# Frivillig uppgift för programmeringsteknik II
# Ta strögware som inspiration

import tkinter as tk
from person import Person
import random
from settings import Settings

class FU:
    def __init__(self):

        # Settings
        self.settings = Settings()
        self.settings.width = 700
        self.settings.height = 700
        self.settings.main_color = 'white'
        self.settings.options_color = 'green'

        # Buttons & Entries
        self.entries = {
            'people' : {'text' : 'Number of people', 'entry' : None, 'label': None, 'default' : '30'},
            'infected' : {'text': 'Number of infected', 'entry' : None, 'label': None, 'default' : '10'},
            'probability' : {'text': 'Probability of infection', 'entry' : None, 'label': None, 'default' : '0.2'},
            'recovery_time' : {'text': 'Duration of sickness', 'entry' : None, 'label': None, 'default' : '7'},
            'speed' : {'text' : 'Speed of people', 'entry': None, 'label' : None, 'default' : '10'},
            'death_rate' : {'text' : 'Probability of death', 'entry': None, 'label' : None, 'default' : '0.3'}
        }

        self.root = tk.Tk()
        self.root.title('Pandemisimulator')
        self.canvas = tk.Canvas(self.root, width = self.settings.width*3/4, height = 700, background=self.settings.main_color)
        self.canvas.grid(column=0, row=0)
        self.button_canvas = tk.Canvas(self.root, width = self.settings.width*1/4, height = self.settings.height, background=self.settings.options_color)
        self.button_canvas.grid(column=1, row=0)

    def run(self):
        self.add_buttons()
        self.add_entries()
        self.root.mainloop()

    def add_buttons(self):
        #self.canvas.create_rectangle(700*3/4, 0,700, 700, fill='black')
        self.buttonframe = tk.Frame(self.button_canvas, background=self.settings.options_color)
        self.buttonframe.place(relx=0.5, rely = 0.03, anchor='n')
        self.quit_button = tk.Button(self.buttonframe,
            text='Quit', command= lambda: self.root.quit(), 
            highlightcolor = '#ffffff', width = 15, height = 2,
            background = self.settings.options_color, highlightthickness=0)
        self.quit_button.pack()
        self.start_button = tk.Button(self.buttonframe,
            text='Start', command= lambda: self.start(), 
            highlightcolor = '#ffffff', width = 15, height = 2,
            background = self.settings.options_color, highlightthickness=0)
        self.start_button.pack()

    def add_entries(self):
        # Adds the entryboxes to the screen, all that have been defined in the
        # self.entries dictionary in the beginning.
        for key, entry in self.entries.items():
            self.entries[key]['label'] = tk.Label(self.buttonframe, text=entry['text'], background=self.settings.options_color)
            self.entries[key]['entry'] = tk.Entry(self.buttonframe, width=10, highlightthickness=0)
            self.entries[key]['label'].pack()
            self.entries[key]['entry'].pack()
            # Inserting default value
            self.entries[key]['entry'].insert(0, self.entries[key]['default'])

        # self.numinf_label = tk.Label(self.buttonframe, text='Number of infected', background=self.settings.options_color)
        # self.numinf_entry = tk.Entry(self.buttonframe, width=10, highlightthickness=0)
        # self.numinf_label.pack()
        # self.numinf_entry.pack()

    def empty_entries(self):
        # Empties the entry boxes.
        for entry in self.entries.values():
            entry['entry'].delete(0, tk.END)
    
    def start(self):
        # Starts simulation.
        data = {k: v['entry'].get() for k, v in self.entries.items()}
        self.empty_entries()
        for key, value in data.items():
            if value != '':
                # If given a value, set it. Else use default value
                setattr(self.settings, key, float(value))
        number_of_people = int(float(data['people'])) if data['people'] != '' else 30
        number_of_inf = int(float(data['infected'])) if data['infected'] != '' else 5
        self.people = [Person(self.canvas, self.settings, is_infected = True if i < number_of_inf else False) \
            for i in range(number_of_people)]
        for person in self.people:
            person.drawPerson()

        # Set to default values again
        for key, entry in self.entries.items():
            self.entries[key]['entry'].insert(0, getattr(self.settings, key))

        self.animation()

    def animation(self):
        delay = 200
        self.canvas.delete("all")
        for person in self.people:
            person.update()
            person.drawPerson()
        for index, person in enumerate(self.people):
            if index == len(self.people):
                # If we are at the last person, everyone has been checked
                break

            for person2 in self.people[index + 1:]:
                if person.isImmune() or person2.isImmune():
                    continue
                #No interactions with immune people
                if person.inContact(person2):
                    if person.isSick() and person2.isSick():
                        continue

                    elif person.isSick() is True and random.random() < self.settings.probability:
   
                        person2.setState(True)

                    elif person.isSick() is True and random.random() < self.settings.probability:
   
                        person.setState(True)

        self.root.after(self.settings.delay, self.animation)

        


if __name__ == '__main__':
    gui = FU()
    gui.run()