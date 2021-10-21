import PySimpleGUI as sg
import os

algo = "dain"

def split_frames(video_input_filename):
	os.system("rm frames/*")
	os.system("rm output/*")
	os.system(f'ffmpeg -i "{video_input_filename}" -compression_level 3 frames/%8d.png')

def run_dain(model):
	os.system(f"./{model}-ncnn-vulkan -v -i frames -o output")

def combine_frames(output_fps):
	os.system(f"ffmpeg -r {output_fps} -pattern_type glob -i 'output/*.png' -c:v libx264 out.mp4")
	

layout = [[sg.Text("Welcome to Vain-App")],[sg.Text("Open video file: "), sg.FileBrowse(key="-IN-")],
	[sg.Text("Choose interpolation algorithm:")],
	[sg.Radio("Dain (Depth-Aware Video Frame Interpolation)", "RADIO1", key="-DAIN-")],
	[sg.Radio("Rife (Real-Time Intermediate Flow Estimation for Video Frame Interpolation)", "RADIO1", key="-RIFE-")],
	[sg.Radio("Cain (Channel Attention Is All You Need for Video Frame Interpolation)", "RADIO1", key="-CAIN-")],
	[sg.Text("Output video FPS (NOT interpolation ratio): "), sg.InputText(key="-FPS-")],
	[sg.Button("Run")],
	[sg.Text("*NOTE: GUI will freeze when running. See terminal window for details on current operation.")],
	[sg.Button("Quit")]]
window = sg.Window("Vain-App",layout)


while True:
	event, values = window.read()
	if event in ("Quit", sg.WIN_CLOSED):
		break
	elif event == "Run":
		if values["-DAIN-"] == True:
			algo = "dain"
		elif values["-RIFE-"] == True:
			algo = "rife"
		elif values["-CAIN-"] == True:
			algo = "cain"
		split_frames(values["-IN-"])
		print(f"Using {algo}!")
		run_dain(algo)
		print("Combining frames!")
		combine_frames(values["-FPS-"])
		
