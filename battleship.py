'''
    File: battleship.py
    Author: John Le
    Purpose: Given a placement file and guessing file, play out
    a game of Battleships to determine if the guessing file is
    a win or loss.
    CSC 120, 001, Spring Semester
'''

import sys

class GridPos:
    # initializes the GridPos object
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ship = None
        self._guessed = False
    
    def gridPosCoords(self):
        # returns the coords of the gridPos object
        return (self._x, self._y)

    def set_ship(self):
        # sets self._ship to True
        self._ship = True

    def set_guessed(self):
        # sets self._guessed to True
        self._guessed = True

    def get_ship(self):
        # determines if a ship is in the GridPos object
        if self._ship == True:
            return True
        return False

    def get_guessed(self):
        # determines if the gridPos object has been
        # previously guessed or not
        if self._guessed == True:
            return True
        return False
    
    def __str__(self):
        # prints out a gridPos object as an X
        # or a dot depending if a ship object
        # is present in the GridPos
        if self._ship == True:
            return ("X")
        return (".")
        
class Board:
    # initializes the Board object
    def __init__(self, list_of_ships):
        self._grid = []
        self._ships = list_of_ships
        self._total_list_of_ship_coords = []
        self.make_list_of_coords()
        self._totalShips = 5
        for i in range(10):
            # creates the 9x9 grid of gridPos objects
            row = []
            for j in range(10):
                row.append(GridPos(i, j))
            self._grid.append(row)
    
    def make_guess(self, x, y):
        # makes a guess given two paramters (x and y coordinate)
        coordinates = (x, y)
        for rows in self._grid:
            if x > 9 or y > 9:
                print("illegal guess")
                break
            for gridPos in rows:
                # searches through all gridPos object (9x9 grid)
                if coordinates == gridPos.gridPosCoords():
                    if gridPos.get_ship() == True:
                        if gridPos.get_guessed() == True:
                            print("hit (again)")
                        elif gridPos.get_guessed() == False:
                            gridPos.set_guessed()
                            for ships in self._ships:
                                # searches through all ship objects present
                                shipCoords = ships.get_coords()
                                if coordinates in shipCoords:
                                    # determines if the right
                                    # ship is being updated
                                    ships.update_health()
                                    if ships.get_health() == 0:
                                        ships.set_sunk()
                                        print("{} sunk".format(ships.get_type()))
                                        for ships in self._ships:
                                            # seaches through all ship objects
                                            # present and determines if
                                            # all 5 ships have been sunk and ends
                                            # the game if all 5 have been sunk
                                            if ships.get_sunk() == True:
                                                self._totalShips -= 1
                                        if self._totalShips != 0:
                                            # resets the win condition of the game
                                            # if all 5 ships had not been sunk yet
                                            #  and checks it again if guessed again
                                            self._totalShips = 5
                                        elif self._totalShips == 0:
                                            print("all ships sunk: game over")
                                            sys.exit(0)
                                    elif ships.get_health() != 0:
                                        # if the ship is not sunk when hit then prints out hit
                                        print("hit")
                    elif gridPos.get_guessed() == True:
                        print("miss (again)")
                    elif gridPos.get_guessed() == False:
                        gridPos.set_guessed()
                        print("miss")


    def add_ship(self, ship_object):
        # adds a ship to the grid of GridPos objects
        for coords in ship_object.get_coords():
            # loops through all coords and updates
            # the matching gridPos coords
            for rows in self._grid:
                for gridPos in rows:
                    if coords == gridPos.gridPosCoords():
                        gridPos.set_ship()
    
    def print_gridPos(self):
        # prints the entire grid of gridPos objects (9x9 grid)
        for rows in self._grid:
            for gridPos in rows:
                print(gridPos)

    def make_list_of_coords(self):
        # adds every coordinate taken by a ship into a list
        for ships in self._ships:
            self._total_list_of_ship_coords += ships.get_coords()
    
    def __str__(self):
        # prints the entire grid of gridPos objects (9x9 grid)
        print(self._grid)

class Ship:
    def __init__(self, type, x1, y1, x2, y2):
        # initializes a ship object with
        # corresponding health depending on the type
        self._list_of_coords = []
        self._type = type
        self._sunk = False
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self._type == "A":
            self._shipHealth = 5
        if self._type == "B":
            self._shipHealth = 4
        if self._type == "S":
            self._shipHealth = 3
        if self._type == "D":
            self._shipHealth = 3
        if self._type == "P":
            self._shipHealth = 2
        self.make_coords()

    def update_health(self):
        # decreases a ships health by 1
        self._shipHealth -= 1
    
    def set_sunk(self):
        # sets self._sunk to True
        self._sunk = True

    def get_length(self):
        # gets the total length as an integer of a ship object
        length = 1
        if self._x1 == self._x2 + 1:
            return 2
        elif self._y1 == self._y2 + 1:
            return 2
        elif self._x1 + 1 == self._x2:
            return 2
        elif self._y1 + 1 == self._y2:
            return 2
        elif self._x1 == self._x2:
            if self._y1 >= self._y2:
                i = self._y2
                while i < self._y1:
                    length += 1
                    i += 1
            else:
                i = self._y1
                while i < self._y2:
                    length += 1
                    i += 1
        elif self._y1 == self._y2:
            if self._x1 >= self._x2:
                i = self._x2
                while i < self._x1:
                    length += 1
                    i += 1
            else:
                i = self._x1
                while i < self._x2:
                    i += 1
                    length += 1
        return int(length)

    def make_coords(self):
        # determines which coordinates are taken up
        # by ship object and adds it to the list of
        # coordinates the ship takes up
        if self._x1 == self._x2:
            if self._y1 >= self._y2:
                i = self._y2
                while i <= self._y1:
                    self._list_of_coords.append(tuple((self._x1, i)))
                    i += 1
            else:
                i = self._y1
                while i <= self._y2:
                    self._list_of_coords.append(tuple((self._x1, i)))
                    i += 1
        if self._y1 == self._y2:
            if self._x1 >= self._x2:
                i = self._x2
                while i <= self._x1:
                    self._list_of_coords.append(tuple((i, self._y1)))
                    i += 1
            else:
                i = self._x1
                while i <= self._x2:
                    self._list_of_coords.append(tuple((i, self._y1)))
                    i += 1
    
    def get_coords(self):
        # returns a list of all the coordinates the ship object takes up
        return self._list_of_coords
    
    def get_sunk(self):
        # returns if the ship is sunk or not
        return self._sunk
    
    def get_type(self):
        # returns the type of ship
        return self._type
    
    def get_health(self):
        # returns the total health of the ship
        return self._shipHealth

