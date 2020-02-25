import sys
import pandas as pd
import numpy as np
import re
import sqlite3
import pickle
from sqlalchemy import create_engine

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import f1_score
import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def load_data(database_filepath):
    print("this is the answer " +  database_filepath)
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('qaiss_df_ready7', engine)
    print(df.columns)
    X = df.message
    Y = df.iloc[:, 4:]
    category_names = list(df.columns[4:])
    return X, Y, category_names


def tokenize(text):
    """
    The function takes in string and returns a list of words that
    are tokenized, lower_case, and lemmatized.
    """
    #loads one text at a  time, need to loop over.
    text = word_tokenize(text)
    lem = WordNetLemmatizer()
    
    token_list = []
    for t in text:
        text = lem.lemmatize(t).lower()
        if text not in stop_words:
            token_list.append(text)
    
    return token_list


def build_model():
    """
    The function can be used to process the model faster but with no CV.
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
     
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """
    The display function will provide, a classification report on each category of the 36,
    and a total accurracy of the model.
    """
    y_pred = model.predict(X_test)
    
    labels = np.unique(y_pred)
    #confusion_mat = confusion_matrix(y_test, y_pred)
    accuracy = (y_pred == Y_test).mean()
    total_accuracy = (y_pred == Y_test).mean().mean()
    
    #report = classification_report(y_test, y_pred)
    for i in range(len(category_names)):
        print("Label:", category_names[i],"\n", classification_report(Y_test.iloc[:, i].values, y_pred[:, i]))
    
    print("Labels:", labels)
    print("Printing Accuracy of each Category:", accuracy)
    print("Total Accuracy:", total_accuracy)


def save_model(model, model_filepath):
    """
    This function takes in the model and requests a file name to save it on disk.
    """
    pickle.dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()