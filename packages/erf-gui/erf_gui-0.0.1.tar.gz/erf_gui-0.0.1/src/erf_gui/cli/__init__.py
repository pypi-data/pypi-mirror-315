import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd

def combine_csv(files):
    # Combine CSV files into one DataFrame
    combined_df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    # Save the combined DataFrame to a new CSV file
    output_file = filedialog.asksaveasfile(defaultextension=".csv", initialfile="combined-output.csv")
    combined_df.to_csv(output_file, index=False)
    print(f"Files combined successfully into {output_file}.")

def select_files_or_folder():
    # Ask the user to select multiple CSV files or a folder
    option = messagebox.askquestion("Select Option", "Do you want to select a folder of files?")
    
    if option == "yes":
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            # Get all CSV files in the selected folder
            files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]
            if files:
                combine_csv(files)
            else:
                print("No CSV files found in the selected folder.")
    else:
        files = filedialog.askopenfilenames(title="Select CSV Files", filetypes=[("CSV files", "*.csv")])
        if files:
            combine_csv(files)
        else:
            print("No files selected.")

def create_gui():
    root = tk.Tk()
    root.title("CSV Combiner")

    select_button = tk.Button(root, text="Select Files or Folder", command=select_files_or_folder)
    select_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
