
# AI based City Layout Optimization Project

AI based City Layout Optimization Project is a Python project that leverages genetic algorithms and local search methods to optimize city grids. It uses heuristics to strategically place buildings, emergency services, and intersections to minimize travel distances while adhering to constraints.

# Sample Outputs

Local Search:
![local](https://github.com/user-attachments/assets/ad8932a4-ebdd-4f61-a576-2f60b27b8099)

Genetic Algorithms:
![gene-ezgif com-optimize(1)](https://github.com/user-attachments/assets/7d9d891e-615d-41c8-a96f-df4b7573dfe2)

## Directory Structure

```
src/
│
├── algorithms/           # Contains core optimization algorithms like A*, Genetic Algorithm & Local Search Algorithm.
├── utils/                # Utility scripts for supporting tasks like fitness calculation and grid generation.
├── visuals/              # Scripts for visualizing city grids and saving annotated results.
├── grid_constants.py     # Configuration file for grid parameters like size, number of buildings, etc.
└── main.py               # Main script to run the optimization.
```

## How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <repo_url>
cd <repo_name>
```

### Step 2: Install Dependencies

Make sure you have Python 3.8+ installed on your system. Then, install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Grid Parameters

Edit the `src/grid_constants.py` file to adjust the parameters for the grid, such as dimensions, number of buildings, and emergency services:

```python
GRID_WIDTH = 15                  # Number of columns in the grid
GRID_HEIGHT = 15                 # Number of rows in the grid
NUM_BUILDINGS = 15               # Total number of buildings to place
NUM_EMERGENCY_SERVICES = 6       # Total number of emergency services to place
RES_DIR = "/path/to/output/dir"  # Directory for saving results
```

### Step 4: Run the Main Script

Navigate to the `src` directory and execute the `main.py` script to start the optimization process:

```bash
python main.py
```

### Step 5: View Results

After running the script, visualizations and result files will be saved in the directory specified in `RES_DIR`. These include images of the optimized grid layouts for each generation and a summary of the results.

---

## Future Enhancements

- Add more parameters to optimize like walkability in the city, e.t.c
- Improve the fitness evaluation by integrating real-world traffic or population data.
- Improve local search by adding options to get out of local optima.
- Extend the visualization module for better interaction and analysis.

Feel free to contribute by opening a pull request or reporting issues!

## Collaborators

The following individuals contributed to the development of this project:

1. **Shrey Chirag Shah**
2. **Jithin Veeragandham**
3. **Sahil Subodh Bane**
4. **Yash Hareshbhai Beladiya**
5. **Yuhui Sun**
