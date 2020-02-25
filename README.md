# Disaster Response Pipeline Project

<h2>Table of Contents</h2>
Libraries Used: Files Description Datasets and Inputs My Questions Data Science Approuch Algo used: My findings Acknowledgments and thanks

<h3>Background</h3>
The project aim is to use tweets used in disasters and their labels, to process them in a ML model. To then deploy the model to be used with an API to categorize new messages to 36 different labels.
The files provided below need to be cleaned and then mergeed into one data set for processing. A sql lite database will be created to store the data and then retrevied for the modeling part. 
To use tweets that are related to disasters, to merge

<h3> Libraries</h3>
Libraries Used: The project was done on Jupyter Notebook and Python 3.0, below are the libraries used:

1. re
2. sqlite2
3. pandas
4. pickple
5. sklearn
6. nltk
7. sqlalchemy
8. numpy

<h3>Files Description</h3>
1. messages.csv - file with all the msg used to train the ML model
2. categories.csv - 36 categories or labels of the messages.
3. disaster_categories.csv - all categories of the dataset
4. disaster_messages.csv - all messages of the dataset
5. process_data.py - script to preprocess the data, and also clean and concat them togther.
6. DisasterResponse.db: sqLite database containing messages and categories
7. train_classifier.py: script to read in the db and train the model, and output a pickle file.
8. classifier.pkl: output of ML model
9. run.py: script to read from the db and run the web app

<h3>Approuch</h3>
1. To build an ETL to clean and preprocess the files, and then ready for modeling
2. To take in the ready file and place in a sql DB for future training and modeling.
3. To read in the ready files from db to train the RF classfier pipeline and out a pickle file, to be used in the API.

<h3> Running the Scripts</h3>
To run the ML model, run the below scprit in your command line:
1. <code>python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db</code>




