import re,glob,os,csv
D=os.path.expanduser("~/mnt/Proyecto Final/01_Datos/01_Crudos/IFLS5/Documentation")
cb={}
for f in glob.glob(D+"/IFLS5_hh_codebooks/*.txt")+glob.glob(D+"/IFLS5_cf_codebooks/*.txt"):
    txt=open(f,encoding="latin-1").read()
    m=re.search(r"recs\s*\n\s*-+\n(.*?)\n\s*(USER SUPPORT|-{20})",txt,re.S)
    if not m: print("sin lista:",os.path.basename(f)); continue
    for line in m.group(1).splitlines():
        mm=re.match(r"\s+([A-Za-z0-9_]+)\s+(.*?)\s*([\d,]+)\s*$",line)
        if mm: cb[mm.group(1).lower()]=(int(mm.group(3).replace(",","")),os.path.basename(f))
        elif line.strip(): print("?",os.path.basename(f),line.strip()[:80])
inv={r["archivo"][:-4]:r for r in csv.DictReader(open(os.path.expanduser("~/w5/inventario.tsv")),delimiter="\t")}
print("en codebook:",len(cb),"archivos:",len(inv))
for k in sorted(set(cb)|set(inv)):
    a=cb.get(k); b=inv.get(k)
    if a is None: print("SOLO ARCHIVO",k,b["filas"])
    elif b is None: print("SOLO CODEBOOK",k,a)
    elif int(b["filas"])!=a[0]: print("DIFIERE",k,"archivo",b["filas"],"codebook",a[0])
