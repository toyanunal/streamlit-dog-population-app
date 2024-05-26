from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import plotly.graph_objects as go
import streamlit as st

class Dog(Agent):
    def __init__(self, unique_id, model, birth_month):
        super().__init__(unique_id, model)
        self.birth_month = birth_month
        self.age = 0

    def step(self):
        self.age += 1
        if self.age >= self.model.maturity_age and (self.model.schedule.time - self.birth_month) % self.model.birth_interval == 0:
            self.reproduce()

    def reproduce(self):
        for _ in range(self.model.offsprings // 2):
            puppy_female = Dog(self.model.next_id(), self.model, self.model.schedule.time)
            self.model.schedule.add(puppy_female)
        for _ in range(self.model.offsprings // 2):
            puppy_male = Dog(self.model.next_id(), self.model, self.model.schedule.time)
            self.model.schedule.add(puppy_male)

class DogPopulationModel(Model):
    def __init__(self, initial_population, birth_interval, offsprings, maturity_age, max_months):
        super().__init__()  # Initialize the base Model class
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.birth_interval = birth_interval
        self.offsprings = offsprings
        self.maturity_age = maturity_age
        self.max_months = max_months

        # Create initial dog population (split equally between males and females)
        for _ in range(initial_population // 2):
            dog_female = Dog(self.next_id(), self, 0)
            self.schedule.add(dog_female)
        for _ in range(initial_population // 2):
            dog_male = Dog(self.next_id(), self, 0)
            self.schedule.add(dog_male)

        self.datacollector = DataCollector(
            model_reporters={"Total Population": lambda m: m.schedule.get_agent_count()}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self):
        for _ in range(self.max_months):
            self.step()

    def next_id(self):
        self.current_id += 1
        return self.current_id

# Function to get user input
def get_user_input():
    st.sidebar.header("Configure Model Parameters")
    initial_population = st.sidebar.number_input("Initial Population", min_value=1, max_value=1000, value=40, step=10)
    birth_interval = st.sidebar.slider("Birth Interval (months)", min_value=1, max_value=12, value=6, step=1)
    offsprings = st.sidebar.slider("Number of Offsprings per Birth", min_value=1, max_value=12, value=6, step=1)
    maturity_age = st.sidebar.slider("Maturity Age (months)", min_value=1, max_value=24, value=12, step=1)
    max_months = st.sidebar.slider("Max Months to Simulate", min_value=1, max_value=120, value=60, step=1)
    return initial_population, birth_interval, offsprings, maturity_age, max_months

# Get user input
initial_population, birth_interval, offsprings, maturity_age, max_months = get_user_input()

# Initialize the model
model = DogPopulationModel(initial_population, birth_interval, offsprings, maturity_age, max_months)
model.run_model()

# Collect data
population_data = model.datacollector.get_model_vars_dataframe()

# Visualization
st.title("Dog Population Growth Over Time")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=population_data.index,
    y=population_data["Total Population"],
    mode='lines+markers',
    name='Total Population',
    hovertemplate='Months: %{x}<br>Population: %{y}<extra></extra>'
))
fig.update_layout(title='Dog Population Growth Over Time',
                  xaxis_title='Months',
                  yaxis_title='Total Population',
                  yaxis=dict(range=[0, population_data["Total Population"].max() * 1.1]))  # Adjust y-axis to make early population more visible

st.plotly_chart(fig)
