import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Function takes in files to be read as pandas and then merged togther. 
    """
    df1 = pd.read_csv(messages_filepath)
    df2 = pd.read_csv(categories_filepath)
    merged = pd.merge(df1, df2,on='id')
    
    return merged


def clean_data(df):
    categories_df = df.categories.str.split(';', expand=True)
    row = categories_df.iloc[0]
    category_colnames = row.apply(lambda x: x[:-2])
    categories_df.columns = category_colnames
    
    for column in categories_df:
        # set each value to be the last character of the string
        categories_df[column] = categories_df[column].apply(lambda x: x[-1:])

        # convert column from string to numeric
        categories_df[column] =  categories_df[column].astype(int)
        
    df.drop(['categories'], axis=1, inplace=True)
    
    df = pd.concat([df, categories_df], axis=1)
    df.drop_duplicates(subset='id', inplace=True)
    
    return df


def save_data(df, database_filename):
    
    """
    Save the dataframe into a sql db.
    """
    
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('qaiss_df_ready7', engine, index=False)  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()