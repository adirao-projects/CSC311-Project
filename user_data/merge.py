import numpy as np
uids =  ["71845", "6124931", "3817598", "5288646", "18350315"]

merged = {}

for u in uids:
    merged[u] = {}
    temps = []
    for t in np.arange(0,2.5,0.5):
        merged[u][t] = []
        for i in range(1,5):
            if i == 1:
                i= ""
            else:
                i = f"_v{i}"
            try:
                f = open(f'{u}_real_GPT{i}_{t}.txt', 'r').read().strip('"').strip("'").split('/n')
                merged[u][t]+=f[:]
            except Exception as e:
                print(e)
            
        f = open(f"{u}_real_GPT_sum_{t}.txt", 'w')
        f.write("\n".join(merged[u][t]))
        f.close()
    
        temps += merged[u][t]
        
    f = open(f"{u}_real_GPT_sum_temps.txt", 'w')
    f.write("\n".join(temps))
    f.close()