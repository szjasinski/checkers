import tkinter as tk


class Checkers(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        my_frame = tk.Frame(parent)

        # holds coords and a corresponding instances of buttons
        COORDS_BUTTON_DICT = {}

        # holds coords and a corresponding list, which contains color and type of figure (zeros if there isn't any figure)
        COORDS_FIGURE_DICT = {}  # ie {(0,0): ["white", "queen"], (1,1): ["red", "pawn"], (2,2): ["0", "0"]}

        # generated for a specified coords. holds coords of possible moves and corresponding coords of beaten figure
        # (if this move implies beating) or 0 (if no beating)
        MOVES_BEATING_DICT = {}  # ie {(3, 2): 0, (4, 5): (3, 4)}

        OLD_COORDS = (0, 0)  # generated when clicking a figure. holds coords of a figure to move
        IS_CLICKED = False

        white_pawn_image = tk.PhotoImage(file="img/white_pawn_1.png")
        red_pawn_image = tk.PhotoImage(file="img/red_pawn_1.png")
        white_queen_image = tk.PhotoImage(file="img/white_queen_1.png")
        red_queen_image = tk.PhotoImage(file="img/red_queen_1.png")
        white_bg = tk.PhotoImage(file="img/white_bg.png")
        grey_bg = tk.PhotoImage(file="img/grey_bg.png")

        white_pawn_highlighted_image = tk.PhotoImage(file="img/white_pawn_highlighted_1.png")
        red_pawn_highlighted_image = tk.PhotoImage(file="img/red_pawn_highlighted_1.png")
        white_queen_highlighted_image = tk.PhotoImage(file="img/white_queen_highlighted_1.png")
        red_queen_highlighted_image = tk.PhotoImage(file="img/red_queen_highlighted_1.png")
        highlighted_bg = tk.PhotoImage(file="img/highlighted_bg.png")

        def highlight_img(coords):
            if IS_CLICKED:
                if COORDS_FIGURE_DICT[coords] == ["white", "pawn"]:
                    COORDS_BUTTON_DICT[coords].config(image=white_pawn_highlighted_image)
                if COORDS_FIGURE_DICT[coords] == ["red", "pawn"]:
                    COORDS_BUTTON_DICT[coords].config(image=red_pawn_highlighted_image)
                if COORDS_FIGURE_DICT[coords] == ["white", "queen"]:
                    COORDS_BUTTON_DICT[coords].config(image=white_queen_highlighted_image)
                if COORDS_FIGURE_DICT[coords] == ["red", "queen"]:
                    COORDS_BUTTON_DICT[coords].config(image=red_queen_highlighted_image)
                for element in MOVES_BEATING_DICT:
                    COORDS_BUTTON_DICT[element].config(image=highlighted_bg)
            else:
                if COORDS_FIGURE_DICT[coords] == ["white", "pawn"]:
                    COORDS_BUTTON_DICT[coords].config(image=white_pawn_image)
                if COORDS_FIGURE_DICT[coords] == ["red", "pawn"]:
                    COORDS_BUTTON_DICT[coords].config(image=red_pawn_image)
                if COORDS_FIGURE_DICT[coords] == ["white", "queen"]:
                    COORDS_BUTTON_DICT[coords].config(image=white_queen_image)
                if COORDS_FIGURE_DICT[coords] == ["red", "queen"]:
                    COORDS_BUTTON_DICT[coords].config(image=red_queen_image)
                for element in MOVES_BEATING_DICT:
                    if COORDS_FIGURE_DICT[element][0] == "0":
                        COORDS_BUTTON_DICT[element].config(image=grey_bg)

        # returns list of coords
        def get_left_top_diagonal(coords):
            diagonal_coords_list = []

            (x, y) = coords
            while x >= 0 and y >= 0:
                if (x, y) != coords:
                    diagonal_coords_list.append((x, y))
                x = x - 1
                y = y - 1

            return diagonal_coords_list

        def get_right_top_diagonal(coords):
            diagonal_coords_list = []

            (x, y) = coords
            while x >= 0 and y <= 7:
                if (x, y) != coords:
                    diagonal_coords_list.append((x, y))
                x = x - 1
                y = y + 1

            return diagonal_coords_list

        def get_right_bottom_diagonal(coords):
            diagonal_coords_list = []

            (x, y) = coords
            while x <= 7 and y <= 7:
                if (x, y) != coords:
                    diagonal_coords_list.append((x, y))
                x = x + 1
                y = y + 1

            return diagonal_coords_list

        def get_left_bottom_diagonal(coords):
            diagonal_coords_list = []

            (x, y) = coords
            while x <= 7 and y >= 0:
                if (x, y) != coords:
                    diagonal_coords_list.append((x, y))
                x = x + 1
                y = y - 1

            return diagonal_coords_list

        def get_queen_moves(my_list, coords):
            # checking for a move without beating
            for square_to_move_to in my_list:
                if COORDS_FIGURE_DICT[square_to_move_to][0] == "0":
                    counter = 0
                    x = 0
                    while x < my_list.index(square_to_move_to):
                        if COORDS_FIGURE_DICT[my_list[x]][0] != "0":
                            counter += 1
                        x += 1
                    if counter == 0:
                        MOVES_BEATING_DICT[square_to_move_to] = 0

            # checking for a move with beating
            for enemy in my_list:
                if COORDS_FIGURE_DICT[enemy][0] != COORDS_FIGURE_DICT[coords][0] \
                        and COORDS_FIGURE_DICT[enemy][1] != "0":
                    for square_to_move_to in my_list:
                        if my_list.index(square_to_move_to) > my_list.index(enemy) and \
                                COORDS_FIGURE_DICT[square_to_move_to][0] == "0":
                            counter = 0
                            x = 0
                            while x < my_list.index(square_to_move_to):
                                if COORDS_FIGURE_DICT[my_list[x]][0] != "0":
                                    counter += 1
                                x += 1
                            if counter == 1:
                                MOVES_BEATING_DICT[square_to_move_to] = enemy

        def get_pawn_moves(my_list, coords):
            # checking for a move without beating
            if len(my_list) >= 1:
                if COORDS_FIGURE_DICT[my_list[0]][0] == "0":
                    MOVES_BEATING_DICT[my_list[0]] = 0

            # checking for a move with beating
            if len(my_list) >= 2:
                if COORDS_FIGURE_DICT[my_list[0]][0] == "white" and COORDS_FIGURE_DICT[coords][0] == "red":
                    if COORDS_FIGURE_DICT[my_list[1]][0] == "0":
                        MOVES_BEATING_DICT[my_list[1]] = my_list[0]
                elif COORDS_FIGURE_DICT[my_list[0]][0] == "red" and COORDS_FIGURE_DICT[coords][0] == "white":
                    if COORDS_FIGURE_DICT[my_list[1]][0] == "0":
                        MOVES_BEATING_DICT[my_list[1]] = my_list[0]

        def get_possible_moves_dict(coords):
            nonlocal MOVES_BEATING_DICT

            MOVES_BEATING_DICT.clear()

            if COORDS_FIGURE_DICT[coords][1] == "pawn":
                if COORDS_FIGURE_DICT[coords][0] == "white":
                    get_pawn_moves(get_right_bottom_diagonal(coords), coords)
                    get_pawn_moves(get_left_bottom_diagonal(coords), coords)
                elif COORDS_FIGURE_DICT[coords][0] == "red":
                    get_pawn_moves(get_right_top_diagonal(coords), coords)
                    get_pawn_moves(get_left_top_diagonal(coords), coords)

            elif COORDS_FIGURE_DICT[coords][1] == "queen":
                get_queen_moves(get_left_top_diagonal(coords), coords)
                get_queen_moves(get_right_top_diagonal(coords), coords)
                get_queen_moves(get_right_bottom_diagonal(coords), coords)
                get_queen_moves(get_left_bottom_diagonal(coords), coords)

        def move_figure(new_coords):
            if new_coords in MOVES_BEATING_DICT:
                if new_coords[0] == 0 or new_coords[0] == 7:
                    COORDS_FIGURE_DICT[new_coords][0] = COORDS_FIGURE_DICT[OLD_COORDS][0]
                    COORDS_FIGURE_DICT[new_coords][1] = "queen"
                    COORDS_FIGURE_DICT[OLD_COORDS] = ["0", "0"]

                else:
                    COORDS_FIGURE_DICT[new_coords] = COORDS_FIGURE_DICT[OLD_COORDS]
                    COORDS_FIGURE_DICT[OLD_COORDS] = ["0", "0"]

                image_names_dict = {tuple(["white", "pawn"]): white_pawn_image,
                                    tuple(["white", "queen"]): white_queen_image,
                                    tuple(["red", "pawn"]): red_pawn_image, tuple(["red", "queen"]): red_queen_image}
                img = image_names_dict[tuple(COORDS_FIGURE_DICT[new_coords])]

                COORDS_BUTTON_DICT[new_coords].config(image=img)
                COORDS_BUTTON_DICT[OLD_COORDS].config(image=grey_bg)

                # checking if there was a beating and removing the beaten figure
                if MOVES_BEATING_DICT[new_coords] != 0:
                    pawn_coords_to_delete = MOVES_BEATING_DICT[new_coords]
                    COORDS_FIGURE_DICT[pawn_coords_to_delete] = ["0", "0"]
                    COORDS_BUTTON_DICT[pawn_coords_to_delete].config(image=grey_bg)

        def my_click(x, y):
            nonlocal IS_CLICKED
            nonlocal OLD_COORDS

            if IS_CLICKED:
                new_coords = (x, y)
                move_figure(new_coords)
                IS_CLICKED = False
                highlight_img(OLD_COORDS)

            else:
                OLD_COORDS = (x, y)
                get_possible_moves_dict(OLD_COORDS)
                if COORDS_FIGURE_DICT[OLD_COORDS][0] != "0":  # if there is a figure at this coords
                    IS_CLICKED = True
                    highlight_img(OLD_COORDS)

        def construct_buttons():
            grid_count = 0
            for x in range(0, 8):
                for y in range(0, 8):
                    btn = tk.Button(my_frame, image=white_bg,
                                    command=lambda row_n=x, column_n=y: my_click(row_n, column_n))
                    COORDS_BUTTON_DICT[(x, y)] = btn
                    COORDS_BUTTON_DICT[(x, y)].grid(row=x, column=y)
                    grid_count += 1

            for coords in COORDS_BUTTON_DICT:
                if (coords[0] + coords[1]) % 2 == 1:
                    COORDS_BUTTON_DICT[coords].config(image=grey_bg)

        def construct_figures():
            nonlocal COORDS_FIGURE_DICT

            COORDS_FIGURE_DICT = COORDS_BUTTON_DICT.copy()

            for coords in COORDS_FIGURE_DICT:
                if coords[0] in [0, 2] and coords[1] % 2 == 1:
                    COORDS_FIGURE_DICT[coords] = ["white", "pawn"]
                elif coords[0] == 1 and coords[1] % 2 == 0:
                    COORDS_FIGURE_DICT[coords] = ["white", "pawn"]
                elif coords[0] in [5, 7] and coords[1] % 2 == 0:
                    COORDS_FIGURE_DICT[coords] = ["red", "pawn"]
                elif coords[0] == 6 and coords[1] % 2 == 1:
                    COORDS_FIGURE_DICT[coords] = ["red", "pawn"]
                else:
                    COORDS_FIGURE_DICT[coords] = ["0", "0"]

            for coords in COORDS_FIGURE_DICT:
                if COORDS_FIGURE_DICT[coords][0] == "white":
                    COORDS_BUTTON_DICT[coords].config(image=white_pawn_image)
                elif COORDS_FIGURE_DICT[coords][0] == "red":
                    COORDS_BUTTON_DICT[coords].config(image=red_pawn_image)

        construct_buttons()
        construct_figures()
        my_frame.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('CHECKERS')
    Checkers(root).pack()
    root.mainloop()
