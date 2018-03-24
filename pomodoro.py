import sys, time, os, wave, pyaudio, threading
from pathlib import Path

class TaskTimer():
	def __init__(self, task_time, callback=lambda: None):
		if not isinstance(task_time, dict):
			raise Exception(
				"""
				time must be a dict containing at least one of the following
				keys: 'hours', 'minutes' or 'seconds'.
				"""
			)

		self.seconds_duration = max(
			task_time["seconds"] +
			task_time["minutes"] * 60 +
			task_time["hours"] * 60 * 60,
			0.000000000000000000000000000000000000000000000000000000000000000001
		)

		self.is_paused = False
		self.pause_time = 0

		self.killed = False

		self.start_time = time.time()
		self.end_time = self.start_time + self.seconds_duration

		self.callback = callback

		threading.Thread(target=self.watch_timer).start()

	def seconds_left(self):
		return self.end_time - time.time() + self.pause_time

	def minutes_left(self):
		return self.seconds_left() / 60

	def hours_left(self):
		return self.minutes_left() / 60

	def is_done(self):
		return self.seconds_left() <= 0

	def set_done_callback(self, callback):
		self.callback = callback

	def watch_timer(self):
		sleep_time = 0.05
		while not self.is_done():
			if self.killed:
				return

			if self.is_paused:
				self.pause_time += sleep_time

			time.sleep(sleep_time)

		self.callback()

	def pause(self):
		self.is_paused = True

	def start(self):
		self.is_paused = False

	def dict_time_left(self):
		return {
			"hours": int(self.hours_left()),
			"minutes": int(self.minutes_left() % 60),
			"seconds": int(self.seconds_left() % 60)
		}

	def kill(self):
		self.killed = True

class TaskInfoWriter():
	def __init__(self):
		pass

	def start_task(self, name=None, logs_dir="./logs"):
		if name == None:
			raise Exception("You must give the task a name.")

		dir_name = time.strftime("%b_%Y")

		file_name = time.strftime("%d_(%a)_%b_%Y")

		current_time = time.strftime("# %H:%M - {}".format(name))

		logs_path = Path(logs_dir)

		if not logs_path.is_dir():
			os.mkdir(logs_path)

		dir_path = Path("./logs/{}".format(dir_name))
		if not dir_path.is_dir():
			os.mkdir(dir_path)

		self.file_dir = "./logs/{}/{}.md".format(dir_name, file_name)
		with open(self.file_dir, "a") as f:
			f.write("{}\n".format(current_time))


	def write_notes(self, notes):
		with open(self.file_dir, "a") as f:
			current_time = time.strftime("# %H:%M - END")
			f.write("{}\n{}\n\n".format(notes, current_time))

class SoundPlayer():
	def __init__(self, sound_file):
		# open a wav format sound file
		self.sound_file = wave.open(sound_file, "rb")

		# instantiate PyAudio
		self.audio_player = pyaudio.PyAudio()

		# open stream
		self.stream = self.audio_player.open(
			format = self.audio_player.get_format_from_width(
				self.sound_file.getsampwidth()
			),
			channels = self.sound_file.getnchannels(),
			rate = self.sound_file.getframerate(),
			output = True,
			stream_callback=self.get_next_frame,
			start=False
		)

	def get_next_frame(self, in_data, frame_count, time_info, status):
		# get the next chunk of sound data
		data = self.sound_file.readframes(frame_count)
		return (data, pyaudio.paContinue)


	def play_sound(self, blocking=False):
		# close stream if it was previously open
		self.stream.stop_stream()

		# start reading sound file from the beginning
		self.sound_file.rewind()

		# start stream (this starts the sound playing)
		self.stream.start_stream()

		# if blocking is False, this will play asynchronously
		while blocking and self.stream.is_active():
			time.sleep(0.1)

	def close(self):
		# stop stream
		self.stream.stop_stream()
		self.stream.close()

		# close wave file
		self.sound_file.close()

		# close PyAudio
		self.audio_player.terminate()

if __name__ == "__main__":
	sound = SoundPlayer("./time.wav")

	print("===================================================================")
	title = input("What is the name of this task?\n")
	writer = TaskInfoWriter()
	writer.start_task(title)

	string_time = input(
		"How long do you want to spend on this task?\n[Hours:Minutes:seconds]\n"
	)
	try:
		array_time = list(map(float, string_time.split(":")))
	except:
		print("Error with time string, defaulting to 25 mins.")
		array_time = [0, 25, 0]
	dict_time = {
		"hours": array_time[0],
		"minutes": array_time[1],
		"seconds": array_time[2]
	}
	task = TaskTimer(dict_time)

	while not task.is_done():
		time.sleep(0.1)

	# TaskInfoWriter.start_task(" ".join(sys.argv[1:]))

	sound.play_sound()

	string_time = input(
		"How long do you want to spend on writing notes?\n[Hours:Minutes:seconds]\n"
	)
	try:
		array_time = list(map(float, string_time.split(":")))
	except:
		print("Error with time string, defaulting to 5 mins.")
		array_time = [0, 5, 0]
	dict_time = {
		"hours": array_time[0],
		"minutes": array_time[1],
		"seconds": array_time[2]
	}
	note = TaskTimer(dict_time, sound.play_sound)
	notes_input_message = (
"""
What notes do you have on the task you have just completed?
(Press enter on an empty line when done)
"""
	)

	notes = []
	while True:
		line = input(notes_input_message if len(notes) < 1 else "")
		if line:
			notes.append(line)
		else:
			break

	writer.write_notes("\n".join(notes)) # if you enter notes before callback, error occours because stream is closed

	string_time = input(
		"How long of a break do you want to take?\n[Hours:Minutes:seconds]\n"
	)
	try:
		array_time = list(map(float, string_time.split(":")))
	except:
		print("Error with time string, defaulting to 5 mins.")
		array_time = [0, 5, 0]
	dict_time = {
		"hours": array_time[0],
		"minutes": array_time[1],
		"seconds": array_time[2]
	}
	break_task = TaskTimer(dict_time)

	while not break_task.is_done():
		time.sleep(0.1)
	sound.play_sound(blocking=True)

	sound.close()
