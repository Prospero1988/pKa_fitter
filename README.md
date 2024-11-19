
# Henderson-Hasselbalch Curve Fitting GUI

This repository provides an easy-to-use graphical user interface (GUI) for fitting a **Henderson-Hasselbalch curve** to experimental data and calculating **pKa** values. The GUI is implemented in Python using `tkinter` and generates high-quality interactive plots with `Plotly`. The repository contains the main script (`pKa_GUI_finall_2.pyw`) and a sample input file (`input.csv`) to demonstrate functionality.

---

### **About the Henderson-Hasselbalch Curve**
The Henderson-Hasselbalch equation is a key tool in chemistry and biochemistry for understanding acid-base equilibria. It is expressed as:

\[
\text{Shift} = \text{Shift}_{\text{min}} + \frac{\text{Shift}_{\text{max}} - \text{Shift}_{\text{min}}}{1 + 10^{(\text{pKa} - \text{pH})}}
\]

This equation relates the pH of a solution to the protonation state of an ionizable group, often measured as a chemical shift in **NMR spectroscopy**. This GUI allows users to:
- Fit a Henderson-Hasselbalch curve to experimental data.
- Calculate the **pKa** value, representing the pH at which the group is 50% protonated.
- Visualize the results interactively.

---

### **Key Features**
#### 1. **User-Friendly Interface**
- **File Input:** Load a two-column CSV file with headers `pH` and `shift`. The sample file `input.csv` demonstrates the required format.
- **Interactive Selection:** Use **SHIFT** or **CTRL** to select specific data points for the fit. This flexibility ensures that users can exclude irrelevant or outlier points.
- **Real-Time Feedback:** A "DRAW" button initiates the fitting process and generates an interactive plot.

#### 2. **Robust Henderson-Hasselbalch Curve Fitting**
- **Error Bars:** Experimental variability is visualized with error bars on the plot.
- **Fitting Parameters:**
  - `Shift_min` and `Shift_max` represent the minimal and maximal chemical shift values observed during protonation/deprotonation.
  - `pKa` is calculated with high precision using advanced curve-fitting techniques.
- **Fine-Tuned Axis Representation:**
  - Numbers on the axes are displayed with two decimal places for clarity.
  - Tick marks and spacing are adjusted for better readability.
  - Axis lines are prominently displayed without distracting grid lines.

#### 3. **High-Quality Visualization**
- Interactive plots generated with **Plotly** include:
  - Annotations of fitted parameters (`pKa`, `Shift_min`, and `Shift_max`).
  - A dynamically updated title showing the name of the loaded CSV file.
  - Exported plots open directly in your default browser with a tab title matching the input file.

#### 4. **Customizable GUI Design**
- Informative instructions are displayed at the top of the GUI:
  - `"Load the appropriate two-column CSV file with headers 'pH' and 'shift'. Use SHIFT or CTRL to select the points you want to include for fitting the Henderson-Hasselbalch curve and calculating pKa. Press DRAW."`
- The interface adjusts dynamically to fit content, and scrollbars are provided for datasets exceeding the visible area.

---

### **Input Format**
The input file must be a two-column CSV file with the following format:
- **Header Row:** `pH` and `shift`.
- **Columns:**
  - `pH`: Numerical values representing the pH of the solution.
  - `shift`: Numerical values representing the observed chemical shift.

**Example (`input.csv`):**
```csv
pH,shift
2.0,8.10
3.0,8.05
4.0,7.90
5.0,7.40
6.0,6.80
7.0,6.50
```

---

### **Output**
The script generates:
1. **Interactive Plotly Visualizations:**
   - Scatterplot of experimental data with error bars.
   - Fitted Henderson-Hasselbalch curve in red.
   - Annotated parameters: `pKa`, `Shift_min`, and `Shift_max`.
   - Saved as an HTML file with the name matching the input file (e.g., `input.html`).
2. **High-Precision Calculations:**
   - `pKa` value.
   - R-squared value to evaluate the goodness of fit.

---

### **How It Works**
1. **File Loading:** The user selects a two-column CSV file containing experimental data. The GUI automatically displays the contents in a scrollable table, sorted by `pH`.
2. **Data Selection:** Users can highlight data points using **SHIFT** or **CTRL** to include only relevant points in the fitting process.
3. **Curve Fitting:** Upon pressing "DRAW":
   - The selected data is passed to a curve-fitting algorithm (`scipy.optimize.curve_fit`).
   - Initial guesses are intelligently derived from the dataset (e.g., `pKa` is estimated from the steepest slope).
   - Fitted parameters are calculated with constraints to ensure realistic values.
4. **Interactive Plot:** A Plotly visualization is generated, saved as an HTML file, and opened in the user's default browser.

---

### **Installation**
To use this script, install the following Python libraries:

1. **Required Libraries:**
   - `pandas`: For handling CSV data.
   - `numpy`: For numerical computations.
   - `scipy`: For curve fitting.
   - `plotly`: For generating interactive plots.
   - `tkinter`: Built-in with Python, used for the GUI.
   - `webbrowser`: Built-in with Python, used for opening plots in the default browser.

2. **Installation Command:**
   Use `pip` to install all dependencies:
   ```bash
   pip install pandas numpy scipy plotly
   ```

---

### **Usage Instructions**
1. Clone this repository or download the files:
   ```bash
   git clone https://github.com/your-username/henderson-hasselbalch-gui.git
   cd henderson-hasselbalch-gui
   ```
2. Run the GUI script:
   ```bash
   python pKa_GUI_finall_2.pyw
   ```
3. Follow the on-screen instructions:
   - Load your dataset (`input.csv`).
   - Select the data points for fitting.
   - Click "DRAW" to generate the curve and calculate parameters.

---

### **Why This Tool is Valuable**
#### 1. **Precision and Flexibility**
The script ensures accurate parameter estimation by:
- Automatically identifying appropriate bounds for fitting parameters.
- Allowing manual selection of data points to exclude outliers.

#### 2. **Clear Visualizations**
Interactive plots provide immediate feedback and make it easy to interpret results, especially for datasets with varying precision or noise.

#### 3. **Intuitive User Interface**
Even users with minimal coding experience can easily:
- Load data.
- Select points for analysis.
- Generate publication-quality plots.

---

### **Repository Contents**
- **`pKa_GUI_finall_2.pyw`:** The main Python script with the GUI implementation.
- **`input.csv`:** A sample dataset for testing.

---

### **Contributing**
Contributions to improve the script or add new features are welcome! Please fork the repository and submit a pull request with your changes.

---

### **License**
This project is licensed under the MIT License.
