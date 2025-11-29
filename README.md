# 🔢 NumPy Matrix Calculator (Streamlit App)

A simple, interactive tool to explore **matrix operations** using Python and NumPy.  
You can type your own matrices or use built-in sample sets and see instant results.

### What you can do:

- **Addition (A + B)** — only for matrices of the same shape  
- **Subtraction (A - B)** — only for matrices of the same shape  
- **Multiplication (A @ B)** — follows standard matrix multiplication rules  
- **Shape validation** — ensures your matrices can be combined  
- **Formatted outputs** — view results in clean tables for easy reading  

### How to give input:

- **Manual Input:** type numbers separated by spaces, and rows separated by Enter.  
  Example:
  ```
  1 2 3
  4 5 6
  ```
- **Predefined Sets:** choose from 4 built-in examples (2x2, 3x3, identity, row/column pairs) for quick testing.

---

## 📦 Requirements

Install the following Python packages before running the app:

- `streamlit` — web interface  
- `numpy` — matrix computations  
- `pandas` — clean table display  

### 🛠️ Install Them:

```
pip install streamlit numpy pandas
```

---

## ▶️ How to Run

1. Make sure Python is installed on your system: https://www.python.org/downloads/  
2. Open a terminal and navigate to the folder with your `app.py`:
   ```
   cd path/to/your/directory
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
4. Your browser will open automatically. If not, go to the URL shown in the terminal (usually `http://localhost:8501`).

---

Start exploring matrices and see the results instantly! ✅
