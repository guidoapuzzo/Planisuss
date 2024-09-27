class SimulationController:

    # Method to simulate the ecosystem
    def simulate(self, cellsList):
        # Step 1: Vegetob growth phase
        for sublist in cellsList:
            for veg in sublist:
                if veg.terrainType != "Water":
                    veg.vegetob.grow()

        # Step 2: Handling erbast and carviz deaths due to vegetob
        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.death_from_vegetob(cellsList)
                if cell.pride:
                    cell.death_from_vegetob(cellsList)

        # Step 3: Herd and pride decision-making
        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdDecision(cellsList)
                if cell.pride:
                    cell.pride.prideDecision(cellsList)

        # Step 4: Fight between prides
        for row in cellsList:
            for cell in row:
                if cell.pride:
                    cell.pride.fight_between_prides(cell.pride, cellsList)

        # Step 5: Herd grazing and carviz hunting
        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdGraze(cellsList)
                if cell.pride:
                    for cr in cell.pride:
                        if cell.erbast:
                            cr.hunt(cellsList)

        # Step 6: Aging of erbast and carviz groups
        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.groupAging()
                if cell.pride:
                    cell.pride.groupAging()
