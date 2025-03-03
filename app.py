# ------------ Imports and Variables ------------

import re
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional

DIRECTIONS : List[str] = ['N', 'E', 'S', 'W']  # Clockwise directions


# --------------- Helper Functions ---------------

def rotate_left(direction: str) -> str:

    """
    Rotates the car's given direction 90 degrees to the left.

    Args:
        direction (str): The current direction ('N', 'E', 'S', or 'W').

    Returns:
        str: The new direction after turning left.
    """

    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]

def rotate_right(direction: str) -> str:
    
    """
    Rotates the car's given direction 90 degrees to the left.

    Args:
        direction (str): The current direction ('N', 'E', 'S', or 'W').

    Returns:
        str: The new direction after turning left.
    """

    return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

def move_forward(x: int, y: int, direction: str, width: int, height: int) -> Tuple[int, int]:

    """
    Moves the car forward in its current direction, if within bounds. 
    If out of bounds, returns current position. 

    Args:
        x (int): The current x-coordinate.
        y (int): The current y-coordinate.
        direction (str): The current direction of the car.
        width (int): The width of the simulation grid.
        height (int): The height of the simulation grid.

    Returns:
        Tuple[int, int]: The new (x, y) coordinates after moving.
    """

    if direction == 'N' and y + 1 <= height:
        return x, y + 1
    elif direction == 'S' and y - 1 >= 0:
        return x, y - 1
    elif direction == 'E' and x + 1 <= width:
        return x + 1, y
    elif direction == 'W' and x - 1 >= 0:
        return x - 1, y
    return x, y  # No movement if out of bounds

def is_valid_coordinates(x: str, y: str, sim: Optional['Simulation'] = None) -> bool:

    """
    Validates the given coordinates, ensuring they are string representations of non-negative integers.
    If the sim argument is included for when car coordinates are being validated, checks if car coordinates
    faill within the simulation boundaries.

    Args:
        x (str): The x-coordinate as a string.
        y (str): The y-coordinate as a string.
        sim (Optional[Simulation]): The simulation object for boundary validation.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """

    positive_coordinates = x.isdigit() and int(x) > 0 and y.isdigit() and int(y) > 0
    return positive_coordinates if not sim else int(x) <= sim.width and int(y) <= sim.height
    
def is_valid_commands(commands: str) -> bool:

    """
    Validates the command string, ensuring it contains only L, R, or F.

    Args:
        commands (str): The string of commands.

    Returns:
        bool: True if the command string is valid, False otherwise.
    """

    return bool(re.fullmatch(r"[LRF]+", commands))


# ------------------- Classes --------------------

class Car:

    """
    Represents an autonomous car in the simulation.

    Attributes:
        name (str): The unique identifier for the car.
        x (int): The current x-coordinate of the car on the grid.
        y (int): The current y-coordinate of the car on the grid.
        direction (str): The direction the car is facing ('N', 'E', 'S', 'W').
        commands (List[str]): The list of movement commands ('L', 'R', 'F') to execute.
        collided (bool): Whether the car has collided with another car.
    """

    def __init__(self, name: str, x: int, y: int, direction: str, commands: str) -> None:

        """
        Initializes a Car object with a name, position, direction, and a list of commands.

        Args:
            name (str): The unique name of the car.
            x (int): The initial x-coordinate.
            y (int): The initial y-coordinate.
            direction (str): The initial direction of the car ('N', 'E', 'S', 'W').
            commands (str): A string of movement commands ('L', 'R', 'F').
        """

        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = list(commands)
        self.collided = False
    
    def execute_command(self, command: str, width: int, height: int) -> None:

        """
        Executes a single command ('L', 'R', or 'F') to update the car's position or direction.

        Args:
            command (str): The movement command to execute.
            width (int): The width of the simulation grid (used for boundary checking).
            height (int): The height of the simulation grid (used for boundary checking).
        """

        if self.collided:
            return # Ignores commands if the car has collided
        if command == 'L':
            self.direction = rotate_left(self.direction)
        elif command == 'R':
            self.direction = rotate_right(self.direction)
        elif command == 'F':
            self.x, self.y = move_forward(self.x, self.y, self.direction, width, height)

    def car_details(self, show_commands: bool = False) -> str:

        """
        Returns a formatted string with the car's current details.

        Args:
            show_commands (bool, optional): Whether to include the remaining commands.

        Returns:
            str: A string representation of the car's state.
        """

        return f"Car Name: {self.name} - Position: ({self.x}, {self.y}) - Direction: {self.direction}" \
            + (f" - Commands: {"".join(self.commands)}" if show_commands else "")

