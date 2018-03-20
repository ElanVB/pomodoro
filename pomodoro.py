import sys, time, wave, pyaudio

class TaskInfoWriter():
	def __init__(self):
		pass

	def start_task(name=None):
		if name == None:
			raise Exception("You must give the task a name.")

		date = time.strftime("%a %d %b %Y")
		file_title = "# {}".format(date)

		current_time = time.strftime("%H:%M")
		task_title = "## {} - {}".format(current_time, name)
		print(file_title)
		print(task_title)

class SoundPlayer():
	def __init__(self, sound_file):
		#define stream chunk
		self.chunk = 1024

		#open a wav format music
		self.sound_file = wave.open(sound_file, "rb")
		#instantiate PyAudio
		self.audio_player = pyaudio.PyAudio()

		#open stream
		self.stream = self.audio_player.open(
			format = self.audio_player.get_format_from_width(
				self.sound_file.getsampwidth()
			),
			channels = self.sound_file.getnchannels(),
			rate = self.sound_file.getframerate(),
			output = True
		)

	def play_sound(self):
		#read data
		data = self.sound_file.readframes(self.chunk)

		#play stream
		while data:
			self.stream.write(data)
			data = self.sound_file.readframes(self.chunk)

		self.sound_file.rewind()

	def close(self):
		#stop stream
		self.stream.stop_stream()
		self.stream.close()

		#close PyAudio
		self.audio_player.terminate()

if __name__ == "__main__":
	s = SoundPlayer("./time.wav")
	TaskInfoWriter.start_task(" ".join(sys.argv[1:]))

	s.play_sound()
	s.close()
