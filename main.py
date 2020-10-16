import pandas as pd
import re
from ratecard import *
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from math import ceil

machines = pd.read_csv('TCO reference - C-Machines.csv')
rates = pd.read_csv('TCO reference - O-Rates.csv')

# csv_to_read = input('path to csv file: ')
# df = pd.read_csv(csv_to_read)

#provisional test on Alphasense
df = pd.read_csv('bill_examples/alphasense_rowitems.csv')

#function to detect column names
def detect_column_names(dataframe):
  usage_options = ['lineItem/UsageType', 'UsageType']
  cost_options = ['lineItem/UnblendedCost', 'TotalCost']
  rate_options = ['BlendedRate', 'UnblendedRate', 'lineItem/UnblendedRate']
  description_options = ['lineItem/LineItemDescription', 'ItemDescription']
  quantity_options = ['lineItem/UsageAmount', 'UsageQuantity']
  productname_options = ['product/ProductName', 'ProductCode']
  type_options = ['ItemType']

  columnnames = {
  'usage': list(set(usage_options).intersection(set(dataframe.columns)))[0],
  'cost': list(set(cost_options).intersection(set(dataframe.columns)))[0],
  'rate': list(set(rate_options).intersection(set(dataframe.columns)))[0],
  'description': list(set(description_options).intersection(set(dataframe.columns)))[0],
  'quantity': list(set(quantity_options).intersection(set(dataframe.columns)))[0],
  'productname': list(set(productname_options).intersection(set(dataframe.columns)))[0],
  # 'type': set(type_options).intersection(set(dataframe.columns)))[0],
  }
  return columnnames


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


testmode = False

sud_dict = {
    'GPU' : True,
    'All' : True,
}

def get_usagetype(row):

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

  return usagetype

def parsecompute(row):
  val = row[columnnames['usage']]
  usagetype = get_usagetype(row)
  try:
    region_aws, rest = val.split('-')
  except:
    region, rest = 'USW2', val
    # return pd.Series([0]*8)
  try:
    usage, machine = rest.split(':')
  except:
    usage, machine = rest, ''
    return pd.Series([0]*8)
  region_gcp = region_dict[region_aws]
  machine = machine.replace('.elasticsearch', '')
  gcpmachine = machines[machines['API Name']==machine].iloc[0]
  gcpmachine_name = [gcpmachine['Family'].lower(), gcpmachine['Type'].lower(), gcpmachine['Memory'], gcpmachine['vCPUs']]
  if gcpmachine_name[1]=='Standard' or gcpmachine_name[1]=='Highmem' or gcpmachine_name[1]=='Highcpu':
    gcpmachine_name[1] = 'Predefined'

  if gcpmachine_name[1] not in ['small', 'micro', 'medium']:
    machine_id = '{}-{}'.format(gcpmachine_name[0],gcpmachine_name[1])
    rates_cpu = compute_ratecard[usagetype]['{}-vcpus'.format(machine_id)][region_gcp]
    rates_mem = compute_ratecard[usagetype]['{}-memory'.format(machine_id)][region_gcp]
    gcp_rate = gcpmachine_name[2]*float(rates_mem)+gcpmachine_name[3]*float(rates_cpu)
    if machine.startswith('p'):
      if gcpmachine['GPU model']=='NVIDIA Tesla K80':
        gcp_rate+=int(gcpmachine['GPUs'])*gpu_rates['NVIDIA Tesla K80'][usagetype]
      elif gcpmachine['GPU model']=='NVIDIA Tesla V100':
        gcp_rate+=int(gcpmachine['GPUs'])*gpu_rates['NVIDIA Tesla V100'][usagetype]
  else:
    machine_id = '{}-{}'.format(gcpmachine_name[0],gcpmachine_name[1])
    gcp_rate = compute_ratecard[usagetype][machine_id][region_gcp]
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

columnnames = detect_column_names(df)

# for key in columnnames:
# 	columnnames[key] = input('Enter column name for {}: '.format(key))

df[columnnames['rate']] = df[columnnames['cost']]/df[columnnames['quantity']]
grouped = df.groupby([columnnames['usage'], columnnames['description'], columnnames['productname']]).agg({columnnames['cost']:'sum', columnnames['rate']:'mean', columnnames['quantity']:'sum'}).reset_index()
boxusage = grouped[grouped[columnnames['usage']].str.contains('BoxUsage')].sort_values(columnnames['usage'])
heavyusage = grouped[(grouped[columnnames['usage']].str.contains('HeavyUsage'))&(~grouped[columnnames['usage']].str.contains('HeavyUsage:db'))].sort_values(columnnames['usage'])
spotusage = grouped[grouped[columnnames['usage']].str.contains('SpotUsage')].sort_values(columnnames['usage'])
if len(boxusage):
  boxusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = boxusage.apply(parsecompute, axis=1)
  # print('Boxusage', sum(boxusage[columnnames['cost']]), sum(boxusage['gcp_cost']))
if len(heavyusage):
  heavyusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = heavyusage.apply(parsecompute, axis=1)
  # print('Heavyusage', sum(heavyusage[columnnames['cost']]), sum(heavyusage['gcp_cost']))
