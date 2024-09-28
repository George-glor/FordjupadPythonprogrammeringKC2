import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from sqlalchemy import create_engine

# Set up database connection
def get_db_connection():
    try:
        engine = create_engine("mssql+pyodbc://@GEORGE/WeatherINSweden?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")
        return engine
    except Exception as e:
        print(f"Database connection error: {e}")
        messagebox.showerror("Database Connection Error", f"Failed to connect to database:\n{e}")
        return None

# Function to fetch data from database
def fetch_data_from_db():
    engine = get_db_connection()
    if engine is not None:
        try:
            query = "SELECT * FROM weather_forecast"
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            messagebox.showerror("Data Fetch Error", f"An error occurred while fetching the data:\n{e}")
    return pd.DataFrame()  

# Fetch data from database
df = fetch_data_from_db()

class WeatherViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Viewer")
        self.filtered_df = df.copy()  

        # skapa windows icon 
        self.set_window_icon()

        # styl konfigurations
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.configure("Treeview", background="#F5F5F5", foreground="#000000", fieldbackground="#FFFFFF")
        style.configure('TButton', font=('Arial', 10), padding=6)

        # skapa a main frame
        main_frame = tk.Frame(root, bg="#EAEAEA")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # skapa filter frame
        filter_frame = tk.Frame(main_frame, bg="#EAEAEA")
        filter_frame.grid(row=0, column=0, sticky="ew")

        # lägg till  label och entry för filtering
        self.filter_label = tk.Label(filter_frame, text="Filter (Column:Value):", bg="#EAEAEA")
        self.filter_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.filter_entry = tk.Entry(filter_frame, width=40)
        self.filter_entry.grid(row=0, column=1, padx=5, pady=5)

        self.filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        self.filter_button.grid(row=0, column=2, padx=5, pady=5)

        # reslutat visar 
        self.tree = ttk.Treeview(main_frame, columns=[col for col in df.columns], show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Scrollbars
        self.vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.hsb.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.tree.configure(xscrollcommand=self.hsb.set)

        
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=tk.NO)  

        self.auto_adjust_column_width()

        self.row_count_label = tk.Label(main_frame, text=f"Number of rows: {len(df)}", font=('Arial', 10, 'bold'), bg="#EAEAEA")
        self.row_count_label.grid(row=2, column=0, pady=10, sticky="w")

        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.display_results(self.filtered_df)

    def set_window_icon(self):
        try:
            self.icon_image = tk.PhotoImage(file='icon.png')  
            self.root.iconphoto(True, self.icon_image)
        except tk.TclError:
            print("Error loading icon image. Make sure the file path is correct and the file is a valid image format.")

    def auto_adjust_column_width(self):
        label = tk.Label(self.root, font=('Arial', 10))
        max_width = {col: len(self.tree.heading(col, 'text')) * 10 for col in self.tree["columns"]}  # Start with heading width

        for item in self.tree.get_children():
            row_values = self.tree.item(item, 'values')
            for col, value in zip(self.tree["columns"], row_values):
                label.config(text=value)
                text_width = label.winfo_reqwidth()
                max_width[col] = max(max_width[col], text_width)

        for col, width in max_width.items():
            self.tree.column(col, width=width + 20)  

    def display_results(self, df_to_display):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in df_to_display.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def apply_filter(self):
        filter_text = self.filter_entry.get()
        if not filter_text:
            self.filtered_df = df.copy()  
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

        self.display_results(self.filtered_df)
        self.row_count_label.config(text=f"Number of rows: {len(self.filtered_df)}")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return  

        try:
            
            self.filtered_df.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Export Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting the data:\n{e}")



root = tk.Tk()
app = WeatherViewerApp(root)
root.mainloop()
