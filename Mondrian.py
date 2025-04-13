#Mondrian algorithm
def mondrian(data, k, target):
    targetVals = ["age","zip"] # QI variables - hardcoded

    partition = []
    if len(data) <= 2 * k - 1:
        return [data]
    #sort by the predefined quasidenfier 
    data = data.sort_values(by=[targetVals[target]]) # Sorts with respect to age or zip depending on target
    #define partition point
    mid = len(data) // 2
    #split the sorted data left and right
    lhs = data[:mid]
    rhs = data[mid:]
    #splits each half until k anonymity condition is met

    # Partition again wrt. next variable to split on...
    partition.extend(mondrian(lhs, k, (target+1)%2)) 
    partition.extend(mondrian(rhs, k, (target+1)%2))
    return partition