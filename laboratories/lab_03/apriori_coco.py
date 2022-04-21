import json
from itertools import combinations
#from tqdm import tqdm

#### ---- Functions ---- ####
def apriori(transaction_list:list, minsup:float=0.02):
    # set of items
    itemset = list(scan(transaction_list).keys()) 
    
    # store not frequent candidates
    not_freq_candidates = [] 
    frequents = []
    
    print("Lunghezza itemset:",len(itemset))
    for i in range(1, len(itemset)):
        print(f"iterazione {i} di {len(itemset)}")
        
        # scan the transaction list to count the support
        supports = scan(transaction_list, k=i)
        supports = {k:v/len(transaction_list) for k,v in supports.items()}
        
        # prune itemsets if below minsup, return frequents and not frequents ones 
        pruned_supports, not_freq = prune(supports, minsup, return_not_freq=True)
        frequents.append(pruned_supports)
        not_freq_candidates.append(list(not_freq.keys()))
        
        # generate new candidates of length k + 1
        candidates = gen_candidates(transaction_list, k=i+1)
        
        # candidates that do not contain a subset not frequent
        pruned_candidates = [] 
        
        # check if the generated candidates contains elements not frequent
        for ca in candidates:
            ca_k_comb = combinations(ca, i-1)
            for comb in ca_k_comb:
                if comb in not_freq_candidates:
                    continue
                else:
                    pruned_candidates.append(ca)
        
        # break statement
        if i == len(itemset) - 1:
            break
        
    return frequents

def scan(transaction_list:list, k:int=1) -> dict:
    # create a dictionary with items as keys
    # and supports as values
    d = dict()
    for transaction in transaction_list:
        # create combinations (without repetition) of size k
        combs = combinations(transaction, k)
        for item in combs:
            d[item] = d.get(item, 0) + 1
    return d


def gen_candidates(items_list:list, k:int=1):
    # generate candidates of length k
    return list(combinations(items_list, k))

def prune(k_itemsets:dict, minsup:int=1, return_not_freq:bool=False):
    # create 2 dictionaries, one containing frequent itemsets
    # while the other one has the non frequent ones
    freq = {k:v for k,v in k_itemsets.items() if v >= minsup}
    not_freq = {k:v for k,v in k_itemsets.items() if v < minsup}
    
    # optional parameter that will return frequent dict 
    # as well as the not frequent one
    if return_not_freq:
        return freq, not_freq 
    return freq
#### ---- Functions ---- ####


with open("coco.json", "r") as f:
    coco = json.load(f) # list of dictionaries. 1 dict for each image
    
    annot = []
    for image in coco:
        annot.append(tuple(image['annotations']))

    results = apriori(annot, .02)
    
print(results)