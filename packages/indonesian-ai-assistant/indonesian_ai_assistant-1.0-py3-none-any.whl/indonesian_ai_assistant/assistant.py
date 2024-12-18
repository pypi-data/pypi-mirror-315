import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import os
import sys

class IndonesianAIAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Mengatur suara ke bahasa Indonesia jika tersedia
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "indonesian" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

        self.chrome_path = self.find_chrome_path()

    def find_chrome_path(self):
        # Path umum untuk Chrome di berbagai sistem operasi
        common_chrome_paths = {
            'win32': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'win64': r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            'darwin': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'linux': '/usr/bin/google-chrome'
        }
        
        if os.name == 'nt':  # Windows
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
                chrome_path = winreg.QueryValue(key, None)
                return chrome_path
            except:
                if 'PROGRAMFILES(X86)' in os.environ:
                    return common_chrome_paths['win64']
                else:
                    return common_chrome_paths['win32']
        elif sys.platform == 'darwin':  # macOS
            return common_chrome_paths['darwin']
        else:  # Linux
            return common_chrome_paths['linux']

    def listen(self):
        with sr.Microphone() as source:
            print("Mendengarkan...")
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language="id-ID")
            print(f"Anda mengatakan: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Maaf, saya tidak mengerti")
            return ""
        except sr.RequestError:
            print("Maaf, layanan speech recognition tidak tersedia")
            return ""

    def speak(self, text):
        print(f"Asisten: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def open_website(self, url, use_chrome=True):
        if use_chrome and self.chrome_path:
            try:
                subprocess.Popen([self.chrome_path, url])
            except Exception as e:
                self.speak(f"Maaf, terjadi kesalahan saat membuka Chrome: {str(e)}")
                webbrowser.open(url)  # Fallback ke browser default
        else:
            webbrowser.open(url)

    def open_application(self, app_name):
        app_paths = {
            "youtube": "https://www.youtube.com",
            "spotify": "https://open.spotify.com",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
            "twitter": "https://twitter.com",
            "shopee": "https://shopee.co.id",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            "zoom": {
                'win32': r"C:\Users\%USERNAME%\AppData\Roaming\Zoom\bin\Zoom.exe",
                'darwin': "/Applications/zoom.us.app",
                'linux': "/usr/bin/zoom"
            },
            "tokopedia": "https://www.tokopedia.com",
            "instagram": "https://www.instagram.com"
        }
        
        app_name = app_name.lower()
        if app_name in app_paths:
            # Khusus untuk Zoom yang memiliki path berbeda tergantung sistem operasi
            if app_name == "zoom":
                zoom_path = app_paths["zoom"]
                if isinstance(zoom_path, dict):
                    if sys.platform in zoom_path:
                        # Expand environment variables in path
                        path = os.path.expandvars(zoom_path[sys.platform])
                        try:
                            subprocess.Popen(path)
                            self.speak(f"Membuka aplikasi Zoom")
                        except FileNotFoundError:
                            self.speak("Maaf, aplikasi Zoom tidak ditemukan. Pastikan Zoom sudah terinstall.")
                    else:
                        self.speak("Maaf, sistem operasi Anda tidak didukung untuk membuka Zoom")
                return

            # Untuk aplikasi web
            if isinstance(app_paths[app_name], str) and app_paths[app_name].startswith("http"):
                self.open_website(app_paths[app_name], use_chrome=True)
                self.speak(f"Membuka {app_name} di Chrome")
            # Untuk aplikasi desktop
            else:
                try:
                    subprocess.Popen(app_paths[app_name])
                    self.speak(f"Membuka aplikasi {app_name}")
                except FileNotFoundError:
                    self.speak(f"Maaf, aplikasi {app_name} tidak ditemukan. Pastikan path-nya benar.")
        else:
            self.speak(f"Maaf, saya tidak tahu cara membuka {app_name}")

    def process_command(self, command):
        if "buka" in command:
            app = command.split("buka", 1)[1].strip()
            self.speak(f"Mencoba membuka {app}")
            self.open_application(app)
        
        elif "selesai" in command or "keluar" in command:
            self.speak("Terima kasih telah menggunakan saya. Sampai jumpa!")
            return False
        
        else:
            self.speak("Maaf, saya tidak mengerti perintah tersebut.")
        
        return True

    def run(self):
        self.speak("Halo, saya asisten virtual Anda. Apa yang bisa saya bantu?")
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)

# Tambahkan fungsi main() ini di bagian bawah file
def main():
    assistant = IndonesianAIAssistant()
    assistant.run()

if __name__ == "__main__":
    main()