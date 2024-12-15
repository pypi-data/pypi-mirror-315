## vizexpln

### Description

A low-code tool for data visualization and interpretation that seamlessly combines the power of Jupyter Notebooks and AI. It provides an intuitive user interface on notebook that enables users to create visualizations, and generate insights from their data. This makes your exploratory data analysis simple and fast. Powered with Gemini multi-model to generate insights from your visualizations 

### Installation

To install vizexpln using pip, run the following command:

```
pip install vizexpln
```

### Example Usage

Once package is installed, you can import the `VizUI` class and create an instance of it. The `VizUI` class takes a Pandas DataFrame as input and provides a user interface for creating visualizations, and generating insights.
To generate insights from your plot, create a Gemini API key and add it in .env file at your notebook folder

```.env
GOOGLE_API_KEY = <add your key>
THIS IS OPTIONAL, You can still make visualizations
```

```python
import pandas as pd
from vizexpln.UI import VizUI

# Load a Pandas DataFrame from a CSV file
df = pd.read_csv("abc.csv")

# Create an instance of the AnalysisUI class
ui = VizUI(df)

# Show the user interface
ui.show()
```
