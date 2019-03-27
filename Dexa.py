"""

README

pip install wikipedia (wikipedia)

ip install wolframalpha (wolframalpha)

pip install -U wxPython (GUI)

pip install SpeechRecognition (speech recognition)

python -m pip install pyaudio (python audio)

https://www.youtube.com/watch?v=lOIJIk_maO4 (for executable)

"""
import webbrowser
import wx
import wikipedia
import wolframalpha
import win32com.client as wincl
import winsound

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(500,150),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
             wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="Dexa")
        location = wx.Point(500,500)
        self.Move(location)
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label="Hello I am Dexa the Python Digital Assistant. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        
        pic = wx.Image("mic.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=pic)
         #                 ,size=(pic.GetWidth(), pic.GetHeight()))
        #self.button = wx.BitmapButton(panel,-1,pos=(420,30), size=(pic.GetWidth(), pic.GetHeight()))
        self.button.SetPosition((420,30))
        #button1 - wx.Button(panel, label= "Hess", pos=(130,10),size=(60,60))
        self.txt.SetHint("How can I help you?")
        self.button.Bind(wx.EVT_BUTTON, self.onClick)
        
        #adding speech to text to the text box
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()


    def onClick(self, event):
        import speech_recognition as sr
        record = sr.Recognizer()
        speak = wincl.Dispatch("SAPI.SpVoice")
        with sr.Microphone() as source:   
            record.adjust_for_ambient_noise(source, duration=2)
            

            winsound.PlaySound('siri_opening.wav', winsound.SND_FILENAME)
            print("===================================================")
            print("What do you want to search?") 
            audio = record.listen(source)
            winsound.PlaySound('siri_closing.wav', winsound.SND_FILENAME)
            message = record.recognize_google(audio)
            print("===================================================")
        if(message.lower() == "who are you?" or message.lower() == "who are you"):
            speak.Speak("I am Dexa, your personal assistant.")
            print("I am Dexa,  your personal assistant.")
        #elif(message.lower()=="hello" or message.lower()=="hi"):
            #speak.Speak("Hello Human.")
            #print("Hello Human.")
        else:
            print(message)
            
            try:
                
                
                self.txt.SetValue(message)
                try:
                    #wolframalpha
                    app_id = "E7EE8H-PXYYTG5H3V"
                    client = wolframalpha.Client(app_id)
                    res = client.query(message)
                    answer = next(res.results).text
                    print(answer)
                    speak.Speak(answer)
                except:
                    try:
                        #wikipedia
                        print (wikipedia.summary(message))
                    except:
                        #try:
                        #yelp
                        url4 = 'https://www.google.com/search?q='
                        webbrowser.open_new(url4+message)
                            
                       # except:
                           # url4 = 'https://www.yelp.com/search?cflt=restaurants&find_loc='
                            #webbrowser.open_new(url4+message)
                            
            except sr.UnknownValueError:
                print("Could not understand. Please try again.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
            
        #This works multiple button clicks 
        self.button.Bind(wx.EVT_BUTTON, self.onClick)
    def onExit(self, event):
            self.Close()
    def OnEnter(self, event):
        speak = wincl.Dispatch("SAPI.SpVoice")
        input = self.txt.GetValue()
        input = input.lower()
        if(input.lower() == "who are you?" or input.lower() == "who are you"):
           speak.Speak("I am Dexa, your personal assistant!")
        #elif(input.lower()=="hello" or input.lower()=="hi"):
            #speak.Speak("Hello Human.")
       
        else:
            print(input)
            try:
                #wolframalpha
                app_id = "E7EE8H-PXYYTG5H3V"
                client = wolframalpha.Client(app_id)
                res = client.query(input)
                answer = next(res.results).text
                print (answer)
                speak.Speak(answer)
            except:
                try:
                    #wikipedia
                    print (wikipedia.summary(input))
                    speak.Speak(wikipedia.summary(input))
                except:
                    #try:
                    #yelp
                    url4 = 'https://www.google.com/search?q='
                    webbrowser.open_new(url4+input)
                        
                   # except:
                       # url4 = 'https://www.yelp.com/search?cflt=restaurants&find_loc='
                        #webbrowser.open_new(url4+message)

        print("===================================================")
        self.button.Bind(wx.EVT_BUTTON, self.onClick)

        


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
