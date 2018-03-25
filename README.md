# pomodoro
## Usage
### Command Line
1. `python pomodoro.py [<log directory>]`
2. -> follow prompts

### GUI (recommended)
1. run `python pomodoro_GUI.py [<log directory>]` command or start `run.sh`
2. Fill in task name
3. Fill in amount of time you wish to spend on task
4. Click play
5. If done before time is up, click stop button
6. Fill in amount of time you wish to spend on taking notes
7. Click play
8. When done, click stop (notes are only saved when this button is clicked!)
9. Fill in amount of time you wish to spend on a break
10. repeat

### My Set Up
I put the following line in my `.bash_profile`:

`alias pom="nohup python3 ~/git_repos/pomodoro/pomodoro_GUI.py ~/personal_pomodoro_logs &>/tmp/pomodoro.log &"`

This will run the GUI when I run the `pom` command and will detach the process from the terminal I am working in.

## Dependencies
* python3 and pip (brew install python3)
* portaudio (brew install portaudio)
* pyaudio (pip install pyaudio)

## Issues
* timer process isn't always killed (check if killed from break window? or if you transitioned between windows?)
* add a script to make it run detached from a terminal window?
* text area scrolled on the x axis (don't allow this)
