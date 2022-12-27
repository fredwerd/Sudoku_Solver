if __name__ == "__main__":

    # check speeds of differing orders. Maybe set a check to determine puzzle difficulty by how many given values there are
    # and change the order depending. Should always finish with brute force

    import numpy as np
    import copy
    import tkinter as tk
    import time

    # initializes empty lists to store GUI inputs and print solution to GUI outside solve function
    all_given = []
    solution = []



    def Solve():
        start_time = time.process_time()
        temp_unsolved = np.zeros([9, 9], dtype=int)
        entry_list = ''
        # retrieves values from the input boxes in a list while checking for input errors
        for entries in all_given:
            entry_list = entry_list + entries.get()
            try:
                int(entry_list[-1])
            except:
                print(entry_list[-1], "is not a valid input")
                return
            if int(entries.get()) > 9:
                print(entries.get(), "is not a valid input")
                return

        # converts input list: all_given into the temp_unsolved array
        for row in range(9):
            for column in range(9):
                temp_unsolved[row, column] = int(entry_list[row * 9 + column])

    # rename utemp_unsolved to temp_unsolved to override input values during testing
        utemp_unsolved = np.array([[9, 0, 0, 0, 6, 0, 0, 0, 3],
                                  [0, 8, 0, 4, 0, 7, 0, 9, 0],
                                  [0, 0, 2, 0, 5, 0, 6, 0, 0],
                                  [0, 4, 0, 0, 0, 0, 0, 1, 0],
                                  [5, 0, 1, 0, 0, 0, 9, 0, 7],
                                  [0, 9, 0, 0, 0, 0, 0, 5, 0],
                                  [0, 0, 8, 0, 7, 0, 5, 0, 0],
                                  [0, 7, 0, 8, 0, 5, 0, 2, 0],
                                  [3, 0, 0, 0, 4, 0, 0, 0, 9]])

        # STEP 1: check for input errors
        for row_error in range(9):
            for column_error in range(9):
                if temp_unsolved[row_error, column_error] == 0:
                    continue
                    # this long thing is counting how many there are of the current index of temp_unsolved in each
                    # row, and column
                elif temp_unsolved[row_error].tolist().count(temp_unsolved[row_error, column_error]) > 1 \
                        or temp_unsolved[:, column_error].tolist().count(
                    temp_unsolved[row_error, column_error]) > 1:
                    # still needs box
                    print("input error: conflict(s) with box at row", row_error, "column", column_error)
                    return

        # STEP 2: create p solution array pseudo_full
        # creates pseudo_full as an 81x9 array correlating p solutions to solution boxes
        # sudoku box location is found by the equation: pseudo_full row = sudoku row * 9 + sudoku column /
        # with rows and columns for either array beginning at 0 compatible with loop indexes
        pseudo_ind = np.arange(1, 10)
        pseudo_full = np.array([pseudo_ind] * 81)

        # STEP 3.1: empty values from pseudo_full according to input values
        for row in range(9):
            for column in range(9):
                if temp_unsolved[row, column] > 0:
                    # column: start at the current column in unsolved (c) and run down equivalent row in pseudo (c2*9+c)
                    for column_clear in range(9):
                        pseudo_full[column_clear * 9 + column, temp_unsolved[row, column] - 1] = 0
                    # row: start at first column of current row (r) and run through the row in pseudo
                    for row_clear in range(9):
                        pseudo_full[row * 9 + row_clear, temp_unsolved[row, column] - 1] = 0
                    # box: check if row and column is the first second or third in smaller 3x3 box
                    # reset loop index to the first slot in the smaller box
                    if column % 3 == 0:
                        first_column = column
                    elif (column - 1) % 3 == 0:
                        first_column = column - 1
                    else:
                        first_column = column - 2
                    if row % 3 == 0:
                        first_row = row
                    elif (row - 1) % 3 == 0:
                        first_row = row - 1
                    else:
                        first_row = row - 2
                    for box_row in range(first_row, first_row + 3):
                        for box_column in range(first_column, first_column + 3):
                            # clear the small box pseudo values
                            pseudo_full[box_row * 9 + box_column, temp_unsolved[row, column] - 1] = 0
                    # current value from given values was erased, so set it back in the pseudo values
                    pseudo_full[row * 9 + column, temp_unsolved[row, column] - 1] = temp_unsolved[row, column]

        # STEP 3.2: save any solutions found into temp_unsolved
        # counts the number of zeros in each row of pseudo_full
        # 8 zeros means a solution was found, so it is saved in temp_unsolved
        for row in range(9):
            for column in range(9):
                if pseudo_full[row * 9 + column].tolist().count(0) == 8:
                    temp_unsolved[row, column] = sum(pseudo_full[row * 9 + column])

        # STEP 4: Only choice: search arrays for boxes that can be solved due to all other options ruled out
        temp_p = np.zeros([9, 9])  # dtype int potentially
        temp_box = np.zeros([1, 9])
        # check temp_unsolved for all the potential boxes 'p' fits in
        for p in range(1, 10):
            for row in range(9):
                for column in range(9):
                    if (temp_unsolved[row, column] == 0 and p in pseudo_full[row * 9 + column]) \
                            or temp_unsolved[row, column] == p:
                        # store the potential value in a temp p, which contains all potential p spots
                        temp_p[row, column] = p
            # run through temp_unsolved again, checking for solutions that are the only choice
            for r2 in range(9):
                for c2 in range(9):
                    if temp_unsolved[r2, c2] == 0:
                        # box finder
                        if c2 % 3 == 0:
                            c3 = c2
                        elif (c2 - 1) % 3 == 0:
                            c3 = c2 - 1
                        else:
                            c3 = c2 - 2
                        if r2 % 3 == 0:
                            r3 = r2
                        elif (r2 - 1) % 3 == 0:
                            r3 = r2 - 1
                        else:
                            r3 = r2 - 2
                        box = 0
                        # fills temp_box with the potential values from temp_p of current 3x3 box
                        for r4 in range(r3, r3 + 3):
                            for c4 in range(c3, c3 + 3):
                                temp_box[0, box] = temp_p[r4, c4]
                                box += 1
                        # if current row has one possible location for the potential value p, save as a solution
                        if sum(temp_p[r2]) == p and p in pseudo_full[r2 * 9 + c2]:
                            temp_unsolved[r2, c2] = p
                        # if current column has one possible location for the potential value p, save as a solution
                        elif sum(temp_p[:, c2]) == p and p in pseudo_full[r2 * 9 + c2]:
                            temp_unsolved[r2, c2] = p
                        # if current box(temp_box) has one possible location for the potential value p, save as solution
                        elif sum(temp_box[0]) == p and p in pseudo_full[r2 * 9 + c2]:
                            temp_unsolved[r2, c2] = p
                # reset the potential values array and check the puzzle for the next number
                temp_p = np.zeros([9, 9])

        # STEP 5: brute force solve
        # bug checking: the first row has no solutions, stop solving here. Shouldn't happen after input conflict check
        if sum(pseudo_full[0]) == 0:
            print('No solutions, please recheck input')
            return

        # brute_pseudo is saved from current possible values
        # will be edited and restored over iterations of bulk solving, copy.deepcopy prevents pseudo_full from changing
        brute_pseudo = copy.deepcopy(pseudo_full)
        # previous_index is an array of row and column values of previously edited index for backtracking
        previous_index = np.zeros([81, 3], dtype=int)
        saved_row = 0
        saved_column = 0
        saved_pseudo = 0
        only = 0
        r = 0
        c = 0
        c2 = 0
        r2 = 0
        br = 0
        bc = 0
        backtrack = False
        conflict = False
        while 0 in temp_unsolved:
            #if r * 9 + c == 16:
                #break
            while r < 9:
                #if r * 9 + c == 16:
                    #break
                while c < 10:
                    #if r * 9 + c == 16:
                        #break
                    #print('current index', r * 9 + c)
                    if c == 9:
                        c = 0
                        r += 1
                    if r == 9:
                        c = 10
                        break
                    # adds previous changed index values only if brute force is trying values and not returning from a conflict
                    if r * 9 + c < 80 and not backtrack:
                        previous_index[r * 9 + c] = [saved_row, saved_column, saved_pseudo]
                    if temp_unsolved[r, c] == 0:
                        backtrack = False
                        only = 0
                        print('unsolved(0) box at', r * 9 + c)
                        while only < 10:
                            print('trying', only + 1)
                            if only == 9:
                                print('yes')
                                if r * 9 + c == 0:
                                    print('error')
                                    only = 99
                                    c = 99
                                    r = 99
                                    del temp_unsolved
                                    break
                                # prevents saving over previous index values if you are backtracking
                                backtrack = True
                                # reset current brute pseudos to p values
                                print('no p value, clearing previous, restarting')
                                brute_pseudo[r * 9 + c] = pseudo_full[r * 9 + c]
                                # use the current space's previous index value
                                # delete the brute pseudo used at previous index value
                                print('previous index to use', previous_index[r * 9 + c, 0], previous_index[r * 9 + c, 1], previous_index[r * 9 + c, 2])
                                brute_pseudo[(9 * previous_index[r * 9 + c, 0]) + previous_index[r * 9 + c, 1], previous_index[r * 9 + c, 2]] = 0
                                # BEFORE THIS LINE, PSEUDO FULL REMAINS, r = 3, c = 7,saved = 3, 7, 2
                                # undo the last change so the while loop after starting at 0 finds that 0 first
                                temp_unsolved[previous_index[r * 9 + c, 0], previous_index[r * 9 + c, 1]] = 0
                                # AFTER THIS LINE, PSEUDO FULL HAS CHANGED
                                # reset current previous index back to 0
                                previous_index[9 * r + c] = [0, 0, 0]
                                # reset saved values to the last index values
                                # they will get stored before r
                                # this allows successive backtracks
                                saved_row = previous_index[9*r+c-1, 0]
                                saved_column = previous_index[9*r+c-1, 1]
                                saved_pseudo = previous_index[9*r+c-1, 2]
                                # restart the indexing at the beginning
                                c = 0
                                r = 0
                                only = 0
                                break
                            if brute_pseudo[r * 9 + c, only] != 0:
                                # check validity
                                c2 = 0
                                r2 = 0
                                br = 0
                                bc = 0
                                # check row
                                while c2 <= c:
                                    # if conflict:
                                    if temp_unsolved[r, c2] == brute_pseudo[r * 9 + c, only]:
                                        # set current pseudo to 0 for now
                                        # this line below is clearing a value in pseudo full? in each conflict check
                                        brute_pseudo[r * 9 + c, only] = 0
                                        # try the next p value in pseudo
                                        only += 1
                                        # don't check the rows
                                        r2 = 10
                                        # don't check box
                                        br = 10
                                        bc = 10
                                        conflict = True
                                        # stop checking for conflicts
                                        break
                                    else:
                                        c2 += 1
                                # check column
                                while r2 <= r:
                                    if temp_unsolved[r2, c] == brute_pseudo[r * 9 + c, only]:
                                        # set current pseudo to 0 for now
                                        brute_pseudo[r * 9 + c, only] = 0
                                        # try the next p value in pseudo
                                        only += 1
                                        # don't check box
                                        br = 10
                                        bc = 10
                                        conflict = True
                                        # stop checking for conflicts
                                        break
                                    else:
                                        r2 += 1
                                # check box
                                # box finder
                                if c % 3 == 0:
                                    c3 = c
                                elif (c - 1) % 3 == 0:
                                    c3 = c - 1
                                else:
                                    c3 = c - 2
                                if r % 3 == 0:
                                    r3 = r
                                elif (r - 1) % 3 == 0:
                                    r3 = r - 1
                                else:
                                    r3 = r - 2
                                # starting at the top left of the current box
                                # check the 3 values in the row, have to check all 3 regardless of current column
                                # move to the next row
                                # don't check the next row, because there will be nothing to check
                                print(only)
                                while br <= 2:
                                    print('row', only)
                                    if conflict:
                                        break
                                    while bc <= 2:
                                        print('column', only)
                                        if temp_unsolved[r3+br, c3+bc] == brute_pseudo[r * 9 + c, only]:
                                            print(only)
                                            # set current pseudo to 0 for now
                                            brute_pseudo[r * 9 + c, only] = 0
                                            # try the next p value in pseudo
                                            only += 1
                                            conflict = True
                                            # stop checking for conflicts
                                            break
                                        else:
                                            bc += 1
                                    if bc == 3:
                                        bc = 0
                                        br += 1
                                print('checking for conflicts')
                                # after the checks, you can save this value into temp_unsolved and retain index values
                                if not conflict:
                                    print('no conflict, placing', only + 1, 'in', r * 9 + c, '...')
                                    temp_unsolved[r, c] = brute_pseudo[r * 9 + c, only]
                                    saved_row = r
                                    saved_column = c
                                    saved_pseudo = only
                                    only = 0
                                    # try next box in row
                                    c += 1
                                    backtrack = False
                                    break  # stops while loop that checks current temp_unsolved box for pseudo values,
                                    # you've already input a potentially accurate value so stop trying more
                                else:
                                    print('conflict, trying:', only + 1, '...')
                                    print(only)
                                    conflict = False
                            else:
                                # brute pseudo has ruled out current "only" as an option
                                only += 1
                    else:
                        # move on if temp unsolved has a solved value
                        c += 1

        # add a while loop to the brute force that stops after a certain number of iterations. like an error check
        # add while loops before brute force to apply new several times before trying brute force

        print(temp_unsolved)
        # stores answer in solution as a list
        for row in range(9):
            for column in range(9):
                solution.insert(row * 9 + column, temp_unsolved[row, column])

        # fills entry boxes with solution
        # actually recreates the entry boxes in the same position with the solution values
        for row in range(9):
            for column in range(9):
                given = tk.Entry(root, justify="center", width=3)
                given.insert(-1, temp_unsolved[row, column])
                given.grid(row=row + 3, column=column + 8)
        end_time = time.process_time()
        print(end_time - start_time, "seconds to run 'solve'")

    # resets input boxes
    def Reset():
        for row in range(9):
            for column in range(9):
                given = tk.Entry(root, justify="center", width=3)
                given.insert(-1, 0)  # fills box with a zero at -1 index? It works, but so does changing the number
                given.grid(row=row + 3, column=column + 8)  # spacial position of box
                all_given.append(given)  # adds the entry box input to the end of the array "all_given"

        # create a loop for the second step hidden pairs
        # check for hidden pairs and delete values
        # if nothing is deleted, stop this check and then...
        # repeat whatever line checks for spots that can only be one number

        # create another loop for pointing pairs
        # check for pointing pairs
        # remove values from temp array in the same row
        # column
        # or smaller gridbox
        # if nothing is deleted stop and check
        # add permanent numbers

        # create a loop for swordfish (I think this might be a shortcut to remove other steps) write it last
        # check first three columns
        # if there is 3 of any number don't check it
        # if there's 2, check the remaining columns temp locations.


        # pointing pairs: eliminates a row because two spaces in a row must contain a number
        # hidden pairs: uses  pairs to eliminate other options. It can only be 6 or 7, so the possibility of 5 is eliiminated
        # swordfish: how I start,  by using distant values to check for obvious choices

        # still not solved, use brute force

    # GUI design
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry("500x300")
    root.configure(bg="#964b00")
    tk.Label(root, text="Sudoku Solver", font="arial", fg="white", bg="#964b00").grid(row=1, column=4)
    tk.Label(root, text="Enter known values", fg="white", bg="#964b00").grid(row=2, column=4)
    # entry box creation
    for row in range(9):
        for column in range(9):
            given = tk.Entry(root, justify="center", width=3)
            given.insert(-1, 0)  # fills box with a zero at -1 index? It works, but so does changing the number
            given.grid(row=row+3, column=column+8)  # spacial position of box
            all_given.append(given) # adds the entry box input to the end of the array "all_given"

    tk.Button(root, text='Solve', command=Solve).grid(row=12, column=17)
    tk.Button(root, text='Reset', command=Reset).grid(row=13, column=17)


    root.mainloop()
