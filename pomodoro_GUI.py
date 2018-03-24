import tkinter as tk
from pomodoro import TaskTimer, SoundPlayer, TaskInfoWriter

PLAY = "\N{Black Right-pointing Triangle}"
PAUSE = "\N{Double Vertical Line}"
NICE_PAUSE = "\N{Double Vertical Bar}"
PLAY_PAUSE = "\N{Black Right-pointing Triangle With Double Vertical Bar}"
STOP = "\N{Black Medium Square}"
NICE_STOP = "\N{Black Square For Stop}"

class PomodoroGUI():
	def __init__(self):
		self.writer = TaskInfoWriter()
		self.sound = SoundPlayer("./time.wav")

		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.quit)

		tk.Grid.rowconfigure(self.root, 0, weight=1)
		tk.Grid.columnconfigure(self.root, 0, weight=1)

		self.screen_dimentions = {}
		self.screen_dimentions['width'] = self.root.winfo_screenwidth()
		self.screen_dimentions['height'] = self.root.winfo_screenheight()
		self.window_dimentions = {}

		self.frames = {}
		self.buttons = {}
		self.text_areas = {}
		self.entries = {}
		self.variables = {}

		self.show_task_window()

		self.root.resizable(width=False, height=False)
		self.focus()
		self.root.mainloop()

	def quit(self):
		if self.timer:
			self.timer.kill()
		self.root.destroy()

	def create_circle(self, x, y, r, **kwargs):
		return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

	def create_circle_arc(self, x, y, r, **kwargs):
		if "start" in kwargs and "end" in kwargs:
			kwargs["extent"] = kwargs["end"] - kwargs["start"]
			del kwargs["end"]
			return self.canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)

	def set_window_scales(self, window_scale):
		window_offset_scale = (1 - window_scale)/2

		self.screen_dimentions['window_scale'] = window_scale
		self.screen_dimentions['window_offset_scale'] = window_offset_scale

	def resize_window(self):
		screen_width = self.screen_dimentions['width']
		screen_height = self.screen_dimentions['height']
		window_scale = self.screen_dimentions['window_scale']
		window_offset_scale = self.screen_dimentions['window_offset_scale']

		window_width = int(screen_height * window_scale)
		# window_width = int(screen_width * window_scale)
		window_height = int(screen_height * window_scale)
		x_offset = int(screen_width - window_width)
		# x_offset = int(screen_width * window_offset_scale)
		y_offset = int(0)
		# y_offset = int(screen_height * window_offset_scale)

		self.root.geometry("%dx%d+%d+%d" %
			(window_width, window_height, x_offset, y_offset))

		self.window_dimentions['width'] = window_width
		self.window_dimentions['height'] = window_height
		self.window_dimentions['x_offset'] = x_offset
		self.window_dimentions['y_offset'] = y_offset

	def focus(self):
		self.root.focus_force()

	def clear_menu_bar(self):
		self.root.config(menu=tk.Menu(self.root))

	def start_timer(self):
		if self.initial_timer:
			if self.current_window == "task":
				for entry in self.entries["task"].values():
					entry.config(state="disabled")

				self.writer.start_task(self.variables["task"]["entries"]["name"].get())

				self.timer = TaskTimer({
					"hours": self.variables["task"]["entries"]["hours"].get(),
					"minutes": self.variables["task"]["entries"]["minutes"].get(),
					"seconds": self.variables["task"]["entries"]["seconds"].get()
				},
					self.task_timer_timeout
				)
			elif self.current_window == "notes":
				for entry in self.entries["notes"].values():
					entry.config(state="disabled")

				self.timer = TaskTimer({
					"hours": self.variables["notes"]["entries"]["hours"].get(),
					"minutes": self.variables["notes"]["entries"]["minutes"].get(),
					"seconds": self.variables["notes"]["entries"]["seconds"].get()
				},
					self.notes_timer_timeout
				)
			elif self.current_window == "break":
				for entry in self.entries["break"].values():
					entry.config(state="disabled")

				self.timer = TaskTimer({
					"hours": self.variables["break"]["entries"]["hours"].get(),
					"minutes": self.variables["break"]["entries"]["minutes"].get(),
					"seconds": self.variables["break"]["entries"]["seconds"].get()
				},
					self.break_timer_timeout
				)

			self.initial_timer = False
		else:
			self.timer.start()

		self.timer_active = True
		self.update_timer()

	def task_timer_timeout(self):
		self.sound.play_sound()
		self.handle_stop_button()

	def notes_timer_timeout(self):
		self.sound.play_sound()
		self.stop_timer()

	def break_timer_timeout(self):
		self.sound.play_sound()
		self.handle_stop_button()

	def stop_timer(self):
		self.timer_active = False
		self.timer.pause()

	def update_timer(self):
		if self.timer_active:
			self.percentage = self.timer.seconds_left()/self.timer.seconds_duration
			self.canvas.delete("all")

			time_left = self.timer.dict_time_left()

			if self.current_window == "task":
				self.variables["task"]["entries"]["hours"].set(time_left["hours"])
				self.variables["task"]["entries"]["minutes"].set(time_left["minutes"])
				self.variables["task"]["entries"]["seconds"].set(time_left["seconds"])
				self.draw_task_circle()
			elif self.current_window == "notes":
				self.variables["notes"]["entries"]["hours"].set(time_left["hours"])
				self.variables["notes"]["entries"]["minutes"].set(time_left["minutes"])
				self.variables["notes"]["entries"]["seconds"].set(time_left["seconds"])
				self.draw_notes_circle()
			elif self.current_window == "break":
				self.variables["break"]["entries"]["hours"].set(time_left["hours"])
				self.variables["break"]["entries"]["minutes"].set(time_left["minutes"])
				self.variables["break"]["entries"]["seconds"].set(time_left["seconds"])
				self.draw_break_circle()

			self.root.after(50, self.update_timer)

	def entry_validate(self, event):
		entry = event.widget
		if entry == self.entries["task"]["name"]:
			if entry.get() == "":
				entry.insert(0, "Enter a title for this task...")
				entry.config(fg = "grey")
		else:
			if entry.get() == "":
				entry.insert(0, "0")

