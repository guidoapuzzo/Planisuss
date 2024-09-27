import sys
sys.path.append(".")

# Import constants and pickle module
from constants import GREEN, RESET
import pickle

class DataPersistence:
    # Constructor to initialize data
    def __init__(self, interval, num_cells, num_carviz, num_erbast, lft_carviz, lft_erbast, scl_water, run_flag, title, car_max, erb_max, hunt_tot):
        self.interval = interval
        self.num_cells = num_cells
        self.num_carviz = num_carviz
        self.num_erbast = num_erbast
        self.lft_carviz = lft_carviz
        self.lft_erbast = lft_erbast
        self.scl_water = scl_water
        self.run_flag = run_flag
        self.title = title
        self.car_max = car_max
        self.erb_max = erb_max
        self.hunt_tot = hunt_tot

    # Get initial values as a dictionary
    def get_init_values(self):
        init_values = {
            'Interval    ': self.interval,
            'NUM_Cells   ': f"{self.num_cells} x {self.num_cells}",
            'NUM_Carviz  ': self.num_carviz,
            'NUM_Erbast  ': self.num_erbast,
            'LFT_Carviz  ': self.lft_carviz,
            'LFT_Erbast  ': self.lft_erbast,
            'SCL_Water   ': self.scl_water,
        }
        return init_values

    # Get final values as a dictionary
    def get_final_values(self):
        final_values = {
            'RUN_Amount  ': self.run_flag,
            'RUN_Time    ': self.title,
            'MAX_Carviz  ': self.car_max,
            'MAX_Erbast  ': self.erb_max,
            'TOT_Kills   ': self.hunt_tot,
        }
        return final_values

    # Save simulation data to a pickle file
    def save_simulation_data(self):
        init_values = self.get_init_values()
        final_values = self.get_final_values()

        simulation_data = {
            'Initial Values': init_values,
            'Final Values': final_values
        }

        try:
            # Try to read existing pickle file
            with open('simulation_data.pickle', 'rb') as file:
                data = pickle.load(file)
                if isinstance(data, dict):
                    prev_values = data
                else:
                    prev_values = {}
        except FileNotFoundError:
            prev_values = {}  # If the file doesn't exist, initialize an empty dictionary

        # Merge existing and new data
        updated_values = {**prev_values, **simulation_data}

        # Save the updated data to the pickle file
        with open('simulation_data.pickle', 'wb') as file:
            pickle.dump(updated_values, file)

        print(f"{GREEN}Simulation data saved successfully.{RESET}\n")

    # Read and print the content of a pickle file
    def read_pickle_file(self, file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            self.content = data

        for title, content in self.content.items():
            print(f"\n{RESET}{title}\n")
            for key, value in content.items():
                print(f"{key}: {value}")
            print()
