import tkinter as tk

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_word = listbox.get(selected_index[0])
        label.config(text=f"Selected Word: {selected_word}")

# Create the main application window
root = tk.Tk()
root.title("Word Selection App")

# Create a Listbox
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
words = ["Apple", "Banana", "Cherry", "Grape", "Lemon", "Orange", "Peach", "Strawberry"]
for word in words:
    listbox.insert(tk.END, word)
listbox.pack(padx=20, pady=10)

# Create a Label
label = tk.Label(root, text="Selected Word: ")
label.pack(padx=20, pady=(0, 10))

# Bind the selection event to the Listbox
listbox.bind('<<ListboxSelect>>', on_select)

# Start the Tkinter event loop
root.mainloop()