################################################################################

	def show_task_window(self):
		self.current_window = "task"
		self.timer_active = False
		self.percentage = 1.0
		self.initial_timer = True

		self.set_window_scales(1.0/3)
		self.resize_window()
		self.root.title('Task Timer')

		self.frames['task'] = tk.Frame(self.root)
		self.variables['task'] = {}

		self.frames['task'].rowconfigure(3)
		self.frames['task'].columnconfigure(6)

		self.add_task_entries()
		self.add_task_canvas()
		self.add_task_buttons()
		# self.clear_menu_bar()

		self.frames['task'].grid(sticky='nswe')

		for row_index in range(3):
			tk.Grid.rowconfigure(self.frames['task'], row_index, weight=1)
		for col_index in range(6):
			tk.Grid.columnconfigure(self.frames['task'], col_index, weight=1, minsize=self.window_dimentions['width']/6)

	def add_task_canvas(self):
		self.variables['task']['canvas'] = {}
		self.variables['task']['canvas']['width'] = self.window_dimentions['width']
		self.variables['task']['canvas']['height'] = self.window_dimentions['height'] - self.entries['task']['name'].winfo_reqheight() - self.entries['task']['hours'].winfo_reqheight()
		width = self.variables['task']['canvas']['width']
		height = self.variables['task']['canvas']['height']

		self.canvas = tk.Canvas(self.frames['task'], width=width, height=height, borderwidth=0, highlightthickness=0)
		self.canvas.grid(row=2, columnspan=6, sticky='swe')
		self.draw_task_circle()

	def draw_task_circle(self):
		percent = self.percentage
		width = self.variables['task']['canvas']['width']
		height = self.variables['task']['canvas']['height']
		self.create_circle_arc(width/2, height/2, min(width, height)/2, fill="red", outline="#DDD", width=4, start=90, end=(359.0 * percent)+90)

	def add_task_entries(self):
		task_frame = self.frames['task']
		self.entries['task'] = {}
		self.variables['task']['entries'] = {}

		task_name = tk.StringVar()
		task_name.set("Enter a title for this task...")
		self.variables['task']['entries']['name'] = task_name

		name_entry = tk.Entry(task_frame, textvariable=task_name)
		name_entry.config(fg = "grey")
		name_entry.bind("<FocusIn>", self.empty_name_entry)
		name_entry.bind("<FocusOut>", self.entry_validate)
		name_entry.grid(row=0, columnspan=6, sticky='we')
		self.entries['task']['name'] = name_entry

		hours = tk.IntVar()
		self.variables['task']['entries']['hours'] = hours

		hours_entry = tk.Entry(task_frame, textvariable=hours)
		hours_entry.bind("<FocusOut>", self.entry_validate)
		hours_entry.grid(row=1, column=0, columnspan=1)
		self.entries['task']['hours'] = hours_entry

		minutes = tk.IntVar()
		minutes.set(25)
		self.variables['task']['entries']['minutes'] = minutes

		minutes_entry = tk.Entry(task_frame, textvariable=minutes)
		minutes_entry.bind("<FocusOut>", self.entry_validate)
		minutes_entry.grid(row=1, column=1, columnspan=1)
		self.entries['task']['minutes'] = minutes_entry

		seconds = tk.IntVar()
		self.variables['task']['entries']['seconds'] = seconds

		seconds_entry = tk.Entry(task_frame, textvariable=seconds)
		seconds_entry.bind("<FocusOut>", self.entry_validate)
		seconds_entry.grid(row=1, column=2, columnspan=1)
		self.entries['task']['seconds_entry'] = seconds_entry

	def empty_name_entry(self, *other_arguments):
		entry = self.entries['task']['name']
		if entry.get() == 'Enter a title for this task...':
			entry.delete(0, "end") # delete all the text in the entry
			entry.insert(0, '') #Insert blank for user input
			entry.config(fg = 'black')

	def add_task_buttons(self):
		task_frame = self.frames['task']
		self.buttons['task'] = {}
		self.variables['task']['buttons'] = {}

		start_button = tk.Button(task_frame, text=PLAY)
		start_button.bind('<Button-1>', self.handle_start_button)
		start_button.grid(row=1, column=3, columnspan=1, sticky="we")
		self.buttons['task']['start'] = start_button

		pause_button = tk.Button(task_frame, text=PAUSE)
		pause_button.bind('<Button-1>', self.handle_pause_button)
		pause_button.grid(row=1, column=4, columnspan=1, sticky="we")
		self.buttons['task']['pause'] = pause_button

		stop_button = tk.Button(task_frame, text=STOP)
		stop_button.bind('<Button-1>', self.handle_stop_button)
		stop_button.grid(row=1, column=5, columnspan=1, sticky="we")
		self.buttons['task']['stop'] = stop_button

	def handle_start_button(self, *other_arguments):
		self.root.focus()
		if self.timer_active == False:
			self.root.after(10, self.start_timer)

	def handle_pause_button(self, *other_arguments):
		self.stop_timer()

	def handle_stop_button(self, *other_arguments):
		self.timer_active = True
		self.percentage = 1.0
		self.update_timer()
		self.stop_timer()

		if self.current_window == "task":
			self.switch_task_to_notes()
		elif self.current_window == "notes":
			self.writer.write_notes(self.text_areas["notes"].get("1.0", "end-1c"))
			self.switch_notes_to_break()
		elif self.current_window == "break":
			self.switch_break_to_task()

	def switch_task_to_notes(self):
		self.remove_task_window()
		self.show_notes_window()

	def remove_task_window(self):
	# def remove_task_window(self, *other_arguments):
		self.frames['task'].grid_forget()

