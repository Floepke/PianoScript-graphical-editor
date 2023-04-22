import tkinter as tk
from tkinter import font

class GridEditor(tk.Toplevel):
    def __init__(self):
        super().__init__()

        # Set background color and disable resize
        self.configure(background="#002B36")
        self.resizable(True, True)

        # Remove title bar
        #self.overrideredirect(True)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set dialog size and position
        dialog_width = screen_width // 2
        dialog_height = screen_height // 2
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2
        self.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")

        # Create main frame for the dialog
        main_frame = tk.Frame(self, bg="#002B36")
        main_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=20)

        font_style = font.Font(family="Courier", size=24)

        # Create buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#002B36")
        buttons_frame.pack(side='left')

        # Create apply button
        button_width = (dialog_width - 60) // 2  # Subtract button spacing and padding
        apply_button = tk.Button(buttons_frame, text="Apply", width=button_width, font=font_style, command=self.apply)
        apply_button.pack(side='bottom', padx=10, pady=10)

        # Create cancel button
        cancel_button = tk.Button(buttons_frame, text="Cancel", width=button_width, font=font_style, command=self.cancel)
        cancel_button.pack(side='bottom', padx=10, pady=10)

        # Create text widget with border
        text_frame = tk.Frame(main_frame)
        text_frame.pack()
        self.text_widget = tk.Text(main_frame, bg="#eee8d5", font=font_style, width=20)
        self.text_widget.pack(expand=True, fill='both')

        # Initialize result variable
        self.result = None

    def apply(self):
        # Set result to text in text widget
        self.result = self.text_widget.get("1.0", tk.END).strip()
        self.destroy()

    def cancel(self):
        # Set result to None and destroy dialog
        self.result = None
        self.destroy()










# TEST
if __name__ == '__main__':
    root = tk.Tk()
    dialog = GridEditor()
    root.wait_window(dialog)
    print(f"Grid map editor string: {dialog.result}")
    root.mainloop()