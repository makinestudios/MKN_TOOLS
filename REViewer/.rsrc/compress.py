###
#TODO: Fix Max issue with asking for the files many times and double executing the compression
###
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import askyesno
import subprocess,time
from os import path, sep, makedirs, chmod, chown
from pwd import getpwnam
from grp import getgrnam
from datetime import date

root = tk.Tk()
root.title="MAkinE RE-Viewer"
makine_logo = tk.PhotoImage(file=path.dirname(__file__)+sep+"makine.gif")


files = []
file_labels=[]

def announce_status( string ):
	status_label.config(text= string )
	root.update()
	
def select_files():
	global files
	print("Selecting...")
	files = askopenfilenames(
		#initialdir="/Volumes/pegasus/01_PROJECTS/",
		initialdir="/Volumes/pegasus/01_PROJECTS/18036_ARCD001_Cruz_Diez_Documentary/07_DI/03_Footage_SLXs/02_ONL_Footage/051518/",
		title="Select movie files."
	)
	announce_status("QUEUED FILES:")
	
	for i , f in enumerate(files):
		
		file_labels.append (
			tk.Label(
				files_frame,
				text=path.basename(str(f)),
				justify=tk.CENTER,
				fg="#555555"
			)
		)
		file_labels[i].pack()
	
	buttons[0].config(state="normal")

def compress_files():
	print("Compressing...")
	today = date.today()
	today_tag = today.strftime("%m%d%y")

	announce_status("PROCESSING FILES...")
	
	root.update()
	
	for b in buttons:
		b.config(state="disabled")
		
	
	for i, f in enumerate(files):
		new_path = "/Volumes/pegasus/01_PROJECTS/"+get_mkn_project_root(f)+sep+"10_Review"+sep+today_tag+sep
		
		if not path.exists(new_path):
			makedirs(new_path)
			#chown(new_path,getpwnam("nobody"),getgrnam("editorial-graphics"))
			chmod(new_path,0o0775)
		
		new_filename = path.splitext(path.basename(f))[0]
		
		dest=new_path+new_filename+"_h264.mov"
		replace = False
		
		if path.exists(dest):
			replace = askyesno('Confirm', '"' + dest + '"'  +" exists, raplce it?") 
			
		if not path.exists(dest) or replace:
			
			subprocess.run([
			"ffmpeg",
			"-i", f ,
			"-c:v" ,"libx264",
			"-x264opts", "keyint=6:scenecut=-1",
			"-profile:v", "main",
			"-pix_fmt", "yuv420p",
			"-q", "0",
			"-strict", "-2",
			"-vb", "16M",
			"-y",
			dest
			])
			file_labels[i].config(fg="#008800")
			if replace :
				file_labels[i].config(text=file_labels[i].cget("text") + " (Replaced)")
		else:
			file_labels[i].config(text=file_labels[i].cget("text") + " (Skipped)")
		
		root.update()
		
	announce_status("PROCESSED FILES:")
	for b in buttons:
		b.config(state="normal")

def get_mkn_project_root( path ):
	
	project_root_path = path.split(sep)[4]
	
	return project_root_path
	
w1 = tk.Label(root,image=makine_logo).pack(side="top")
explanation = """
Select movies to generate REVIEW files.
"""

status_label = tk.Label(
	root,
	justify=tk.RIGHT,
	padx =50,
	text="NO FILE SELECTED"
	)
desc_label = tk.Label(
	root,
	justify=tk.RIGHT,
	padx =50,
	text=explanation
	)
files_frame = tk.Frame(
	root
	)

desc_label.pack(side="top")
status_label.pack(side="top")
files_frame.pack(side="top")	

buttons = [
	tk.Button(root, text='Compress Files', width=25,command=compress_files,state="disabled"),
	tk.Button(root, text='Select Files', width=25,command=select_files)
	]

for i in buttons:
	i.pack(side="bottom")

	
root.mainloop()
