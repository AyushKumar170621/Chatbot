from tkinter import *
from chat import getresponse,bot_name,SpeakText
import speech_recognition as sr
import pyttsx3
import time
import threading
from PIL import Image,ImageTk
from data import databaseRecord

BG_GRAY = "#ABB2B9"
BG_COLOR =  "#645CAA"   #"#17202A"
NEW_BG="#00FFD1"
TEXT_COLOR = "#EEEEEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
last=False


class ChatApplication:
    def __init__(self):
        self.window=Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title('Chat')
        self.window.resizable(width=False,height=False)
        self.window.configure(width=800,height=700,bg=NEW_BG)

        #head label
        head_label = Label(self.window,bg=BG_COLOR,fg=TEXT_COLOR,text="Welcome to Chatbot",font='FONT_BOLD',pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line = Label(self.window,width=450,bg=BG_COLOR)
        line.place(relwidth=1,rely=0.07,relheight=0.012)


        #text widget
        self.text_widget = Text(self.window,width=20,height=2,bg=BG_COLOR,fg=TEXT_COLOR,font=FONT,padx=5,pady=5,wrap=WORD)
        self.text_widget.place(relwidth=1,relheight=0.745,rely=0.08)
        self.text_widget.configure(cursor="arrow",state=DISABLED)

        #scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1,relx=1)
        scrollbar.configure(command=self.text_widget.yview)

        #bottom label
        bottom_label = Label(self.window,bg=BG_COLOR,height=80)
        bottom_label.place(relwidth=1,rely=0.825)

        #msg entry

        self.msg_entry = Entry(bottom_label,bg="#182747",fg=TEXT_COLOR)
        self.msg_entry.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.012)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        #send button 
        send_button =Button(bottom_label,text="send",width=10,bg=BG_GRAY,font=FONT_BOLD,command=lambda : self._on_enter_pressed(None))
        send_button.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.11)
        rec_button =Button(bottom_label,text="Rec",width=10,bg=BG_GRAY,font=FONT_BOLD,command=lambda : self.getSpeechResponse(None))
        rec_button.place(relx=0.88,rely=0.008,relheight=0.06,relwidth=0.11)

    def _on_enter_pressed(self,event):
        msg=self.msg_entry.get()
        if last==True:
            data=msg.split()
            databaseRecord(data[0], data[1])
            self.window.quit()
        else:
            self._insert_msg(msg, "You")

    def _insert_msg(self,msg,sender):
        if not msg:
            return
        self.msg_entry.delete(0,END)
        msg1 = f"{sender} : {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        if msg=="thanks" or msg=="bye":
            global last
            last=True
            retmsg=getresponse(msg)+"\nAre You Satisfied! Please Give Your name and answer"
        else:
            retmsg=getresponse(msg)
        msg2 = f"{bot_name} : {retmsg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        t=threading.Thread(target=SpeakText,args=(retmsg,))
        t.start()

    def getSpeechResponse(self,event):
        r = sr.Recognizer()
        
    
         # Exception handling to handle
         # exceptions at the runtime
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                #listens for the user's input
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                self._insert_msg(MyText, "You")
                #SpeakText(MyText)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")


if __name__== "__main__":
    app=ChatApplication()
    app.run()