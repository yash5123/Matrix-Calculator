import streamlit as st
import numpy as np

st.set_page_config(
    page_title="NumPy Matrix Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PREDEF_SET_1_A = "1 2\n3 4" 
PREDEF_SET_1_B = "5 6\n7 8" 

PREDEF_SET_2_A = "1 2\n3 4\n5 6" 
PREDEF_SET_2_B = "7 8 9\n10 11 12" 

PREDEF_SET_3_A = "1 0 0\n0 1 0\n0 0 1" 
PREDEF_SET_3_B = "2 0 0\n0 3 0\n0 0 4" 

PREDEF_SET_4_A = "10 20 30"
PREDEF_SET_4_B = "1\n2\n3"

PREDEFINED_OPTIONS = {
    'Predefined Set 1: 2x2 Square': (PREDEF_SET_1_A, PREDEF_SET_1_B, "A(2x2), B(2x2)"),
    'Predefined Set 2: 3x2 and 2x3 for A@B': (PREDEF_SET_2_A, PREDEF_SET_2_B, "A(3x2), B(2x3)"),
    'Predefined Set 3: 3x3 Identity & Diagonal': (PREDEF_SET_3_A, PREDEF_SET_3_B, "A(3x3), B(3x3)"),
    'Predefined Set 4: 1x3 and 3x1 for A@B': (PREDEF_SET_4_A, PREDEF_SET_4_B, "A(1x3), B(3x1)"),
}

if 'matrix_a' not in st.session_state:
    st.session_state.matrix_a = None
if 'matrix_b' not in st.session_state: 
    st.session_state.matrix_b = None
if 'result' not in st.session_state:
    st.session_state.result = None
if 'operation_name' not in st.session_state:
    st.session_state.operation_name = None
if 'input_choice' not in st.session_state:
    st.session_state.input_choice = 'Manual Input' 

def parse_matrix_input(matrix_str, matrix_name):
    if not matrix_str.strip():
        return None 
    try:
        rows_list = [
            [float(x) for x in line.split() if x]
            for line in matrix_str.strip().split('\n') if line.strip()
        ]
        if not rows_list:
            st.error(f"Matrix {matrix_name} has no valid rows/elements.")
            return None
        
        cols = len(rows_list[0])
        for i, row in enumerate(rows_list):
            if len(row) != cols:
                st.error(
                    f"Matrix {matrix_name} is inconsistent. Row 1 has {cols} columns, but row {i + 1} has {len(row)}."
                )
                return None

        return np.array(rows_list, dtype=float)

    except ValueError:
        st.error(f"Matrix {matrix_name}: Input must contain only valid numbers.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while processing Matrix {matrix_name}: {e}")
        return None

def display_matrix_status(col, matrix, name):
    shape_str = f'({matrix.shape[0]}x{matrix.shape[1]})' if matrix is not None else 'Undefined'
    col.subheader(f"{name}: {shape_str}")
    if matrix is not None:
        col.dataframe(matrix)
    else:
        col.info(f"Matrix {name} is not yet defined.")

def perform_operation(operation, name, error_message):
    st.session_state.operation_name = name
    A = st.session_state.matrix_a
    B = st.session_state.matrix_b

    try:
        if A is None or B is None:
             st.error("Operation failed: One or both matrices are undefined.")
             st.session_state.result = None
             return
             
        st.session_state.result = operation(A, B)
    except ValueError as e:
        st.error(f"Operation failed: {error_message}. Current shapes: A={A.shape}, B={B.shape}. Details: {e}")
        st.session_state.result = None
    except Exception as e:
        st.error(f"An unexpected error occurred during calculation: {e}")
        st.session_state.result = None
        
def set_predefined_matrices(choice):
    A_str, B_str, _ = PREDEFINED_OPTIONS[choice]
    A = parse_matrix_input(A_str, 'A')
    B = parse_matrix_input(B_str, 'B')
    
    if A is not None and B is not None:
        st.session_state.matrix_a = A
        st.session_state.matrix_b = B
        st.success(f"Loaded **{choice}** into Matrices A and B.")
    else:
        st.error("Failed to parse predefined matrices.")
        st.session_state.matrix_a = None
        st.session_state.matrix_b = None

st.title("🔢 NumPy Matrix Calculator")
st.markdown("""
Use the selector below to choose your input method: **Manual Input** or one of **four Predefined Sets**.
""")

st.session_state.input_choice = st.selectbox(
    "Choose an option to define Matrices A and B:",
    ['Manual Input'] + list(PREDEFINED_OPTIONS.keys()),
    key='input_choice_selectbox',
    index=0 
)
    
if st.session_state.input_choice != 'Manual Input':
    selected_key = st.session_state.input_choice
    A_str, B_str, description = PREDEFINED_OPTIONS[selected_key]
    
    st.markdown(f"#### Selected Set: **{description}**")
    
    predef_col1, predef_col2 = st.columns(2)
    with predef_col1:
        st.write("**Matrix A:**")
        st.code(A_str)
    with predef_col2:
        st.write("**Matrix B:**")
        st.code(B_str)
        
    if st.button(f"Load '{selected_key}'", key='load_predefined', type='primary', use_container_width=True):
        set_predefined_matrices(selected_key)
        st.session_state.result = None 
else:
    st.info("Please enter your matrix values manually below, then click 'Define Matrix A/B'.")


st.divider()

if st.session_state.input_choice == 'Manual Input':
    st.markdown("### 📝 Manual Matrix Input")
    st.markdown("""
    * Enter elements separated by **spaces**.
    * Separate rows using **new lines** (press Enter).
    """)
    
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        st.header("Matrix A Input")
        a_input = st.text_area(
            "Enter elements for Matrix A:",
            key='a_text_input',
            height=150,
            placeholder="1 2 3\n4 5 6\n7 8 9",
            value="" 
        )

        if st.button("Define Matrix A", key='define_a', type='primary', use_container_width=True):
            matrix_a = parse_matrix_input(a_input, 'A')
            if matrix_a is not None:
                st.session_state.matrix_a = matrix_a
                st.success(f"Matrix A ({matrix_a.shape[0]}x{matrix_a.shape[1]}) defined.")
            else:
                st.session_state.matrix_a = None
                st.session_state.result = None

    with input_col2:
        st.header("Matrix B Input")
        b_input = st.text_area(
            "Enter elements for Matrix B:",
            key='b_text_input',
            height=150,
            placeholder="1 0 0\n0 1 0\n0 0 1",
            value=""
        )

        if st.button("Define Matrix B", key='define_b', type='primary', use_container_width=True):
            matrix_b = parse_matrix_input(b_input, 'B')
            if matrix_b is not None:
                st.session_state.matrix_b = matrix_b
                st.success(f"Matrix B ({matrix_b.shape[0]}x{matrix_b.shape[1]}) defined.")
            else:
                st.session_state.matrix_b = None
                st.session_state.result = None
    
st.divider()

st.header("Defined Matrices Overview")
defined_col1, defined_col2 = st.columns(2)
display_matrix_status(defined_col1, st.session_state.matrix_a, "Matrix A")
display_matrix_status(defined_col2, st.session_state.matrix_b, "Matrix B")

st.divider()

st.header("Matrix Operations")

A = st.session_state.matrix_a
B = st.session_state.matrix_b

is_ready = A is not None and B is not None

if not is_ready:
    st.warning("Please **define** or **load** both Matrix A and Matrix B to enable operations.")

op_cols = st.columns(3)

with op_cols[0]:
    if st.button("A + B (Addition)", disabled=not is_ready, use_container_width=True):
        perform_operation(
            lambda a, b: a + b,
            "Addition (A + B)",
            "Addition requires both matrices to have the exact same shape ($m \times n$)"
        )

with op_cols[1]:
    if st.button("A - B (Subtraction)", disabled=not is_ready, use_container_width=True):
        perform_operation(
            lambda a, b: a - b,
            "Subtraction (A - B)",
            "Subtraction requires both matrices to have the exact same shape ($m \times n$)"
        )

with op_cols[2]:
    if st.button("A @ B (Multiplication)", disabled=not is_ready, use_container_width=True):
        if is_ready and A.shape[1] == B.shape[0]:
            perform_operation(
                lambda a, b: a @ b,
                "Multiplication (A @ B)",
                "Multiplication requires A's columns to match B's rows ($n=k$ in $A[m, n] \cdot B[k, p]$)"
            )
        elif is_ready:
            st.error(
                f"Multiplication requires inner dimensions to match. A columns: {A.shape[1]}, B rows: {B.shape[0]}."
            )
            st.session_state.result = None
            st.session_state.operation_name = "Multiplication (A @ B)"

st.divider()

st.header("Calculation Result")

result = st.session_state.result
op_name = st.session_state.operation_name

if result is not None:
    st.success(f"Result of **{op_name}** (Shape: {result.shape[0]}x{result.shape[1]}):")
    st.dataframe(result, use_container_width=True)
elif op_name:
    st.info(f"Check the error message above for the calculation of **{op_name}**.")
else:
    st.info("The result will appear here after an operation is successfully performed.")