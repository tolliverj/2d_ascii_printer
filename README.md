# 2d_ascii_printer
This is a script to take a URL containing a HTML table of x-coordinates, characters, and y-coordinates to display a 2D matrix of ASCII characters which gets printed into the console..

I have a call from the main execution block to print_ascii_from_url() which 
#       calls get_html_table_from_url() and parse_table_return_grid_chars() and then the
#       rest of the code executes to print the ASCII characters all within
#       print_ascii_from_url(). I have some error checking that makes sure the table
#       headers are present in the HTML table at the URL, some try blocks, and to make sure
#       the coordinate table cells are numbers. I also have some error checking to make
#       sure there not multiple coordinates for the same coordinates and any missing I add
#       a space character to fill in the gaps.
