# fpe.py
import pandas as pd
import numpy as np
import numbers
import warnings

warnings.filterwarnings('ignore')

def fpefs(data):
    df = pd.DataFrame(data)
    col = len(df.columns)
    nfeatures = col - 1
    del df  # memory is released
    X = data.iloc[:, 0:nfeatures]
    y = data.iloc[:, -1]
    
    for f in range(nfeatures):
        K = X.iloc[:, f]
        da = K.iloc[0]
        if isinstance(da, (numbers.Number, numbers.Real)):
            K = round(((K - K.min()) / (K.max() - K.min())), 2)
            X.iloc[:, f] = pd.Series(K)
    
    def unique(list1):
        return list(set(list1))
    
    label = unique(y)
    numberOfLabel = len(label)
    Prob = []
    
    for j in range(nfeatures):
        mu, ncount, Pvalue = 0, 0, 0
        dp = pd.Series(X.iloc[:, j])
        md = dp.groupby(dp).apply(lambda px: px.index.tolist()).to_dict()
        ulist = md.keys()
        sizeulist = len(ulist)
        
        for m in ulist:
            mlist = []
            mindex = md[m]
            for idx in mindex:
                if y[idx] not in mlist:
                    mlist.append(y[idx])
                if numberOfLabel == len(mlist):
                    break
            nc = len(mlist)
            if nc < numberOfLabel:
                mu += float(nc) / numberOfLabel
                ncount += 1
        
        if ncount > 0:
            Pvalue = round((1 - (0.5) * ((sizeulist - ncount) / sizeulist + mu / ncount)), 2)
        
        Prob.append(Pvalue)
        print(j, mu, ncount, sizeulist, Pvalue)
    
    Prob = pd.Series(Prob)
    estimatedProbability = pd.concat([pd.DataFrame(X.columns), Prob], axis=1)
    return estimatedProbability
