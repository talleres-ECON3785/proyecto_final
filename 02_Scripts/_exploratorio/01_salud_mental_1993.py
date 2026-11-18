"""Índice de salud mental IFLS1 (1993). Entrada: 01_Datos/01_Crudos/IFLS1/Household Data. Salida: 01_Datos/02_Procesados/salud_mental_1993.{csv,dta}
Ítems KK05 (libro III): 1 a menudo, 3 a veces, 5 nunca -> 2/1/0; 6/8/9 -> NA.
- sm3_93: insomnio + tristeza + ansiedad (0-6). Ítems que se repiten en IFLS3 (kk04, kk07, kk08) -> índice del panel.
- sm6_93: los 6 ítems de 1993 (0-12). Solo línea base / heterogeneidad.
- triste_93, ansioso_93: 1 si a menudo o a veces.
NA si falta cualquier ítem del índice."""
import pyreadstat as p, pandas as pd, numpy as np, os
base=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # raiz del repo
hh=os.path.join(base,'01_Datos','01_Crudos','IFLS1','Household Data')
rd=lambda f,**k: p.read_dta(os.path.join(hh,f+'.dta'),**k)[0]
kk=rd('buk3kk2')
items={'kk05_a':'insomnio','kk05_b':'fatiga','kk05_c':'irritable','kk05_d':'dolores','kk05_e':'tristeza','kk05_f':'ansiedad'}
d=kk[['pidlink','hhid93','commid93']].copy()
for v,n in items.items(): d[n+'_93']=kk[v].map({1:2,3:1,5:0})
d['sm3_93']=d[['insomnio_93','tristeza_93','ansiedad_93']].sum(axis=1,min_count=3)
d['sm6_93']=d[[n+'_93' for n in items.values()]].sum(axis=1,min_count=6)
d['triste_93']=(d.tristeza_93>=1).where(d.tristeza_93.notna()).astype('float')
d['ansioso_93']=(d.ansiedad_93>=1).where(d.ansiedad_93.notna()).astype('float')
w=rd('indivwt',usecols=['pidlink','smpgrp','respwt','impage'])
r=rd('bukkar2',usecols=['pidlink','ar07','ar02'])
d=d.merge(w,on='pidlink',how='left').merge(r,on='pidlink',how='left')
d['mujer']=d.ar07.map({1:0,3:1}); d=d.rename(columns={'impage':'edad_93','ar02':'parentesco_93'}).drop(columns='ar07')
assert d.pidlink.is_unique and len(d)==len(kk)
out=os.path.join(base,'01_Datos','02_Procesados','salud_mental_1993')
d.to_csv(out+'.csv',index=False); p.write_dta(d,out+'.dta')
print(len(d)); print(d[['sm3_93','sm6_93','triste_93','ansioso_93']].describe().round(3).to_string())
print('NA sm3',d.sm3_93.isna().sum(),' NA sm6',d.sm6_93.isna().sum())
print(d.sm3_93.value_counts().sort_index().to_dict()); print(d.sm6_93.value_counts().sort_index().to_dict())
print('corr sm3 sm6',d[['sm3_93','sm6_93']].corr().iloc[0,1].round(3))
