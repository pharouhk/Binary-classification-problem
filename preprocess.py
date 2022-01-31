import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import LabelEncoder
from collections import Counter


def count_rowise_nulls(data):
    """
    Function that counts the number of nulls in the last three cells in a row of a dataframe
    :param data: takes the dataframe as input
    return: count of nulls
    """
    cnt_nulls = [] #list to hold the count of non nulls
    row_len = data.shape[0] #the number of rows in the dataset
    col_len = len(data.columns) #the number of columns
    for i in range(row_len):
        each_row = data.iloc[i,:] #gets an array of each row
        if any(list(each_row.isnull())[-3:]): #checks if any of the last 3 row values are null, which includes the class label
            cnt_nulls.append(each_row[-3:].isnull().sum()) #stores the number of nulls in the last 3 adjacent cells
        else:
            cnt_nulls.append(0) #this is executed if there is no null in the last 3 values in the row
    return cnt_nulls

def get_dtypes(data):
	"""
	Function that gets the actual data type for each column in a dataframe
    :param data: takes the dataframe as input
    return: a dictionary of the data types
	"""
	column_data_types = {} #this dictionary will hold the data type for each column 
	for col in data.columns:
		data_types = [] 
		for val in data[col]:#looping through the values in each column
			try:
				data_types.append(type(int(val))) #we would try to convert to an integer 
			except:
				data_types.append(type(val))  #if the above operation fails we exit and store the data type 
		count_dict = dict(Counter(data_types)) #this counts the occurence of each data type in each column
		col_dtype = max(count_dict, key=count_dict.get) #this variable stores the highest occuring data type
		column_data_types[col] = col_dtype
	return column_data_types


def data_relocation(data, col_types, null_condition):
	"""
	This function relocates the data from the point of malformation to the assumed position as part of the
	data cleaning process.
	:param data: the dataframe to be cleaned
	:param col_types: the dictionary of the prevalent data types
	:null_condition: the count of nulls
	return: doesn't return any value but updates the dataframe in-memory
	"""
	col_types_val = list(col_types.values()) #getting the dtypes and storing it as a list
	length = data.shape[0] #storing the number of rows
	for ind, num in zip(range(length),null_condition): #this will loop through each row and null_condition
	    if num == 1: #this allows us to focus on missing class label instances for now
	        start_indices = [] #creates a place holder to store the column index of where the malformation began
	        row_array = list(data.iloc[ind,:].values) #stores the original malformed row values
	        for i, val in zip(range(len(row_array)), row_array): #loops through each row value
	            try:
	                col_types_val[i](val) #this tries to apply the prevailing column type to each value
	            except:
	                start_indices.append(i) #this is executed once the above operation fails which registers the \
	                #index of a variable with the wrong data type.
	        start_index = start_indices[0] #this retrieves the first index only which marks the beginning of the malformation
	        
	        #the logic below keeps all values before the start_index, replaces the value of the start index with null\
	        #then relocates the original values to the next cell
	        new_row_array = list(row_array[:start_index] + [np.nan] + row_array[start_index:-1])
	        data.loc[ind,:] = new_row_array #the dataframe is updated with the new row


def preprocess_categorical(data, features):
	for col in features:
		data[col].replace({0:'0'}, inplace=True)#replace the filled null values as string ero
		le = LabelEncoder() # Create an instance of label Encoder.
		data[col] = le.fit_transform(data[col]) #fit and transform the variable to numeric
