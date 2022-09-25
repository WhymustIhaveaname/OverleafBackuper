## Usage

* Copy `settings.template.py` to `settings.py` and modify relating info. Then
* `./bakuper.py --lsuser` : list users
* `./bakuper.py --help`   : print help
* `./bakuper.py`          : do one backup

## Todo

- [ ] Backup recursively folders in a project (now I am ignoring them)
- [ ] Backup figures (I cannot find them)
- [ ] Update the files rather than overwritting them

## Useful Docker Commands

* `docker ps`: list the running containers

```
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                 PORTS                   NAMES
8463fbd49381   sharelatex/sharelatex:2.5.2   "/sbin/my_init"          13 months ago   Up 3 weeks             0.0.0.0:xx->80/tcp   sharelatex
8410ebff4ee9   mongo:4.0                     "docker-entrypoint.s…"   18 months ago   Up 3 weeks (healthy)   27017/tcp               mongo
b9123a22456a   redis:5.0                     "docker-entrypoint.s…"   18 months ago   Up 3 weeks             6379/tcp                redis
```

* `docker exec -it <container id> bash`: access the running container

```
# docker exec -it 8410ebff4ee9 bash
root@8410ebff4ee9:/#
```

* `mongo --port 27017 --host 127.0.0.1`: connect to a local mongodb

* `docker inspect mongo | grep IPAddress`: get ip address of docker `mongo`

```
# docker inspect mongo | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.18.0.3",
```

## Useful MongoDB Commands

* `show dbs`: show databases

```
> show dbs
admin       0.000GB
config      0.000GB
local       0.000GB
sharelatex  0.002G
```

* `use databasename`: enter database

```
> use sharelatex
switched to db sharelatex
```

* `show collections == show tables`: list collections. MongoDB hierachy: database > collection (table) > document

```
> show collections
_migrations
deletedProjects
docHistory
docHistoryIndex
docOps
docs
projectHistoryMetaData
projects
rooms
spellingPreferences
systemmessages
tokens
users
```

* `db.users.find()`: list all contents in collection `users`

```
> db.users.find()
{ "_id" : ObjectId("6045e9697aff510088ad7541"), "auditLog" : [ ], "thirdPartyIdentifiers" : [ ], "samlIdentifiers" : [ ], "awareOfV2" : false, "betaProgram" : false, "alphaProgram" : false, "refered_user_count" : 0, "refered_users" : [ ], "referal_id" : "9fe58a49", "must_reconfirm" : false, "featuresOverrides" : [ ], "features" : { "trackChanges" : true, "references" : true, "templates" : true, "compileGroup" : "standard", "compileTimeout" : 180, "gitBridge" : true, "github" : true, "dropbox" : true, "versioning" : true, "collaborators" : -1 }, "ace" : { "syntaxValidation" : true, "pdfViewer" : "pdfjs", "spellCheckLanguage" : "en", "autoPairDelimiters" : false, "autoComplete" : true, "fontSize" : 12, "overallTheme" : "", "theme" : "textmate", "mode" : "none" }, "holdingAccount" : false, "loginCount" : 29, "lastLoginIp" : "127.0.0.1", "signUpDate" : ISODate("2021-03-08T09:07:53.207Z"), "staffAccess" : { "adminMetrics" : false, "groupManagement" : false, "groupMetrics" : false, "institutionManagement" : false, "institutionMetrics" : false, "publisherManagement" : false, "publisherMetrics" : false }, "isAdmin" : true...
```
