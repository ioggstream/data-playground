# Get credential
gcloud container clusters get-credentials --region europe-west1 --project deleteme-kube-autopilot deleteme-autopilot

# Check login
kubectl get ns

# Crea e setta il namespace di default.
kubectl create ns test-mysql
kubectl config set-context --current --namespace test-mysql

# Installa MySQL o quello che vuoi.
kubectl apply -f mysql.yaml

# Configura il port-forward verso il container e metti il processo in background.
kubectl port-forward svc/mysql 13306:3306 &

# Si connette al container mysql dal PC di sviluppo
mysql --host 127.0.0.1 --port 13306 -uroot -p
