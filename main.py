from graphics import *


def main():

    # Initializing variables
    patchwork_size = None
    patchwork_colour = None
    patchwork_colour_list = []

    # Prompt user to input patchwork size until valid input is given
    while patchwork_size not in (5, 7):
        patchwork_size = int(input("Enter the common width and height of patches (5 or 7): "))

        # Output invalid size error message
        if patchwork_size not in (5, 7):
            print("Invalid patchwork size input. Please try again. (Enter a valid patchwork size)")

    # Prompt user to input colour one at a time until 3 valid inputs are given and there is at least 2 different colours
    for i in ("first", "second", "third"):
        while patchwork_colour not in ("red", "green", "blue", "magenta", "orange", "cyan"):
            patchwork_colour = input(
                "Enter the {} colour of the patchwork (red, green, blue, magenta, orange, or cyan): ".format(i)).lower()

            # Output invalid colour error message
            if patchwork_colour not in ("red", "green", "blue", "magenta", "orange", "cyan"):
                print("Invalid patchwork colour input. Please try again. (Enter a valid colour)")

            # Output error message for inputting 3 same colours
            elif i == "third" and patchwork_colour_list[0] == patchwork_colour_list[1] \
                    and patchwork_colour == patchwork_colour_list[1]:
                print("The patchwork must be made up of at least 2 different colours. Please try again. "
                      "(Enter a different valid colour)")
                patchwork_colour = None

            # Add colour to list if valid
            else:
                patchwork_colour_list.append(patchwork_colour)
                patchwork_colour = None
                break

    # Initialize window
    win = GraphWin("My Patchwork", patchwork_size * 100, patchwork_size * 100, autoflush=False)

    # Initialize patchwork layout design and colour in the form of matrices according to antepenultimate digit
    # "F" stands for final-digit patch, " " stands for penultimate-digit patch
    if patchwork_size == 5:

        patchwork_design_matrix = [["F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F"]]

        patchwork_colour_matrix = [[1, 1, 2, 3, 3],
                                   [1, 1, 2, 3, 3],
                                   [2, 2, 2, 2, 2],
                                   [3, 3, 2, 1, 1],
                                   [3, 3, 2, 1, 1]]

    else:

        patchwork_design_matrix = [["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"],
                                   ["F", " ", "F", " ", "F", " ", "F"]]

        patchwork_colour_matrix = [[1, 1, 1, 2, 3, 3, 3],
                                   [1, 1, 1, 2, 3, 3, 3],
                                   [1, 1, 1, 2, 3, 3, 3],
                                   [2, 2, 2, 2, 2, 2, 2],
                                   [3, 3, 3, 2, 1, 1, 1],
                                   [3, 3, 3, 2, 1, 1, 1],
                                   [3, 3, 3, 2, 1, 1, 1]]

    # Draw each patch in the window using drawing functions according to the matrices above
    for row in range(patchwork_size):
        for col in range(patchwork_size):
            if patchwork_design_matrix[row][col] == "F":
                draw_final_digit_patch(win, col * 100, row * 100,
                                       patchwork_colour_list[patchwork_colour_matrix[row][col]-1])
            else:
                draw_penultimate_digit_patch(win, col * 100, row * 100,
                                             patchwork_colour_list[patchwork_colour_matrix[row][col]-1])

    # Keep the window open and provide functionality to edit the patchwork
    while win.isOpen():
        click_point = win.checkMouse()
        if click_point:

            # Initialize x and y coordinates of patch that the user clicked
            selected_x_index = int(click_point.getX() // 100)
            selected_y_index = int(click_point.getY() // 100)
            selected_x = (click_point.getX() // 100) * 100
            selected_y = (click_point.getY() // 100) * 100

            # Draw black border lines around the patch clicked
            border1 = Line(Point(selected_x-1, selected_y-1), Point(selected_x + 102, selected_y-1))
            border2 = Line(Point(selected_x-1, selected_y-1), Point(selected_x-1, selected_y + 102))
            border3 = Line(Point(selected_x + 102, selected_y-1), Point(selected_x + 102, selected_y + 102))
            border4 = Line(Point(selected_x-1, selected_y + 102), Point(selected_x + 102, selected_y + 102))
            border1.setWidth(2), border2.setWidth(2), border3.setWidth(2), border4.setWidth(2)
            border1.draw(win), border2.draw(win), border3.draw(win), border4.draw(win)

            # Set the patch to be selected
            selected = True
            while selected:
                if win.isOpen():
                    key = win.checkKey()

                # Both design and colour matrix of the patchwork will be updated after every edit
                # "x" stands for empty patch

                # Delete the patch if "d" is pressed
                if key == "d":
                    delete_patch(win, selected_x, selected_y)
                    patchwork_design_matrix[selected_y_index][selected_x_index] = "x"

                # If patch is empty and "1", "2" or "3" is pressed,
                # Create a new penultimate-digit patch of colour 1, 2 and 3, respectively
                elif key in ("1", "2", "3") \
                        and patchwork_design_matrix[selected_y_index][selected_x_index] == "x":
                    draw_penultimate_digit_patch(win, selected_x, selected_y, patchwork_colour_list[int(key)-1])
                    patchwork_design_matrix[selected_y_index][selected_x_index] = " "
                    patchwork_colour_matrix[selected_y_index][selected_x_index] = int(key)

                # If patch is empty and "4", "5" or "6" is pressed,
                # Create a new final-digit patch of colour 1, 2 and 3, respectively
                elif key in ("4", "5", "6") \
                        and patchwork_design_matrix[selected_y_index][selected_x_index] == "x":
                    draw_final_digit_patch(win, selected_x, selected_y, patchwork_colour_list[int(key)-4])
                    patchwork_design_matrix[selected_y_index][selected_x_index] = "F"
                    patchwork_colour_matrix[selected_y_index][selected_x_index] = int(key)-3

                # If patch is non-empty and the patch on the left side is empty while "Left" arrow key is pressed,
                # Move the selected patch to the empty space on the left by
                # Deleting the selected patch and creating a new patch with the same design on the left patch
                elif key == "Left" and patchwork_design_matrix[selected_y_index][selected_x_index] != "x":

                    if selected_x_index - 1 >= 0 and \
                            patchwork_design_matrix[selected_y_index][selected_x_index-1] == "x":

                        delete_patch(win, selected_x, selected_y)

                        if patchwork_design_matrix[selected_y_index][selected_x_index] == " ":
                            draw_penultimate_digit_patch(win, selected_x-100, selected_y, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index][selected_x_index-1] = " "

                        else:
                            draw_final_digit_patch(win, selected_x-100, selected_y, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index][selected_x_index-1] = "F"

                        patchwork_design_matrix[selected_y_index][selected_x_index] = "x"
                        patchwork_colour_matrix[selected_y_index][selected_x_index-1] = patchwork_colour_matrix[selected_y_index][selected_x_index]

                # If patch is non-empty and the patch on the right side is empty while "Right" arrow key is pressed,
                # Move the selected patch to the empty space on the right by
                # Deleting the selected patch and creating a new patch with the same design on the right patch
                elif key == "Right" and patchwork_design_matrix[selected_y_index][selected_x_index] != "x":

                    if selected_x_index + 1 < patchwork_size and \
                            patchwork_design_matrix[selected_y_index][selected_x_index+1] == "x":

                        delete_patch(win, selected_x, selected_y)

                        if patchwork_design_matrix[selected_y_index][selected_x_index] == " ":
                            draw_penultimate_digit_patch(win, selected_x+100, selected_y, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index][selected_x_index+1] = " "

                        else:
                            draw_final_digit_patch(win, selected_x+100, selected_y, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index][selected_x_index+1] = "F"

                        patchwork_design_matrix[selected_y_index][selected_x_index] = "x"
                        patchwork_colour_matrix[selected_y_index][selected_x_index+1] = patchwork_colour_matrix[selected_y_index][selected_x_index]

                # If patch is non-empty and the patch above it is empty while "Up" arrow key is pressed,
                # Move the selected patch to the empty space above by
                # Deleting the selected patch and creating a new patch with the same design on the patch above
                elif key == "Up" and patchwork_design_matrix[selected_y_index][selected_x_index] != "x":

                    if selected_y_index - 1 >= 0 and \
                            patchwork_design_matrix[selected_y_index-1][selected_x_index] == "x":

                        delete_patch(win, selected_x, selected_y)

                        if patchwork_design_matrix[selected_y_index][selected_x_index] == " ":
                            draw_penultimate_digit_patch(win, selected_x, selected_y-100, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index-1][selected_x_index] = " "

                        else:
                            draw_final_digit_patch(win, selected_x, selected_y-100, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index-1][selected_x_index] = "F"

                        patchwork_design_matrix[selected_y_index][selected_x_index] = "x"
                        patchwork_colour_matrix[selected_y_index-1][selected_x_index] = patchwork_colour_matrix[selected_y_index][selected_x_index]

                # If patch is non-empty and the patch below it is empty while "Down" arrow key is pressed,
                # Move the selected patch to the empty space below by
                # Deleting the selected patch and creating a new patch with the same design on the patch below
                elif key == "Down" and patchwork_design_matrix[selected_y_index][selected_x_index] != "x":

                    if selected_y_index + 1 < patchwork_size and \
                            patchwork_design_matrix[selected_y_index+1][selected_x_index] == "x":

                        delete_patch(win, selected_x, selected_y)

                        if patchwork_design_matrix[selected_y_index][selected_x_index] == " ":
                            draw_penultimate_digit_patch(win, selected_x, selected_y+100, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index+1][selected_x_index] = " "
                        else:
                            draw_final_digit_patch(win, selected_x, selected_y+100, patchwork_colour_list[patchwork_colour_matrix[selected_y_index][selected_x_index]-1])
                            patchwork_design_matrix[selected_y_index+1][selected_x_index] = "F"

                        patchwork_design_matrix[selected_y_index][selected_x_index] = "x"
                        patchwork_colour_matrix[selected_y_index+1][selected_x_index] = patchwork_colour_matrix[selected_y_index][selected_x_index]

                # Deselect the patch and remove border if "Esc" key is pressed
                elif key == "Escape":
                    border1.undraw(), border2.undraw(), border3.undraw(), border4.undraw()
                    selected = False


# Drawing function of the penultimate-digit patch
def draw_penultimate_digit_patch(win, x, y, color):
    # Decide the starting point and pattern of each grid in the box using mod and common difference
    for row in range(1, 6):
        row_diff = (row - 1) // 2 * 40
        if row % 2 == 1:

            for col in range(1, 6):
                col_diff = (col - 1) // 2 * 40

                if col % 2 == 1:
                    # Draw an arc of the circle by using a white triangle to cover 1/4 portion of the circle
                    c = Circle(Point(x + 10 + col_diff, y + row_diff + 10), 10)
                    t = Polygon(Point(x + 10 + col_diff, y + row_diff + 10), Point(x + 20 + col_diff, y + row_diff),
                                Point(x + 20 + col_diff, y + row_diff + 20))
                    c.setFill(color)
                    c.setOutline("white")
                    c.draw(win)
                    t.setFill("white")
                    t.setOutline("white")
                    t.draw(win)

                else:
                    # Draw a square
                    r = Rectangle(Point(x + 20 + col_diff, y + row_diff), Point(x + 40 + col_diff, y + 20 + row_diff))
                    r.setFill(color)
                    r.setOutline("white")
                    r.draw(win)

        else:

            for col in range(1, 6):
                col_diff = (col - 1) // 2 * 40

                if col % 2 == 1:
                    # Draw a square
                    r = Rectangle(Point(x + col_diff, y + 20 + row_diff), Point(x + 20 + col_diff, y + 40 + row_diff))
                    r.setFill(color)
                    r.setOutline("white")
                    r.draw(win)

                else:
                    # Draw a circle and a triangle in the same way as above except flipping the triangle to other side
                    c = Circle(Point(x + 30 + col_diff, y + 30 + row_diff), 10)
                    t = Polygon(Point(x + 30 + col_diff, y + 30 + row_diff), Point(x + 20 + col_diff, y + 20 + row_diff)
                                , Point(x + 20 + col_diff, y + 40 + row_diff))
                    c.setFill(color)
                    c.setOutline("white")
                    c.draw(win)
                    t.setFill("white")
                    t.setOutline("white")
                    t.draw(win)


# Drawing function of the final-digit patch
def draw_final_digit_patch(win, x, y, color):
    # Draw lines with starting points from the very top and bottom of the box and end at the center
    for starting_point in range(11):
        l1 = Line(Point(x + starting_point * 10, y), Point(x + 50, y + 50))
        l2 = Line(Point(x + starting_point * 10, y + 100), Point(x + 50, y + 50))
        l1.setFill(color)
        l1.draw(win)
        l2.setFill(color)
        l2.draw(win)

    # Draw lines with starting points from the very left and right side of the box and end at the center
    for starting_point in range(11):
        l1 = Line(Point(x, y + starting_point * 10), Point(x + 50, y + 50))
        l2 = Line(Point(x + 100, y + starting_point * 10), Point(x + 50, y + 50))
        l1.setFill(color)
        l1.draw(win)
        l2.setFill(color)
        l2.draw(win)


# Deleting patch function
def delete_patch(win, x, y):
    # Check for each object in the window
    for item in win.items[:]:
        # If object is a polygon with a point that lies in the patch, then undraw the object
        if isinstance(item, Polygon):
            if x <= item.getPoints()[0].getX() <= x + 100 and \
                    y <= item.getPoints()[0].getY() <= y + 100:
                item.undraw()
                win.update()

        # If center point of object lies in the patch, then undraw the object
        else:
            if x <= item.getCenter().getX() <= x + 100 and \
                    y <= item.getCenter().getY() <= y + 100:
                item.undraw()
                win.update()


# Call the main function to run the program
main()
