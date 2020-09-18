import pandas as pd
import re

machines = pd.read_csv('TCO reference - C-Machines.csv')
rates = pd.read_csv('TCO reference - O-Rates.csv')

csv_to_read = input('path to csv file: ')

#function to detect column names



df = pd.read_csv(csv_to_read)
#Main component
def sud(nunits, rate):
  n30, remaining = int(nunits)//744, int(nunits)%744
  n15, remaining = remaining//360, remaining%360
  h30, h15, h0 = n30*744, n15*360, remaining
  final = (0.7*h30/nunits + 0.85*h15/nunits + remaining/nunits)*rate
  return final#Returns normalized rate after sud

ratedict = {
    'box': 'List-price',
    'heavy': 'Commitment-1yr',
    'spot': 'Preemptible-use'
}

ssd_rate = {
    'box' : 0.08,
    'heavy' : 0.051,
    'spot' : 0.048
}

gpu_rates = {
    'NVIDIA Tesla K80':{
        'box' : 0.45,
        'heavy' : 0.283, 
        'spot' : 0.135
    },
    'NVIDIA Tesla V100':{
        'box' : 2.48,
        'heavy' : 1.562,
        'spot' : 0.74,
    },
    # 'NVIDIA GRID K520':{
    #     'box' : 2.48,
    #     'heavy' : 1.562,
    #     'spot' : 0.74,
    # },
    # 'NVIDIA Tesla M60':{
    #     'box' : 2.48,
    #     'heavy' : 1.562,
    #     'spot' : 0.74,
    # },
    # 'NVIDIA T4 Tensor Core':{
    #     'box' : 2.48,
    #     'heavy' : 1.562,
    #     'spot' : 0.74,
    # }
}

region_dict = {
    'USW2' : 'us-west1',
    'APS2' : 'australia-southeast1',
    'USE1' : 'us-east-1'
}

testmode = False

sud_dict = {
    'GPU' : True,
    'All' : True,
}
def parseusage(row):
  usagetype = ''
  val = row[columnnames['usage']]
  if 'BoxUsage' in val:
    usagetype = 'box'
  elif 'HeavyUsage' in val:
    usagetype = 'heavy'
  elif 'SpotUsage' in val:
    usagetype = 'spot'
  # print(val)
  if row[columnnames['productname']]=='Amazon Elastic MapReduce':
    usagetype = 'spot'
  try:
    region, rest = val.split('-')
  except:
    region, rest = 'USE1', val
    return pd.Series([0]*8)
  try:
    usage, machine = rest.split(':')
  except:
    usage, machine = rest, ''
    return pd.Series([0]*8)
  machine = machine.replace('.elasticsearch', '')
  gcpmachine = machines[machines['API Name']==machine].iloc[0]
  gcpmachine_name = [gcpmachine['Family'].upper(), gcpmachine['Type'].capitalize(), gcpmachine['Memory'], gcpmachine['vCPUs']]
  if gcpmachine_name[1]=='Standard' or gcpmachine_name[1]=='Highmem' or gcpmachine_name[1]=='Highcpu':
    gcpmachine_name[1] = 'Predefined'
  if gcpmachine_name[1] not in ['Small', 'Micro', 'Medium']:
    rates_cpu = rates[(rates['Family']==gcpmachine_name[0])&(rates['Type']==gcpmachine_name[1])&(rates['Metric']=='vCPUs')&(rates['Code']==region_dict[region])].iloc[0][ratedict[usagetype]].replace('$', '')
    rates_mem = rates[(rates['Family']==gcpmachine_name[0])&(rates['Type']==gcpmachine_name[1])&(rates['Metric']=='Memory')&(rates['Code']==region_dict[region])].iloc[0][ratedict[usagetype]].replace('$', '')
    gcp_rate = gcpmachine_name[2]*float(rates_mem)+gcpmachine_name[3]*float(rates_cpu)
    if machine.startswith('p'):
      if gcpmachine['GPU model']=='NVIDIA Tesla K80':
        gcp_rate+=int(gcpmachine['GPUs'])*gpu_rates['NVIDIA Tesla K80'][usagetype]
      elif gcpmachine['GPU model']=='NVIDIA Tesla V100':
        gcp_rate+=int(gcpmachine['GPUs'])*gpu_rates['NVIDIA Tesla V100'][usagetype]
  else:
    gcp_rate = float(rates[(rates['Family']==gcpmachine_name[0])&(rates['Type']==gcpmachine_name[1])].iloc[0][ratedict[usagetype]].replace('$', ''))
  original_rate = gcp_rate
  if row[columnnames['rate']]:
    nunits = row[columnnames['cost']]/row[columnnames['rate']]
    if usagetype=='heavy' or usagetype=='box':
      gcp_rate = sud(nunits, gcp_rate)
  else:
    nunits = 0
  ssd_cost = 0
  if gcpmachine['Instance Storage']!=0 and gcpmachine['SSD/HDD?']=='SSD':
    ssd_cost +=int(gcpmachine['Instance Storage'])*ssd_rate[usagetype]*(nunits//744)
  sud_savings = nunits*(original_rate-gcp_rate)
  # print(ssd_cost, int(gcpmachine['Instance Storage']), ssd_rate[usagetype], nunits, nunits//744)
  returner = [nunits]+gcpmachine_name[:2]+[gcp_rate, nunits*gcp_rate+ssd_cost, sud_savings, ssd_cost, sud_savings/(nunits*original_rate)*100]
  return pd.Series(returner)

columnnames = {
  'usage' : 'lineItem/UsageType',
  'cost' : 'lineItem/UnblendedCost',
  'rate' : 'UnblendedRate',
  'description': 'lineItem/LineItemDescription',
  'quantity' : 'lineItem/UsageAmount',
  'productname' : 'product/ProductName',
}

# columnnames = {
#       'usage' : 'UsageType',
#       'cost' : 'TotalCost',
#       'rate' : 'UnblendedRate',
#       'type' : 'ItemType',
#       'description': 'ItemDescription',
#       'quantity' : 'UsageQuantity',
#       'productname' : 'ProductCode',
#   }

# for key in columnnames:
# 	columnnames[key] = input('Enter column name for {}: '.format(key))

df['UnblendedRate'] = df[columnnames['cost']]/df[columnnames['quantity']]
grouped = df.groupby([columnnames['usage'], columnnames['description'], columnnames['productname']]).agg({columnnames['cost']:'sum', columnnames['rate']:'mean', columnnames['quantity']:'sum'}).reset_index()
boxusage = grouped[grouped[columnnames['usage']].str.contains('BoxUsage')].sort_values(columnnames['usage'])
heavyusage = grouped[grouped[columnnames['usage']].str.contains('HeavyUsage')].sort_values(columnnames['usage'])
spotusage = grouped[grouped[columnnames['usage']].str.contains('SpotUsage')].sort_values(columnnames['usage'])
if len(boxusage):
  boxusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = boxusage.apply(parseusage, axis=1)
  print('Boxusage', sum(boxusage[columnnames['cost']]), sum(boxusage['gcp_cost']))
if len(heavyusage):
  heavyusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = heavyusage.apply(parseusage, axis=1)
  print('Heavyusage', sum(heavyusage[columnnames['cost']]), sum(heavyusage['gcp_cost']))
if len(spotusage):
  spotusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = spotusage.apply(parseusage, axis=1)
  print('Spotusage', sum(spotusage[columnnames['cost']]), sum(spotusage['gcp_cost']))