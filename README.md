# FAME: Facial Analyzer for Multimedia Entertainment
> FAME aims to provide an SaaS solution for multimedia content creators to perform audience facial recognition analysis at manageable costs powered by advanced cloud-enabled machine learning capabilities.

## Setup Steps

### Building Locally

Make sure you install python version 3.7+.
Install pip dependencies by running 

```pipenv install
```
Then run your application locally
```bash
python manage.py runserver
```

### Deploy to IBM cloud
When you are ready to deploy to IBM Cloud on Cloud Foundry or Kubernetes, run one of the commands:

```bash
ibmcloud dev deploy -t buildpack // to Cloud Foundry
ibmcloud dev deploy -t container // to K8s cluster
```

You can build and debug your app locally with:

```bash
ibmcloud dev build --debug
ibmcloud dev debug
```
