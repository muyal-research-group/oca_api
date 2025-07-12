# OCA - API
OCA is a backend API designed to support catalogs, querying, and data management for observatories and contextual variables. It provides an extensible architecture for working with scientific data products, metadata models, and semantic queries using a custom query language.


## 📦 Project Structure
```
├── ocaapi/ # FastAPI server with controller/service/repository structure

├── db/ # MongoDB cluster config, scripts, keyfile
├── docs/ # Markdown documentation (arch, model, etc.)
├── tests/ # Pytest test suite
├── docker-compose.yml # OCA API definition
├── cluster.yml # MongoDB cluster definition
├── run_local.sh # Script to launch local dev server
├── pyproject.toml # Poetry project file
└── mkdocs.yml # MkDocs configuration for documentation
```
## 🧪 Getting Started

### 1. 🔑 Create MongoDB Keyfile
You must use the script ```db/createkey.sh``` ⚠️ Please execute this command insde the ```db/``` folder, if you dont execute it in that path, you should move the ```keyfile``` to ```db/```. 


```sh
cd db && chmod +x ./createkey.sh && ./createkey.sh

```
### 2. ⚙️ Configure MongoDB
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
### 3. 🐳 Start MongoDB Cluster

```sh
docker compose -f cluste.yml up -d
```

### 4. 🧠 Create Admin User
Enter to the first mongodb node  ⚠️ update the ```<container_id``` with the actual identifier of the container running at 27017:

Find the container running MongoDB on port 27017:
```sh
docker ps
```

Then enter the container:

```sh
docker exec -it <container_id> sh
```

Inside the MongoDB shell:

```sh 
use admin;

db.createUser({
  user: "oca",
  pwd: "d22a75e9e729debc",
  roles: [{ role: "root", db: "admin" }]
});
```
Verify user creation:

```sh
db.getUsers();
```
You should see something like:


```sh
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
### 5. 🔒 Enable Authentication


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

Restart the cluster:
```sh
docker compose -f cluste.yml up -d
```

### 6. 🔐 Test Authentication

Then verify if you can logging try first to get inside the terminal of the mongo db at ```27017``` and in the terminal of the mongo db execute this: 

```sh
mongosh -u oca -p d22a75e9e729debc --authenticationDatabase admin
```
you must authenticated correctly. if you cannot authenticated please try again from the step (5)

### 7. 🚀 Start the API Server

```
chmod +x ./run_local.sh && ./run_local.sh

INFO:     Will watch for changes in these directories: 
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [6783] using WatchFiles
INFO:     Started server process [6785]
INFO:     Waiting for application startup.
INFO:     Application startup complete
```

## 📚 Documentation

```sh
poetry add mkdocs --group=dev
mkdocs serve
```

## 🧪 Tests

```
pytest tests/<name_of_test_file>.py -s -vvvv
```

### 🧾 License
MIT License


## 🤝 Contributing

Contributions are welcome and encouraged!

To contribute to this project:

1. **Fork the Repository**

   Click the **Fork** button at the top-right of this repository on GitHub to create your own copy.

2. **Clone Your Fork**

    ```bash
      git clone https://github.com/<your-username>/oca.git
      cd oca
    ```
3. Create a New Branch
Use a descriptive branch name based on your contribution:

    ```sh
    git checkout -b fix/bug-description
    ```

4. Make Your Changes
Add new features, fix bugs, or improve documentation — all changes should happen in your fork and branch.

5. Commit Your Changes
Follow conventional commit messages if possible:

    ```sh 
    git commit -am "fix(api): handle null value in query result"
    ```

6. Push to Your Fork
Once you've committed your changes locally, you need to upload (push) them to your remote fork on GitHub:
    ```sh
    git push origin fix/bug-description
    ```



- ```origin``` is the default name for the remote that points to your fork (you can check with git remote -v)

- ```fix/bug-description``` is the name of your local branch

  This command sends your local branch to your GitHub fork under the same branch name.

  💡 If you've renamed your remote or you're unsure of the name, run:

  ```sh
  git remote -v
  ```
  This will show you the list of remotes and their corresponding URLs.

  After pushing, your changes will appear in your GitHub fork, and you’ll be able to open a pull request (PR) from that branch to the original repository.



7. Open a Pull Request
- Go to your fork on GitHub

- Click "Compare & Pull Request"

- Write a clear title and description

- Submit it to the main branch of the original repository

8. ✅ Wait for Review

    Your changes will be reviewed, and you may be asked to make adjustments before merging.