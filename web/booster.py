import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a Streamlit app
st.title('Interactive Line Plot')

# Plot the data
fig, ax = plt.subplots()
line, = ax.plot(x, y)
ax.fill_between(x, y, color="skyblue", alpha=0.3)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Line Plot')

# Display the plot using Streamlit
st.pyplot(fig)

# Function to handle mouse clicks
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        st.sidebar.text(f"Clicked point: ({event.xdata:.2f}, {event.ydata:.2f})")
        st.sidebar.text_input('Enter X-axis value:', value=f'{event.xdata:.2f}')

# Connect the click event handler
cid = fig.canvas.mpl_connect('button_press_event', onclick)
