import sys

sys.path.append(".")
import time
import noise
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.style as mplstyle
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from Model.CellModel import Cell
from Model.Creatures import Vegetob, Carviz, Erbast, Creatures
from Controller.DataPersistence import DataPersistence
from Controller.SimulationController import SimulationController
from constants import NUM_CELLS, MAX_DAYS, MAX_LIFE_E, MAX_LIFE_C, GREEN, YELLOW, RED, RESET

mplstyle.use(['fast'])

# Set TkAgg backend
plt.switch_backend('TkAgg')


class SimulationView:
    def __init__(self):
        self.max_days = MAX_DAYS
        self.erb_lifetime = MAX_LIFE_E
        self.car_lifetime = MAX_LIFE_C
        self.num_cells = NUM_CELLS
        self.day = 0
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0
        self.x_data = [0]
        self.y_erb_data = [self.erb_counter]
        self.y_car_data = [self.car_counter]
        self.y_hunt_data = [self.hunt_counter]
        self.pop_erb = [self.y_erb_data]
        self.pop_car = [self.y_car_data]
        self.car_max = 0
        self.erb_max = 0
        self.hunt_tot = 0
        self.num_car = 10
        self.num_erb = 20
        self.water_scale = 15
        self.run_flag = 1
        self.has_started = False
        self.cellsList = np.empty((self.num_cells, self.num_cells), dtype=object)
        self.water_cells = np.zeros((self.num_cells, self.num_cells), dtype=bool)
        self.colorsList = np.zeros((self.num_cells, self.num_cells))
        self.setup_plots()
        self.setup_sliders()
        self.setup_buttons()
        self.button_events()
        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)
        self.animation_paused = True
        self.interval = self.slider1.val
        self.animation = None
        self.has_finished = False
        self.dp = None
        self.simulation_controller = SimulationController()
        self.initialize_animation()

    def setup_animation_values(self):
        self.interval = self.slider1.val
        self.num_cells = self.slider2.val
        self.num_car = self.slider3.val
        self.car_lifetime = self.slider4.val
        self.num_erb = self.slider5.val
        self.erb_lifetime = self.slider6.val
        self.water_scale = self.slider7.val

        self.cellsList = np.empty((self.num_cells, self.num_cells), dtype=object)
        self.water_cells = np.zeros((self.num_cells, self.num_cells), dtype=bool)
        self.colorsList = np.zeros((self.num_cells, self.num_cells))

        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)

    def setup_plots(self):
        plt.style.use('dark_background')
        self.cmap = colors.ListedColormap(['blue', 'green', 'yellow', 'red', 'black'])
        self.bounds = [0, 10, 20, 30, 40, 50]
        self.norm = colors.BoundaryNorm(self.bounds, self.cmap.N)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.ax1.minorticks_off()
        self.ax2.minorticks_off()
        self.line_erb = self.ax2.plot(self.x_data, self.y_erb_data, color='yellow', label='Erbast')
        self.line_car = self.ax2.plot(self.x_data, self.y_car_data, color='red', label='Carviz')
        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)
        self.fig.subplots_adjust(bottom=0.35, top=0.95, left=0.1, right=0.9, wspace=0.3)

    def setup_sliders(self):
        # Create sliders
        self.slider1_ax = self.fig.add_axes([0.15, 0.25, 0.25, 0.03])
        self.slider2_ax = self.fig.add_axes([0.15, 0.2, 0.25, 0.03])
        self.slider3_ax = self.fig.add_axes([0.15, 0.15, 0.25, 0.03])
        self.slider4_ax = self.fig.add_axes([0.15, 0.1, 0.25, 0.03])
        self.slider5_ax = self.fig.add_axes([0.6, 0.25, 0.25, 0.03])
        self.slider6_ax = self.fig.add_axes([0.6, 0.2, 0.25, 0.03])
        self.slider7_ax = self.fig.add_axes([0.6, 0.15, 0.25, 0.03])

        self.slider1 = Slider(self.slider1_ax, 'Animation Speed', 0, 500, valinit=60, valstep=10)
        self.slider2 = Slider(self.slider2_ax, 'Number Cells', 50, 100, valinit=50, valstep=10)
        self.slider3 = Slider(self.slider3_ax, 'Carviz Pop', 10, 500, valinit=10, valstep=1)
        self.slider4 = Slider(self.slider4_ax, 'Carviz Life', 10, 500, valinit=10, valstep=1)
        self.slider5 = Slider(self.slider5_ax, 'Erbast Pop', 10, 500, valinit=10, valstep=1)
        self.slider6 = Slider(self.slider6_ax, 'Erbast Life', 10, 500, valinit=10, valstep=1)
        self.slider7 = Slider(self.slider7_ax, 'Water Amount', 1e-6, 20, valinit=15, valstep=5)
        self.slider1.on_changed(self.update_animation_interval)

    def update_animation_interval(self, val):
        # Update the animation interval based on the slider value
        self.interval = self.slider1.val
        if self.animation is not None and not self.has_finished:
            self.animation.event_source.stop()
            self.animation = FuncAnimation(
                self.fig, self.update, interval=self.interval, save_count=200
            )

            if not self.animation_paused:
                self.animation.event_source.start()

    def setup_buttons(self):

        self.start_button_ax = self.fig.add_axes([0.3, 0.05, 0.1, 0.04])
        self.reset_button_ax = self.fig.add_axes([0.45, 0.05, 0.1, 0.04])
        self.pause_button_ax = self.fig.add_axes([0.6, 0.05, 0.1, 0.04])

        self.start_button = Button(self.start_button_ax, 'Start', color="darkgray")
        self.reset_button = Button(self.reset_button_ax, 'Reset', color="darkgray")
        self.pause_button = Button(self.pause_button_ax, 'Pause/Resume', color="darkgray")

    def button_events(self):

        self.start_button.on_clicked(self.start_animation)
        self.pause_button.on_clicked(self.pause_animation)
        self.reset_button.on_clicked(self.reset_animation)

    def initialize_cells_list(self):
        creatures = Creatures()
        creatures.update_num_cells(self.num_cells)
        scale = self.water_scale
        for i in range(self.num_cells):
            for j in range(self.num_cells):
                noise_value = noise.pnoise2(i / scale, j / scale, octaves=6, persistence=0.5, lacunarity=2.0,
                                            repeatx=self.num_cells, repeaty=self.num_cells)
                vg = Vegetob()
                vg.row = i
                vg.column = j
                vg.density = vg.generateDensity()
                if noise_value > 0.25:  # Assign cells as water based on noise threshold
                    self.water_cells[i][j] = True
                else:
                    self.cellsList[i][j] = Cell(i, j, "Ground", vg)

        # Group neighboring water cells together
        for i in range(self.num_cells):
            for j in range(self.num_cells):
                if self.water_cells[i][j]:
                    if i > 0 and self.cellsList[i - 1][j].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i - 1][j]
                    elif j > 0 and self.cellsList[i][j - 1].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i][j - 1]
                    else:
                        self.cellsList[i][j] = Cell(i, j, "Water", None)

    def update_population_counts(self):
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0

        for row in range(self.num_cells):
            for column in range(self.num_cells):
                if (
                        row < len(self.cellsList)
                        and column < len(self.cellsList[row])
                        and self.cellsList[row][column].terrainType == "Water"
                ):
                    self.colorsList[row][column] = 5
                elif (
                        row < len(self.cellsList)
                        and column < len(self.cellsList[row])
                        and len(self.cellsList[row][column].erbast) > 0
                        and len(self.cellsList[row][column].pride) > 0
                ):
                    self.car_counter += 1
                    self.erb_counter += 1
                    self.hunt_counter += 1
                    self.colorsList[row][column] = 45
                elif (
                        row < len(self.cellsList)
                        and column < len(self.cellsList[row])
                        and len(self.cellsList[row][column].erbast) > 0
                ):
                    self.erb_counter += 1
                    self.colorsList[row][column] = 25
                elif (
                        row < len(self.cellsList)
                        and column < len(self.cellsList[row])
                        and len(self.cellsList[row][column].pride) > 0
                ):
                    self.colorsList[row][column] = 35
                    self.car_counter += 1
                elif (
                        row < len(self.cellsList)
                        and column < len(self.cellsList[row])
                        and self.cellsList[row][column].terrainType == "Ground"
                ):
                    self.colorsList[row][column] = 15

    def update(self, frame):
        if self.has_started:
            self.simulation_controller.simulate(self.cellsList)
            self.update_population_counts()
            self.day += 1
            self.im.set_array(self.colorsList)
            # Calculate the time in Planisuss convention
            centuries = self.day // 1000
            decades = (self.day % 1000) // 100
            years = (self.day % 100) // 10
            months = self.day % 10

            title_parts = []
            if centuries > 0:
                title_parts.append(f"{centuries} Centuries")
            if decades > 0:
                title_parts.append(f"{decades} Decades")
            if years > 0:
                title_parts.append(f"{years} Years")
            if months > 0:
                title_parts.append(f"{months} Months")

            title = ", ".join(title_parts)
            self.ax1.set_title(title)
            self.ax1.title.set_fontsize(8)
            self.title = title
            self.x_data.append(self.day)

            new_erb_pop = [self.erb_counter]
            new_car_pop = [self.car_counter]

            prev_erb_pop = self.pop_erb[-1]
            prev_car_pop = self.pop_car[-1]

            self.pop_erb.append(np.concatenate([prev_erb_pop, new_erb_pop]))
            self.pop_car.append(np.concatenate([prev_car_pop, new_car_pop]))

            self.y_erb_data = self.pop_erb[-1]
            self.y_car_data = self.pop_car[-1]
            self.y_hunt_data.append(self.hunt_counter)

            self.x_erb_data = np.arange(len(self.pop_erb))
            self.x_car_data = np.arange(len(self.pop_car))

            self.line_erb[0].set_data(self.x_erb_data, self.y_erb_data)
            self.line_car[0].set_data(self.x_car_data, self.y_car_data)

            max_y = max(max(self.y_erb_data), max(self.y_car_data))
            max_x = max(len(self.x_erb_data), len(self.x_car_data))
            gap = 0.02 * max(max_x, max_y)

            self.ax2.set_xlim(0, max_x + gap)
            self.ax2.set_ylim(0, max_y + gap)

            self.erb_max = max(self.y_erb_data)
            self.car_max = max(self.y_car_data)

            self.hunt_tot = sum(self.y_hunt_data)

            self.ax2.set_xlabel('Days', fontsize=8)
            self.ax2.set_ylabel('Population', fontsize=8)

            self.ax2.set_title((
                f'\n\n Max Carviz: {self.car_max}      Max Erbast: {self.erb_max}      Cur Carviz: {self.car_counter}      Cur Erbast: {self.erb_counter}      Tot Kills: {self.hunt_tot}'))
            self.ax2.title.set_fontsize(8)

            self.dp = DataPersistence(
                self.slider1.val,
                self.slider2.val,
                self.slider3.val,
                self.slider5.val,
                self.slider4.val,
                self.slider6.val,
                int(self.slider7.val),
                self.run_flag,
                self.title,
                self.car_max,
                self.erb_max,
                self.hunt_tot
            )
            self.dp.get_init_values()

            if self.day >= 0 and self.car_counter == 0 and self.animation_paused == False and not self.has_finished:
                self.has_finished = True
                print(f"\n{GREEN}Simulation Successfully Finished!\n{RESET}")

                self.run_flag += 1
                time.sleep(0.1)
                self.animation.event_source.stop()
                if self.erb_counter > 0:
                    print(f"{YELLOW}Erbasts Survived!{RESET}\n")

                if self.erb_counter == 0:
                    print(f"{RED}Carvizes Survived!{RESET}\n")

                self.dp.get_final_values()
                self.dp.save_simulation_data()
                self.animation_paused = True
                self.dp.read_pickle_file('simulation_data.pickle')

            return self.im, self.line_erb, self.line_car

    def initialize_animation(self):
        self.animation = FuncAnimation(
            self.fig, self.update, interval=self.interval, save_count=200
        )
        self.animation.pause()

    def start_animation(self, event=None):
        self.day = 0
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0
        self.x_data = [0]
        self.y_data = [0]
        self.y_erb_data = [self.erb_counter]
        self.y_car_data = [self.car_counter]
        self.y_hunt_data = [self.hunt_counter]
        self.pop_erb = [self.y_erb_data]
        self.pop_car = [self.y_car_data]

        self.interval = self.slider1.val

        self.setup_animation_values()

        self.initialize_cells_list()

        self.has_started = True

        self.im.set_array(self.colorsList)

        if self.animation_paused:
            self.animation_paused = False

            self.animate()

            self.start_button.set_active(False)
            self.start_button.color = 'gray'

        elif not self.animation_paused and self.has_started:
            self.animate()
            self.animation.new_frame_seq()

    def reset_animation(self, event=None):
        if self.animation_paused:

            self.animation_paused = False
            self.animation.event_source.start()
            self.start_animation()

        else:

            self.animation_paused = False
            self.animation.event_source.start()
            self.start_animation()

        self.has_finished = False

    def pause_animation(self, event):
        if not self.animation_paused:
            self.animation.event_source.stop()
            self.animation_paused = True

        else:
            self.animation.event_source.start()
            self.animation_paused = False

    def animate(self):
        if not self.animation_paused:
            for _ in range(self.num_car):
                carv = Carviz(lifetime=self.car_lifetime)
                carv_placed = False
                while not carv_placed:
                    row = random.randint(0, self.num_cells - 1)
                    column = random.randint(0, self.num_cells - 1)

                    if (
                            row < self.num_cells and column < self.num_cells
                            and row < len(self.cellsList) and column < len(self.cellsList[row])
                            and self.cellsList[row][column].terrainType != "Water"
                    ):
                        carv.row = row
                        carv.column = column
                        self.cellsList[row][column].pride.append(carv)
                        carv_placed = True

            for _ in range(self.num_erb):
                erb = Erbast(lifetime=self.erb_lifetime)
                erb_placed = False
                while not erb_placed:
                    row = random.randint(0, self.num_cells - 1)
                    column = random.randint(0, self.num_cells - 1)
                    if (
                            row < self.num_cells and column < self.num_cells
                            and row < len(self.cellsList) and column < len(self.cellsList[row])
                            and self.cellsList[row][column].terrainType != "Water"
                            and len(self.cellsList[row][column].erbast) == 0
                    ):
                        erb.row = row
                        erb.column = column
                        self.cellsList[row][column].erbast.append(erb)
                        erb_placed = True
