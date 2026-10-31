import re
from urllib.request import urlopen

# -----------------------------------------------------------------------------------------/
#                                                                          Date: 10/30/2026
# Author: Jameson Tolliver
# About:  This is a script to take a URL containing a HTML table of x-coordinates,
#         characters, and y-coordinates to display a 2D matrix of ASCII characters
#         which gets printed into the console.
#
# HTML TABLE MAP:
# +-------+-----------+-------+------------------------------------------------------------+
# | X-POS | CHARACTER | Y-POS |                                                            #
# +-------+-----------+-------+------------------------------------------------------------+
# |   0   |     █     |   2   |                                                            #
# |   0   |     ▀     |   1   |                                                            #
# -----------------------------------------------------------------------------------------/

# -----------------------------------------------------------------------------------------/
# Description:
#
#       I have a call from the main execution block to print_ascii_from_url() which 
#       calls get_html_table_from_url() and parse_table_return_grid_chars() and then the
#       rest of the code executes to print the ASCII characters all within
#       print_ascii_from_url(). I have some error checking that makes sure the table
#       headers are present in the HTML table at the URL, some try blocks, and to make sure
#       the coordinate table cells are numbers. I also have some error checking to make
#       sure there not multiple coordinates for the same coordinates and any missing I add
#       a space character to fill in the gaps.
#
# -----------------------------------------------------------------------------------------/

# -------------------------------------------------------------/
# FUNCTION: Get the HTML from a url, return a HTML string
# -------------------------------------------------------------/

def get_html_table_from_url(url):

        try:
                # INITIALIZATIONS / DECLARATIONS --------------/
                html_str = "" # To store HTTP response as HTML
                table_start_position = 0 # The start and the end position of the table
                table_end_position = 0 # The start and the end position of the table

                # Context manager used to retrieve the above table URL
                with urlopen(url) as response:

                        # Read the HTTP response and store it as a string
                        html_str = response.read().decode("utf-8")

                # Find the start and the end position of the table
                table_start_position = html_str.find("<table")
                table_end_position = html_str.find("</table>")

                # If the HTML string doesn't contain the opening and closing <table> tags, and the required matching headers: throw an exception
                if (table_start_position == -1 or 
                        table_end_position == -1 or
                        html_str.find('x-coordinate') == -1 or 
                        html_str.find('y-coordinate') == -1 or 
                        html_str.find('Character') == -1):
                        raise Exception("An error occurred while fetching the URL or no table element was found in the html.")

                # Extract table element from the HTML
                html_str = html_str[table_start_position:table_end_position + len("</table>")]

                # Return HTML table
                return html_str

        # If any exceptions are raised during the whole execution of this try block, catch them and print the error message.
        except Exception as e:
                print("Error message:", str(e))

# -----------------------------------------------------------------------------------/
# FUNCTION: Takes a table element and returns an array of coordinates
#           and characters: [{x: 0, y: 0, char:' '}{...}]
# -----------------------------------------------------------------------------------/

def parse_table_return_grid_chars (html_str):

        try:
                # INITIALIZATIONS / DECLARATIONS --------------/
                highest_x_item = 0 # Store the number x items
                highest_y_item = 0 # Store the number y items
                table_contents = "" # Holds the table contents on separate lines
                table_cells = [] # Array to hold the 
                grid_chars = [] # An array to hold the grid characters in: [{x: 0, y: 0, char:' '}{...}]
                check_set = set() # A set to check / keep track of the grid coordinates: {(0,0), (0,1), ...}

                # Place all tags on a new line and strip the tags, leaving only the data behind 
                table_contents = re.sub(r"<[^>]+>", "", html_str.replace("><", ">\n<"))

                # Split the remaining lines into an array, removing empty lines
                table_cells = [line.strip() for line in table_contents.splitlines() if line.strip()]

                # Remove the header array items
                table_cells.remove("x-coordinate")
                table_cells.remove("Character")
                table_cells.remove("y-coordinate")

                # Loop through the cleaned contents array
                for td_num in range(0, len(table_cells), 3):

                        # If the data in the table cells cells 0 and 2 are digits and the pair is not in the check_set 
                        if (table_cells[td_num].isdigit() and 
                                table_cells[td_num + 2].isdigit() and 
                                (int(table_cells[td_num]), int(table_cells[td_num + 2])) not in check_set):

                                # Add the pair to the set
                                check_set.add((int(table_cells[td_num]), int(table_cells[td_num + 2])))
                        else:
                                raise Exception("Invalid coordinates found in the html: duplicates.")

                        # add the set of the 3 to the array: [{x: 0, y: 0, char:' '}{...}]
                        grid_chars.append({"x": int(table_cells[td_num]), "y": int(table_cells[td_num + 2]), "char": table_cells[td_num + 1]})

                # Store the highest values of each axis: x and y
                highest_x_item = max(item['x'] for item in grid_chars)
                highest_y_item = max(item['y'] for item in grid_chars)

                # Fill in missing items in the grid with empty characters
                # Loop through all possible (x, y) coordinates within the bounds of the grid (which is the max x and y values found in the grid)
                for x in range(highest_x_item + 1):
                        for y in range(highest_y_item + 1):

                                # Check if the (x, y) coordinate is not already in the check_set
                                if (x, y) not in check_set:

                                        # Create a new item and append it to the grid.
                                        missing_item = {"x": x, "y": y, "char": " "}
                                        grid_chars.append(missing_item)

                # Sort the grid by y coordinates descending then x coordinates
                grid_chars.sort(key=lambda item: (-int(item['y']), int(item['x'])))

                return grid_chars

        # If any exceptions are raised during the whole execution of this try block, catch them and print the error message.
        except Exception as e:
                print("Error message:", str(e))

# -----------------------------------------------------------------------------------------------------/
# FUNCTION: Takes a URL containing a HTML table of characters and coordinates to create ASCII graphics
# -----------------------------------------------------------------------------------------------------/

def print_ascii_from_url(url):

        try:
                # Get the HTML table string from a URL
                table_str = get_html_table_from_url(url)

                # Parse the HTML table and return all the necessary coordinates and characters: [{x: 0, y: 0, char:' '}{...}]
                char_grid = parse_table_return_grid_chars(table_str)

                # For use in the for loop, being the largest coordinate value of the grid
                highest_x_item = max(item['x'] for item in char_grid)
                highest_y_item = max(item['y'] for item in char_grid)

                # Print the grid in a human-readable format from (highest y, lowest x) to (lowest y, highest x)
                for y in reversed(range(highest_y_item + 1)):

                        #  To store the character to be displayed
                        row = ""

                        # Loop through from the left, which starts at 0 and goes to the highest x coordinate value found in the grid per y
                        for x in range(highest_x_item + 1):

                                # Find the item in the grid with the current (x, y) coordinates
                                item = next((item for item in char_grid if item['x'] == x and item['y'] == y), None)
                                if item:
                                        row += item['char']

                        # Print the entire row and move to the next one
                        print(row)

        # If any exceptions are raised during the whole execution of this try block, catch them and print the error message.
        except Exception as e:
                print("Error message:", str(e))

# -----------------------------------------------------------------------------------------------------/
#                                       MAIN EXECUTION BLOCK
# -----------------------------------------------------------------------------------------------------/

# Print an ASCII map from the URL into the console
print_ascii_from_url("http://jamesont.com/ascii_table_example.htm")




