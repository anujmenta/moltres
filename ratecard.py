import requests

resp = requests.get('https://cloudpricingcalculator.appspot.com/static/data/pricelist.json').json()


# region_dict = {
#   'USE1' : 'us-east4',
#   'USE2' : 'us-central1',
#   'USW1' : 'us-west1',
#   'USW2' : 'us-west1',
#   'UGE1' : 'us-east1',
#   'UGW1' : 'us-west1',
#   'CA' : "northamerica-northeast1",
#   'CPT' : 'us-central1',
#   'AP' : 'asia',
#   'APE1' : 'asia-east2',
#   'APN1' : 'asia-northeast1',
#   'APN2' : 'asia-northeast3',
#   'APN3' : 'asia-northeast2',
#   'APS1' : 'asia-southeast1',
#   'APS2' : 'australia-southeast1',
#   'APS3' : 'asia-south1',
#   'CAN1' : 'us-central1',
#   'EUC1' : 'europe-west3',
#   'EUW1' : 'europe-west2',
#   'EUW2' : 'europe-west2',
#   'EUW3' : 'europe-west1',
#   'EUN1' : 'europe-north1',
#   'EUS1' : 'europe-west3',
#   'MES1' : 'us-central1',
#   'SAE1' : 'southamerica-east1',
# }

region_dict = {
  'US' : 'us',
  'USE1' : 'us-east4',
  'USE2' : 'us-central1',
  'USW1' : 'us-west1',
  'USW2' : 'us-west1',
  'UGE1' : 'us-east1',
  'UGW1' : 'us-west1',
  'CPT' : 'us-central1',
  'CA' : "northamerica-northeast1",
  'AP' : 'asia',
  'IN' : 'asia',
  'JP' : 'asia', 
  'ZA' : 'asia', 
  'ME' : 'asia', 
  'SA' : 'southamerica',
  'APE1' : 'asia-east2',
  'APN1' : 'asia-northeast1',
  'APN2' : 'asia-northeast3',
  'APN3' : 'asia-northeast2',
  'APS1' : 'asia-southeast1',
  'AU' : 'australia',
  'APS2' : 'australia-southeast1',
  'APS3' : 'asia-south1',
  'CAN1' : 'us-central1',
  'EU' : 'europe',
  'AFS1' : 'europe',
  'EUC1' : 'europe-west3',
  'EUW1' : 'europe-west2',
  'EUW2' : 'europe-west2',
  'EUW3' : 'europe-west1',
  'EUN1' : 'europe-north1',
  'EUS1' : 'europe-west3',
  'MES1' : 'us-central1',
  'SAE1' : 'southamerica-east1',
}


compute_ratecard = {
	'box':{
		'n1-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-PREDEFINED-VM-CORE"] ,
		'n1-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-PREDEFINED-VM-RAM"] ,
		'n1-custom-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUSTOM-VM-CORE"] ,
		'n1-custom-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUSTOM-VM-RAM"] ,
		'e2-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-PREDEFINED-VM-CORE"] ,
		'e2-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-PREDEFINED-VM-RAM"] ,
		'e2-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MICRO"] ,
		'e2-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-SMALL"] ,
		'e2-medium' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MEDIUM"] ,
		'f1-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-F1-MICRO"] ,
		'g1-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-G1-SMALL"] ,
	},
	'heavy':{
		'n1-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUD-3-YEAR-CPU"] ,
		'n1-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUD-3-YEAR-RAM"] ,
		'n1-custom-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUD-3-YEAR-CPU"] ,
		'n1-custom-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUD-3-YEAR-RAM"] ,
		'e2-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-CUD-3-YEAR-CPU"] ,
		'e2-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-CUD-3-YEAR-RAM"] ,
		'e2-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MICRO"] ,
		'e2-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-SMALL"] ,
		'e2-medium' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MEDIUM"] ,
		'f1-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-F1-MICRO"] ,
		'g1-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-G1-SMALL"] ,
	},
	'spot':{
		'n1-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-PREDEFINED-VM-CORE-PREEMPTIBLE"] ,
		'n1-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-PREDEFINED-VM-RAM-PREEMPTIBLE"] ,
		'n1-custom-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUSTOM-VM-CORE-PREEMPTIBLE"] ,
		'n1-custom-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-N1-CUSTOM-VM-RAM-PREEMPTIBLE"] ,
		'e2-predefined-vcpus' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-PREDEFINED-VM-CORE-PREEMPTIBLE"] ,
		'e2-predefined-memory' : resp['gcp_price_list']["CP-COMPUTEENGINE-E2-PREDEFINED-VM-RAM-PREEMPTIBLE"] ,
		'e2-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MICRO-PREEMPTIBLE"] ,
		'e2-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-SMALL-PREEMPTIBLE"] ,
		'e2-medium' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-E2-MEDIUM-PREEMPTIBLE"] ,
		'f1-micro' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-F1-MICRO-PREEMPTIBLE"] ,
		'g1-small' : resp['gcp_price_list']["CP-COMPUTEENGINE-VMIMAGE-G1-SMALL-PREEMPTIBLE"] ,
	},
}

