

## MongoDB cluster
1. Create key: 
You must use the script ```db/createkey.sh``` ⚠️ Please execute this command insde the ```db/``` folder, if you dont execute it in that path, you should move the ```keyfile``` to ```db/```. 


```sh
cd db && chmod +x ./createkey.sh && ./createkey.sh

```

2. Update the mongodb configuration ```db/oca-db-0.conf```
```conf
#replication:
#  replSetName: rs0

net:
  bindIp: 0.0.0.0
  port: 27017

#security:
  #authorization: enabled
  #keyFile: /etc/mongo/keyfile
```
3. Start the cluster:
```sh
docker compose -f cluste.yml up -d
```


4. Enter to the first mongodb node  ⚠️ update the ```<container_id``` with the actual identifier of the container running at 27017:

```sh
docker exec -it <container_id> sh
```

5. Inside the terminal of the container execute this:
```sh 
use admin;

db.createUser({
  user: "oca",
  pwd: "d22a75e9e729debc",
  roles: [{ role: "root", db: "admin" }]
});
```
Check if the user was created succefully with this command: 
```sh
db.getUsers();
## You'll see something like this 
{
  users: [
    {
      _id: 'admin.oca',
      userId: UUID('233cf8af-61d0-40ae-80e5-99bfa2031391'),
      user: 'oca',
      db: 'admin',
      roles: [ { role: 'root', db: 'admin' } ],
      mechanisms: [ 'SCRAM-SHA-1', 'SCRAM-SHA-256' ]
    }
  ],
  ok: 1
}
```

6. Test if the user is persisted:

```sh
docker compose -f cluste.yml down
```

Then you must mofidy the ```db/oca-db-0.conf``` and enable only security like this:

```conf
#replication:
#  replSetName: rs0

net:
  bindIp: 0.0.0.0
  port: 27017

security:
  authorization: enabled
  keyFile: /etc/mongo/keyfile
```

Then start the cluster again
```sh
docker compose -f cluste.yml up -d
```

Then verify if you can logging try first to get inside the terminal of the mongo db at ```27017``` and in the terminal of the mongo db execute this: 

```sh
mongosh -u oca -p d22a75e9e729debc --authenticationDatabase admin
```
you must authenticated correctly. if you cannot authenticated please try again from the step (5)

6. Now you can  start the server

```
chmod +x ./run_local.sh && ./run_local.sh

INFO:     Will watch for changes in these directories: 
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [6783] using WatchFiles
INFO:     Started server process [6785]
INFO:     Waiting for application startup.
INFO:     Application startup complete
```