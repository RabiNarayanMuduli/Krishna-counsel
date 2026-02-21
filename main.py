# import customtkinter as ctk
# from brain import ask_Vrinda
# from avatar import AvatarController
# import threading
# import speech_recognition as sr
# import asyncio
# import edge_tts
# import pygame
# import uuid
# import os
# from auth import register_user, login_user, save_history
#
# current_user = None
# app_state = "menu"  # menu, login, register, main
#
#
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("dark-blue")
#
#
# class KrishnaCounselApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#
#         # Conversation Memory
#         self.chat_history = []
#
#         self.title("🪷 Krishna Counsel - Vrinda")
#         self.geometry("650x800")
#
#         # ---------------- Container ----------------
#         self.container = ctk.CTkFrame(self)
#         self.container.pack(fill="both", expand=True)
#
#         # ---------------- Avatar ----------------
#         self.avatar_label = ctk.CTkLabel(self, text="")
#         self.avatar_label.pack(pady=10)
#
#         self.avatar = AvatarController(self.avatar_label)
#
#         self.idle_gif = "avatars/idle.gif"
#         self.thinking_gif = "avatars/thinking.gif"
#         self.speaking_gif = "avatars/speaking.gif"
#
#         self.avatar.change_avatar(self.idle_gif)
#
#         # ---------------- Chat ----------------
#         self.chat_area = ctk.CTkTextbox(self, width=600, height=400)
#         self.chat_area.pack(pady=10)
#         self.chat_area.configure(state="disabled")
#
#         # ---------------- Input ----------------
#         self.input_frame = ctk.CTkFrame(self)
#         self.input_frame.pack(pady=10)
#
#         self.user_input = ctk.CTkEntry(self.input_frame, width=350)
#         self.user_input.pack(side="left", padx=5)
#
#         self.send_button = ctk.CTkButton(
#             self.input_frame, text="Send", command=self.handle_send
#         )
#         self.send_button.pack(side="left", padx=5)
#
#         self.voice_button = ctk.CTkButton(
#             self.input_frame, text="🎙 Speak", command=self.toggle_recording
#         )
#         self.voice_button.pack(side="left", padx=5)
#
#         # ---------------- Voice Recognition ----------------
#         self.recording = False
#         self.recognizer = sr.Recognizer()
#         self.audio_data = None
#
#         # ---------------- Neural TTS ----------------
#         pygame.mixer.init()
#         self.is_speaking = False
#
#     # =====================================================
#     # ================== CHAT =============================
#     # =====================================================
#
#     def handle_send(self):
#         self.stop_speaking()
#
#         query = self.user_input.get().strip()
#         if not query:
#             return
#
#         self.add_message("You", query)
#         self.chat_history.append({"role": "user", "content": query})
#
#         self.user_input.delete(0, "end")
#
#         threading.Thread(
#             target=self.get_response,
#             args=(query,),
#             daemon=True
#         ).start()
#
#     def get_response(self, query):
#         self.avatar.change_avatar(self.thinking_gif)
#
#         response = ask_Vrinda(query, self.chat_history)
#
#         self.chat_history.append({"role": "assistant", "content": response})
#
#         self.add_message("Vrinda", response)
#
#         self.avatar.change_avatar(self.speaking_gif)
#         self.speak(response)
#
#     def add_message(self, sender, message):
#         self.chat_area.configure(state="normal")
#         self.chat_area.insert("end", f"{sender}: {message}\n\n")
#         self.chat_area.configure(state="disabled")
#         self.chat_area.see("end")
#
#     # =====================================================
#     # ================== VOICE INPUT ======================
#     # =====================================================
#
#     def toggle_recording(self):
#         if not self.recording:
#             self.start_recording()
#         else:
#             self.stop_recording()
#
#     def start_recording(self):
#         self.stop_speaking()
#
#         self.recording = True
#         self.voice_button.configure(text="⏹ Stop")
#
#         self.add_message("System", "🎙 Listening...")
#
#         threading.Thread(target=self.record_audio, daemon=True).start()
#
#     def record_audio(self):
#         try:
#             with sr.Microphone() as source:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
#                 self.audio_data = self.recognizer.listen(source)
#         except:
#             self.recording = False
#             self.voice_button.configure(text="🎙 Speak")
#
#     def stop_recording(self):
#         self.recording = False
#         self.voice_button.configure(text="🎙 Speak")
#
#         self.add_message("System", "⏳ Processing voice...")
#
#         threading.Thread(target=self.process_audio, daemon=True).start()
#
#     def show_login_screen(self):
#         for widget in self.container.winfo_children():
#             widget.destroy()
#
#         title = ctk.CTkLabel(self.container, text="Login", font=("Arial", 24))
#         title.pack(pady=20)
#
#         self.login_username = ctk.CTkEntry(self.container, placeholder_text="Username")
#         self.login_username.pack(pady=10)
#
#         self.login_password = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
#         self.login_password.pack(pady=10)
#
#         login_btn = ctk.CTkButton(self.container, text="Login", command=self.handle_login)
#         login_btn.pack(pady=10)
#
#         register_btn = ctk.CTkButton(self.container, text="Register", command=self.show_register_screen)
#         register_btn.pack(pady=5)
#
#         guest_btn = ctk.CTkButton(self.container, text="Continue as Guest", command=self.continue_guest)
#         guest_btn.pack(pady=5)
#
#     def handle_login(self):
#         global current_user
#
#         username = self.login_username.get()
#         password = self.login_password.get()
#
#         success, message = login_user(username, password)
#
#         if success:
#             current_user = username
#             self.show_chat_screen()
#         else:
#             print(message)
#
#     def continue_guest(self):
#         global current_user
#         current_user = "guest"
#         self.show_chat_screen()
#
#     def show_register_screen(self):
#         for widget in self.container.winfo_children():
#             widget.destroy()
#
#         title = ctk.CTkLabel(self.container, text="Register", font=("Arial", 24))
#         title.pack(pady=20)
#
#         self.reg_username = ctk.CTkEntry(self.container, placeholder_text="Username")
#         self.reg_username.pack(pady=10)
#
#         self.reg_password = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
#         self.reg_password.pack(pady=10)
#
#         register_btn = ctk.CTkButton(self.container, text="Register", command=self.handle_register)
#         register_btn.pack(pady=10)
#
#         back_btn = ctk.CTkButton(self.container, text="Back to Login", command=self.show_login_screen)
#         back_btn.pack(pady=5)
#
#     def show_register_screen(self):
#         for widget in self.container.winfo_children():
#             widget.destroy()
#
#         title = ctk.CTkLabel(self.container, text="Register", font=("Arial", 24))
#         title.pack(pady=20)
#
#         self.reg_username = ctk.CTkEntry(self.container, placeholder_text="Username")
#         self.reg_username.pack(pady=10)
#
#         self.reg_password = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
#         self.reg_password.pack(pady=10)
#
#         register_btn = ctk.CTkButton(self.container, text="Register", command=self.handle_register)
#         register_btn.pack(pady=10)
#
#         back_btn = ctk.CTkButton(self.container, text="Back to Login", command=self.show_login_screen)
#         back_btn.pack(pady=5)
#
#     def handle_register(self):
#         username = self.reg_username.get()
#         password = self.reg_password.get()
#
#         success, message = register_user(username, password)
#         print(message)
#
#         if success:
#             self.show_login_screen()
#
#     def process_audio(self):
#         try:
#             text = self.recognizer.recognize_google(self.audio_data)
#
#             self.add_message("You (Voice)", text)
#
#             self.avatar.change_avatar(self.thinking_gif)
#
#             response = ask_Vrinda(text)
#
#             self.add_message("Vrinda", response)
#
#             self.avatar.change_avatar(self.speaking_gif)
#             self.speak(response)
#
#         except:
#             self.add_message("System", "Voice recognition failed.")
#             self.avatar.change_avatar(self.idle_gif)
#
#     # =====================================================
#     # ================== TTS ==============================
#     # =====================================================
#
#     def speak(self, text):
#         self.stop_speaking()
#
#         threading.Thread(
#             target=self._generate_and_play,
#             args=(text,),
#             daemon=True
#         ).start()
#
#     def _generate_and_play(self, text):
#         try:
#             filename = f"Vrinda_{uuid.uuid4().hex}.mp3"
#
#             asyncio.run(self._tts_async(text, filename))
#
#             self.is_speaking = True
#
#             pygame.mixer.music.load(filename)
#             pygame.mixer.music.play()
#
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#
#             self.is_speaking = False
#             os.remove(filename)
#
#             # Back to idle
#             self.avatar.change_avatar(self.idle_gif)
#
#         except:
#             self.is_speaking = False
#             self.avatar.change_avatar(self.idle_gif)
#
#     async def _tts_async(self, text, filename):
#         communicate = edge_tts.Communicate(
#             text,
#             voice="en-IN-NeerjaNeural"
#         )
#         await communicate.save(filename)
#
#     def stop_speaking(self):
#         try:
#             pygame.mixer.music.stop()
#         except:
#             pass
#
#         self.is_speaking = False
#         self.avatar.change_avatar(self.idle_gif)
#
#
# if __name__ == "__main__":
#     app = KrishnaCounselApp()
#     app.mainloop()
import customtkinter as ctk
from brain import ask_Vrinda
from avatar import AvatarController
import threading
import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import uuid
import os
from auth import register_user, login_user, save_history

