## Next activity and timestamp prediction with LSTM
This repositories focuses on perdicting next activity and timestamp from logistic log using LSTM. The workflow is threefold. We first sample representative data from our logistic log following the method itroduced in the paper **"Selecting Representative Sample Traces from Large Event Logs"**. Then we preprocess the data, create feature set and divide the data into train and test set. Finally we use the data to train LSTM model and evaluate the result. Training the lSTM model is comparable with the benchmark implementation presented in the paper **"Predictive Business Process Monitoring with LSTM Neural Networks"**.

## Installation

The project is implemented with scrips and jupyter notebook both in python and tensorflow. 
- Tensorflow: follow the instruction in the tensorflow website https://www.tensorflow.org/install for installation.
- PM4Py: pip install pm4py

## Reproduction
### Sampling
- Run sampling.py from Sampling repository to get a representative sample dataset (only if data is very large)
### Prediction 
- To include graph properties (the route taken by the cases in the process) in the feature set use the scripts from repository "activity_timestamp_pred_with_routing", otherwise follow the scripts from repository "activity_timestamp_pred".
- Run format_logistic.ipnyb notebook to transform the csv file into correct format
- Run main.ipnyb notebook to preprocess data, create features, train model and evaluate the result.
