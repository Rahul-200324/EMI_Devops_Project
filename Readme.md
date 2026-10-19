EMI Calculater project 
------------------------------------------------------------------------------------------------------------------------

I used Python (Flask), Git and Github (For source code management), Docker (Build image and container), Kubernetes (Manage cotainers), Jenkins( CI- CD pipeline), Terraform and Monitoring part Grafana. 

-------------------------------------------------------------------------------------------------------------------------

# Push the application to Github 

git init 
git add .
git remote add origin <repo link>
git remote -v
git branch
git checkout -b main
git push origin main

-------------------------------------------------------------------------------------------------------------------------

# Docker image and creating container 

images:
    1. Emi_image
    2. Mysql_image
containers:
    1. Emi_container
    2. mysql_container

docker ps -a
docker images

docker login 
docker pull mysql
docker build -t emi_image .

docker run -d --name emi-mysql -e MYSQL_USER_PASSWORD=root -e MYSQL_DATABASE=emi-devops -p 3600:3600 mysql:latest

docker run -d --name emi-container --p 5008:5008 -e MYSQL_USER_PASSWORD=root -e MYSQL_DATABASE=emi-devops emi_image:latest

# To go inside mysql 

docker exec -d emi-mysql //bin/bash 
mysql -u root -p

# SQL querys

SHOW DATABASES;
USE DATABASE-NAME;
SHOW TABLES;
SELECT * FROM users;

Open browser and open localhost:5008 

---------------------------------------------------------------------------------------------------------------------------