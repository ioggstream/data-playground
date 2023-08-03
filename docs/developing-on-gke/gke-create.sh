# Install required components
gcloud components install gke-gcloud-auth-plugin kubectl

# Create project and set as default
gcloud projects create deleteme-kube-autopilot
gcloud config set project deleteme-kube-autopilot

# Deploy GKE autopilot and wait for completion
gcloud container clusters create-auto deleteme-autopilot --region europe-west1 --project deleteme-kube-autopilot

# Get credential
gcloud container clusters get-credentials --region europe-west1 --project deleteme-kube-autopilot deleteme-autopilot

# Check login
kubectl get ns
