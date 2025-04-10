#example of modrian code found online, has time imported to measure execution time
import pandas as pd
import time

start_time=time.time()

k=3

data=pd.read_csv('data.csv')

print(data.head())

def mondrian(data,k):
    partition=[]

    if(len(data)<=2*k-1):
        partition.append(data)
        return [data]
    
    #define QIs
    qis=['Age']

    #sort by QIs
    data=data.sort_values(by=qis)

    #number of total values
    si=data['Age'].count()
    
    mid=si//2

    lhs=data[:mid]
    rhs=data[mid:]

    partition.extend(mondrian(lhs, k))
    partition.extend(mondrian(rhs,k))

    return partition

results_partitions=mondrian(data,k)

results_final=[]

for i, partition in enumerate(results_partitions,start=1):
    part_min=partition['Age'].min()
    part_max=partition['Age'].max()

    gen=f"[{part_min}-{part_max}]"

    partition['Age']=gen
    
    results_final.append(partition)

    print(f"Partition, length={len(partition)}:")
    if(len(partition)<k):
       print("Error: partition too small")
    else:
        print(partition)

anonymized_data=pd.concat(results_final,ignore_index=True)
anonymized_data.to_csv('anonymized_data.csv',index=False)
    
end_time=time.time()
print(f"Execution time: {end_time-start_time} seconds") 
