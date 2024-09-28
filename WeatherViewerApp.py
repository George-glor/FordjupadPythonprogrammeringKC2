import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine

# Skapa anslutning till SQL-databasen
DATABASE_URL = "mssql+pyodbc://@GEORGE/WeatherINSweden?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Läs in data från SQL-databasen
query = "SELECT * FROM weather_forecast"
df = pd.read_sql(query, con=engine)

class WeatherViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Viewer")
        self.filtered_df = df.copy()  

        # Skapa GUI-komponenter
        self.create_gui()

        # Visa all data initialt
        self.display_results(self.filtered_df)

    def create_gui(self):
       
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill="x", pady=10)

        self.filter_label = tk.Label(filter_frame, text="Filter (Column:Value):")
        self.filter_label.pack(side="left", padx=5)

        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side="left", padx=5)

        self.filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(side="left", padx=5)

        self.tree = ttk.Treeview(main_frame, columns=[col for col in df.columns], show='headings')
        self.tree.pack(fill="both", expand=True)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=tk.NO)  

        self.auto_adjust_column_width()

    def auto_adjust_column_width(self):
        # Skapa en label för textmätning
        label = tk.Label(self.root, font=('Arial', 10))
        max_width = {col: len(self.tree.heading(col, 'text')) * 10 for col in self.tree["columns"]}  # Starta med rubrikens bredd

        # Kontrollera alla kolumnvärden
        for item in self.tree.get_children():
            row_values = self.tree.item(item, 'values')
            for col, value in zip(self.tree["columns"], row_values):
                label.config(text=value)
                text_width = label.winfo_reqwidth()
                max_width[col] = max(max_width[col], text_width)

        # Ställ in kolumnbredd baserat på det bredaste innehållet
        for col, width in max_width.items():
            self.tree.column(col, width=width + 20)  

    def display_results(self, df_to_display):
        # Rensa tidigare resultat
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Visa resultat
        for _, row in df_to_display.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def apply_filter(self):
        filter_text = self.filter_entry.get()
        if not filter_text:
            self.filtered_df = df.copy()  
        else:
            try:
                column, value = filter_text.split(':', 1)
                column = column.strip()
                value = value.strip()
                if column in df.columns:
                    self.filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
                else:
                    messagebox.showwarning("Invalid Column", f"Column '{column}' does not exist.")
                    self.filtered_df = df.copy()
            except ValueError:
                messagebox.showwarning("Invalid Filter", "Filter format should be 'Column:Value'.")
                self.filtered_df = df.copy()

        # Uppdatera visningen med filtrerad data
        self.display_results(self.filtered_df)

# Skapa applikationsfönstret
root = tk.Tk()
app = WeatherViewerApp(root)
root.mainloop()
