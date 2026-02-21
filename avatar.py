import customtkinter as ctk
from PIL import Image


class AvatarController:
    def __init__(self, label_widget, size=(250, 250)):
        self.label = label_widget
        self.size = size
        self.frames = []
        self.current_path = None
        self.frame_index = 0
        self.animation_id = None

    def change_avatar(self, gif_path):
        if self.current_path == gif_path:
            return

        self.current_path = gif_path

        # Stop previous animation safely
        if self.animation_id:
            self.label.after_cancel(self.animation_id)

        self.frames.clear()

        gif = Image.open(gif_path)

        try:
            while True:
                frame = gif.copy().resize(self.size)

                ctk_image = ctk.CTkImage(
                    light_image=frame,
                    dark_image=frame,
                    size=self.size
                )

                self.frames.append(ctk_image)
                gif.seek(len(self.frames))
        except EOFError:
            pass

        self.frame_index = 0
        self.animate()

    def animate(self):
        if not self.frames:
            return

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.label.configure(image=self.frames[self.frame_index])

        self.frame_index += 1

        self.animation_id = self.label.after(100, self.animate)