current_user = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class KrishnaCounselApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🪷 Krishna Counsel - Vrinda")
        self.geometry("650x800")

        self.chat_history = []

        # Container (screen switcher)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Voice
        self.recording = False
        self.recognizer = sr.Recognizer()
        self.audio_data = None

        # TTS
        pygame.mixer.init()
        self.is_speaking = False

        # Start with login
        self.show_login_screen()

    # =====================================================
    # ================= LOGIN SCREEN ======================
    # =====================================================

    def show_login_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.container, text="Login", font=("Arial", 24))
        title.pack(pady=20)

        self.login_username = ctk.CTkEntry(self.container, placeholder_text="Username")
        self.login_username.pack(pady=10)

        self.login_password = ctk.CTkEntry(
            self.container, placeholder_text="Password", show="*"
        )
        self.login_password.pack(pady=10)

        login_btn = ctk.CTkButton(
            self.container, text="Login", command=self.handle_login
        )
        login_btn.pack(pady=10)

        register_btn = ctk.CTkButton(
            self.container, text="Register", command=self.show_register_screen
        )
        register_btn.pack(pady=5)

        guest_btn = ctk.CTkButton(
            self.container, text="Continue as Guest", command=self.continue_guest
        )
        guest_btn.pack(pady=5)

    def handle_login(self):
        global current_user

        username = self.login_username.get()
        password = self.login_password.get()

        success, message = login_user(username, password)

        if success:
            current_user = username
            self.show_chat_screen()
        else:
            print(message)

    def continue_guest(self):
        global current_user
        current_user = "guest"
        self.show_chat_screen()

    # =====================================================
    # ================= REGISTER SCREEN ===================
    # =====================================================

    def show_register_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.container, text="Register", font=("Arial", 24))
        title.pack(pady=20)

        self.reg_username = ctk.CTkEntry(self.container, placeholder_text="Username")
        self.reg_username.pack(pady=10)

        self.reg_password = ctk.CTkEntry(
            self.container, placeholder_text="Password", show="*"
        )
        self.reg_password.pack(pady=10)

        register_btn = ctk.CTkButton(
            self.container, text="Register", command=self.handle_register
        )
        register_btn.pack(pady=10)

        back_btn = ctk.CTkButton(
            self.container, text="Back to Login", command=self.show_login_screen
        )
        back_btn.pack(pady=5)

    def handle_register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        success, message = register_user(username, password)
        print(message)

        if success:
            self.show_login_screen()

    # =====================================================
    # ================= CHAT SCREEN =======================
    # =====================================================

    def show_chat_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Avatar
        self.avatar_label = ctk.CTkLabel(self.container, text="")
        self.avatar_label.pack(pady=10)

        self.avatar = AvatarController(self.avatar_label)

        self.idle_gif = "avatars/idle.gif"
        self.thinking_gif = "avatars/thinking.gif"
        self.speaking_gif = "avatars/speaking.gif"

        self.avatar.change_avatar(self.idle_gif)

        # Chat
        self.chat_area = ctk.CTkTextbox(self.container, width=600, height=400)
        self.chat_area.pack(pady=10)
        self.chat_area.configure(state="disabled")

        # Input
        self.input_frame = ctk.CTkFrame(self.container)
        self.input_frame.pack(pady=10)

        self.user_input = ctk.CTkEntry(self.input_frame, width=350)
        self.user_input.pack(side="left", padx=5)

        self.send_button = ctk.CTkButton(
            self.input_frame, text="Send", command=self.handle_send
        )
        self.send_button.pack(side="left", padx=5)

        self.voice_button = ctk.CTkButton(
            self.input_frame, text="🎙 Speak", command=self.toggle_recording
        )
        self.voice_button.pack(side="left", padx=5)

        # Logout Button
        logout_btn = ctk.CTkButton(
            self.container, text="Logout", command=self.logout
        )
        logout_btn.pack(pady=5)

    def logout(self):
        global current_user
        current_user = None
        self.chat_history = []
        self.show_login_screen()

    # =====================================================
    # ================= CHAT LOGIC ========================
    # =====================================================

    def handle_send(self):
        self.stop_speaking()

        query = self.user_input.get().strip()
        if not query:
            return

        self.add_message("You", query)
        self.chat_history.append({"role": "user", "content": query})
        self.user_input.delete(0, "end")

        threading.Thread(
            target=self.get_response,
            args=(query,),
            daemon=True
        ).start()

    def get_response(self, query):
        self.avatar.change_avatar(self.thinking_gif)

        response = ask_Vrinda(query, self.chat_history)

        self.chat_history.append({"role": "assistant", "content": response})
        self.add_message("Vrinda", response)

        # Save to Mongo (only if not guest)
        if current_user != "guest":
            save_history(current_user, query, response)

        self.avatar.change_avatar(self.speaking_gif)
        self.speak(response)

    def add_message(self, sender, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    # =====================================================
    # ================= VOICE =============================
    # =====================================================

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.stop_speaking()
        self.recording = True
        self.voice_button.configure(text="⏹ Stop")
        self.add_message("System", "🎙 Listening...")
        threading.Thread(target=self.record_audio, daemon=True).start()

    def record_audio(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.audio_data = self.recognizer.listen(source)
        except:
            self.recording = False
            self.voice_button.configure(text="🎙 Speak")

    def stop_recording(self):
        self.recording = False
        self.voice_button.configure(text="🎙 Speak")
        self.add_message("System", "⏳ Processing voice...")
        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        try:
            text = self.recognizer.recognize_google(self.audio_data)
            self.add_message("You (Voice)", text)
            self.get_response(text)
        except:
            self.add_message("System", "Voice recognition failed.")
            self.avatar.change_avatar(self.idle_gif)

    # =====================================================
    # ================= TTS ===============================
    # =====================================================

    def speak(self, text):
        self.stop_speaking()
        threading.Thread(
            target=self._generate_and_play,
            args=(text,),
            daemon=True
        ).start()

    def _generate_and_play(self, text):
        try:
            filename = f"Vrinda_{uuid.uuid4().hex}.mp3"
            asyncio.run(self._tts_async(text, filename))

            self.is_speaking = True
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            self.is_speaking = False
            os.remove(filename)
            self.avatar.change_avatar(self.idle_gif)

        except:
            self.is_speaking = False
            self.avatar.change_avatar(self.idle_gif)

    async def _tts_async(self, text, filename):
        communicate = edge_tts.Communicate(
            text,
            voice="en-IN-NeerjaNeural"
        )
        await communicate.save(filename)

    def stop_speaking(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

        self.is_speaking = False


if __name__ == "__main__":
    app = KrishnaCounselApp()
    app.mainloop()