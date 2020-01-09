# Boston Crime Analysis

This repository is an analysis of Boston crime using regression, Markov chain, and traveling salesman problem. The analysis also includes the relationship between temperature and crime rate.

## Getting Started

There are two ways to view the analysis. 

First: you can click the analysis folder and go through each .ipynb file.<br/>
Second: you can also download this project and run the application to view the analysis.

### Prerequisites

The project requires some packages.

python: 3.7.6 <br/>
Flask: 1.1.1 <br/>
requests: 2.22.0

### Running the web application

- change the directory to this folder
- run the app.py file

## Analysis

This is a brief detail about data analysis, for full analysis, please kindly visit each file.

### [Data Preprocess](https://github.com/chaipi-chaya/Boston-Crime-Analysis/blob/master/analysis/data_preprocess.ipynb)

I identified missing data and used machine learning for filling null values. Then, I merged two data set into one csv file.

### [Data Analysis Overall](https://github.com/chaipi-chaya/Boston-Crime-Analysis/blob/master/analysis/data_analysis_overall.ipynb)

I used the csv file above to analyze basic information of the data, from data distribution to trend in time series.

### [Crime Pattern](https://github.com/chaipi-chaya/Boston-Crime-Analysis/blob/master/analysis/crime_pattern_analysis.ipynb)

I created the probabilities distribution of districts for each type of crime (Markov Chain) and saved the result for plotting graph in the web application.

### [Regression](https://github.com/chaipi-chaya/Boston-Crime-Analysis/blob/master/analysis/regression_analysis.ipynb)

I analyzed the correlation between weather and crime rate and created a prediction model using linear regression.

### [Travelling Salesman Promblem](https://github.com/chaipi-chaya/Boston-Crime-Analysis/blob/master/analysis/shortest_patrol_route.ipynb)

I used the Traveling salesman model to create the shortest patrol route in district B2.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
