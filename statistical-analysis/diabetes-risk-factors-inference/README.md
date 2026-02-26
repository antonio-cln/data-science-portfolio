## Directory contents 📂
| Content | Description   |
| --- | --- |
| [analysis.ipynb](./analysis.ipynb)  | Jupyter Notebook containing Python code and visualizations  |
| [analysis.html](https://antonio-cln.github.io/data-science-portfolio/statistical-analysis/diabetes-risk-factors-inference/analysis.html)  | HTML rendered version of the analysis (suggested) |
| [technical-presentation.pdf](./technical-presentation.pdf) | Technical presentation of the findings |

## Analysis Overview 
The goal of this analysis is to identify which health metrics (BMI, Glucose levels, Age, etc.) serve as the strongest predictors for diabetes.  
<br>

#### Tools importing & Data Ingestion
The analysis begins with the setup of Packages and auxiliary functions, ensuring all statistical tools and custom plotting utilities are initialized. This is followed by Dataset loading and presentation, where the raw diabetes data is imported and the initial variables are showed.

#### Data Cleaning
The core processing phase starts with Data cleaning, addressing missing values, data imbalance and general readability.

#### Exploratory Data Analysis
Once refined, the analysis moves into Exploratory Data Analysis, utilizing visualizations to start gathering insights from univariate and bivariate analysis.

#### Statistical Modeling
The modeling stage is split into two distinct parts: Unsupervised Analysis, which seeks to find underlying data pattern hinting at what variables are best predictors of both classes, and Supervised analysis, placing heavy emphasis on model interpretation and performance comparison to determine which variables provide the highest predictive power for an individual having diabetes or not.

#### Conclusions
The analysis ends in the Conclusions chapter that synthesizes the findings from the previous stages to identify the most significant risk factors and possible analysis improvements.
