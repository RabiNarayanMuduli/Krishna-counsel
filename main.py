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
#hiiii
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class KrishnaCounselApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Conversation Memory
        self.chat_history = []

        self.title("🪷 Krishna Counsel - Vrinda")
        self.geometry("650x800")

        # ---------------- Avatar ----------------
        self.avatar_label = ctk.CTkLabel(self, text="")
        self.avatar_label.pack(pady=10)

        self.avatar = AvatarController(self.avatar_label)

        self.idle_gif = "avatars/idle.gif"
        self.thinking_gif = "avatars/thinking.gif"
        self.speaking_gif = "avatars/speaking.gif"

        self.avatar.change_avatar(self.idle_gif)

        # ---------------- Chat ----------------
        self.chat_area = ctk.CTkTextbox(self, width=600, height=400)
        self.chat_area.pack(pady=10)
        self.chat_area.configure(state="disabled")

        # ---------------- Input ----------------
        self.input_frame = ctk.CTkFrame(self)
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

        # ---------------- Voice Recognition ----------------
        self.recording = False
        self.recognizer = sr.Recognizer()
        self.audio_data = None

        # ---------------- Neural TTS ----------------
        pygame.mixer.init()
        self.is_speaking = False

    # =====================================================
    # ================== CHAT =============================
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

        self.avatar.change_avatar(self.speaking_gif)
        self.speak(response)

    def add_message(self, sender, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    # =====================================================
    # ================== VOICE INPUT ======================
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

            self.avatar.change_avatar(self.thinking_gif)

            response = ask_Vrinda(text)

            self.add_message("Vrinda", response)

            self.avatar.change_avatar(self.speaking_gif)
            self.speak(response)

        except:
            self.add_message("System", "Voice recognition failed.")
            self.avatar.change_avatar(self.idle_gif)

    # =====================================================
    # ================== TTS ==============================
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

            # Back to idle
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
        self.avatar.change_avatar(self.idle_gif)


if __name__ == "__main__":
    app = KrishnaCounselApp()
    app.mainloop()