# persistentdisk_ratecard = {
# 	'snapshot': resp['gcp_price_list']["CP-COMPUTEENGINE-STORAGE-PD-SNAPSHOT"],

# }

persistentdisk_ratecard = {
  'snapshot': {
      "us": 0.026,
      "us-central1": 0.026,
      "us-east1": 0.026,
      "us-east4": 0.029,
      "us-west4": 0.029,
      "us-west1": 0.026,
      "us-west2": 0.031,
      "us-west3": 0.031,
      "europe": 0.026,
      "europe-west1": 0.026,
      "europe-west2": 0.031,
      "europe-west3": 0.031,
      "europe-west4": 0.029,
      "europe-west6": 0.034,
      "europe-north1": 0.029,
      "northamerica-northeast1": 0.029,
      "asia-east": 0.026,
      "asia-east1": 0.026,
      "asia-east2": 0.032,
      "asia-northeast": 0.034,
      "asia-northeast1": 0.034,
      "asia-northeast2": 0.034,
      "asia-northeast3": 0.034,
      "asia-southeast": 0.029,
      "asia-southeast1": 0.029,
      "australia-southeast1": 0.035,
      "australia": 0.035,
      "southamerica-east1": 0.039,
      "asia-south1": 0.031,
      "asia-southeast2": 0.034
    },
  'gp2': {
      "us": 0.1,
      "us-central1": 0.1,
      "us-east1": 0.1,
      "us-east4": 0.11,
      "us-west4": 0.11,
      "us-west1": 0.1,
      "us-west2": 0.12,
      "us-west3": 0.12,
      "europe": 0.1,
      "europe-west1": 0.1,
      "europe-west2": 0.12,
      "europe-west3": 0.12,
      "europe-west4": 0.11,
      "europe-west6": 0.12,
      "europe-north1": 0.11,
      "northamerica-northeast1": 0.11,
      "asia-east": 0.1,
      "asia-east1": 0.1,
      "asia-east2": 0.11,
      "asia-northeast": 0.13,
      "asia-northeast1": 0.13,
      "asia-northeast2": 0.13,
      "asia-northeast3": 0.13,
      "asia-southeast": 0.11,
      "asia-southeast1": 0.11,
      "australia-southeast1": 0.135,
      "australia": 0.135,
      "southamerica-east1": 0.15,
      "asia-south1": 0.12,
      "asia-southeast2": 0.13,
    },
  'magnetic': {
      "us": 0.04,
      "us-central1": 0.04,
      "us-east1": 0.04,
      "us-east4": 0.044,
      "us-west4": 0.044,
      "us-west1": 0.04,
      "us-west2": 0.048,
      "us-west3": 0.048,
      "europe": 0.04,
      "europe-west1": 0.04,
      "europe-west2": 0.048,
      "europe-west3": 0.048,
      "europe-west4": 0.044,
      "europe-west6": 0.052,
      "europe-north1": 0.044,
      "northamerica-northeast1": 0.044,
      "asia-east": 0.04,
      "asia-east1": 0.04,
      "asia-east2": 0.05,
      "asia-northeast": 0.052,
      "asia-northeast1": 0.052,
      "asia-northeast2": 0.052,
      "asia-northeast3": 0.052,
      "asia-southeast": 0.044,
      "asia-southeast1": 0.044,
      "australia-southeast1": 0.054,
      "australia": 0.054,
      "southamerica-east1": 0.06,
      "asia-south1": 0.048,
      "asia-southeast2": 0.052
    },
}

