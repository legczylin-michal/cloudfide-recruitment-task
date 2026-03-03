# import pandas for DataFrame
import pandas as pd
# import sys for error prints
import sys

# solution
def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """ Creates new column according to transformation formula based on existing columns """

    # validate new column name
    for character in new_column:
        # allow only alpchabetical signs and underscore
        if not (character.isalpha() or character == "_"):
            print(f"ERROR: Invalid new_column name: \"{new_column}\"", file=sys.stderr)
            return pd.DataFrame([])

    # remove leading and trailing white spaces from transformation formula
    expr = role.strip()

    # define a sequence of colums names involved in transformation formula as well as operations
    sequence = []
    # currently read column name
    name = ""
    # iterate over transformation formula
    for character in expr:
        # ignore whitespaces
        if character.isspace():
            continue
        # collect alphabetical signs and underscores to retrieve singe column name
        elif character.isalpha() or character == "_":
            name += character
        # if operation sign encountered, add read column name, add operation sign and reset column name
        elif character in ["+", "-", "*"]:
            sequence.append(name)
            sequence.append(character)
            name = ""
        # otherwise raise an error
        else:
            print(f"ERROR: Unallowed character encountered in role: \"{character}\"", file=sys.stderr)
            return pd.DataFrame([])
    # do not forget to add the last column name read
    sequence.append(name)

    # column names used in transformation formula
    desired_columns_names_set = set(sequence).difference(set(["+", "-", "*"]))
    # column names present in dataframe
    present_columns_names_set = set(df.columns)
    # column names to be used and not present in dataframe
    diff = desired_columns_names_set.difference(present_columns_names_set)
    # if there are some columns to be used yet they are not present in dataframe, then raise an error
    if len(diff) != 0:
        print(f"ERROR: Columns not present in dataframe were encountered: {diff}", file=sys.stderr)
        return pd.DataFrame([])

    # substitute column names into respective and actual columns from dataframe 
    series = [el if el in ["+", "-", "*"] else df[el] for el in sequence]

    # since multiplication has higher priority of action let's deal with it first
    i = 0
    while i < len(series):
        # if multiplication encountered
        if type(series[i]) == str and series[i] == "*":
            # modify first operand so it becomes result of multiplication
            series[i - 1] = series[i - 1] * series[i + 1]
            # remove second operand
            series.pop(i + 1)
            # remove operator
            series.pop(i)
            # update index accordingly
            i -= 2
        i += 1

    # addition and substraction
    i = 0
    while i < len(series):
        # if addition encountered
        if type(series[i]) == str and series[i] == "+":
            # modify first operand so it becomes result of addition
            series[i - 1] = series[i - 1] + series[i + 1]
            # remove second operand
            series.pop(i + 1)
            # remove operator
            series.pop(i)
            # update index accordingly
            i -= 2
        # if substraction encountered
        elif type(series[i]) == str and series[i] == "-":
            # modify first operand so it becomes result of substraction
            series[i - 1] = series[i - 1] - series[i + 1]
            # remove second operand
            series.pop(i + 1)
            # remove operator
            series.pop(i)
            # update index accordingly
            i -= 2
        i += 1

    # prepare the result
    result = df.copy()
    # create the target column
    result[new_column] = series[0]

    # return the result
    return result