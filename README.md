# Project Moltres
Project Moltres aims to compare and contrast the pricing of different services on AWS and GCP

The project is still riddled with bugs, edge-cases and random errors. The long-term goal of the project is to be able to smartly and beautifully give a visualization of how much a company can save by using a different cloud provider 

At the moment, we are only focusing on AWS to GCP, meaning the tool will let the user upload their monthly AWS bill and show insights on how much and where the users can save money if/when they move to the Google Cloud Platform. 

Service status:

The services here are categorized into the following states:
1. Finished : Testing and merging to master done
2. Testing : The coding is done but tests are not done yet
3. In progress : Branch created and code being written
4. Icebox : Up next

| Category | Sub-category(GCP) |Sub-category(AWS)| Status |
| -------- | -------- | -------- |------ |
| Compute     | Compute Engine : Premptible VMS     | Elastic Compute cloud:Spot usage     |Testing |
| Compute     | Compute Engine : Regular VMS     | Elastic Compute cloud:Box usage     |Testing |
| Storage     | Persistent Disk     | Elastic Block Storage     | Icebox |
| Storage     | Cloud Storage     | Simple Storage Services(S3)     | Icebox |
| Storage     | Filestore     | Elastic File storage     | Icebox |
| Networking     | Network Egress     | Data Transfer     | Icebox |
| Networking     | Cloud Load Balancer     | Elastic Load Balancer     | Icebox |
| Networking     | Cloud NAT     | NAT Gateway     | Icebox |
| Networking     | Idle Addresses     | Idle Addresses     | Icebox |
| DB Services     | Cloud SQL     | Amazon RDS     | Icebox |
| DB Services     | GCP Search     | Elasticsearch     | Icebox |
| DB Services     | GCP Cache      | Elasticache     | Icebox |
| DB Services     | BigQuery     | Redshift     | Icebox |
| Support     | GCP Support     | AWS Support     |Icebox |


Disclaimer: This project is not associated with any cloud platforms. 