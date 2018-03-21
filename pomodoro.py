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
			stream_callback=self.get_next_frame
		)

	def get_next_frame(self, in_data, frame_count, time_info, status):
		# get the next chunk of sound data
		data = self.sound_file.readframes(frame_count)
		return (data, pyaudio.paContinue)


	def play_sound(self, blocking=False):
		# close stream if it was previously open
		s.stream.stop_stream()

		# start reading sound file from the beginning
		self.sound_file.rewind()

		# start stream (this starts the sound playing)
		self.stream.start_stream()

		# if blocking is False, this will play asynchronously
		while blocking and s.stream.is_active():
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
	s = SoundPlayer("./time.wav")
	TaskInfoWriter.start_task(" ".join(sys.argv[1:]))

	s.play_sound(blocking=True)

	s.close()
