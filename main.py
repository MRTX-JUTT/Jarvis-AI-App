import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader  # Pygame کی جگہ یہ استعمال کریں
import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser

# Android Permissions (مائیکروفون اور فائل کے لیے ضروری)
from android.permissions import request_permissions, Permission

# Android specific interaction
try:
    from jnius import autoclass
    ANDROID = True
except:
    ANDROID = False

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
        # مائیکروفون کی اجازت مانگنا
        if ANDROID:
            request_permissions([Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

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
        print(f"Jarvis: {text}")
        try:
            tts = gTTS(text=text, lang='en')
            filename = os.path.join(self.user_data_dir, "voice.mp3")
            tts.save(filename)
            
            # Kivy SoundLoader استعمال ہو رہا ہے
            sound = SoundLoader.load(filename)
            if sound:
                sound.play()
        except Exception as e:
            print(f"Speak Error: {e}")

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
                print(f"Open App Error: {e}")
        return False

    def run_jarvis(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                Clock.schedule_once(lambda dt: setattr(self.label, 'text', "LISTENING..."))
                audio = r.listen(source, timeout=5)

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
        except:
            self.speak("Sorry Sir, I couldn't hear you clearly.")

if __name__ == '__main__':
    # یہاں آپ کی پرانی غلطی تھی، اب یہ ٹھیک ہے:
    JarvisAI().run()