if len(spotusage):
  spotusage[['nunits', 'gcp_family', 'gcp_type', 'gcp_rate', 'gcp_cost', 'sud_savings', 'ssd_cost', 'sud_savings_percentage']] = spotusage.apply(parsecompute, axis=1)
  # print('Spotusage', sum(spotusage[columnnames['cost']]), sum(spotusage['gcp_cost']))

######################################################################################################################################################

persistentdisk = grouped[(grouped[columnnames['usage']].str.contains('VolumeUsage.gp2')) | (grouped[columnnames['usage']].str.contains('SnapshotUsage')) | ((grouped[columnnames['usage']].str.contains('VolumeUsage'))&(grouped[columnnames['description']].str.contains('Magnetic provisioned storage')))].sort_values(columnnames['usage'])


def parsepd(row):
  value = row[columnnames['usage']]
  if not value.startswith('EBS'):
    region, cat = value.split('-EBS:')
  else:
    region, cat = 'USE1', value.replace('EBS:', '')
  if cat=='SnapshotUsage':
    return pd.Series([persistentdisk_ratecard['snapshot'][region_dict[region]], row[columnnames['quantity']]*persistentdisk_ratecard['snapshot'][region_dict[region]]])
  elif cat=='VolumeUsage.gp2':
    return pd.Series([persistentdisk_ratecard['gp2'][region_dict[region]], row[columnnames['quantity']]*persistentdisk_ratecard['gp2'][region_dict[region]]])
  elif 'Magnetic provisioned storage' in row[columnnames['description']]:
    return pd.Series([persistentdisk_ratecard['magnetic'][region_dict[region]], row[columnnames['quantity']]*persistentdisk_ratecard['magnetic'][region_dict[region]]])


persistentdisk[['GCP_rate', 'GCP_cost']] = persistentdisk.apply(parsepd, axis=1)

print("PD AWS: ", sum(persistentdisk[columnnames['cost']]), " PD GCP: ", sum(persistentdisk['GCP_cost']))


######################################################################################################################################################

def nat_gateway_cost(dataframe):
  nat_gateway_bytes = dataframe[dataframe[columnnames['usage']].str.contains('NatGateway-Bytes')].copy()
  nat_gateway_hours = dataframe[dataframe[columnnames['usage']].str.contains('NatGateway-Hours')].copy()
  nat_gateway_hours['ninstances'] = nat_gateway_hours[columnnames['quantity']]/720
  ninstances = sum(nat_gateway_hours['ninstances'])
  ngb = sum(nat_gateway_bytes[columnnames['quantity']])
  if ninstances<=32:
    cost = ninstances*nat_gateway_ratecard['us-vm-low']*720+ngb*nat_gateway_ratecard['us-bytes']
  else:
    cost = nat_gateway_ratecard['us-vm-high']*720+ngb*nat_gateway_ratecard['us-bytes']
  return [cost, sum(nat_gateway_bytes[columnnames['cost']])+sum(nat_gateway_hours[columnnames['cost']])]

nat_gcp, nat_aws = nat_gateway_cost(grouped)#df is the grouped dataframe

#feed this input into the viz tool
######################################################################################################################################################

idleaddress = grouped[grouped[columnnames['usage']].str.contains('ElasticIP:IdleAddress')]

def idle_addresses_cost(row):
  ninstances = int(row[columnnames['quantity']]/720)
  return pd.Series([ninstances*idle_addresses_ratecard['us']*720, row[columnnames['cost']]])

idleaddress[['gcp_cost', 'aws_cost']] = idleaddress.apply(idle_addresses_cost, axis=1)

######################################################################################################################################################

loadbalancer = grouped[((grouped[columnnames['usage']].str.contains('DataProcessing-Bytes'))|(grouped[columnnames['usage']].str.contains('LCUUsage'))|(grouped[columnnames['usage']].str.contains('LoadBalancerUsage')))&(grouped[columnnames['productname']]=='Amazon Elastic Compute Cloud')]

def loadbalancer_cost(row):
  rowsplit = row[columnnames['usage']].split('-')
  region_gcp = region_dict[rowsplit[0]]
  usecase = '-'.join(rowsplit[1:])
  return pd.Series([region_gcp, usecase])

loadbalancer[['region', 'usecase']] = loadbalancer.apply(loadbalancer_cost, axis=1)

load_grouped = loadbalancer.groupby(['region', 'usecase']).sum().reset_index()[['region', 'usecase', columnnames['quantity']]]

def loadgrouped_cost(row):
  region = row['region']
  usecase = row['usecase']
  quantity = row[columnnames['quantity']]
  if usecase=='LoadBalancerUsage':
    nrules = ceil(quantity/720)
    cost = loadbalancer_ratecard['forwarding_rules'][region]*720
    if nrules>5:
      cost+=(nrules-5)*loadbalancer_ratecard['forwarding_rules_extra'][region]*720
    return pd.Series([nrules, cost])
  else:
    cost = quantity*loadbalancer_ratecard['ingress'][region]
    return pd.Series([quantity, cost])

