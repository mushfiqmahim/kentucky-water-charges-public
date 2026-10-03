from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
import json,hashlib,numpy as np,pandas as pd
from scipy.stats import t
from check_inputs import validate_inputs
validate_inputs()
P=Path(__file__).resolve().parents[1];O=P/'results';O.mkdir(exist_ok=True)
r=pd.read_csv(P/'data/Source_Verification_Register_v4.csv',dtype={'utility_id':str});p=pd.read_csv(P/'data/analysis_inputs_v4.csv',dtype={'utility_id':str})
for v in r.itertuples():
 for q in [2000,4000,6000]:
  amount=Decimal(str(v.minimum));left=max(0,q-int(v.included_gallons))
  for width,rate in json.loads(v.applicable_blocks_per_1000):
   take=left if width is None else min(left,width);amount+=Decimal(take)*Decimal(rate)/1000;left-=take
  assert not left
  base=float(amount.quantize(Decimal('.01'),rounding=ROUND_HALF_UP));full=float((amount+Decimal(str(v.applied_extra))+Decimal(str(v.extra_per_1000))*q/1000).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
  assert abs(base-getattr(v,f'base_{q}'))<1e-8 and abs(full-getattr(v,f'total_{q}'))<1e-8
  mask=p.utility_id.eq(v.utility_id)&p.gallons.eq(q);p.loc[mask,f'base_bill_{v.year}']=base;p.loc[mask,f'charge_inclusive_bill_or_scenario_{v.year}']=full
b19='charge_inclusive_bill_or_scenario_2019';b24='charge_inclusive_bill_or_scenario_2024'
def transform(z):
 z=z.copy();z['account_pct']=100*(z['2024']/z['2019']-1);z['x']=100*np.log(z['2024']/z['2019']);z['ln_n19']=np.log(z['2019']);z['ln_bill19']=np.log(z[b19]);z['y_full']=100*np.log(z[b24]/z[b19]);z['y_base']=100*np.log(z.base_bill_2024/z.base_bill_2019);z['full_pct_change']=100*(z[b24]/z[b19]-1);z['bill_change_dollars']=z[b24]-z[b19];z['real_pct_change']=100*((z[b24]/z[b19])/(315.605/256.974)-1);return z
p=transform(p)
def fit(z,label,y='y_full',controls=('ln_n19',),weighted=False):
 X=np.column_stack([np.ones(len(z)),z.x,*[z[c] for c in controls]]);Y=z[y].to_numpy();w=z.design_weight.to_numpy() if weighted else np.ones(len(z));A=X*np.sqrt(w[:,None]);v=Y*np.sqrt(w);inv=np.linalg.pinv(A);beta=inv@v;e=v-A@beta;h=np.sum(A*inv.T,axis=1);n,k=A.shape;cov=(inv*(e/(1-h))[None,:])@(inv*(e/(1-h))[None,:]).T;se=np.sqrt(np.diag(cov));crit=t.ppf(.975,n-k);names=['intercept','x',*controls]
 return {'model':label,'n':n,'df':n-k,'slope':float(beta[1]),'se_HC3':float(se[1]),'ci_low':float(beta[1]-crit*se[1]),'ci_high':float(beta[1]+crit*se[1]),'p':float(2*t.sf(abs(beta[1]/se[1]),n-k)),'r2':float(1-e@e/np.sum(w*(Y-np.average(Y,weights=w))**2)),'coefficients':{name:{'estimate':float(beta[i]),'HC3_SE':float(se[i]),'CI95':[float(beta[i]-crit*se[i]),float(beta[i]+crit*se[i])]} for i,name in enumerate(names)}}
def models(z):
 s=z[(z.gallons==4000)&z.main_eligible];b=z[(z.gallons==4000)&z.price_status.eq('supported')]
 out=[fit(s,'Primary'),fit(s,'Unadjusted',controls=()),fit(b,'Broader supported'),fit(s,'Base only',y='y_base'),fit(s,'Add log initial charge',controls=('ln_n19','ln_bill19')),fit(s,'Add raw initial charge',controls=('ln_n19',b19)),fit(s,'Original design weights',weighted=True),fit(s,'Dollar change',y='bill_change_dollars'),fit(s[s.utility_id!='23300'],'Omit Hyden-Leslie')]
 for q in [2000,6000]:out.append(fit(z[(z.gallons==q)&z.main_eligible],f'{q} gallons'))
 out.append(fit(s[s.arc_mixed==0],'Exclude mixed; ARC adjusted',controls=('ln_n19','arc_all')));out.append(fit(pd.concat([s,z[(z.gallons==4000)&z.utility_id.eq('25000')]]),'Martin conditional scenario'));return out
new=models(p);(O/'models_v4.json').write_text(json.dumps(new,indent=2));out=pd.DataFrame([{k:v for k,v in x.items() if k!='coefficients'} for x in new]);out.to_csv(O/'models_v4.csv',index=False)
# Independently recompute current HC3 with normal equations.
checks=[]
for version,z in [('v4',p)]:
 for label,mask in [('Primary',z.main_eligible),('Broader supported',z.price_status.eq('supported'))]:
  s=z[z.gallons.eq(4000)&mask];X=np.column_stack([np.ones(len(s)),s.x,s.ln_n19]);Y=s.y_full.to_numpy();bread=np.linalg.inv(X.T@X);beta=bread@X.T@Y;e=Y-X@beta;h=np.diag(X@bread@X.T);meat=sum(np.outer(row,row)*(err/(1-lev))**2 for row,err,lev in zip(X,e,h));se=np.sqrt(np.diag(bread@meat@bread));ci=beta[1]+np.array([-1,1])*t.ppf(.975,len(s)-3)*se[1];ref=next(x for x in new if x['model']==label);assert abs(beta[1]-ref['slope'])<1e-9 and np.allclose(ci,[ref['ci_low'],ref['ci_high']],atol=1e-9,rtol=0);checks.append({'version':version,'model':label,'slope':float(beta[1]),'ci':ci.tolist(),'agreement_tolerance':1e-9})
(O/'independent_numerical_checks.json').write_text(json.dumps(checks,indent=2))
ng=[];geo=[];levels=[]
for version,z in [('v4',p)]:
 s=z[(z.gallons==4000)&z.main_eligible]
 for band in [0,.1,1]:
  low=s[s.account_pct < -band];high=s[s.account_pct > band];ng.append({'version':version,'band_percent':band,'decline_n':len(low),'neutral_n':sum(s.account_pct.abs()<=band),'growth_n':len(high),'decline_median':low.full_pct_change.median(),'growth_median':high.full_pct_change.median(),'gap_pp':low.full_pct_change.median()-high.full_pct_change.median()})
 for label,ids in [('All',[]),('Omit Estill',['21500']),('Omit Powell',['28300']),('Omit both',['21500','28300'])]:geo.append({'version':version,**{k:v for k,v in fit(s[~s.utility_id.isin(ids)],label).items() if k!='coefficients'}})
 for group,zz in [('Declining',s[s.account_pct<0]),('Growing',s[s.account_pct>0])]:levels.append({'version':version,'group':group,'n':len(zz),'mean_accounts_2019':zz['2019'].mean(),'mean_charge_2019':zz[b19].mean(),'mean_charge_2024':zz[b24].mean(),'median_charge_2019':zz[b19].median(),'median_charge_2024':zz[b24].median(),'mean_dollar_change':zz.bill_change_dollars.mean(),'median_pct_growth':zz.full_pct_change.median(),'median_real_growth':zz.real_pct_change.median()})
pd.DataFrame(ng).to_csv(O/'neutral_band_diagnostics.csv',index=False);pd.DataFrame(geo).to_csv(O/'geographic_omission_diagnostics.csv',index=False);pd.DataFrame(levels).to_csv(O/'group_levels.csv',index=False)
s=p[(p.gallons==4000)&p.main_eligible];assert len(s)==20
loo=pd.DataFrame([{'omitted':v.utility_name,'utility_id':v.utility_id,**{k:w for k,w in fit(s[s.utility_id!=v.utility_id],'Leave one out').items() if k!='coefficients'}} for v in s.itertuples()]);loo.to_csv(O/'leave_one_out_v4.csv',index=False)
X=np.column_stack([np.ones(len(s)),s.x,s.ln_n19]);pi=np.linalg.pinv(X);res=s.y_full-X@(pi@s.y_full);h=np.sum(X*pi.T,axis=1);mse=np.sum(res**2)/(len(s)-3);inf=s[['utility_id','utility_name']].copy();inf['leverage']=h;inf['cooks_distance']=res**2/(3*mse)*h/(1-h)**2;inf.to_csv(O/'influence_v4.csv',index=False)
p.to_csv(O/'analysis_panel_v4.csv',index=False);s.to_csv(O/'primary_districts_v4.csv',index=False)
bridge=s[['utility_id','utility_name','base_bill_2019','base_bill_2024',b19,b24]].copy();bridge['delta_base']=bridge.base_bill_2024-bridge.base_bill_2019;bridge['delta_total']=bridge[b24]-bridge[b19];bridge['delta_extras']=bridge.delta_total-bridge.delta_base;bridge.to_csv(O/'price_bridge_v4.csv',index=False)
summary={'primary':new[0],'bridge':bridge[['delta_base','delta_extras','delta_total']].sum().to_dict(),'loo_range':[loo.slope.min(),loo.slope.max()],'max_cook':inf.loc[inf.cooks_distance.idxmax(),'utility_name'],'mean_charge_2019':s[b19].mean(),'mean_charge_2024':s[b24].mean(),'mean_pct_growth':s.full_pct_change.mean(),'median_accounts_2019':s['2019'].median(),'arc_all':int(s.arc_all.sum()),'mixed':int(s.arc_mixed.sum())};(O/'summary_v4.json').write_text(json.dumps(summary,indent=2))
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10});(P/'results/figures').mkdir(exist_ok=True);fig,ax=plt.subplots(figsize=(7,4.3));ax.scatter(s.x,s.y_full,color='#245c78');coef=np.polyfit(s.x,s.y_full,1);xx=np.linspace(s.x.min(),s.x.max(),100);ax.plot(xx,np.polyval(coef,xx),color='#555555',lw=1)
for uid,label in [('23300','Hyden-Leslie'),('19400','Knott'),('28300','Powell')]:
 rr=s[s.utility_id==uid].iloc[0];ax.annotate(label,(rr.x,rr.y_full),xytext=(4,5),textcoords='offset points',fontsize=8)
