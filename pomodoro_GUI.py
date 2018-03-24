import tkinter as tk

PLAY = "\N{Black Right-pointing Triangle}"
PAUSE = "\N{Double Vertical Line}"
NICE_PAUSE = "\N{Double Vertical Bar}"
PLAY_PAUSE = "\N{Black Right-pointing Triangle With Double Vertical Bar}"
STOP = "\N{Black Medium Square}"
NICE_STOP = "\N{Black Square For Stop}"

class PomodoroGUI():
	def __init__(self):
		self.root = tk.Tk()

		tk.Grid.rowconfigure(self.root, 0, weight=1)
		tk.Grid.columnconfigure(self.root, 0, weight=1)

		self.screen_dimentions = {}
		self.screen_dimentions['width'] = self.root.winfo_screenwidth()
		self.screen_dimentions['height'] = self.root.winfo_screenheight()
		self.window_dimentions = {}

		self.frames = {}
		self.buttons = {}
		self.labels = {}
		self.entries = {}
		self.variables = {}
		self.menus = {}

		self.timer = False
		self.percentage = 1.0

		self.show_task_window()

		self.root.resizable(width=False, height=False)
		self.focus()
		self.root.mainloop()

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

		window_width = int(screen_width * window_scale)
		window_height = int(screen_height * window_scale)
		x_offset = int(screen_width * window_offset_scale)
		y_offset = int(screen_height * window_offset_scale)

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

	def show_task_window(self):
		self.set_window_scales(1.0/3)
		self.resize_window()
		self.root.title('Task Timer')

		self.frames['task'] = tk.Frame(self.root)
		self.variables['task'] = {}

		self.frames['task'].rowconfigure(3)
		self.frames['task'].columnconfigure(6)

		self.add_task_entries()
		self.add_task_canvas()
		self.update_timer()
		self.add_task_buttons()
		self.clear_menu_bar()

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
		self.create_circle_arc(width/2, height/2, min(width, height)/2, fill="blue", outline="#DDD", width=4, start=90, end=(359.0 * percent)+90)

	def start_timer(self):
		timer = True
		self.update_timer()

	def stop_timer(self):
		timer = False

	def update_timer(self):
		# PUT THINGS HERE!
		if self.timer:
			self.percentage -= 0.01
			self.canvas.delete("all")
			self.draw_task_circle()
			self.root.after(100, self.update_timer)

	def add_task_entries(self):
		task_frame = self.frames['task']
		self.entries['task'] = {}
		self.variables['task']['entries'] = {}

		task_name = tk.StringVar()
		self.variables['task']['entries']['name'] = task_name

		name_entry = tk.Entry(task_frame, textvariable=task_name)
		name_entry.grid(row=0, columnspan=6, sticky='we')
		self.entries['task']['name'] = name_entry

		hours = tk.IntVar()
		self.variables['task']['entries']['hours'] = hours

		hours_entry = tk.Entry(task_frame, textvariable=hours)
		hours_entry.grid(row=1, column=0, columnspan=1)
		self.entries['task']['hours'] = hours_entry

		minutes = tk.IntVar()
		minutes.set(25)
		self.variables['task']['entries']['minutes'] = minutes

		minutes_entry = tk.Entry(task_frame, textvariable=minutes)
		minutes_entry.grid(row=1, column=1, columnspan=1)
		self.entries['task']['minutes'] = minutes_entry

		seconds = tk.IntVar()
		self.variables['task']['entries']['seconds'] = seconds

		seconds_entry = tk.Entry(task_frame, textvariable=seconds)
		seconds_entry.grid(row=1, column=2, columnspan=1)
		self.entries['task']['seconds_entry'] = seconds_entry

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
		if self.timer == False:
			self.timer = True
			self.update_timer()
			# actually start the timer here
			# disable entries here

	def handle_pause_button(self, *other_arguments):
		self.timer = False
		# actually pause the timer here

	def handle_stop_button(self, *other_arguments):
		self.timer = True
		self.percentage = 1.0
		self.update_timer()
		self.timer = False
		# actually stop the timer here and bring notes screen up
		# (or that will happen as a result of the timer ending)

	def switch_connect_to_measure(self):
		self.remove_task_window()
		# self.show_measure_window()

	def remove_task_window(self):
	# def remove_task_window(self, *other_arguments):
		self.frames['task'].grid_forget()

if __name__ == "__main__":
	PomodoroGUI()
