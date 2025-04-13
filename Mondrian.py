#Mondrian algorithm
def mondrian(data, k, qi):
    partition = []
    if len(data) <= 2 * k - 1:
        return [data]
    #sort by the given quasi-identifier
    data = data.sort_values(by=[qi])
    mid = len(data) // 2
    lhs = data[:mid]
    rhs = data[mid:]
    partition.extend(mondrian(lhs, k, qi))
    partition.extend(mondrian(rhs, k, qi))
    return partition
