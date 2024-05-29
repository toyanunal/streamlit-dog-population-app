from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import plotly.graph_objects as go
import streamlit as st

class FemaleDog(Agent):
    def __init__(self, unique_id, model, birth_month, state="Newborn"):
        super().__init__(unique_id, model)
        self.birth_month = birth_month
        self.age = 0
        self.state = state

    def step(self):
        self.age += 1
        if self.random.random() < self.model.mortality_rate / 12:  # Monthly mortality rate
            self.model.schedule.remove(self)
            return

        self.update_state()

        if self.state == "Reproductive" and (self.model.schedule.time - self.birth_month) % self.model.birth_interval == 0:
            self.reproduce()

    def update_state(self):
        if self.state == "Newborn" and self.age >= self.model.female_puberty:
            self.state = "Early Age"
        elif self.state == "Early Age" and self.age >= self.model.maturity_age:
            self.state = "Reproductive"
        elif self.state == "Reproductive" and self.random.random() < self.model.spay_probability:
            self.state = "Spayed"

    def reproduce(self):
        male_ratio = self.model.sex_ratio / (1 + self.model.sex_ratio)
        num_males = int(self.model.litter_size * male_ratio)
        num_females = self.model.litter_size - num_males

        for _ in range(num_females):
            puppy_female = FemaleDog(self.model.next_id(), self.model, self.model.schedule.time)
            self.model.schedule.add(puppy_female)
        for _ in range(num_males):
            puppy_male = MaleDog(self.model.next_id(), self.model, self.model.schedule.time)
            self.model.schedule.add(puppy_male)

class MaleDog(Agent):
    def __init__(self, unique_id, model, birth_month, state="Newborn"):
        super().__init__(unique_id, model)
        self.birth_month = birth_month
        self.age = 0
        self.state = state

    def step(self):
        self.age += 1
        if self.random.random() < self.model.mortality_rate / 12:  # Monthly mortality rate
            self.model.schedule.remove(self)
            return

        self.update_state()

    def update_state(self):
        if self.state == "Newborn" and self.age >= self.model.male_puberty:
            self.state = "Early Age"
        elif self.state == "Early Age" and self.age >= self.model.maturity_age:
            self.state = "Reproductive"

class DogPopulationModel(Model):
    def __init__(self, initial_population, birth_interval, litter_size, female_puberty, male_puberty, maturity_age, spay_probability, sex_ratio, mortality_rate, max_months):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.birth_interval = birth_interval
        self.litter_size = litter_size
        self.female_puberty = female_puberty
        self.male_puberty = male_puberty
        self.maturity_age = maturity_age
        self.spay_probability = spay_probability
        self.sex_ratio = sex_ratio
        self.mortality_rate = mortality_rate
        self.max_months = max_months

        # Create initial dog population
        self.create_initial_population(initial_population)

        self.datacollector = DataCollector(
            model_reporters={"Total Population": lambda m: m.schedule.get_agent_count(),
                             "Female Population": lambda m: sum(isinstance(agent, FemaleDog) for agent in m.schedule.agents)}
        )

    def create_initial_population(self, initial_population):
        num_females = initial_population // 2
        num_males = initial_population - num_females

        female_structure = {
            "Newborn": int(0.1 * num_females),
            "Early Age": int(0.1 * num_females),
            "Reproductive": int(0.1 * num_females),
            "Pregnant": int(0.1 * num_females),
            "Non-Reproductive": int(0.6 * num_females)
        }

        male_structure = {
            "Newborn": int(0.1 * num_males),
            "Early Age": int(0.1 * num_males),
            "Reproductive": int(0.8 * num_males)
        }

        for state, count in female_structure.items():
            for _ in range(count):
                dog_female = FemaleDog(self.next_id(), self, 0, state)
                self.schedule.add(dog_female)

        for state, count in male_structure.items():
            for _ in range(count):
                dog_male = MaleDog(self.next_id(), self, 0, state)
                self.schedule.add(dog_male)

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
    initial_population = st.sidebar.number_input("Initial Population", min_value=1, max_value=1000, value=100, step=10)
    birth_interval = st.sidebar.slider("Birth Interval (months)", min_value=1, max_value=12, value=7, step=1)
    litter_size = st.sidebar.slider("Litter Size", min_value=1, max_value=12, value=6, step=1)
    female_puberty = st.sidebar.slider("Female Dog Puberty (months)", min_value=1, max_value=24, value=8, step=1)
    male_puberty = st.sidebar.slider("Male Dog Puberty (months)", min_value=1, max_value=24, value=10, step=1)
    maturity_age = st.sidebar.slider("Maturity Age (months)", min_value=1, max_value=24, value=12, step=1)
    spay_probability = st.sidebar.slider("Spay Probability", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
    sex_ratio = st.sidebar.slider("Sex Ratio (Males/Females)", min_value=0.10, max_value=10.0, value=2.0, step=0.1)
    mortality_rate = st.sidebar.slider("Mortality Rate (per year)", min_value=0.0, max_value=1.0, value=0.33, step=0.01)
    max_months = st.sidebar.slider("Max Months to Simulate", min_value=1, max_value=120, value=60, step=1)
    return initial_population, birth_interval, litter_size, female_puberty, male_puberty, maturity_age, spay_probability, sex_ratio, mortality_rate, max_months

# Get user input
initial_population, birth_interval, litter_size, female_puberty, male_puberty, maturity_age, spay_probability, sex_ratio, mortality_rate, max_months = get_user_input()

# Initialize the model
model = DogPopulationModel(initial_population, birth_interval, litter_size, female_puberty, male_puberty, maturity_age, spay_probability, sex_ratio, mortality_rate, max_months)
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
