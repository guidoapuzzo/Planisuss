import sys

sys.path.append(".")
from Model.Creatures import Vegetob
from Model.Herd import Herd
from Model.Pride import Pride

# Create a class named 'Cell' to represent a cell in your simulation
class Cell:
    def __init__(self, row, column, terrainType, vegetob):
        self.row = row
        self.column = column
        self.terrainType = terrainType
        self.vegetob = vegetob
        self.erbast = Herd(row, column)
        self.pride = Pride(row, column)

    # Method to get the number of erbast (herd) in the cell
    def lenOfErbast(self):
        amountOfErbast = len(self.erbast)
        return amountOfErbast

    # Method to append an erbast (herd) to the cell
    def appendErbast(self, erb):
        self.erbast.append(erb)

    # Method to remove an erbast (herd) from the cell
    def delErbast(self, erb):
        self.erbast.remove(erb)

    # Method to get the number of carviz (pride) in the cell
    def lenOfCarviz(self):
        amountOfCarviz = len(self.pride)
        return amountOfCarviz

    # Method to append a carviz (pride) to the cell
    def appendPride(self, pride):
        self.pride.append(pride)

    # Method to remove a carviz (pride) from the cell
    def delPride(self, pride):
        self.pride.remove(pride)

    # Method to generate a vegetob in the cell based on terrain type
    def genVegetob(self):
        if self.terrainType == "Ground":
            return Vegetob()
        else:
            return "Water"

    # Method to handle death from vegetob in the cell
    def death_from_vegetob(self, listOfVegetobs):
        vegetob_full_density_counter = 0

        if self.erbast:
            erb = self.erbast[0]
            kernel = erb.get_adjacent_cells(self.row, self.column)
            if len(kernel) == 8:

                for i in range(len(kernel)):
                    if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob:
                        if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob.density == 100:
                            vegetob_full_density_counter += 1

                if vegetob_full_density_counter == 8:
                    if self.erbast:
                        self.erbast.clear()

                vegetob_full_density_counter = 0

        if self.pride:
            carv = self.pride[0]
            kernel = carv.get_adjacent_cells(self.row, self.column)

            if len(kernel) == 8:

                for i in range(len(kernel)):
                    if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob:
                        if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob.density == 100:
                            vegetob_full_density_counter += 1

                if vegetob_full_density_counter == 8:
                    if self.pride:
                        self.pride.clear()

    # Method to return a string representation of the cell
    def __str__(self):
        if self.terrainType == "Ground":
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob.density}, {self.erbast}, {self.pride})"
        else:
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob}, erbast: {self.erbast}, carviz: {self.pride})"

    def __repr__(self):
        return self.__str__()
