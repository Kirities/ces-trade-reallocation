"""Render evidence figures in PNG and SVG using archived calculations."""
from pathlib import Path
import csv, sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from trade_model import allocate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
BLUE='#0072B2'; ORANGE='#B34B00'; GREEN='#00765E'; GREY='#5C6470'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#253247','text.color':'#253247','svg.fonttype':'none','svg.hashsalt':'vietnam-trade-reallocation','savefig.dpi':180})

def export(fig,name,caption):
    fig.text(0.02,0.012,caption,fontsize=8,color=GREY)
    for ext in ['png','svg']: fig.savefig(OUT/f'{name}.{ext}',facecolor='white',metadata={'Date':None})
    svg=OUT/f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8',newline='\n')
    plt.close(fig)

def read(name):
    return [{k:float(v) for k,v in row.items()} for row in csv.DictReader((ROOT/'results'/name).open())]

a=read('annual_indicators.csv'); y=[r['year'] for r in a]
fig,axs=plt.subplots(1,2,figsize=(11.8,4.7)); fig.subplots_adjust(left=.08,right=.98,bottom=.20,top=.84,wspace=.28)
for key,label,col,style in [('vietnam','Vietnam',BLUE,'-'),('china','China',ORANGE,'--')]:
    axs[0].plot(y,[r[f'{key}_index_2017'] for r in a],label=label,color=col,linestyle=style,marker='o',markersize=3)
    axs[1].plot(y,[100*r[f'{key}_share'] for r in a],label=label,color=col,linestyle=style,marker='o',markersize=3)
for ax in axs:
    ax.axvspan(2018,2024,color='#E6ECF2',alpha=.5,zorder=0); ax.set_xlim(2010,2024); ax.set_xticks([2010,2014,2017,2020,2024]); ax.grid(axis='y',alpha=.18); ax.set_xlabel('Year'); ax.legend(frameon=False)
axs[0].set(title='A  Nominal U.S. imports by origin',ylabel='Index (2017 = 100)',ylim=(0,320))
axs[1].set(title='B  Shares of total U.S. goods imports',ylabel='Import share (%)',ylim=(0,25))
fig.suptitle('Vietnam gained market share as U.S. sourcing shifted',fontsize=15,fontweight='bold',y=.96)
export(fig,'trade_reallocation','Observed annual data, 2010-2024. Shading marks 2018 onward; it does not identify a tariff effect. Source: U.S. Census Bureau.')

d=read('growth_decomposition.csv'); d=next(r for r in d if r['start']==2017 and r['end']==2024)
fig,ax=plt.subplots(figsize=(8.3,4.6)); fig.subplots_adjust(left=.13,right=.97,bottom=.22,top=.82)
vals=[d['market_size_musd']/1000,d['share_shift_musd']/1000,d['change_musd']/1000]
bars=ax.bar(['U.S. import market growth','Vietnam share shift','Total change'],vals,color=[GREY,BLUE,GREEN],width=.55)
for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+1.8,f'{v:.2f}',ha='center',fontweight='bold')
ax.set(ylabel='Change in nominal imports (USD billion)',ylim=(0,105),title='Accounting for Vietnam\'s 2017-2024 export expansion'); ax.grid(axis='y',alpha=.15)
export(fig,'growth_decomposition','Symmetric decomposition of the USD 89.84bn increase. The share component is an accounting residual, not a causal tariff estimate.')

s=json.loads((ROOT/'results/summary.json').read_text()); w=(s['vietnam_share_2017'],s['china_share_2017'],1-s['vietnam_share_2017']-s['china_share_2017'])
fig,axs=plt.subplots(1,2,figsize=(11.8,4.8)); fig.subplots_adjust(left=.08,right=.97,bottom=.21,top=.82,wspace=.27)
x=np.linspace(1,1.2,101)
for sig,col,ls in [(2,GREY,':'),(4,BLUE,'-'),(6,ORANGE,'--'),(8,GREEN,'-.')]:
    gains=[100*(allocate(w,sig,(0,.25,0),(c,1,1)).customs[0]/(100*w[0])-1) for c in x]
    axs[0].plot(100*(x-1),gains,label=f'Elasticity = {sig}',color=col,linestyle=ls)
axs[0].axhline(0,color=GREY,linewidth=.8); axs[0].set(title='A  Sensitivity to Vietnam cost increases',xlabel='Vietnam producer-cost increase (%)',ylabel='Vietnam customs receipts change (%)'); axs[0].legend(frameon=False,fontsize=8)
for tv,col,ls,label in [(0,BLUE,'-','Vietnam tariff = 0%'),(.1,ORANGE,'--','Vietnam tariff = 10%')]:
    m=allocate(w,4,(tv,.25,0))
    z=np.linspace(.25,.75,101)
    axs[1].plot(100*z,z*m.customs[0],color=col,linestyle=ls,label=label)
axs[1].set(title='B  Retained-value accounting sensitivity',xlabel='Assumed domestic value-added share (%)',ylabel='DVA proxy per USD 100 import expenditure',ylim=(0,2)); axs[1].legend(frameon=False,fontsize=8)
for ax in axs: ax.grid(alpha=.15)
fig.suptitle('The opportunity is conditional on costs and market access',fontsize=15,fontweight='bold',y=.96)
export(fig,'scenario_sensitivity','Illustrative CES model, 2017 weights; China tariff = 25%. Panel B elasticity = 4. Parameters are assumptions, not historical estimates.')

fig,ax=plt.subplots(figsize=(8.6,4.8)); fig.subplots_adjust(left=.11,right=.86,bottom=.22,top=.83)
costs=np.linspace(1,1.2,81); tcs=np.linspace(0,.4,81)
z=np.array([[100*(allocate(w,4,(0,t,0),(c,1,1)).customs[0]/(100*w[0])-1) for c in costs] for t in tcs])
im=ax.imshow(z,origin='lower',aspect='auto',extent=[0,20,0,40],cmap='BrBG',vmin=-50,vmax=50)
cs=ax.contour(100*(costs-1),100*tcs,z,levels=[0],colors=['#111111'],linewidths=1.5); ax.clabel(cs,fmt={0:'No receipt gain'},fontsize=9)
ax.set(xlabel='Vietnam producer-cost increase (%)',ylabel='Illustrative China tariff (%)',title='Cost increases can erase the tariff advantage')
fig.colorbar(im,ax=ax,label='Vietnam customs receipts change (%)')
export(fig,'cost_tariff_frontier','Illustrative CES model; 2017 weights, elasticity = 4, Vietnam tariff = 0%. Black line is the numerically evaluated zero-gain contour.')
print('Rendered 4 figures in PNG and SVG')