################################################################################

	def show_notes_window(self):
		self.current_window = "notes"
		self.timer_active = False
		self.percentage = 1.0
		self.initial_timer = True

		self.set_window_scales(1.0/3)
		self.resize_window()
		self.root.title('Task Notes')

		self.frames['notes'] = tk.Frame(self.root)
		self.variables['notes'] = {}

		self.frames['notes'].rowconfigure(3)
		self.frames['notes'].columnconfigure(4)

		self.add_notes_entries()
		self.add_notes_canvas()
		self.add_notes_buttons()
		self.add_notes_text_area()
		# self.clear_menu_bar()

		self.frames['notes'].grid(sticky='nswe')

		for row_index in range(3):
			tk.Grid.rowconfigure(self.frames['notes'], row_index, weight=1)
		for col_index in range(4):
			tk.Grid.columnconfigure(self.frames['notes'], col_index, weight=1, minsize=self.window_dimentions['width']/4)

	def add_notes_entries(self):
		notes_frame = self.frames['notes']
		self.entries['notes'] = {}
		self.variables['notes']['entries'] = {}

		hours = tk.IntVar()
		self.variables['notes']['entries']['hours'] = hours

		hours_entry = tk.Entry(notes_frame, textvariable=hours)
		hours_entry.bind("<FocusOut>", self.entry_validate)
		hours_entry.grid(row=0, column=0, columnspan=1)
		self.entries['notes']['hours'] = hours_entry

		minutes = tk.IntVar()
		minutes.set(5)
		self.variables['notes']['entries']['minutes'] = minutes

		minutes_entry = tk.Entry(notes_frame, textvariable=minutes)
		minutes_entry.bind("<FocusOut>", self.entry_validate)
		minutes_entry.grid(row=0, column=1, columnspan=1)
		self.entries['notes']['minutes'] = minutes_entry

		seconds = tk.IntVar()
		self.variables['notes']['entries']['seconds'] = seconds

		seconds_entry = tk.Entry(notes_frame, textvariable=seconds)
		seconds_entry.bind("<FocusOut>", self.entry_validate)
		seconds_entry.grid(row=0, column=2, columnspan=1)
		self.entries['notes']['seconds_entry'] = seconds_entry

	def add_notes_canvas(self):
		self.variables['notes']['canvas'] = {}
		self.variables['notes']['canvas']['width'] = self.window_dimentions['width']/4
		self.variables['notes']['canvas']['height'] = self.window_dimentions['height']/4
		width = self.variables['notes']['canvas']['width']
		height = self.variables['notes']['canvas']['height']

		self.canvas = tk.Canvas(self.frames['notes'], width=width, height=height, borderwidth=0, highlightthickness=0)
		self.canvas.grid(row=0, rowspan=2, column=3, columnspan=1, sticky='nswe')
		self.draw_notes_circle()

	def draw_notes_circle(self):
		percent = self.percentage
		width = self.variables['notes']['canvas']['width']
		height = self.variables['notes']['canvas']['height']
		self.create_circle_arc(width/2, height/2, min(width, height)/2, fill="green", outline="#DDD", width=4, start=90, end=(359.0 * percent)+90)

	def add_notes_buttons(self):
		notes_frame = self.frames['notes']
		self.buttons['notes'] = {}
		self.variables['notes']['buttons'] = {}

		start_button = tk.Button(notes_frame, text=PLAY)
		start_button.bind('<Button-1>', self.handle_start_button)
		start_button.grid(row=1, column=0, columnspan=1, sticky="we")
		self.buttons['notes']['start'] = start_button

		pause_button = tk.Button(notes_frame, text=PAUSE)
		pause_button.bind('<Button-1>', self.handle_pause_button)
		pause_button.grid(row=1, column=1, columnspan=1, sticky="we")
		self.buttons['notes']['pause'] = pause_button

		stop_button = tk.Button(notes_frame, text=STOP)
		stop_button.bind('<Button-1>', self.handle_stop_button)
		stop_button.grid(row=1, column=2, columnspan=1, sticky="we")
		self.buttons['notes']['stop'] = stop_button

	def add_notes_text_area(self):
		notes_frame = self.frames['notes']
		self.text_areas['notes'] = {}

		text_area = tk.Text(notes_frame, wrap=tk.WORD, width=1, height=12)
		self.text_areas['notes'] = text_area
		text_area.grid(row=2, rowspan=1, column=0, columnspan=4, sticky="swe")
		text_area.focus()

	# def get_notes_text(self):
	# 	# delete and insert are also things
	# 	return self.text_areas['notes'].get("1.0", "end-1rc")

	def switch_notes_to_break(self):
		self.remove_notes_window()
		self.show_break_window()

	def remove_notes_window(self):
		self.frames['notes'].grid_forget()