nat_gateway_ratecard = {
	'us-vm-low' : resp['gcp_price_list']["CP-NETWORK-SERVICES-CLOUD-NAT-GATEWAY-UPTIME-LOW-VM-NUMBER"]['us'],
	'us-vm-high' : resp['gcp_price_list']["CP-NETWORK-SERVICES-CLOUD-NAT-GATEWAY-UPTIME-HIGH-VM-NUMBER"]['us'],
	'us-bytes' : resp['gcp_price_list']["CP-NETWORK-SERVICES-CLOUD-NAT-TRAFFIC"]['us'],
}

idle_addresses_ratecard = {
	'us' : resp['gcp_price_list']["CP-NETWORK-SERVICES-IP-ADDRESSES"]['us'],
}

loadbalancer_ratecard = {
  'forwarding_rules' : resp['gcp_price_list']['FORWARDING_RULE_CHARGE_BASE'],
  'forwarding_rules_extra' : resp['gcp_price_list']['FORWARDING_RULE_CHARGE_EXTRA'],
  'ingress' : resp['gcp_price_list']['NETWORK_LOAD_BALANCED_INGRESS'],
}

network_egress_ratecard = {
  'vm-vm-internal' : {
    'northamerica': resp['gcp_price_list']["CP-VM-EGRESS-TOSAME-REGION-FROM-NA"],
    'europe': resp['gcp_price_list']["CP-VM-EGRESS-TOSAME-REGION-FROM-EUROPE"],
    'asia': resp['gcp_price_list']["CP-VM-EGRESS-TOSAME-REGION-FROM-APAC"],
    'southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TOSAME-REGION-FROM-SA"],
    'us': resp['gcp_price_list']["CP-VM-EGRESS-TOSAME-REGION-FROM-NA"],
    'australia' : {"australia-southeast1": 0.01},
  },
  'to-worldwide':{
    'northamerica' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-NA"]["tiers"],
    'us' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-NA"]["tiers"],
    'europe' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-EUROPE"]["tiers"],
    'asia' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-APAC"]["tiers"],
    'australia' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-AUS"]["tiers"],
    'southamerica' : resp['gcp_price_list']["CP-INTERNET-EGRESS-PREMIUM-TIER-TO-WORLDWIDE-FROM-SA"]["tiers"],
  },
  'vm-vm-external':{
    'northamerica-europe': resp['gcp_price_list']["CP-VM-EGRESS-TO-EU-FROM-NA"],
    'europe-europe': resp['gcp_price_list']["CP-VM-EGRESS-TO-EU-FROM-EUROPE"],
    'asia-europe': resp['gcp_price_list']["CP-VM-EGRESS-TO-EU-FROM-APAC"],
    'southamerica-europe': resp['gcp_price_list']["CP-VM-EGRESS-TO-EU-FROM-SA"],
    'us-europe': resp['gcp_price_list']["CP-VM-EGRESS-TO-EU-FROM-NA"],
    'northamerica-us': resp['gcp_price_list']["CP-VM-EGRESS-TO-NORTH-AMERICA-FROM-NA"],
    'europe-us': resp['gcp_price_list']["CP-VM-EGRESS-TO-NORTH-AMERICA-FROM-EUROPE"],
    'asia-us': resp['gcp_price_list']["CP-VM-EGRESS-TO-NORTH-AMERICA-FROM-APAC"],
    'southamerica-us': resp['gcp_price_list']["CP-VM-EGRESS-TO-NORTH-AMERICA-FROM-SA"],
    'us-us': resp['gcp_price_list']["CP-VM-EGRESS-TO-NORTH-AMERICA-FROM-NA"],
    'northamerica-asia': resp['gcp_price_list']["CP-VM-EGRESS-TO-ASIA-FROM-NA"],
    'europe-asia': resp['gcp_price_list']["CP-VM-EGRESS-TO-ASIA-FROM-EUROPE"],
    'asia-asia': resp['gcp_price_list']["CP-VM-EGRESS-TO-ASIA-FROM-APAC"],
    'southamerica-asia': resp['gcp_price_list']["CP-VM-EGRESS-TO-ASIA-FROM-SA"],
    'us-asia': resp['gcp_price_list']["CP-VM-EGRESS-TO-ASIA-FROM-NA"],
    'northamerica-southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TO-SOUTHAMERICA-FROM-NA"],
    'europe-southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TO-SOUTHAMERICA-FROM-EUROPE"],
    'asia-southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TO-SOUTHAMERICA-FROM-APAC"],
    'southamerica-southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TO-SOUTHAMERICA-FROM-SA"],
    'us-southamerica': resp['gcp_price_list']["CP-VM-EGRESS-TO-SOUTHAMERICA-FROM-NA"],
    'northamerica-australia': resp['gcp_price_list']["CP-VM-EGRESS-TO-AUSTRALIA-FROM-NA"],
    'europe-australia': resp['gcp_price_list']["CP-VM-EGRESS-TO-AUSTRALIA-FROM-EUROPE"],
    'asia-australia': resp['gcp_price_list']["CP-VM-EGRESS-TO-AUSTRALIA-FROM-APAC"],
    'southamerica-australia': resp['gcp_price_list']["CP-VM-EGRESS-TO-AUSTRALIA-FROM-SA"],
    'us-australia': resp['gcp_price_list']["CP-VM-EGRESS-TO-AUSTRALIA-FROM-NA"],
    'australia-europe' : {"australia-southeast1": 0.15}, 
    'australia-us' : {"australia-southeast1": 0.15}, 
    'australia-asia' : {"australia-southeast1": 0.15}, 
    'australia-southamerica' : {"australia-southeast1": 0.15}, 
    'australia-northamerica' : {"australia-southeast1": 0.15}, 
  }
}