load_grouped[['rules/gb', 'gcp_cost']] = load_grouped.apply(loadgrouped_cost, axis=1)
aws_loadbalancer = round(sum(loadbalancer[columnnames['cost']]),2)
gcp_loadbalancer = round(sum(load_grouped['gcp_cost']),2)
######################################################################################################################################################

wb = Workbook()

report_filename = 'tco_report.xlsx'

ws_summary = wb.active
ws_summary.title = 'Summary'

ws_summary.append([''])
ws_summary.append(['', 'Summarized View - Total Cost of Ownership on GCP'])
center = ws_summary['B2']
center.alignment = Alignment(horizontal='center')
ws_summary.merge_cells(start_row=2, start_column=2, end_row=2, end_column=7)
ws_summary.append(['', 'Compute', 'GCE - Preemptible VMs', '${}'.format(round(sum(spotusage['gcp_cost']), 2)), 'EC2 - Spot Usage', '${}'.format(round(sum(spotusage[columnnames['cost']]), 2))])
ws_summary.append(['', 'Compute', 'GCE - Regular VMs', '${}'.format(round(sum(boxusage['gcp_cost'])+sum(heavyusage['gcp_cost']), 2)), 'EC2 - Spot Usage', '${}'.format(round(sum(boxusage[columnnames['cost']])+sum(heavyusage[columnnames['cost']]), 2))])

ws_box = wb.create_sheet(title='BoxUsage')
box_pyxl = dataframe_to_rows(boxusage)
for r_idx, row in enumerate(box_pyxl, 1):
    for c_idx, value in enumerate(row, 1):
         ws_box.cell(row=r_idx, column=c_idx, value=value)

ws_heavy = wb.create_sheet(title='HeavyUsage')
heavy_pyxl = dataframe_to_rows(heavyusage)
for r_idx, row in enumerate(heavy_pyxl, 1):
    for c_idx, value in enumerate(row, 1):
         ws_heavy.cell(row=r_idx, column=c_idx, value=value)

ws_spot = wb.create_sheet(title='SpotUsage')
spot_pyxl = dataframe_to_rows(spotusage)
for r_idx, row in enumerate(spot_pyxl, 1):
    for c_idx, value in enumerate(row, 1):
         ws_spot.cell(row=r_idx, column=c_idx, value=value)

ws_summary.append(['', '', '', '${}'.format(round(sum(spotusage['gcp_cost'])+sum(boxusage['gcp_cost'])+sum(heavyusage['gcp_cost']), 2)), '', '${}'.format(round(sum(spotusage[columnnames['cost']])+sum(boxusage[columnnames['cost']])+sum(heavyusage[columnnames['cost']]), 2))])

ws_summary.append(['', 'Storage', 'Persistent Disk', '${}'.format(round(sum(persistentdisk['GCP_cost']), 2)), 'Elastic Block Storage', '${}'.format(round(sum(persistentdisk[columnnames['cost']]), 2))])
ws_pd = wb.create_sheet(title='Persistent Disk')
pd_pyxl = dataframe_to_rows(persistentdisk)
for r_idx, row in enumerate(pd_pyxl, 1):
    for c_idx, value in enumerate(row, 1):
         ws_pd.cell(row=r_idx, column=c_idx, value=value)

ws_summary.append(['', 'Storage', 'Cloud Storage', '', 'Simple Storage Service(S3)', ''])
ws_summary.append(['', 'Storage', 'Filestore', '', 'Elastic File Storage', ''])
ws_summary.append(['', '', '', '', '', ''])
ws_summary.append(['', 'Networking', 'Cloud Load Balancer', '${}'.format(gcp_loadbalancer), 'Elastic Load Balancer', '${}'.format(aws_loadbalancer)])
ws_summary.append(['', 'Networking', 'Cloud NAT', '${}'.format(round(nat_gcp,2)), 'NAT Gateway', '${}'.format(round(nat_aws,2))])
ws_summary.append(['', 'Networking', 'Network Egress', '', 'Data Transfer', ''])
ws_summary.append(['', 'Networking', 'Idle Addresseses', '${}'.format(round(sum(idleaddress['gcp_cost']), 2)), 'Idle Addresses', '${}'.format(round(sum(idleaddress['aws_cost']), 2))])
ws_summary.append(['', '', '', '', '', ''])
ws_summary.append(['', 'DB Services', 'Cloud SQL', '', 'Amazon RDS', ''])
ws_summary.append(['', 'DB Services', 'Search on GCP', '', 'ElasticSearch', ''])
ws_summary.append(['', 'DB Services', 'Cache on GCP', '', 'Elasticache', ''])
ws_summary.append(['', 'DB Services', 'BigQuery', '', 'Redshit', ''])
ws_summary.append(['', '', '', '', '', ''])
ws_summary.append(['', 'Support', 'GCP Support', '', 'AWS Support Business', ''])
ws_summary.append(['', 'Misc', 'Unclassified', '', 'Misc', ''])
ws_summary.append(['', '', '', '', '', ''])
ws_summary.append(['', 'GCP Monthly ', '', 'AWS Monthly', '', ''])

wb.save(filename=report_filename)