def create_list_of_ships(file):
    '''Creates a list of ships from a given placement file in order
    to input into a Board object.
    Parameters: file is a file
    Pre-Condition: file is a file
    Post-Condition: Returns a list of ship objects'''
    list_of_coords = []
    list_of_ships = []
    ship_type_count = []
    placements = open(file, "r")
    for line in placements:
        ship = line.strip("\n")
        ship = ship.split(" ")
        type = ship[0]
        x1 = int(ship[1])
        y1 = int(ship[2])
        x2 = int(ship[3])
        y2 = int(ship[4])
        if (tuple((x1, y1))) in list_of_coords:
            # determines if a given coordinate is already been used
            print("ERROR: overlapping ship: " + line)
            sys.exit(0)
        if (tuple((x2, y2))) in list_of_coords:
            # determines if a given coordinate is already been used
            print("ERROR: overlapping ship: " + line)
            sys.exit(0)
        if x1 > 9 or x2 > 9 or y1 > 9 or y2> 9:
            # determines if a given coordinate is outside of the playing grid
            print("ERROR: ship out-of-bounds: " + line)
            sys.exit(0)
        if x1 != x2 and y1 != y2:
            # determines if a given coordinate will make the ship diagonal
            print("ERROR: ship not horizontal or vertical: " + line)
            sys.exit(0)
        if type == "A":
            # determines what ship type it is and updates coordinates taken up
            # and adds it to a list of all ships
            newShip = Ship("A", x1, y1, x2, y2)
            if newShip.get_length() != 5:
                print("ERROR: incorrect ship size: " + line)
                sys.exit(0)
            ship_type_count.append(5)
            list_of_coords += newShip.get_coords()
            list_of_ships.append(newShip)
        if type == "B":
            # same as previous comment
            newShip = Ship("B", x1, y1, x2, y2)
            if newShip.get_length() != 4:
                print("ERROR: incorrect ship size: " + line)
                sys.exit(0)
            ship_type_count.append(4)
            list_of_coords += newShip.get_coords()
            list_of_ships.append(newShip)
        if type == "S":
            # same as previous comment
            newShip = Ship("S", x1, y1, x2, y2)
            if newShip.get_length() != 3:
                print("ERROR: incorrect ship size: " + line)
                sys.exit(0)
            ship_type_count.append(3)
            list_of_coords += newShip.get_coords()
            list_of_ships.append(newShip)
        if type == "D":
            # same as previous comment
            newShip = Ship("D", x1, y1, x2, y2)
            if newShip.get_length() != 3:
                print("ERROR: incorrect ship size: " + line)
                sys.exit(0)
            ship_type_count.append(3)
            list_of_coords += newShip.get_coords()
            list_of_ships.append(newShip)
        if type == "P":
            # same as previous comment
            newShip = Ship("P", x1, y1, x2, y2)
            ship_type_count.append(2)
            if newShip.get_length() != 2:
                print("ERROR: incorrect ship size: " + line)
                sys.exit(0)
            list_of_coords += newShip.get_coords()
            list_of_ships.append(newShip)
    if sorted(ship_type_count) != [2, 3, 3, 4, 5]:
        # determines if all 5 types of ships are present 
        print("ERROR: fleet composition incorrect")
        sys.exit(0)
    return list_of_ships

def process_guess(file, playingBoard):
    '''Opens the guess file and processing it accordingly and
    makes guesses on the playing board to determine if it is a win
    or a loss.
    Parameters: file is a file, playingBoard is an object
    Pre-Condition: file is a file, playingBoard is a Board object
    Return Value: Prints the results of the game including hits or misses.'''
    guessFile = open(file, "r")
    for line in guessFile:
        guesses = line.strip("\n")
        guesses = guesses.split(" ")
        if guesses[0] == "":
            sys.exit(0)
        x = int(guesses[0])
        y = int(guesses[1])
        playingBoard.make_guess(x, y)

def main():
    '''Runs all functions and creates all needed objects to correctly process
    two given inputs for placing and guessing ships.
    Paramters: N/A
    Pre-Condition: N/A
    Return Value: Prints the results of the game including hits or misses.'''
    placementFile = input()
    playingBoard = Board(create_list_of_ships(placementFile))
    list_of_ships = create_list_of_ships(placementFile)
    for ship in list_of_ships:
        # adds all ships created into the Board object that was
        # previously created
        playingBoard.add_ship(ship)
    process_guess(input(), playingBoard)

main()