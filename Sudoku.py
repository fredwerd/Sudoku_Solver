if __name__ == "__main__":


    # check speeds of differing orders. Maybe set a check to determine puzzle difficulty by how many given values there are
    # and change the order depending. Should always finish with brute force

    import numpy as np
    import copy
    import tkinter as tk

    all_given = []
    def Solve(): # This is the gui button, runs entire solving code
        entry_list = ''
        temp_unsolved = np.zeros([9, 9])

        # retrieves values from the input boxes in a list
        for entries in all_given:
            entry_list = entry_list + entries.get()
        # converts list into the temp_unsolved array
        for row in range(9):
            for column in range(9):
                temp_unsolved[row, column] = entry_list[row * 9 + column]

    # uncomment this to test code faster
        temp_unsolved = np.array([[9, 0, 0, 0, 6, 0, 0, 0, 3],
                                  [0, 8, 0, 4, 0, 7, 0, 9, 0],
                                  [0, 0, 2, 0, 5, 0, 6, 0, 0],
                                  [0, 4, 0, 0, 0, 0, 0, 1, 0],
                                  [5, 0, 1, 0, 0, 0, 9, 0, 7],
                                  [0, 9, 0, 0, 0, 0, 0, 5, 0],
                                  [0, 0, 8, 0, 7, 0, 5, 0, 0],
                                  [0, 7, 0, 8, 0, 5, 0, 2, 0],
                                  [3, 0, 0, 0, 4, 0, 0, 0, 9]])

            # checks for input errors
        for r in range(0, 9):
            for c in range(0, 9):
                if temp_unsolved[r, c] == 0:
                    continue
                if temp_unsolved[r].tolist().count(temp_unsolved[r, c]) > 1 \
                        or temp_unsolved[:, c].tolist().count(temp_unsolved[r, c]) > 1:
                    # still needs box
                    print('input error: illegal box at row', r, 'column', c)
        # create a temporary solving array size 9x9, with each value as its own size 9 array filled with 1 through 9

        # initializes potential solution array
        pseudo_ind = np.arange(1, 10)
        pseudo_full = np.array([pseudo_ind] * 81)

        # while no_change = False: this should run until it goes through the entire puzzle without solving a square

        # finds every potential value and stores in pseudo_full. Checks pseudo_full for single solution boxes
        for r in range(0, 9):
            for c in range(0, 9):
                if temp_unsolved[r, c] > 0:
                    # set value to 0 if spot can't be the number
                    # column: start at the column in unsolved (c) and run down equivalent row in pseudo (x*9+c)
                    for c1 in range(0, 9):
                        pseudo_full[c1 * 9 + c, temp_unsolved[r, c] - 1] = 0
                    # row: start at first column of current row (r) and run through the row
                    for r1 in range(0, 9):
                        pseudo_full[r * 9 + r1, temp_unsolved[r, c] - 1] = 0
                    # box: check if row and column is the first second or third in smaller box
                    # reset loop index to the first slot in the smaller box
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
                    for r4 in range(r3, r3 + 3):
                        for c4 in range(c3, c3 + 3):
                            # remove every current number pseudo of smaller box only
                            pseudo_full[r4 * 9 + c4, temp_unsolved[r, c] - 1] = 0
                    # current value from given values was erased, so set it back in the pseudo values
                    pseudo_full[r * 9 + c, temp_unsolved[r, c] - 1] = temp_unsolved[r, c]


            # test that original is restored
            for r in range(0, 9):
                for c in range(0, 9):
                    if temp_unsolved[r, c] > 0:
                        if pseudo_full[r * 9 + c, temp_unsolved[r, c] - 1] == temp_unsolved[r, c]:
                            pass
                        else:
                            print('Potential illegal initial value at row', r, 'column', c)
                            break

            # set any for sure number into temp_unsolved
            v = 0
            for ROW in range(0, 9):
                for COLUMN in range(0, 9):
                    if temp_unsolved[ROW, COLUMN] == 0:
                        for PSEUDO_INDEX in range(0, 9):
                            if pseudo_full[ROW * 9 + COLUMN, PSEUDO_INDEX] == 0:
                                v += 1
                            if v == 8:
                                temp_unsolved[ROW, COLUMN] = sum(pseudo_full[ROW * 9 + COLUMN])
                                v = 0
                        v = 0
        # to do: end of first while loop
        print(temp_unsolved)

        # solves any square that is the only possible location for a solution number
        temp_p = np.zeros([9, 9])
        temp_box = np.zeros([1, 9])
        box = 0
        # by number, enter every possible unsolved spot for that p
        for p in range(1, 10):
            for r in range(0, 9):
                for c in range(0, 9):
                    if (temp_unsolved[r, c] == 0 and p in pseudo_full[r * 9 + c]) or temp_unsolved[r, c] == p:
                        # check if space can be current p
                        # if it can, store the potential value in a temp p, which should contain all possible p spots
                        temp_p[r, c] = p
            for r1 in range(0, 9):
                for c1 in range(0, 9):
                    if temp_unsolved[r1, c1] == 0:
                        # box finder
                        if c1 % 3 == 0:
                            c3 = c1
                        elif (c1 - 1) % 3 == 0:
                            c3 = c1 - 1
                        else:
                            c3 = c1 - 2
                        if r1 % 3 == 0:
                            r3 = r1
                        elif (r1 - 1) % 3 == 0:
                            r3 = r1 - 1
                        else:
                            r3 = r1 - 2
                        box = 0
                        for r4 in range(r3, r3 + 3):
                            for c4 in range(c3, c3 + 3):
                                temp_box[0, box] = temp_p[r4, c4]
                                box += 1
                        # check row
                        if sum(temp_p[r1]) == p and p in pseudo_full[r1 * 9 + c1]:
                            temp_unsolved[r1, c1] = p
                            print('y', p)
                        # check column
                        elif sum(temp_p[:, c1]) == p and p in pseudo_full[r1 * 9 + c1]:
                            temp_unsolved[r1, c1] = p
                            print('y again', p)
                        # check box
                        elif sum(temp_box[0]) == p and p in pseudo_full[r1 * 9 + c1]:
                            temp_unsolved[r1, c1] = p
                            print('yet again,', p)
                temp_p = np.zeros([9, 9])
        print(temp_unsolved)


        # error checking necessary for bulk solve
        if sum(pseudo_full[0]) == 0:
            print('No solutions, please recheck input')
            del temp_unsolved
            # put a break here if the entire script is a while loop


        # beginning of brute solving

        # temp array of possible values that will be edited and restored over iterations of bulk solving
        brute_pseudo = copy.deepcopy(pseudo_full)
        # row, column of previously edited index
        previous_index = np.zeros([81, 3], dtype=int)
        saved_row = 0
        saved_column = 0
        saved_pseudo = 0
        only = 0
        r = 0
        c = 0
        c1 = 0
        r1 = 0
        br = 0
        bc = 0
        backtrack = False
        conflict = False
        while 0 in temp_unsolved:
            print('not solved yet')
            #if r * 9 + c == 16:
                #break
            while r < 9:
                #if r * 9 + c == 16:
                    #break
                print('does this repeat more than once?')
                while c < 10:
                    #if r * 9 + c == 16:
                        #break
                    print('current index', r * 9 + c)
                    if c == 9:
                        c = 0
                        r += 1
                    if r == 9:
                        c = 10
                        break
                    # put an r * 9 + c value here in the loop.
                    # adds previous changed index values. If current run is backtracking, this will override index values
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
                                # reset current brute pseudos to possible values
                                print('no possible value, clearing previous, restarting')
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
                                c1 = 0
                                r1 = 0
                                br = 0
                                bc = 0
                                # check row
                                while c1 <= c:
                                    # if conflict:
                                    if temp_unsolved[r, c1] == brute_pseudo[r * 9 + c, only]:
                                        # set current pseudo to 0 for now
                                        # this line below is clearing a value in pseudo full? in each conflict check
                                        brute_pseudo[r * 9 + c, only] = 0
                                        # try the next possible value in pseudo
                                        only += 1
                                        # don't check the rows
                                        r1 = 10
                                        # don't check box
                                        br = 10
                                        bc = 10
                                        conflict = True
                                        # stop checking for conflicts
                                        break
                                    else:
                                        c1 += 1
                                # check column
                                while r1 <= r:
                                    if temp_unsolved[r1, c] == brute_pseudo[r * 9 + c, only]:
                                        # set current pseudo to 0 for now
                                        brute_pseudo[r * 9 + c, only] = 0
                                        # try the next possible value in pseudo
                                        only += 1
                                        # don't check box
                                        br = 10
                                        bc = 10
                                        conflict = True
                                        # stop checking for conflicts
                                        break
                                    else:
                                        r1 += 1
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
                                            # try the next possible value in pseudo
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

    # GUI intializing
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry("1100x500")
    tk.Label(root, text="Sudoku Solver").grid(row=10, column=4)
    tk.Label(root, text="Enter known values").grid(row=11, column=4)

    for row in range(9):
        for column in range(9):
            given = tk.Entry(root)
            given.insert(-1, 0)
            given.grid(row=row, column=column)
            all_given.append(given)

    tk.Button(root, text='Solve', command=Solve).grid(row=10, column=0)
    root.mainloop()