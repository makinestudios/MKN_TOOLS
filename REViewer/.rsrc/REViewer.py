import pickle, copy
from os import path, sep, makedirs
from tkinter import Tk, Frame, Label, Button, PhotoImage, RIGHT, CENTER
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import askyesno
import subprocess,time
from datetime import date

class REViewer():
            
    def getPath():
        return path.dirname(path.realpath(__file__))
    def loadPrefs( p ):
        print(p)
        REViewer.preferences.last_path = p[0]
        REViewer.preferences.colors = p[1]
        print("When loading last_path was :" + REViewer.preferences.last_path)
    def savePrefs( self ):
        prefs = []
        prefs.append( REViewer.preferences.last_path )
        prefs.append( REViewer.preferences.colors )
        print("When saving last_path was :" + prefs[0] )
        pickle.dump( prefs , open( "pref.p" , "wb" ))
        
    class info():
        title = "MAkinE REViewer"
        ver = 0.1
        stage = "beta"
        description="""Select movies to generate REVIEW files."""
        mkn_proj_root="/Volumes/pegasus/01_PROJECTS"
    
    class rsrc():
        logo_filename = "makine.gif"
    class strings():
        dbg_msg_1="Selecting..."
        dbg_msg_2="Compressing..."
        btn_exec='Compress Files'
        btn_select='Select Files'
        msg_1="Select movie files."
        stat_1="NO FILE SELECTED"
        stat_2="QUEUED FILES:"
        stat_3="PROCESSING FILES..."

    class preferences():
        last_path="/Volumes/pegasus/01_PROJECTS/"
        class colors():
            failure=""
            success=""
            normal="#555555"
            active=""
            done="#008800"        
            
    def get_mkn_project_root( path ):
        
        project_root_path = path.split(sep)[4]
        
        return project_root_path

class REViewerGUI:
    
    file_labels=[]
    files=[]
    
    def __init__(self, master):
        
        # window
        
        self.master = master
        master.title( REViewer.info.title + " " + str( REViewer.info.ver ) + " " + REViewer.info.stage )
        
        #labels 
        
        logo = PhotoImage( file= REViewer.getPath() + sep + REViewer.rsrc.logo_filename )
        
        self.logo = Label( master,image=logo)
        self.logo.image = logo

        self.status_label = Label(
            master,
            justify= RIGHT,
            padx =50,
            text=REViewer.strings.stat_1
            )

        self.desc_label = Label(
            master,
            justify=RIGHT,
            padx =50,
            text=REViewer.info.description
            )
        
        self.files_frame = Frame(
            master
        )
        #buttons
        
        self.buttons = [
            Button(master, text=REViewer.strings.btn_exec, width=25,command=self.compress_files,state="disabled"),
            Button(master, text=REViewer.strings.btn_select , width=25,command=self.select_files)
        ]
        
        #pack everything
        
        self.logo.pack(side="top")  
        self.desc_label.pack(side="top")
        self.status_label.pack(side="top")
        self.files_frame.pack(side="top")
        
        for i in self.buttons:
            i.pack(side="bottom")
        
    def announce_status( self, string ):
        self.status_label.config(text= string )
        self.master.update()
    
    def select_files(self):
        print( REViewer.strings.dbg_msg_1 )
        self.files = askopenfilenames(
            initialdir=REViewer.preferences.last_path,
            title= REViewer.strings.msg_1
        )
        
        REViewer.preferences.last_path = path.dirname(path.realpath(self.files[-1]))
        REViewer.savePrefs( self )
        
        self.announce_status( REViewer.strings.stat_2 )
        
        for i , f in enumerate(self.files):
            
            self.file_labels.append (
                    Label(
                    self.files_frame,
                    text=path.basename(str(f)),
                    justify=CENTER,
                    fg=REViewer.preferences.colors.normal
                )
            )
            self.file_labels[i].pack()
            REViewer.preferences.last_path = path.realpath(path.dirname(f))
        
        self.buttons[0].config(state="normal")
        
    
    def compress_files( self ):
        print( REViewer.strings.dbg_msg_2 )
        
        today = date.today()
        today_tag = today.strftime("%m%d%y")

        self.announce_status( REViewer.strings.stat_3 )
        
        root.update()
        
        for b in self.buttons:
            b.config(state="disabled")
            
        
        for i, f in enumerate( self.files ):
            
            new_path = REViewer.info.mkn_proj_root + sep + REViewer.get_mkn_project_root(f)+sep+"10_Review"+sep+today_tag+sep
            
            print(new_path)
            
            if not path.exists(new_path):
                #print(new_path)
                makedirs(new_path)
                #chown(new_path,getpwnam("nobody"),getgrnam("editorial-graphics"))
                #chmod(new_path,0o0775)
            
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
                self.file_labels[i].config( fg=REViewer.preferences.colors.done )
                if replace :
                    self.file_labels[i].config(text=self.file_labels[i].cget("text") + " (Replaced)")
            else:
                self.file_labels[i].config(text=file_labels[i].cget("text") + " (Skipped)")
            
            root.update()
            
        self.announce_status("PROCESSED FILES:")
        
        for b in self.buttons:
            b.config(state="normal")
        

if path.exists("pref.p"):
    saved_prefs = pickle.load( open( "pref.p" , "rb") )
    print(saved_prefs)
    print("FUCK : " + str(saved_prefs[0]) )
    REViewer.loadPrefs( saved_prefs )

root = Tk()
my_gui = REViewerGUI(root)
root.mainloop()
