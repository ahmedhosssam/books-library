#!/bin/bash

#minikube start
minikube kubectl -- delete deployment flask-app-deployment
minikube kubectl -- delete service flask-app-service
minikube kubectl -- delete ingress flask-app-ingress
minikube kubectl -- delete pvc json-pvc
minikube kubectl -- delete pv json-pv

docker build -t ahmedhosssam/flask-app:1722344571 .
docker push ahmedhosssam/flask-app:1722344571

minikube kubectl -- apply -f pv.yaml
minikube kubectl -- apply -f pvc.yaml
minikube kubectl -- apply -f deployment.yaml
minikube kubectl -- apply -f service.yaml
minikube kubectl -- apply -f ingress.yaml
