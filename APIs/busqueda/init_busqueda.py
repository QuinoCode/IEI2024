import webbrowser
import os

# Define the path to the HTML file
html_file_path = 'APIs/busqueda/busqueda.html'

# Make sure the file exists
if os.path.isfile(html_file_path):
    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_file_path))
else:
    print(f"Error: The file '{html_file_path}' does not exist.")