################################################################################

	def show_break_window(self):
		self.current_window = "break"
		self.timer_active = False
		self.percentage = 1.0
		self.initial_timer = True

		self.set_window_scales(1.0/3)
		self.resize_window()
		self.root.title('Break Timer')

		self.frames['break'] = tk.Frame(self.root)
		self.variables['break'] = {}

		self.frames['break'].rowconfigure(3)
		self.frames['break'].columnconfigure(6)

		self.add_break_entries()
		self.add_break_canvas()
		self.add_break_buttons()

		self.frames['break'].grid(sticky='nswe')

		for row_index in range(2):
			tk.Grid.rowconfigure(self.frames['break'], row_index, weight=1)
		for col_index in range(6):
			tk.Grid.columnconfigure(self.frames['break'], col_index, weight=1, minsize=self.window_dimentions['width']/6)

	def add_break_canvas(self):
		self.variables['break']['canvas'] = {}
		self.variables['break']['canvas']['width'] = self.window_dimentions['width']
		self.variables['break']['canvas']['height'] = self.window_dimentions['height'] - self.entries['break']['hours'].winfo_reqheight()
		width = self.variables['break']['canvas']['width']
		height = self.variables['break']['canvas']['height']

		self.canvas = tk.Canvas(self.frames['break'], width=width, height=height, borderwidth=0, highlightthickness=0)
		self.canvas.grid(row=2, columnspan=6, sticky='swe')
		self.draw_break_circle()

	def draw_break_circle(self):
		percent = self.percentage
		width = self.variables['break']['canvas']['width']
		height = self.variables['break']['canvas']['height']
		self.create_circle_arc(width/2, height/2, min(width, height)/2, fill="blue", outline="#DDD", width=4, start=90, end=(359.0 * percent)+90)

	def add_break_entries(self):
		break_frame = self.frames['break']
		self.entries['break'] = {}
		self.variables['break']['entries'] = {}

		hours = tk.IntVar()
		self.variables['break']['entries']['hours'] = hours

		hours_entry = tk.Entry(break_frame, textvariable=hours)
		hours_entry.bind("<FocusOut>", self.entry_validate)
		hours_entry.grid(row=0, column=0, columnspan=1)
		self.entries['break']['hours'] = hours_entry

		minutes = tk.IntVar()
		minutes.set(5)
		self.variables['break']['entries']['minutes'] = minutes

		minutes_entry = tk.Entry(break_frame, textvariable=minutes)
		minutes_entry.bind("<FocusOut>", self.entry_validate)
		minutes_entry.grid(row=0, column=1, columnspan=1)
		self.entries['break']['minutes'] = minutes_entry

		seconds = tk.IntVar()
		self.variables['break']['entries']['seconds'] = seconds

		seconds_entry = tk.Entry(break_frame, textvariable=seconds)
		seconds_entry.bind("<FocusOut>", self.entry_validate)
		seconds_entry.grid(row=0, column=2, columnspan=1)
		self.entries['break']['seconds_entry'] = seconds_entry

	def add_break_buttons(self):
		break_frame = self.frames['break']
		self.buttons['break'] = {}
		self.variables['break']['buttons'] = {}

		start_button = tk.Button(break_frame, text=PLAY)
		start_button.bind('<Button-1>', self.handle_start_button)
		start_button.grid(row=0, column=3, columnspan=1, sticky="we")
		self.buttons['break']['start'] = start_button

		pause_button = tk.Button(break_frame, text=PAUSE)
		pause_button.bind('<Button-1>', self.handle_pause_button)
		pause_button.grid(row=0, column=4, columnspan=1, sticky="we")
		self.buttons['break']['pause'] = pause_button

		stop_button = tk.Button(break_frame, text=STOP)
		stop_button.bind('<Button-1>', self.handle_stop_button)
		stop_button.grid(row=0, column=5, columnspan=1, sticky="we")
		self.buttons['break']['stop'] = stop_button

	def switch_break_to_task(self):
		self.remove_break_window()
		self.show_task_window()

	def remove_break_window(self):
		self.frames['break'].grid_forget()

if __name__ == "__main__":
	PomodoroGUI()
