#!/bin/bash

# for AWS
kubectl delete deployment flask-app-deployment
kubectl delete service flask-app-service
kubectl delete ingress flask-app-ingress
kubectl delete pvc json-pvc
kubectl delete pv json-pv

kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

# for local clusters
#minikube start
#minikube kubectl -- delete deployment flask-app-deployment
#minikube kubectl -- delete service flask-app-service
#minikube kubectl -- delete ingress flask-app-ingress
#minikube kubectl -- delete pvc json-pvc
#minikube kubectl -- delete pv json-pv
#
#docker build -t ahmedhosssam/flask-app:1722344581 .
#docker push ahmedhosssam/flask-app:1722344581
#
#minikube kubectl -- apply -f pv.yaml
#minikube kubectl -- apply -f pvc.yaml
#minikube kubectl -- apply -f deployment.yaml
#minikube kubectl -- apply -f service.yaml
#minikube kubectl -- apply -f ingress.yaml