cloudstorage_ratecard = {
  'class-a-standard':resp['gcp_price_list']["CP-BIGSTORE-CLASS-A-REQUEST"],
  'class-a-nearline':resp['gcp_price_list']["CP-BIGSTORE-NEARLINE-CLASS-A-REQUEST"],
  'class-a-coldline':resp['gcp_price_list']["CP-BIGSTORE-COLDLINE-CLASS-A-REQUEST"],
  'class-a-archive':resp['gcp_price_list']["CP-BIGSTORE-ARCHIVE-CLASS-A-REQUEST"],
  'class-b-standard':resp['gcp_price_list']["CP-BIGSTORE-CLASS-B-REQUEST"],
  'class-b-nearline':resp['gcp_price_list']["CP-BIGSTORE-NEARLINE-CLASS-B-REQUEST"],
  'class-b-coldline':resp['gcp_price_list']["CP-BIGSTORE-COLDLINE-CLASS-B-REQUEST"],
  'class-b-archive':resp['gcp_price_list']["CP-BIGSTORE-ARCHIVE-CLASS-B-REQUEST"],
  'retrieval-standard':{
      "us-central1": 0,
      "us-east1": 0,
      "us-east4": 0,
      "us-west4": 0,
      "us-west1": 0,
      "us-west2": 0,
      "us-west3": 0,
      "europe-west1": 0,
      "europe-west2": 0,
      "europe-west3": 0,
      "europe-west4": 0,
      "europe-west6": 0,
      "europe-north1": 0,
      "northamerica-northeast1": 0,
      "asia-east1": 0,
      "asia-east2": 0,
      "asia-northeast1": 0,
      "asia-southeast2": 0,
      "asia-northeast2": 0,
      "asia-northeast3": 0,
      "asia-southeast1": 0,
      "australia-southeast1": 0,
      "southamerica-east1": 0,
      "asia-south1": 0,
      "us": 0,
      "europe": 0,
      "asia": 0,
      "eur4": 0,
      "nam4": 0,
    },
  'retrieval-nearline':{
      "us-central1": 0.01,
      "us-east1": 0.01,
      "us-east4": 0.01,
      "us-west4": 0.01,
      "us-west1": 0.01,
      "us-west2": 0.01,
      "us-west3": 0.01,
      "europe-west1": 0.01,
      "europe-west2": 0.01,
      "europe-west3": 0.01,
      "europe-west4": 0.01,
      "europe-west6": 0.01,
      "europe-north1": 0.01,
      "northamerica-northeast1": 0.01,
      "asia-east1": 0.01,
      "asia-east2": 0.01,
      "asia-northeast1": 0.01,
      "asia-southeast2": 0.01,
      "asia-northeast2": 0.01,
      "asia-northeast3": 0.01,
      "asia-southeast1": 0.01,
      "australia-southeast1": 0.01,
      "southamerica-east1": 0.01,
      "asia-south1": 0.01,
      "us": 0.01,
      "europe": 0.01,
      "asia": 0.01,
      "eur4": 0.01,
      "nam4": 0.01,
    },
  'retrieval-coldline':resp['gcp_price_list']["CP-BIGSTORE-DATA-RETRIEVAL-COLDLINE"],
  'retrieval-archive':resp['gcp_price_list']["CP-BIGSTORE-DATA-RETRIEVAL-ARCHIVE"],
  'storage-standard':resp['gcp_price_list']["CP-BIGSTORE-STORAGE-REGIONAL"],
  'storage-nearline':resp['gcp_price_list']["CP-BIGSTORE-STORAGE-NEARLINE"],
  'storage-coldline':resp['gcp_price_list']["CP-BIGSTORE-STORAGE-COLDLINE"],
  'storage-archive':resp['gcp_price_list']["CP-BIGSTORE-STORAGE-ARCHIVE"],
}

