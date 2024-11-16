import matplotlib.pyplot as plt  
import numpy as np
import streamlit as st
import re
import io
from PIL import Image

# --- Default Setup Function ---
def default_setup(): 
    plt.grid(True, which='major', axis='both', color='#01A79D', linewidth=0.5)  # Grid on both the axes
    plt.gcf().set_facecolor('Black')  # Outer background
    plt.gca().set_facecolor('Black')  # Inner background
    plt.minorticks_on()  # Minor ticks on axes
    plt.tick_params(axis='both', which='both', color='white', labelcolor='white')  # Styling for tick labels
    plt.xlabel('x-axis', c='w')  # Label for x-axis
    plt.ylabel('y-axis', c='w')  # Label for y-axis
    plt.title('Graph', fontname='serif', color='white', fontsize=15) 

# --- Convert Equation Function ---
def convert_equation(equation):
    # Replace ^ with ** for exponentiation
    equation = equation.replace('^', '**')
    
    # Add multiplication where needed (between numbers and variables like 4x)
    equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
    
    # Replace sin, cos, log, etc., with their numpy equivalents
    equation = re.sub(r'\bsin\(', 'np.sin(', equation)
    equation = re.sub(r'\bcos\(', 'np.cos(', equation)
    equation = re.sub(r'\btan\(', 'np.tan(', equation)
    equation = re.sub(r'\blog\(', 'np.log(', equation)
    equation = re.sub(r'\bsqrt\(', 'np.sqrt(', equation)
    equation = re.sub(r'\be\^', 'np.exp', equation)

    return equation

# --- Input Equation Function ---
def input_eq(): 
    input_Eq = st.text_input("Write an 'expression' in terms of x [use only small letters]:", key="input_eq")

    x_min_slider = st.slider("Enter the minimum value of x (default: -10):", -100.0, 0.0, -10.0, key="x_min_slider")
    x_min_manual = st.text_input("Or manually input the minimum value of x:", str(x_min_slider), key="x_min_manual")
    x_min = float(x_min_manual) if x_min_manual else x_min_slider

    x_max_slider = st.slider("Enter the maximum value of x (default: 10):", 0.0, 100.0, 10.0, key="x_max_slider")
    x_max_manual = st.text_input("Or manually input the maximum value of x:", str(x_max_slider), key="x_max_manual")
    x_max = float(x_max_manual) if x_max_manual else x_max_slider
    
    x = np.linspace(x_min, x_max, 100)  # Generates x values from x_min to x_max
    
    con_input_Eq = ""
    if input_Eq:
        con_input_Eq = convert_equation(input_Eq)  # Convert input equation to a usable format

    y = np.zeros_like(x)  # Default to zero if no equation is provided
    if con_input_Eq:
        try:
            y = eval(con_input_Eq, {"np": np, "x": x})  # Evaluate the equation safely
        except Exception as e:
            st.error(f"Error evaluating the equation: {e}")
            y = np.zeros_like(x)  # Fallback in case of error
    
    return x, y, con_input_Eq, input_Eq  # Return x, y, converted equation, and input equation

# --- Setup Plot for Different Themes ---
def setup_plot(x, y, theme):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    ax.grid(True, which='major', axis='both', linewidth=0.5)
    ax.minorticks_on()

    # Theme-based settings
    if theme == "blueprint":
        fig.patch.set_facecolor('#0252AD')
        ax.set_facecolor('#0252AD')
        grid_color = 'white'
        label_color = 'white'
        line_color = 'red'
        title_color = 'white'
    elif theme == "manim":
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        grid_color = '#01A79D'
        label_color = 'white'
        line_color = 'blue'
        title_color = 'white'
    elif theme == "light abnormal":
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        grid_color = 'green'
        label_color = 'red'
        line_color = 'blue'
        title_color = 'red'
    elif theme == "light normal":
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        grid_color = '#01A79D'
        label_color = 'black'
        line_color = 'red'
        title_color = 'black'
    else:
        raise ValueError(f"Unknown theme: {theme}")

    # Apply theme settings
    ax.grid(color=grid_color)
    ax.tick_params(axis='both', which='both', colors=label_color)
    ax.set_xlabel('X-axis', color=label_color)
    ax.set_ylabel('Y-axis', color=label_color)
    ax.set_title('Graph', color=title_color, fontname='serif', fontsize=15)
    ax.plot(x, y, color=line_color)

    return fig  # Return the figure to pass to Streamlit

# --- Save Plot Function ---
def save_plot():
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

# --- Streamlit App ---
st.set_page_config(page_title="Graph.F(X)")
st.title("Graph.F(X)")  

# Sidebar content

st.sidebar.image("skepsis_f(x).png")
st.sidebar.title("**Graph.F[X]**")  
st.sidebar.write("*Skepsis Foundation's*") 
st.sidebar.write("### **Developed By Nachiketa Vellikad**") 
st.sidebar.write("*Beta_ve--0.2*") 
st.sidebar.write("***Write any expression in terms of x and with numerical data, and have fun!***") 

# Input equation and process
x, y, con_input_Eq, input_Eq = input_eq()

# Choose theme buttons
col1, col2, col3, col4 = st.columns(4)  # Create a row with 4 columns for button alignment
with col1:
    blueprint_button = st.button('Blueprint')
with col2:
    manim_button = st.button('Manim')
with col3:
    light_abnormal_button = st.button('Light Abnormal')
with col4:
    light_normal_button = st.button('Light Normal')

# Logic to handle theme selection
if blueprint_button:
    theme = "blueprint"
elif manim_button:
    theme = "manim"
elif light_abnormal_button:
    theme = "light abnormal"
elif light_normal_button:
    theme = "light normal"
else:
    theme = None

# Plot the graph based on the selected theme
if con_input_Eq:
    if theme:
        try:
            fig = setup_plot(x, y, theme)  # Get the figure from setup_plot function
            st.pyplot(fig)  # Display the plot in Streamlit with the selected theme
        except ValueError as e:
            st.error(f"Error: {e}")
    else:
        # Default graph plot without theme
        st.subheader(f"Equation: {con_input_Eq}")
        plt.plot(x, y, label=f"{input_Eq}", color='b', linewidth=2)
        default_setup()  # Apply default setup (you can customize if needed)
        st.pyplot(plt)  # Display the plot

# Add download button
if con_input_Eq:
    buf = save_plot()
    st.download_button("Download Graphed plot", buf, "skepsisFX_Graph.png", "image/png")
