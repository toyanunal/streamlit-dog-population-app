# Dog Population Streamlit App

## Description
This Streamlit application uses an agent-based model to simulate and visualize the growth and management of stray dog populations. The model incorporates assumptions and parameters from the presentation "Agent-based models to identify and evaluate dog population management strategies" by AnyLogic. Users can adjust various parameters such as initial population size, birth interval, litter size, maturity age, and spay probability to see their effects on the dog population over time.

## Deployed Application
* [https://toyanunal-streamlit-dog-populat-dog-population-streamlit-jgvirj.streamlit.app/](https://toyanunal-streamlit-dog-populat-dog-population-streamlit-jgvirj.streamlit.app/)

## Technologies Used
* VSCode (as text editor)
* Chrome (as web browser)
* Python (as programming language)
* Streamlit (as framework)
* Mesa (for agent-based modeling)
* Plotly (for data visualization)

## Installation

### Prerequisites
* Python 3.6 or higher
* pip (Python package installer)

### Setup
1. Navigate to your projects directory.
2. Clone the repository and install the required packages:
    ```sh
    git clone https://github.com/toyanunal/streamlit-dog-population-app.git
    cd streamlit-dog-population-app
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```sh
    streamlit run dog_population_streamlit.py
    ```

2. Open your web browser and go to `http://localhost:8501` to access the app.

## Parameters and Assumptions
The model is based on the following assumptions and parameters, inspired by the "Agent-based models to identify and evaluate dog population management strategies" presentation:

### Model Parameters
| Name                          | Value                 | Source   |
|-------------------------------|-----------------------|----------|
| Weaning Period                | 8 weeks               | AnyLogic |
| Female Dog Puberty            | 8 months              | AnyLogic |
| Male Dog Puberty              | 10 months             | AnyLogic |
| Oestrous Duration             | 9 days                | AnyLogic |
| Time to New Proestrous        | 7 months              | AnyLogic |
| Gestation Period              | 63 days               | AnyLogic |
| Litter Size                   | 6 puppies             | AnyLogic |
| Sex Ratio for New Litters     | 2:1 (male:female)     | AnyLogic |
| Mortality Rate                | 0.33 per year         | AnyLogic |
| Cost Female Spay              | $40 US                | AnyLogic |
| Initial Dog Population Size   | 100 (50 male, 50 female) | Custom |
| Spay Probability              | Adjustable            | Custom |

## Screenshots
### Home page
![image](https://github.com/toyanunal/streamlit-dog-population-app/assets/59750131/96965843-bea6-48b9-810d-5564c740160d)

## References
* ["Agent-based models to identify and evaluate dog population management strategies"](https://www.anylogic.com/upload/iblock/e11/e11d627ebb120af6a0369ae8d55799fd.pdf) by AnyLogic.

This README provides an overview of your Dog Population Streamlit App, detailing the technologies used, installation steps, usage instructions, and the parameters and assumptions of the model. Additionally, it acknowledges the presentation that inspired the model's assumptions and parameters.
