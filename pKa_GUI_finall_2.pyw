import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.io import write_html
import webbrowser

# Henderson-Hasselbalch equation
def henderson_hasselbalch(pH, pKa, shift_min, shift_max):
    return shift_min + (shift_max - shift_min) / (1 + 10**(pKa - pH))

# Function to calculate R-squared
def calculate_r_squared(y, y_fit):
    residuals = y - y_fit
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

class HendersonHasselbalchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Henderson-Hasselbalch Curve Fitting")
        
        # Set default GUI window size (width x height)
        self.root.geometry("400x600")
        
        # Initialize variables
        self.data = None
        self.file_path = None
        
        # Instruction label
        self.instruction_label = tk.Label(
            root,
            text="Load the appropriate two-column CSV file with headers 'pH' and 'shift'. Use SHIFT or CTRL to select the points you want to include for fitting the Henderson-Hasselbalch curve and calculating pKa. Press DRAW.",
            wraplength=360,  # Wrap text to fit within 400 pixels
            justify="center"  # Center align the text
        )
        self.instruction_label.pack(pady=(10,5))


        # File loading button
        self.load_button = tk.Button(root, text="Load CSV File", command=self.load_file)
        self.load_button.pack(pady=10)
        
        # Frame for displaying data
        self.data_frame = tk.Frame(root)
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.data_frame, columns=("pH", "shift"), show="headings", selectmode="extended")
        self.tree.heading("pH", text="pH")
        self.tree.heading("shift", text="Shift")
        self.tree.column("pH", anchor="center", width=100)
        self.tree.column("shift", anchor="center", width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        # Vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        
        # Draw button
        self.draw_button = tk.Button(root, text="DRAW!", command=self.process_and_draw, state="disabled")
        self.draw_button.pack(pady=10)

    def load_file(self):
        # Open file dialog to load CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        
        try:
            # Load CSV data into pandas DataFrame and sort by pH
            self.data = pd.read_csv(file_path).sort_values(by="pH")
            self.file_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return
        
        # Clear previous data in Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate Treeview with data
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", iid=index, values=(row["pH"], row["shift"]))

        # Enable draw button
        self.draw_button.config(state="normal")
    
    def process_and_draw(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return

        # Get selected rows
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No rows selected!")
            return

        selected_rows = [self.tree.item(item)["values"] for item in selected_items]
        filtered_data = pd.DataFrame(selected_rows, columns=["pH", "shift"])

        try:
            # Perform curve fitting and plot results
            self.perform_curve_fit(filtered_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data: {e}")
    
    def perform_curve_fit(self, filtered_data):
        # Extract pH and shift values
        pH = filtered_data["pH"].astype(float).values
        shift = filtered_data["shift"].astype(float).values
        
        # Calculate initial guess for pKa
        derivative = np.diff(shift) / np.diff(pH)
        min_derivative_index = np.argmin(derivative)
        initial_pKa_guess = pH[min_derivative_index + 1]
        
        # Set initial parameter guesses and bounds
        initial_guess_refined = [initial_pKa_guess, min(shift), max(shift)]
        bounds = ([0, min(shift) - 1, min(shift) - 1], [14, max(shift) + 1, max(shift) + 1])
        
        # Perform curve fitting
        params, _ = curve_fit(henderson_hasselbalch, pH, shift, bounds=bounds, p0=initial_guess_refined)
        pKa, shift_min, shift_max = params
        
        # Generate fitted curve
        pH_fit = np.linspace(min(pH), max(pH), 100)
        shift_fit = henderson_hasselbalch(pH_fit, pKa, shift_min, shift_max)
        
        # Calculate R-squared
        shift_fit_data = henderson_hasselbalch(pH, pKa, shift_min, shift_max)
        r_squared = calculate_r_squared(shift, shift_fit_data)
        
        # Plot results using Plotly
        error = np.full_like(shift, np.abs(shift - shift_fit_data).mean())
        fig = go.Figure()

        # Add experimental data with error bars
        fig.add_trace(go.Scatter(
            x=pH, 
            y=shift, 
            mode='markers', 
            name='Experimental data',
            error_y=dict(type='data', array=error, visible=True),
            marker=dict(color='blue')
        ))

        # Add fitted curve
        fig.add_trace(go.Scatter(
            x=pH_fit, 
            y=shift_fit, 
            mode='lines', 
            name='Fitted curve',
            line=dict(color='red')
        ))

        # Add annotations for the fitted equation and parameters
        annotation_text = (
            f'Fitted Henderson-Hasselbalch equation:<br>'
            f'shift = {shift_min:.2f} + ({shift_max:.2f} - {shift_min:.2f}) / (1 + 10^({pKa:.2f} - pH))<br>'
            f'<b><span style="color:red">pKa = {pKa:.2f}</span></b><br>'
            f'Maximal chemical shift = {shift_min:.2f}<br>'
            f'Minimal chemical shift = {shift_max:.2f}<br>'
            f'<b><span style="color:green">R-squared = {r_squared:.4f}</span></b><br>'
        )
        fig.add_annotation(x=1.05, y=0.5, showarrow=False, text=annotation_text, xref="paper", yref="paper", align="left")
        
        # Update layout for white background and no grid
        fig.update_layout(
            title=f"Henderson-Hasselbalch Curve Fitting<br>File: {self.file_path.split('/')[-1]}",
            xaxis_title="pH",
            yaxis_title="Shift",
            legend_title="Legend",
            template="plotly_white",
            xaxis=dict(
                showgrid=False,            # Disable grid lines
                zeroline=True,             # Enable axis line
                zerolinecolor="black",     # Set axis line color
                linecolor="black",         # Set outer axis line color
                linewidth=2,               # Thickness of the axis line
                tickformat=".2f",          # Format numbers with 2 decimal places
                ticklabelposition="outside",  # Move labels slightly outside the axis
                ticks="outside",           # Add tick marks
                ticklen=5                  # Length of tick marks
            ),
            yaxis=dict(
                showgrid=False,            # Disable grid lines
                zeroline=True,             # Enable axis line
                zerolinecolor="black",     # Set axis line color
                linecolor="black",         # Set outer axis line color
                linewidth=2,               # Thickness of the axis line
                tickformat=".2f",          # Format numbers with 2 decimal places
                ticklabelposition="outside",  # Move labels slightly outside the axis
                ticks="outside",           # Add tick marks
                ticklen=5                  # Length of tick marks
            )
        )
        
        # Save plot to HTML and set browser tab title
        output_path = self.file_path.split('/')[-1].split('.')[0]
        output_file = f"{output_path}.html"
        write_html(fig, file=output_file, auto_open=False, config={"title": f"Henderson-Hasselbalch: {self.file_path.split('/')[-1]}"})

        # Open the saved HTML file in the default browser
        webbrowser.open(output_file)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HendersonHasselbalchApp(root)
    root.mainloop()