ax.set(xlabel='Residential-account change (100 × natural log ratio)',ylabel='Benchmark charge growth (100 × natural log ratio)');ax.axvline(0,color='.8',lw=.6);fig.tight_layout()
for ext in ['png','pdf']:fig.savefig(P/f'results/figures/figure1_association.{ext}',dpi=180)
plt.close(fig);show=out[out.model.isin(['Primary','Broader supported','Base only','Add log initial charge','Omit Hyden-Leslie','2000 gallons','6000 gallons'])].iloc[::-1];fig,ax=plt.subplots(figsize=(7,4.2));ax.errorbar(show.slope,range(len(show)),xerr=np.array([show.slope-show.ci_low,show.ci_high-show.slope]),fmt='o',color='#245c78',capsize=3);ax.set_yticks(range(len(show)),show.model);ax.axvline(0,color='.5',ls='--',lw=.8);ax.set_xlabel('Account-growth coefficient and 95% HC3 interval');fig.tight_layout()
for ext in ['png','pdf']:fig.savefig(P/f'results/figures/figure2_sensitivity.{ext}',dpi=180)
print(out[['model','n','slope','ci_low','ci_high']].to_string(index=False));print(json.dumps(summary,indent=2));print(pd.DataFrame(ng).to_string(index=False))
