# Atomic and Molecular Data for Plasma Models

We do data mining in this project to retrieve data about cross sections and rate coefficients for both heavy particle impact and photon impact. We focus on the NIFS database and the NFRI database.


# NIFS

For the NIFS database, there have no data about photon impact, so we only extract the information on data for heavy particle impact. And the data for this kind of process are store in CHART and CMOL. 
We collect cross sections for charge transfer and ionisation by heavy particle collisions in CHART, while we use CMOL for both cross sections and rate coefficients by heavy particle - molecule collisions.
For the NIFS folder, we create two folders named "CHART" and "CMOL" in it to save their code and data separately. And for the CMOL folder, we further create two folders called "Cross Section" and "Rate Coefficient" in it to save their own basic information on data and numerical data tables.
The codes are saved in ".py" files, the basic information of  retrieved data for each category are saved in one ".csv" file, while the sets of numerical data for each record are saved either in ".csv" files or ".txt" files.

# NFRI

For the NFRI database, we extract the information on data for both heavy particle impact and photon impact. We also collect cross sections and rate coefficients about the two type of collision processes.
For the NFRI folder, we save the code as well as all the data retrieved from the database in it directly.
The codes are saved in ".py" files, the basic information of  retrieved data for each category are saved in one ".csv" file, while the sets of numerical data for each record are saved either in ".csv" files or ".txt" files.


## 