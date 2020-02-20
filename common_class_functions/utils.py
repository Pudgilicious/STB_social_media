def insert_into_table(table, col_names, entry):
    """
    @type table: str
    @param table: name of the DB table
    @type col_names: list of str
    @param col_names: relevant column names of DB table
    @type entry: list of str
    @param entry: variables to be inserted into DB table
    @return: the generated SQL command
    """
    if len(col_names) != len(entry):
        return print('Error: number of arguments do not match.')
    
    output_string = 'INSERT INTO {} ('.format(table)
    
    for col in col_names:
        output_string += col
        if col != col_names[-1]:
            output_string += ', '
    
    output_string += ') VALUES ('
    
    for item in entry:
        output_string += '"{}"'.format(item)
        if item != entry[-1]:
            output_string += ', '

    output_string += ')'
    
    return output_string