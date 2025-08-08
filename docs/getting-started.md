
This guide will help you set up the QLX API project from scratch, including deploying a MongoDB cluster and understanding the core architecture components of the QLX API.

## Step 1: MongoDB Cluster

The QLX API uses MongoDB as its primary database to store observatories, products, Xvars, assignments and catalogs relationships. To get started, you’ll need to deploy a MongoDB instance locally.

### Step 1.1: First steps
:warning: It is important to first start one of the nodes with authorization disabled and without replication. You can perform this by modify the configuration file in ```db/configs/mongo1.conf``` in the security settings: 

```yml
# Security settings
security:
  authorization: disabled
  #keyFile: /data/key/mongokey

#replication:
#  replSetName: rs0 
```


### Step 1.2 Deploy the containerized cluster
Then you can deploy the local cluster using docker compose: 

```bash
docker compose -f db/dbcluster.yml up -d
```

### Step 1.3: Create a user

To create a new user use the ```db/scripts/create_user.sh``` copy the content and connect to the node that has authorized disabled, and create the user, the default username is ```oca``` and password is ```d22a75e9e729debc```.

if all the steps are completed successfully you will be able to connect to mongodb using your credentials, like this:

```bash
mongosh -u oca -p d22a75e9e729debc --authenticationDatabase admin
```


## Step 2: Install dependencies

First you must install the package manager ```poetry```:

```bash
pip3 install poetry
```

Once the package manager is fully installed you must run the commands in order:

```bash
peotry shell 
poetry install
```

## Step 3: Deploy server

To deploy the server execute the ```run_local.sh``` bash script:

```
./run_local.sh
```

Or you can run the ```uvicorn``` command:

```bash
uvicorn ocaapi.server:app --host ${OCA_HOST-0.0.0.0} --port ${OCA_PORT-5000} --reload
```

The default port is ```5000```, you can change it directly on the command or update the environment variable ```OCA_PORT```. 