class Simulation:

    """
    Represents a simulation environment for autonomous cars moving on a 2D grid.

    Attributes:
        width (int): The width of the simulation grid.
        height (int): The height of the simulation grid.
        cars (List[Car]): A list of all cars in the simulation.
        car_names (Set[str]): A set of unique car names to prevent duplicates.
        positions (Dict[Tuple[int, int], Set[Car]]): 
            A dictionary mapping grid positions (x, y) to sets of cars currently at those positions.
    """

    def __init__(self, width: int, height: int) -> None:

        """
        Initializes the simulation with a given grid size.

        Args:
            width (int): The width of the simulation grid.
            height (int): The height of the simulation grid.
        """

        self.width: int = width
        self.height: int = height
        self.cars: List['Car'] = []
        self.car_names: Set[str] = set()
        self.positions: Dict[Tuple[int, int], Set['Car']] = defaultdict(set)
    
    def add_car(self, name: str, x: int, y: int, direction: str, commands: str) -> None:

        """
        Adds a car to the simulation at a specified position and direction.

        Args:
            name (str): The unique name of the car.
            x (int): The starting x-coordinate of the car.
            y (int): The starting y-coordinate of the car.
            direction (str): The initial direction of the car ('N', 'E', 'S', 'W').
            commands (str): The sequence of commands ('L', 'R', 'F') for the car.
        """

        car = Car(name, x, y, direction, commands)
        self.cars.append(car)
        self.car_names.add(name)
        self.positions[(x, y)].add(car)

    def reset(self) -> None:

        """
        Resets the simulation by removing all cars and clearing positions.
        """

        self.cars.clear()
        self.car_names.clear()
        self.positions.clear()

    def show_cars(self, show_commands = False):

        """
        Displays the current list of cars in the simulation.

        Args:
            show_commands (bool, optional): If True, includes the remaining commands for each car.
        """

        print("\nYour current list of cars are:")
        for car in self.cars:
            print(f"- {car.car_details(show_commands = show_commands)}")

    def run(self) -> bool:

        """
        Runs the simulation, executing each car's commands sequentially.

        Returns:
            bool: True if the simulation runs successfully, False if no cars are present.
        """

        if not self.cars:
            print("\nNo cars added to simulation. Please add at least one car before running.")
            return False
        
        self.show_cars()
        step: int = 0
        max_commands: int = max(len(car.commands) for car in self.cars)
        
        print("\nAfter simulation, the result is:")

        for i in range(max_commands):
            step += 1
            
            for car in self.cars:
                prev_x, prev_y = car.x, car.y

                if not car.collided and car.commands:
                    command = car.commands.pop(0)
                    car.execute_command(command, self.width, self.height)
                    
                    # Collision handling
                    collided_cars = []

                    for collided_car in self.positions[(car.x, car.y)]:
                        if collided_car != car:
                            collided_car.collided = True
                            collided_cars.append(collided_car.name)

                    collided_cars = sorted(collided_cars, reverse = True)
                    
                    if command == "F" and len(collided_cars) > 0:
                        car.collided = True
                        print(f"- {car.name}, collides with {', '.join(collided_cars)} at ({car.x}, {car.y}) at step {step}.")
                        print(f"- {', '.join(collided_cars)}, collides with {car.name} at ({car.x}, {car.y}) at step {step}.")

                    self.positions[(prev_x, prev_y)].remove(car)
                    self.positions[(car.x, car.y)].add(car)

        # Displaying final positions of cars that did not collide
        for car in self.cars:
            if not car.collided:
                print(f"- {car.name}, ({car.x}, {car.y}) {car.direction}")

        return True


# --------- Program Execution Functions ----------

