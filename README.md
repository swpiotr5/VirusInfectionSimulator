# VirusInfectionSimulator

## Project: Simulation of Infection Spread in a Population

### Project Description
The goal of this project is to create a simulation of infection spread in a population, which models the movement of individuals, infection, and interactions between them. The simulation allows for saving and loading the state at any point, enabling users to resume the simulation from a specific point.

The project takes into account two initial cases:
- The initial population and randomly selected individuals do not have immunity.
- The initial population and randomly selected individuals have immunity.

The simulation consists of 25 steps per second, providing smooth animation and accurately representing the progression of infection.

### Design Patterns Used

1. **State Pattern**:
   The "State" pattern is used to model an object that can be in different states. Each state corresponds to a specific behavior of the object. Transitions between states are defined based on certain conditions.

2. **Memento Pattern**:
   The "Memento" pattern is applied to store the state of an object at a specific point in time. It allows saving a "snapshot" of an object's state, which can later be loaded to resume the simulation. The state is encapsulated, and access to it is provided through specialized methods.

### Key Features

- **Infection Simulation**:
  - Models the movement of individuals in space.
  - Models the infection spread between individuals.
  
- **Save and Load State**:
  - Allows saving the simulation state at any point.
  - Loads previously saved states, enabling the continuation of the simulation.

- **Visualization**:
  - Visualizes the movement of individuals.
  - Represents infection status in the population.
  
- **Two Initial Cases**:
  - Individuals do not have immunity.
  - Individuals have immunity.

### Project Structure

- **VirusInfectionSimulator**: The main class responsible for running the simulation.
- **Person**: Class representing an individual in the simulation. Each person can have a health status (sick, healthy, immune).
- **Vector2D**: Class used to model the movement of individuals. Vectors are used to determine direction and speed.
- **Memento**: Class responsible for storing an object's state.
- **State**: Class implementing different states of an object, depending on the phase of the simulation (e.g., infected, healthy, immune).

### Usage Instructions

1. **Cloning the repository**:
   ```bash
   git clone https://github.com/swpiotr5/virusinfectionsimulator.git
   cd virusinfectionsimulator
