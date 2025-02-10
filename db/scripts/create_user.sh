use admin;
db.createUser({
  user: "oca",
  pwd: "d22a75e9e729debc",
  roles: [{ role: "root", db: "admin" }]
});

mongosh -u oca -p d22a75e9e729debc --authenticationDatabase admin