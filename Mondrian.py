#Mondrian algorithm
def mondrian(data, k):
    partition = []
    if len(data) <= 2 * k - 1:
        return [data]
    #sort by the predefined quasidenfier 
    data = data.sort_values(by=['Age'])
    #define partition point
    mid = len(data) // 2
    #split the sorted data left and right
    lhs = data[:mid]
    rhs = data[mid:]
    #splits each half until k anonymity condition is met
    partition.extend(mondrian(lhs, k))
    partition.extend(mondrian(rhs, k))
    return partition