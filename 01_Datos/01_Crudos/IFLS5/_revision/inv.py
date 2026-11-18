import pyreadstat, os, sys, glob
base=os.path.expanduser("~/mnt/Proyecto Final/01_Datos/01_Crudos/IFLS5")
out=[]
for sub in ["Household Data","Community Data"]:
    for f in sorted(glob.glob(f"{base}/{sub}/*.dta")):
        with open(f,'rb') as fh: b=fh.read(30)
        ver = b[0] if b[0]!=ord('<') else b.split(b'<release>')[1][:3].decode()
        try:
            _,m=pyreadstat.read_dta(f,metadataonly=True)
            out.append((sub[:4],os.path.basename(f),m.number_rows,m.number_columns,ver,round(os.path.getsize(f)/1e6,1)))
        except Exception as e:
            out.append((sub[:4],os.path.basename(f),'ERR',str(e)[:60],ver,0))
import csv
with open(os.path.expanduser("~/w5/inventario.tsv"),"w") as fh:
    w=csv.writer(fh,delimiter="\t"); w.writerow(["grupo","archivo","filas","cols","version","MB"]); w.writerows(out)
