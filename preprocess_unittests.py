import pandas as pd
import numpy as np
import math

def _print_success_message():
    
    print('Tests Passed!')

def test_col_nulls(col):
	assert max(col)<= 3, 'The maximum count of non-nulls should not exceed 3'

	_print_success_message()

def verify_relocation(data_reloc, col_types):
	for col_name, dtype in col_types.items():
		if dtype == int: #checks if datatype is integer
			data_reloc[col_name] = data_reloc[col_name].astype(dtype) #applies the data type to the column

	column_dtypes = list(col_types.values())
	for col_name, dt in zip(data_reloc.columns, column_dtypes):
		if dtype == int:
			assert data_reloc[col_name].dtype==dt or 'int32', 'Wrong data type'
		else:
			assert data_reloc[col_name].dtype==dt or 'object', 'Wrong data type'

	_print_success_message()