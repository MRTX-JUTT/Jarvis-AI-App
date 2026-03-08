import threading
import os
import webbrowser
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Android specific imports
try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

import speech_recognition as sr

apps_dictionary = {
    "whatsapp": "com.whatsapp",
    "easypaisa": "inc.fss.mwallet",
    "jazzcash": "com.techlogix.mobilinkcustomer",
    "facebook": "com.facebook.katana",
    "instagram": "com.instagram.android",
    "binance": "com.binance.dev",
    "pubg": "com.tencent.ig",
    "youtube": "com.google.android.youtube",
    "snapchat": "com.snapchat.android",
    "linkedin": "com.linkedin.android",
    "capcut": "com.lemon.lvoverseas",
    "canva": "com.canva.editor",
    "calculator": "com.google.android.calculator",
    "camera": "com.android.camera",
    "settings": "com.android.settings",
    "play store": "com.android.vending",
    "chrome": "com.android.chrome",
    "gmail": "com.google.android.gm",
    "tiktok": "com.zhiliaoapp.musically",
    "telegram": "org.telegram.messenger",
    "sadapay": "com.sadapay.app",
    "meezan bank": "com.vsoftcorp.mbl",
    "discord": "com.discord",
    "hbl": "com.hbl.hblmobile",
    "terabox": "com.dubox.drive",
    "tcl home": "com.tcl.clhome"
}

class JarvisAI(App):
    def build(self):
        if ANDROID:
            request_permissions([
                Permission.RECORD_AUDIO, 
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE,
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE
            ])
            # Setup Native TTS for Male Voice
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            self.tts = TextToSpeech(autoclass('org.kivy.android.PythonActivity').mActivity, None)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=25)
        self.label = Label(
            text="[b]JARVIS[/b]\n[color=00ffff]READY FOR COMMANDS[/color]", 
            font_size='26sp', markup=True, halign='center'
        )
        self.btn = Button(
            text="ACTIVATE", size_hint=(1, 0.4),
            background_color=(0, 0.7, 0.9, 1), font_size='22sp'
        )
        self.btn.bind(on_press=self.start_thread)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        return self.layout

    def speak(self, text):
        if ANDROID:
            self.tts.speak(text, autoclass('android.speech.tts.TextToSpeech').QUEUE_FLUSH, None, None)
        else:
            print(f"JARVIS: {text}")

    def start_thread(self, instance):
        threading.Thread(target=self.run_jarvis).start()

    def open_app(self, package_name):
        if ANDROID:
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                currentActivity = PythonActivity.mActivity
                pm = currentActivity.getPackageManager()
                intent = pm.getLaunchIntentForPackage(package_name)
                if intent:
                    currentActivity.startActivity(intent)
                    return True
            except Exception as e:
                print(f"Error: {e}")
        return False

    def run_jarvis(self):
        r = sr.Recognizer()
        # Mic parameters adjust for Android
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True

        try:
            # FIX: Adding a small sleep before opening microphone
            Clock.schedule_once(lambda dt: setattr(self.label, 'text', "INITIALIZING MIC..."))
            time.sleep(1) 

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                Clock.schedule_once(lambda dt: setattr(self.label, 'text', "LISTENING..."))
                audio = r.listen(source, timeout=8, phrase_time_limit=6)

            query = r.recognize_google(audio).lower()
            Clock.schedule_once(lambda dt: setattr(self.label, 'text', f"You said:\n{query}"))

            app_found = False
            for app_name, package in apps_dictionary.items():
                if app_name in query:
                    self.speak(f"Opening {app_name}, Sir")
                    self.open_app(package)
                    app_found = True
                    break
            
            if not app_found:
                self.speak("Searching for your request")
                webbrowser.open(f"https://www.google.com/search?q={query}")

        except Exception as e:
            # Display exact error for debugging
            Clock.schedule_once(lambda dt: setattr(self.label, 'text', f"Error: {str(e)[:20]}"))
            self.speak("Mic access denied or timed out.")

if __name__ == '__main__':
    JarvisAI().run()
