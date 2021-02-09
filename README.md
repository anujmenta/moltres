# Project Moltres
Project Moltres aims to compare and contrast the pricing of different services on AWS and GCP

The project is still riddled with bugs, edge-cases and random errors. The long-term goal of the project is to be able to smartly and beautifully give a visualization of how much a company can save by using a different cloud provider 

At the moment, we are only focusing on AWS to GCP, meaning the tool will let the user upload their monthly AWS bill and show insights on how much and where the users can save money if/when they move to the Google Cloud Platform. 

Service status:

The services here are categorized into the following states:
1. Plotlyd : Plotted graphs on Plotly and integrated into report
2. Visualized : Generating output into a Excel sheet
3. Finished : Testing and merging to master done
4. Testing : The coding is done but tests are not done yet
5. In progress : Branch created and code being written
6. Icebox : Up next 

| Category | Sub-category(GCP) |Sub-category(AWS)| Status |
| -------- | -------- | -------- |------ |
| Compute     | Compute Engine : Premptible VMS     | Elastic Compute cloud:Spot usage     |Visualized |
| Compute     | Compute Engine : Regular VMS     | Elastic Compute cloud:Box usage     |Visualized |
| Storage     | Persistent Disk     | Elastic Block Storage     | Visualized |
| Storage     | Cloud Storage     | Simple Storage Services(S3)     | Visualized |
| Storage     | Filestore     | Elastic File storage     | Icebox |
| Networking     | Network Egress     | Data Transfer     | Visualized |
| Networking     | Cloud Load Balancer     | Elastic Load Balancer     | Visualized |
| Networking     | Cloud NAT     | NAT Gateway     | Visualized |
| Networking     | Idle Addresses     | Idle Addresses     | Visualized |
| DB Services     | Cloud SQL     | Amazon RDS     | Visualized |
| DB Services     | GCP Search     | Elasticsearch     | Icebox |
| DB Services     | GCP Cache      | Elasticache     | Icebox |
| DB Services     | BigQuery     | Redshift     | Icebox |
| Support     | GCP Support     | AWS Support     |Icebox |


Disclaimer: This project is not in collaboration/associated/sponsored with/by any cloud platforms. 

Setup instructions:

1. Install Anaconda
2. Create virtual environment using this command "conda env create --file requirements.txt "
3. Activate virtual environment using "conda activate env"
4. Run the file 'main.py' and follow the instructions