cloudsql_ratecard = {
  'sqlserver':{
    "non-ha-vcpus" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-VCPU"],
    "non-ha-memory" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-MEMORY"],
  },
  'mysql':{
    "non-ha-vcpus" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-VCPU"],
    "non-ha-memory" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-MEMORY"],
  },
  'postgres':{
    "non-ha-vcpus" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-VCPU"],
    "non-ha-memory" : resp['gcp_price_list']["CP-CLOUDSQLSERVER-MEMORY"],
  },
  "storage-ssd" : resp['gcp_price_list']["CP-CLOUDSQL-STORAGE-SSD"],
  "cloudsql-storage-backup" : resp['gcp_price_list']["CP-CLOUDSQL-BACKUP"],
}


cloudsql_machineref = {
'db.t3.micro' : 'db-f1-micro',
'db.t2.micro' : 'db-f1-micro',
'db.t1.micro' : 'db-f1-micro',
'db.t2.small' : 'db-g1-small',
'db.t3.small' : 'db-g1-small',
'db.m1.small' : 'db-g1-small',
'db.t2.medium' : 'db-n1-standard-1',
'db.t3.medium' : 'db-n1-standard-1',
'db.cv11.medium' : 'db-g1-small',
'db.cv11.small' : 'db-f1-micro',
'db.mv11.medium' : 'db-n1-standard-1',
'db.m3.medium' : 'db-n1-standard-1',
'db.m1.medium' : 'db-n1-standard-1',
'db.t2.large' : 'db-n1-standard-2',
'db.t3.large' : 'db-n1-standard-2',
'db.m6g.large' : 'db-n1-standard-2',
'db.rv11.large' : 'db-n1-highmem-2',
'db.cv11.large' : 'db-n1-custom-2',
'db.mv11.large' : 'db-n1-standard-2',
'db.m5.large' : 'db-n1-standard-2',
'db.m4.large' : 'db-n1-standard-2',
'db.m3.large' : 'db-n1-standard-2',
'db.r6g.large' : 'db-n1-highmem-2',
'db.m1.large' : 'db-n1-standard-2',
'db.r5.large' : 'db-n1-highmem-2',
'db.r4.large' : 'db-n1-highmem-2',
'db.r3.large' : 'db-n1-highmem-2',
'db.t3.xlarge' : 'db-n1-standard-4',
'db.t2.xlarge' : 'db-n1-standard-4',
'db.m6g.xlarge' : 'db-n1-standard-4',
'db.m2.xlarge' : 'db-n1-highmem-2',
'db.cv11.xlarge' : 'db-n1-custom-4',
'db.mv11.xlarge' : 'db-n1-standard-4',
'db.rv11.xlarge' : 'db-n1-highmem-4',
'db.m5.xlarge' : 'db-n1-standard-4',
'db.m4.xlarge' : 'db-n1-standard-4',
'db.m3.xlarge' : 'db-n1-standard-4',
'db.r6g.xlarge' : 'db-n1-highmem-4',
'db.m1.xlarge' : 'db-n1-standard-4',
'db.r3.xlarge' : 'db-n1-highmem-4',
'db.r5.xlarge' : 'db-n1-highmem-4',
'db.r4.xlarge' : 'db-n1-highmem-4',
'db.t3.2xlarge' : 'db-n1-standard-8',
'db.t2.2xlarge' : 'db-n1-standard-8',
'db.m6g.2xlarge' : 'db-n1-standard-8',
'db.m2.2xlarge' : 'db-n1-highmem-4',
'db.rv11.2xlarge' : 'db-n1-highmem-8',
'db.mv11.2xlarge' : 'db-n1-standard-8',
'db.cv11.2xlarge' : 'db-n1-custom-8',
'db.m5.2xlarge' : 'db-n1-standard-8',
'db.m4.2xlarge' : 'db-n1-standard-8',
'db.m3.2xlarge' : 'db-n1-standard-8',
'db.r6g.2xlarge' : 'db-n1-highmem-8',
'db.r3.2xlarge' : 'db-n1-highmem-8',
'db.r5.2xlarge' : 'db-n1-highmem-8',
'db.r4.2xlarge' : 'db-n1-highmem-8',
'db.m6g.4xlarge' : 'db-n1-standard-16',
'db.m2.4xlarge' : 'db-n1-highmem-8',
'db.cv11.4xlarge' : 'db-n1-custom-16',
'db.rv11.4xlarge' : 'db-n1-highmem-16',
'db.mv11.4xlarge' : 'db-n1-standard-16',
'db.m5.4xlarge' : 'db-n1-standard-16',
'db.m4.4xlarge' : 'db-n1-standard-16',
'db.r6g.4xlarge' : 'db-n1-highmem-16',
'db.r3.4xlarge' : 'db-n1-highmem-16',
'db.r4.4xlarge' : 'db-n1-highmem-16',
'db.r5.4xlarge' : 'db-n1-highmem-16',
'db.m6g.8xlarge' : 'db-n1-standard-32',
'db.m5.8xlarge' : 'db-n1-standard-32',
'db.cv11.9xlarge' : 'db-n1-custom-36',
'db.r6g.8xlarge' : 'db-n1-highmem-32',
'db.m4.10xlarge' : 'db-n1-standard-40',
'db.m6g.12xlarge' : 'db-n1-standard-48',
'db.r3.8xlarge' : 'db-n1-highmem-32',
'db.r5.8xlarge' : 'db-n1-highmem-32',
'db.r4.8xlarge' : 'db-n1-highmem-32',
'db.rv11.12xlarge' : 'db-n1-highmem-48',
'db.mv11.12xlarge' : 'db-n1-standard-48',
'db.m5.12xlarge' : 'db-n1-standard-48',
'db.m6g.16xlarge' : 'db-n1-standard-64',
'db.r6g.12xlarge' : 'db-n1-highmem-48',
'db.m5.16xlarge' : 'db-n1-standard-64',
'db.m4.16xlarge' : 'db-n1-standard-64',
'db.r5.12xlarge' : 'db-n1-highmem-48',
'db.cv11.18xlarge' : 'db-n1-custom-72',
'db.r6g.16xlarge' : 'db-n1-highmem-64',
'db.r4.16xlarge' : 'db-n1-highmem-64',
'db.r5.16xlarge' : 'db-n1-highmem-64',
'db.mv11.24xlarge' : 'db-n1-standard-96',
'db.rv11.24xlarge' : 'db-n1-highmem-96',
'db.m5.24xlarge' : 'db-n1-standard-96',
'db.r5.24xlarge' : 'db-n1-highmem-96',
'db.x1e.32xlarge' : 'db-n1-custom-128',
'db.z1d.2xlarge' : 'db-n1-highmem-8',
'db.z1d.6xlarge' : 'db-n1-highmem-24',
'db.z1d.xlarge' : 'db-n1-highmem-4',
'db.x1.16xlarge' : 'db-n1-custom-64',
'db.x1e.8xlarge' : 'db-n1-custom-32',
'db.x1e.2xlarge' : 'db-n1-custom-8',
'db.z1d.3xlarge' : 'db-n1-highmem-12',
'db.x1.32xlarge' : 'db-n1-custom-128',
'db.x1e.16xlarge' : 'db-n1-custom-64',
'db.z1d.12xlarge' : 'db-n1-highmem-48',
'db.z1d.large' : 'db-n1-highmem-2',
'db.x1e.4xlarge' : 'db-n1-custom-16',
'db.x1e.xlarge' : 'db-n1-custom-4',
}