def create_simulation() -> Simulation:

    """
    Prompts the user to enter the dimensions of the simulation grid 
    and creates a new `Simulation` instance.

    The function continuously asks for valid input until the user provides 
    two positive integers for the grid dimensions.

    Returns:
        Simulation: A new simulation instance with the specified width and height.
    """

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

def add_car(sim: Simulation) -> None:

    """
    Prompts the user to enter details for a new car and adds it to the simulation.

    The function ensures that:
    - The car has a unique name.
    - The car's position is within the simulation bounds and unoccupied.
    - The car's direction is valid ('N', 'E', 'S', or 'W').
    - The command sequence contains only valid characters ('L', 'R', 'F').

    The function continuously prompts the user to input appropriate values for the above variables. 

    Args:
        sim (Simulation): The simulation instance where the car will be added.
    """

    valid_name = False
    valid_position = False
    valid_commands = False

    while not valid_name:

        name = input("\nPlease enter the name of the car: ").strip()

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

        x, y, direction = car_values

        if not is_valid_coordinates(x, y, sim):
            print("Invalid car coordinates. Please enter two Positive Integer values within the set simulation bounds.")
            continue

        if direction not in DIRECTIONS:
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

def restart_program() -> None:

    """
    Restarts the simulation by calling the `main` function.

    This function is typically used when the user wants to reset the simulation
    and start fresh with a new grid and cars.

    Side Effects:
        - Prints a restart message to the console.
        - Calls the `main` function to begin a new simulation.
    """
        
    print("\nRestarting simulation...")
    main() # Calls the main function to restart the simulation

def exit_program() -> None:
        
    """
    Terminates the simulation program.

    This function is called when the user chooses to exit, ensuring a graceful shutdown.

    Side Effects:
        - Prints a farewell message to the console.
        - Terminates the program execution using `sys.exit()`.

    Raises:
        SystemExit: This exception is raised to halt program execution.
    """

    print("\nThank you for running the simulation. Goodbye!")
    exit() # Terminates the program

def main() -> None:

    """
    The main entry point for the Auto Driving Car Simulation.

    This function:
    - Initializes a new simulation by prompting the user for grid dimensions.
    - Provides a menu for the user to:
        1. Add cars to the simulation.
        2. Run the simulation.
        3. Restart the simulation.
        4. Exit the simulation.

    The function continuously loops until the user chooses to restart or exit.

    Side Effects:
        - Prints messages and menus to the console.
        - Takes user input for actions.
        - Calls other functions (`add_car`, `restart_program`, `exit_program`, `run`).

    Raises:
        SystemExit: When the user chooses to exit the simulation.
    """

    print("\nWelcome to Auto Driving Car Simulation!")

    # Creates a new simulation grid
    sim = create_simulation()
    
    while True:
        # Displaying menu options
        print("\nPlease choose from the following options:")
        print("\n[1] Add a car to field")
        print(f"[2] Run simulation {'(Warning - No cars added yet)' if not sim.cars else ''}")
        print("[3] Start over (Restart simulation)")
        print("[4] Exit simulation")
        # User menu input
        choice = input()
        
        if choice == '1':
            
            # Adding a car and displaying all cars currently in the simulation
            add_car(sim)
            continue
        
        elif choice == '2':

            # Simulation run-point
            result = sim.run()

            # If no cars added to the simulation, sends user back to previous menu 
            if not result:
                continue
                
            # Post-simulation options
            print("\n[1] Start over (Restart simulation)")
            print("[2] Reset simulation with new cars")
            print("[3] Exit simulation")
            choice = input()

            # Restart program with new simulation and cars
            if choice == '1':
                restart_program()

            # Reset simulation - keeps simulation, resets cars
            elif choice == '2':
                print("\nSimulation reset - Please add new cars!")
                sim.reset()
                continue

            # Closes the program
            elif choice == '3':
                exit_program()

            # Flags invalid user input
            else:
                print("\nInvalid input, select between options 1-3.")

        # Restart program with new simulation and cars
        elif choice == '3':
            restart_program()

        # Closes the program
        elif choice == '4':
            exit_program()

        # Flags invalid user input
        else:
            print("\nInvalid input, select between options 1-4.")


# -------------- Program Execution ---------------

if __name__ == "__main__":
    main()
