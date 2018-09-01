import wx
import wx.adv
#new
import os
import re
import win32api
#upto this

import wikipedia
import wolframalpha
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import webbrowser as wb

# variable 's' contains only the path at very beginning it contains empty string.
s = ''
def find_file(root_folder, rex):
    global s
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            result = rex.search(f)
            if result:
                s = ''
                s+=str(os.path.join(root, f))
                break
                           
def ab(file_name):
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        find_file( drive, rex )

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(450, 700),                # This is for the frame
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
             wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="Chicken-The Warrier")
        #panel = wx.Panel(self)
        panel = wx.Panel(self, 0)
        #imagen = wx.StaticBitmap(panel, -1, wx.Bitmap('Aussie-Cortana.jpg', wx.BITMAP_TYPE_ANY),
        #                         pos = wx.Point(0, 0), size = (550, 700))
        imagen_gif = wx.adv.AnimationCtrl(panel, wx.ID_ANY, wx.adv.NullAnimation, (20, 0), (-1, -1), wx.adv.AC_DEFAULT_STYLE)
        imagen_gif.LoadFile('cortana-gif-8.gif')
        imagen_gif.Play()
        self.Centre()
        my_sizer = wx.BoxSizer(wx.VERTICAL)
       # my_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
       
        
        lbl = wx.StaticText(panel)
        my_sizer.Add(lbl, -1, wx.ALL, 300)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,45))   #This is for the search box
        self.txt.SetFocus()        
        
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 68)
        self.SetBackgroundColour("black")
        panel.SetSizer(my_sizer)
        self.Show()
    def OnEnter(self, event):
        input = self.txt.GetValue()
        ActInp = input
        input = input.lower()
        ab(ActInp)
        if s == '' :
            try:
                #wikipedia
                #Gonna Fix the bug i.e if I am searching amitabh bacchan it is working with the real data about amitabh bachhan,But If I am asking "Who Is Amitabh Bachhan?"
                #It fails to answer and come up with some different and unexpected output as well.So Lets fix this bug.
                '''r = sr.Recognizer()
                with sr.Microphone() as source:
                    print('Say Something:')
                    audio = r.listen(source)
                    print ('Done!')

                text = r.recognize_google(audio, language = 'hi-IN')
                print (text)
                print (r.recognize_google(audio))'''
                input = input.split(' ')
                input = " ".join(input[2:])      #Here I am cosidering the 2nd word only as input.And ignoring the word like,"What is"/"How is"/"Who is" that kind of.
                tts = gTTS(text="According to wikipedia " + wikipedia.summary(input,sentences=3), lang='en',slow=False)
                tts.save("New.mp3")
                playsound("F:\\MyPA\\New.mp3")
                
            except:
                try:
                    #Chrome operation
                    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                    f_text = 'https://www.google.co.in/search?q='+input
                    wb.get(chrome_path).open(f_text)
                except:
                    #wolframalpha
                    app_id = "GRXYYG-7U9HLUEWY9"
                    client = wolframalpha.Client(app_id)
                    res = client.query(input)
                    tts = gTTS(text="According to Your Question " + next(res.results).text, lang='en',slow=False)
                    tts.save("New1.mp3")
                    playsound("F:\\MyPA\\New1.mp3")
        else:
            os.startfile(s)
if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
