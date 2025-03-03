# ------------ Imports and Variables ------------

import re
from collections import defaultdict

directions = ['N', 'E', 'S', 'W']  # Clockwise directions


# --------------- Helper Functions ---------------

def rotate_left(direction):

    return directions[(directions.index(direction) - 1) % 4]

def rotate_right(direction):

    return directions[(directions.index(direction) + 1) % 4]

def move_forward(x, y, direction, width, height):

    if direction == 'N' and y + 1 < height:
        return x, y + 1
    
    elif direction == 'S' and y - 1 >= 0:
        return x, y - 1
    
    elif direction == 'E' and x + 1 < width:
        return x + 1, y
    
    elif direction == 'W' and x - 1 >= 0:
        return x - 1, y
    
    return x, y  # No movement if out of bounds

def is_valid_coordinates(x, y, sim = None):

    positive_coordinates = x.isdigit() and int(x) > 0 and y.isdigit() and int(y) > 0

    if not sim:
        return positive_coordinates
    
    else:
        return int(x) <= sim.width and int(y) <= sim.height
    
def is_valid_commands(commands):

    return bool(re.fullmatch(r"[LRF]+", commands))


# ------------------- Classes --------------------

class Car:

    def __init__(self, name, x, y, direction, commands):

        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = list(commands)
        self.collided = False
    
    def execute_command(self, command, width, height):

        if self.collided:
            return
        
        if command == 'L':
            self.direction = rotate_left(self.direction)

        elif command == 'R':
            self.direction = rotate_right(self.direction)

        elif command == 'F':
            self.x, self.y = move_forward(self.x, self.y, self.direction, width, height)

    def car_details(self, show_commands = False):

        return f"Car Name: {self.name} - Position: ({self.x}, {self.y}) - Direction: {self.direction}" + (f" - Commands: {"".join(self.commands)}" if show_commands else "")

class Simulation:

    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.cars = []
        self.car_names = set()
        self.positions = defaultdict(set)
    
    def add_car(self, name, x, y, direction, commands):

        car = Car(name, x, y, direction, commands)
        self.cars.append(car)
        self.car_names.add(name)
        self.positions[(x, y)].add(car)

    def reset(self):

        self.cars = []
        self.positions = {}

    def show_cars(self, show_commands = False):
        
        print("\nYour current list of cars are:")
        for car in self.cars:
            print(f"- {car.car_details(show_commands = show_commands)}")

    def run(self):
        
        self.show_cars()
        step = 0
        max_commands = max(len(car.commands) for car in self.cars)
        
        print("\nAfter simulation, the result is:")

        for i in range(max_commands):
            step += 1
            
            for car in self.cars:

                prev_x, prev_y = car.x, car.y

                if not car.collided and car.commands:
                    command = car.commands.pop(0)
                    car.execute_command(command, self.width, self.height)
                    
                    if command == "F" and len(self.positions[(car.x, car.y)]) > 0:
                        print(f"- {car.name}, collides with {', '.join(c.name for c in self.positions[(car.x, car.y)])} at ({car.x}, {car.y}) at step {step}.")
                        car.collided = True

                        collided_cars = []
                        for collided_car in self.positions[(car.x, car.y)]:
                            collided_car.collided = True
                            collided_cars.append(collided_car)
                        print(f"- {', '.join(c.name for c in collided_cars)}, collides with {car.name} at ({car.x}, {car.y}) at step {step}.")

                    self.positions[(prev_x, prev_y)].remove(car)
                    self.positions[(car.x, car.y)].add(car)
        
        for car in self.cars:

            if not car.collided:
                print(f"- {car.name}, ({car.x}, {car.y}) {car.direction}")

        return True


# --------- Program Execution Functions ----------

def create_simulation():

    valid_simulation_field = False

    while not valid_simulation_field:

        sim_values = input("\nPlease enter the width and height of the simulation field in x y format: ").split()

        if len(sim_values) != 2:
            print("Invalid input. Please enter exactly two Positive Integer values: x y.")

        else:

            width, height = sim_values

            if is_valid_coordinates(width, height):
                sim = Simulation(int(width), int(height))
                print(f"\nYou have created a field of {width} x {height}.")
                valid_simulation_field = True

            else:
                print("Please enter valid (Positive Integers only) values for width and height of the simulation.")

    return sim

def add_car(sim):

    valid_name = False
    valid_position = False
    valid_commands = False

    while not valid_name:

        name = input("\nPlease enter the name of the car: ")

        if name in sim.car_names:
            print("There is already a car created with this name. Please input a different car name.")
            continue

        else:
            valid_name = True

    while not valid_position:

        car_values = input(f"\nPlease enter initial position of car {name} in x y Direction format: ").split()

        if len(car_values) != 3:
            print("Invalid input. Please enter exactly two Positive Integer values followed by a direction (N, S, E or W): x y direction.")
            continue 

        else:
            x, y, direction = car_values

            if not is_valid_coordinates(x, y, sim):
                print("Invalid car coordinates. Please enter two Positive Integer values within the set simulation bounds.")
                continue

            if direction not in directions:
                print("Invalid car direction. Please enter N, S, W, or E.")
                continue

            if (int(x), int(y)) in sim.positions:
                print("There is already a car at this position. Please input different car coordinates.")
                continue

        valid_position = True

    while not valid_commands:

        commands = input(f"\nPlease enter the commands for car {name}: ")

        if not is_valid_commands(commands):
            print("Invalid car commands. Please enter a string containing only L, R or F.")
            continue

        valid_commands = True

    sim.add_car(name, int(x), int(y), direction, commands)
    sim.show_cars(show_commands = True)

def restart_program():
    print("\nRestarting simulation...")
    main()

def exit_program():
    print("\nThank you for running the simulation. Goodbye!")
    exit()

def main():
    print("\nWelcome to Auto Driving Car Simulation!")

    sim = create_simulation()
    
    while True:
        print("\nPlease choose from the following options:")
        print("\n[1] Add a car to field")
        print(f"[2] Run simulation {'(Warning - No cars added yet)' if not sim.cars else ''}")
        print("[3] Start over (Restart simulation)")
        print("[4] Exit simulation")
        choice = input()
        
        if choice == '1':
            
            add_car(sim)
            continue
        
        elif choice == '2':

            if not sim.cars:
                print("\nNo cars added to simulation. Please add at least one car before running.")
                continue

            sim.run()
                
            print("\n[1] Start over (Restart simulation)")
            print("[2] Reset simulation with new cars")
            print("[3] Exit simulation")
            choice = input()

            if choice == '1':
                restart_program()

            elif choice == '2':
                print("\nSimulation reset - Please add new cars!")
                sim.reset()
                continue

            elif choice == '3':
                exit_program()

            else:
                print("\nInvalid input, select between options 1-3.")

        elif choice == '3':
            restart_program()

        elif choice == '4':
            exit_program()

        else:
            print("\nInvalid input, select between options 1-4.")


# -------------- Program Execution ---------------

if __name__ == "__main__":
    main()
