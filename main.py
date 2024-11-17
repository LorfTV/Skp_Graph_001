import matplotlib.pyplot as plt  
import numpy as np
import streamlit as st
import re
import io

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

    # Default colors for themes
    grid_color = '#4CE4C9'  # Default grid color for themes  # Default label color
    title_color = "#F0F6FC"  # Default title color
    line_color = 'blue'  # Default line color

    # Theme-based settings
    if theme == "Manim": 
        line_color = "cyan"  
        plt.gca().set_facecolor('#0D1117')
        plt.gcf().set_facecolor('#0D1117')
        ax.grid(True, linestyle="--", linewidth=0.5, color="#4CE4C9")
        ax.set_title("Graph", color="#F0F6FC", fontfamily="serif", size=22, weight='bold')
        ax.set_xlabel("X-axis", color="#F0F6FC", fontfamily="serif", size=14)
        ax.set_ylabel("Y-axis", color="#F0F6FC", fontfamily="serif", size=14)
        ax.tick_params(axis="both", which="major", length=7, colors="#F0F6FC", direction="inout")
        ax.tick_params(axis="both", which="minor", length=4, colors="#F0F6FC", direction="in")
    elif theme == "Blueprint":
        line_color = "red"  # Red for Blueprint theme
        plt.gca().set_facecolor('#1C4E80')
        plt.gcf().set_facecolor('#1C4E80')  
        ax.grid(True, linestyle="--", linewidth=0.5, color="#FFFFFF")
        ax.set_title("Graph", color="#FFFFFF", fontfamily="DejaVu Sans Mono", size=22, weight='bold')
        ax.set_xlabel("X-axis", color="#FFFFFF", fontfamily="DejaVu Sans Mono", size=14)
        ax.set_ylabel("Y-axis", color="#FFFFFF", fontfamily="DejaVu Sans Mono", size=14)
        ax.tick_params(axis="both", which="major", length=7, colors="#FFFFFF", direction="inout")
        ax.tick_params(axis="both", which="minor", length=4, colors="#FFFFFF", direction="in")
    elif theme == "DrSimple":
        line_color = "green"  # Green for DrSimple theme
        ax.set_facecolor("#F5F5F5")
        ax.grid(True, linestyle="-", linewidth=0.5, color="#D6D6D6")
        ax.set_title("Graph", color="#333333", fontfamily="DejaVu Sans", size=22, weight='bold')
        ax.set_xlabel("X-axis", color="#333333", fontfamily="DejaVu Sans Mono", size=14)
        ax.set_ylabel("Y-axis", color="#333333", fontfamily="DejaVu Sans Mono", size=14)
        ax.tick_params(axis="both", which="major", length=7, colors="#333333", direction="out")
        ax.tick_params(axis="both", which="minor", length=4, colors="#333333", direction="out")
        title_color = 'black'
    else:
        raise ValueError(f"Unknown theme: {theme}")

    # Apply theme settings
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
st.sidebar.title("**Graph.F[X]**")  
st.sidebar.write("*Skepsis Foundation's*") 
st.sidebar.write("### **Developed By Nachiketa Vellikad**") 
st.sidebar.write("*Beta_ve--0.2*") 
st.sidebar.write("***Write any expression in terms of x and with numerical data, and have fun!***") 

# Input equation and process
x, y, con_input_Eq, input_Eq = input_eq() 
st.write("Decide a Theme for the Graph!") 

# Choose theme buttons
col1, col2, col3, col4 = st.columns(4)  # Create a row with 4 columns for button alignment
with col1:
    blueprint_button = st.button('Blueprint')
with col2:
    manim_button = st.button('Manim')
with col3:
    dr_simple = st.button('DrSimple')


# Logic to handle theme selection 
if blueprint_button:
    theme = "Blueprint"
elif manim_button:
    theme = "Manim"
elif dr_simple:
    theme = "DrSimple"
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
        st.write("Select a theme to apply.") 

