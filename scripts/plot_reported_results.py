from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,"axes.spines.right":False})
with (R/"results/main_results.csv").open() as f: rows=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(9,4.3));fig.patch.set_facecolor("white")
y=[float(r["mean_top1"])*100 for r in rows];err=[float(r["sd_across_seeds"])*100 for r in rows]
ax.bar([r["experiment"] for r in rows],y,yerr=err,capsize=4,color=["#12998b" if r["normalization"]=="1" else "#99a9bb" for r in rows],width=.65)
for i,v in enumerate(y): ax.text(i,v+err[i]+2,f"{v:.2f}".replace(".", ","),ha="center",fontsize=10)
ax.set_ylim(0,90);ax.set_ylabel("Akurasi top-1 (%)");ax.set_title("Perbandingan konfigurasi preprocessing",loc="left",weight="bold",pad=15)
ax.set_axisbelow(True);ax.grid(axis="y",alpha=.15)
fig.text(.12,.015,"Hijau: memakai normalisasi. Galat: SD antar-3 seed atas rata-rata LOSO. Sumber: Tabel 4.8.",fontsize=9,color="#475569")
fig.tight_layout(rect=(0,.05,1,1));fig.savefig(R/"assets/accuracy.png",dpi=180);plt.close(fig)
with (R/"results/e7_signer_results.csv").open() as f: rows=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(9,3.4))
y=[float(r["mean_top1"])*100 for r in rows];err=[float(r["sd_across_seeds"])*100 for r in rows]
ax.bar(["Signer "+r["signer"] for r in rows],y,yerr=err,capsize=5,color=["#334e68","#334e68","#c26c38","#334e68"],width=.5)
for i,v in enumerate(y): ax.text(i,v+err[i]+2,f"{v:.2f}".replace(".", ","),ha="center",fontsize=10)
ax.set_ylim(0,105);ax.set_ylabel("Akurasi top-1 (%)");ax.set_title("Performa E7 pada setiap signer uji",loc="left",weight="bold",pad=15)
ax.set_axisbelow(True);ax.grid(axis="y",alpha=.15)
fig.text(.12,.015,"Batang: rata-rata 3 seed per signer. Galat: SD antar-seed. Sumber: Tabel 4.13.",fontsize=9,color="#475569")
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(R/"assets/signers.png",dpi=180);plt.close(fig)
