import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk
import os, time, subprocess


class RingBox:
    def __init__(self, master, ring, data):
        self.master = master
        self.ring = ring
        self.data = data
        self.current_record_index = 0
        self.is_ring_complete = False
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Load the ring image
        self.image = Image.open("ring.png")
        self.image = self.image.resize((500, 500))  # Adjust the image size as needed
        
        self.label = tk.Label(self.frame, text="Ring: " + str(self.ring), font=("Verdana", 45, "bold"))
        self.label.pack(pady=(0, 10))
        
        self.canvas = tk.Canvas(self.frame, width=500, height=500)
        self.canvas.pack()
        
        # Set the image as the background
        self.bg_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        
        self.text_widget = tk.Text(self.frame, width=30, height=10, font=("Arial", 14))
        #self.text_widget.pack()
        
        self.next_frame = tk.Frame(self.frame)
        self.next_frame.pack(pady=10)
        
        self.next_label = tk.Label(self.next_frame, text="Next Division:", font=("Verdana bold", 15))
        self.next_label.pack(side=tk.LEFT)
        
        self.next_text = tk.Text(self.next_frame, width=30, height=4, font=("Arial", 12))
        self.next_text.pack(side=tk.LEFT)
        
        self.button = tk.Button(self.frame, text="Next", command=self.next_record, font=("Arial", 12, "bold"))
        self.button.pack(pady=0)

        self.back_frame = tk.Frame(self.frame)
        self.back_frame.pack(pady=0)

        self.back_button = tk.Button(self.back_frame, text="Back", command=self.previous_record, font=("Arial", 10, "bold"))
        self.back_button.pack(side=tk.LEFT)
        
        
        self.display_record()
    
    def display_record(self):
        if self.is_ring_complete:
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, "Ring Complete")
            self.button.config(state=tk.DISABLED)
            self.next_text.delete("1.0", tk.END)
            self.next_text.insert(tk.END, "Ring Complete")
            
            # Clear previous text on the canvas
            self.canvas.delete("current_division_text")
            self.canvas.delete("time_to_complete_text")
            
            # Display "Ring Complete" on the canvas
            self.canvas.create_text(250, 250, text="Ring Complete", font=("Verdana", 40, "bold"), fill="white", tags="ring_complete_text")
        else:
            record = self.data[self.current_record_index]
            #self.text_widget.delete("1.0", tk.END)
            #self.text_widget.insert(tk.END, "Division Name: " + record["division name"] + "\n")
            #self.text_widget.insert(tk.END, "Time To Complete: " + str(record["time to complete"]) + "\n\n")
            if self.current_record_index + 1 < len(self.data):
                next_record = self.data[self.current_record_index + 1]
                self.next_text.delete("1.0", tk.END)
                self.next_text.insert(tk.END, "Division Name: " + next_record["division name"] + "\n")
                self.next_text.insert(tk.END, "Time To Complete: " + str(next_record["time to complete"]) + "\n\n")
            else:
                self.next_text.delete("1.0", tk.END)
                self.next_text.insert(tk.END, "Ring Complete")
        
            # Clear previous text on the canvas
            self.canvas.delete("ring_complete_text")
        
            # Display the text on the canvas
            division_text = "Division:"
            time_text = "Time To Complete:"
            current_division_text = record["division name"]
            time_to_complete_text = str(record["time to complete"]) + " mins"
        
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
            self.canvas.create_text(250, 50, anchor=tk.CENTER, text=division_text, font=("Verdana", 25), fill="white")
            self.canvas.create_text(250, 250, anchor=tk.CENTER, text=current_division_text, font=("Verdana", 30, "bold"), fill="white", tags="current_division_text", width=500)
            self.canvas.create_text(250, 435, anchor=tk.CENTER, text=time_text, font=("Verdana", 25), fill="white")
            self.canvas.create_text(250, 475, anchor=tk.CENTER, text=time_to_complete_text, font=("Verdana", 40, "bold"), fill="white", tags="time_to_complete_text", width = 500)
    
    def next_record(self):
        self.current_record_index += 1
        if self.current_record_index >= len(self.data):
            self.is_ring_complete = True
        self.display_record()

    def previous_record(self):
        self.current_record_index -= 1
        self.is_ring_complete = False
        self.display_record()

def select_file():
    filetypes = [("Excel Files", "*.xlsx")]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    #filepath = "C:\\Users\\saone\\Documents\\Python Stuff\\tournament_schedule_display\\sample_schedule.xlsx"
    if filepath:
        # Read the selected XLSX file
        df = pd.read_excel(filepath)
        
        # Get the unique values from the "ring number" column
        unique_rings = df["ring number"].unique()
        
        # Destroy the existing widgets and go back to the original window
        # frame.destroy()
        create_columns(unique_rings, df)

def restart_application():
    # Close the current window
    root.destroy()

    # Re-run the script
    # python = sys.executable
    # os.execl(python, python, *sys.argv)
    script_folder = os.path.dirname(__file__)
    script_name = os.path.basename(__file__)
    full_script_path = script_folder + "\\" + script_name

    subprocess.run(["python", full_script_path])
    
def create_columns(unique_rings, df):
    global frame
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    
    for ring in unique_rings:
        # Filter the DataFrame based on the ring value
        filtered_df = df[df["ring number"] == ring]
        
        # Create a RingBox instance for each ring
        RingBox(frame, ring, filtered_df.to_dict("records"))

def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time, font="Verdana 125 bold")
    root.after(1000, update_clock)
root = tk.Tk()
root.title("Tournament Schedule Display")

# Create a label for the clock
clock_label = tk.Label(root, text="", font=("Verdana bold", 25))
clock_label.pack(side=tk.BOTTOM, pady=(10,0))

# Update the clock
update_clock()

# Set minimum window size
root.minsize(500, 400)

# Set the application to full screen
root.attributes('-fullscreen', True)

# Configure the window to be resizable when not in full-screen mode
root.resizable(True, True)

# Remove window decorations
root.overrideredirect(True)

# Function to handle the close button manually
def close_app():
    root.destroy()

# Create a custom close button
close_button = tk.Button(root, text="X", command=close_app, font=("Arial", 16), bg="red", fg="white")
close_button.place(x=root.winfo_screenwidth() - 40, y=0, width=40, height=40)

button = tk.Button(root, text="Select Raw Schedule File", command=select_file, font=("Arial", 16))
button.pack(padx=10, pady=(25, 5))

# to speed up testing only, remove when complete
# select_file()

restart_button = tk.Button(root, text="Restart", command=restart_application, font=("Arial", 10))
restart_button.place(relx=0.01, rely=0.01)


root.mainloop()