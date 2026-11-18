import pyreadstat, os, glob, itertools, csv, numpy as np, pandas as pd, sys, time
base=os.path.expanduser("~/mnt/Proyecto Final/01_Datos/01_Crudos/IFLS5")
ID=["hhid14","pid14","pidlink","commid14","fcode14","mkid14","fcode","fcode_a","fcode_inf","time_occ","pid"]
import os.path
OUT=os.path.expanduser("~/w5/llaves.tsv")
done=set(l.split("\t")[0] for l in open(OUT)) if os.path.exists(OUT) else set()
res=[]
T0=time.time()
files=sorted(glob.glob(f"{base}/Household Data/*.dta"))+sorted(glob.glob(f"{base}/Community Data/*.dta"))
for f in files:
    t=time.time(); n=os.path.basename(f)[:-4]
    if n in done: continue
    if time.time()-T0>140: break
    df,m=pyreadstat.read_dta(f)
    cols=list(df.columns)
    big=sum(int((pd.to_numeric(df[c],errors='coerce').abs()>1e90).sum()) for c in cols if df[c].dtype!=object)
    objnum=[c for c in cols if df[c].dtype==object and df[c].notna().any() and pd.to_numeric(df[c].dropna(),errors='coerce').notna().all() and c not in ID and not c.startswith(("hhid","commid","pidlink","fcode","mkid","kec","kab","prov","sc0"))]
    base_ids=[c for c in ["hhid14","pid14","pidlink","commid14","mkid14","fcode14","fcode","fcode_inf","fcode_a"] if c in cols]
    typ=[c for c in cols if c.endswith("type") or c in ("time_occ","nt_num","movenum","kwn","kwn_num","ch05","ba63a","bx63a","ep05","ep06","tk28year","day","cadrenum","fascode","prmgrd","scdgrade","c0","c16a","c18a","e10evt","dhtype")]
    found=None
    cands=[]
    for k in range(1,4):
        for comb in itertools.combinations(base_ids+typ,k):
            cands.append(list(comb))
    for c in cands:
        if df[c].isna().any().any(): 
            continue
        if not df.duplicated(c).any(): found=c; break
    res.append([n,len(df),len(cols),"+".join(found) if found else "no determinada",big,len(objnum),";".join(objnum[:5]),"|".join(typ)])
    print(n,len(df),found,big,len(objnum),round(time.time()-t,1),flush=True)
    with open(OUT,"a") as fh: csv.writer(fh,delimiter="\t").writerow(res[-1])
