import tkinter as tk

def adjust_pane_sizes(event):
    # Get the new width of the window
    window_width = event.width

    # Calculate the width of the right pane (1/3 of window width)
    right_pane_width = window_width // 3

    # Set the right pane's width
    paned_window.paneconfig(pane2, width=right_pane_width)

# Create the main application window
root = tk.Tk()
root.title("Resize Test")

# Create a PanedWindow
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)

# Create two panes
pane1 = tk.Frame(paned_window, bg="lightblue")
pane2 = tk.Frame(paned_window, bg="lightgreen")

# Add the panes to the PanedWindow
paned_window.add(pane1)
paned_window.add(pane2)

# Bind the <Configure> event to adjust_pane_sizes
paned_window.bind("<Configure>", adjust_pane_sizes)

# Pack the PanedWindow to the main window
paned_window.pack(fill=tk.BOTH, expand=True)

# Create a label inside each pane
label1 = tk.Label(pane1, text="Flexible Pane")
label2 = tk.Label(pane2, text="Right Pane")

label1.pack(padx=20, pady=20)
label2.pack(padx=20, pady=20)

# Start the Tkinter main loop
root.mainloop()
