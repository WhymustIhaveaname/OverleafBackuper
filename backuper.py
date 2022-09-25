#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time,sys,traceback

LOGLEVEL={0:"DEBUG",1:"INFO",2:"WARN",3:"ERR",4:"FATAL"}
LOGFILE="backuper.log"

def log(*msg,l=1,end="\n",logfile=LOGFILE):
    msg=", ".join(map(str,msg))
    st=traceback.extract_stack()[-2]
    lstr=LOGLEVEL[l]
    #now_str="%s %03d"%(time.strftime("%y/%m/%d %H:%M:%S",time.localtime()),math.modf(time.time())[0]*1000)
    now_str="%s"%(time.strftime("%y/%b/%d %H:%M:%S",time.localtime()),)
    perfix="%s [%s,%s:%03d]"%(now_str,lstr,st.name,st.lineno)
    if l<3:
        tempstr="%s %s%s"%(perfix,str(msg),end)
    else:
        tempstr="%s %s:\n%s%s"%(perfix,str(msg),traceback.format_exc(limit=5),end)
    print(tempstr,end="")
    if l>=1:
        with open(logfile,"a") as f:
            f.write(tempstr)

import pymongo,os
from settings import *

class Backuper():
    def __init__(self,ip="localhost",port=27017):
        self.client       = pymongo.MongoClient("mongodb://%s:%d/"%(ip,port),timeoutMS=100,connectTimeoutMS=100,socketTimeoutMS=100,serverSelectionTimeoutMS=100)
        self.db           = self.client["sharelatex"]

    def backup(self):
        self.get_users()
        self.get_projects()
        self.get_docs()

        for p in self.projects:
            log("backuping %s/%s"%(p['owner_name'],p['project_name']),l=0)
            target_dir  = os.path.join(backup_folder,p['owner_name'],p['project_name'])
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                log("created %s"%(target_dir))
            # for f in p['root']['fileRefs']:
            #     target_file = os.path.join(target_dir,f['name'])
            #     log("trying to bk %s"%(target_file))
            #     log(f['_id'] in self.docs) # False
            #     with open(target_file,"wb") as f2:
            #         f2.write(self.docs[f['_id']])
            #     input()
            for f in p['root']['docs']:
                target_file = os.path.join(target_dir,f['name'])
                with open(target_file,"w") as f2:
                    f2.write(self.docs[f['_id']]['lines'])

    def get_projects(self):
        """
            need to call self.get_users() before
        """
        self.projects = []
        for i in self.db["projects"].find():
            # i contain keys '_id', 'owner_ref', 'lastUpdatedBy', 'auditLog', 'collabratecUsers', 'tokenAccessReadAndWrite_refs',
            # 'tokenAccessReadOnly_refs', 'deletedFiles', 'deletedDocs', 'trashed', 'description', 'deletedByExternalDataSource',
            # 'spellCheckLanguage', 'compiler', 'publicAccesLevel', 'rootFolder', 'readOnly_refs', 'collaberator_refs', 'active',
            # 'lastUpdated', 'name', '__v', 'version', 'rootDoc_id', 'lastOpened'
            try:
                self.projects.append({ "_id"          : i["_id"],
                                       "owner_name"   : self.user_names[i["owner_ref"]],
                                       'project_name' : i['name'],
                                       'root'         : i["rootFolder"][0]})
                # rootFolder looks like
                # [{  "_id" : ObjectId("604716745214200074d6238c"),
                #     "folders" : [ ],
                #     "fileRefs" : [ ],
                #     "docs" : [ { "_id" : ObjectId("604716745214200074d6238e"), "name" : "main.tex" } ],
                #     "name" : "rootFolder" } ]
                # [{  '_id': ObjectId('6325897acacb99007385ded0'),
                #     'folders': [{   '_id': ObjectId('632589889d35d60073266c75'),
                #                     'folders': [],
                #                     'fileRefs': [{'linkedFileData': None, 'hash': 'b6c9371d35c450b3993f7e6d95aaffe6e208f1c1', '_id': ObjectId('63258a1c9d35d60073266c77'), 'rev': 0, 'created': datetime.datetime(2022, 9, 17, 8, 49, 32, 99000), 'name': 'KleinJ.png'}],
                #                     'docs': [{'_id': ObjectId('632589949d35d60073266c76'), 'name': 'chaprt1.tex'}],
                #                     'name': 'folder1'}],
                #     'fileRefs': [{'linkedFileData': None, 'hash': '5fa655f8dc13f9cba54227451a78617a790334de', '_id': ObjectId('63258a389d35d60073266c78'), 'rev': 0, 'created': datetime.datetime(2022, 9, 17, 8, 50, 0, 901000), 'name': 'WeierstrassInvariantG.png'}],
                #     'docs': [{'_id': ObjectId('6325897a9d35d60073266c73'), 'name': 'main.tex'}, {'_id': ObjectId('6325897a9d35d60073266c74'), 'name': 'references.bib'}],
                #     'name': 'rootFolder'}]
            except:
                log(i,l=3)

    def get_docs(self):
        self.docs = {}
        for i in self.db["docs"].find():
            # i contains keys "_id", "lines", "project_id", "ranges", "rev"
            try:
                self.docs[i["_id"]]          = i
                self.docs[i["_id"]]['lines'] = "\n".join(i['lines'])
            except:
                log(i,l=3)

    def get_users(self,printflag=False):
        users   = []
        timefmt = "%y/%b/%d"
        for i in self.db["users"].find():
            # i contain keys ['_id', 'auditLog', 'thirdPartyIdentifiers', 'samlIdentifiers', 'awareOfV2', 'betaProgram',
            # 'alphaProgram', 'refered_user_count', 'refered_users', 'referal_id', 'must_reconfirm', 'featuresOverrides',
            # 'features', 'ace', 'holdingAccount', 'loginCount', 'lastLoginIp', 'signUpDate', 'staffAccess', 'isAdmin',
            # 'institution', 'role', 'first_name', 'emails', 'email', '__v', 'hashedPassword', 'lastLoggedIn']
            try:
                users.append({'_id'         : i['_id'],
                              'first_name'  : i['first_name'],
                              'email'       : i['email'],
                              'loginCount'  : i['loginCount'],
                              'isAdmin'     : i['isAdmin']})
                if 'lastLoggedIn' in i:
                    users[-1]['lastLoggedIn'] = i['lastLoggedIn'].strftime(timefmt)
                else:
                    #users[-1]['lastLoggedIn'] = "not found"
                    users.pop()
            except:
                log(i,l=3)


        if printflag:
            users.sort(key=lambda x: x['loginCount'],reverse=True)
            users.insert(0,{'first_name'  : 'first_name',
                            'email'       : 'email',
                            'loginCount'  : 'loginCount',
                            'isAdmin'     : 'isAdmin',
                            'lastLoggedIn': 'lastLogin'})
            users_str = []
            for i in users:
                s = "%15s %30s %7s %s %4s"%(i['first_name'],i['email'],i['isAdmin'],i['lastLoggedIn'],i['loginCount'])
                users_str.append(s)
            print("\n".join(users_str))
            return

        self.user_names = {i['_id']:i['first_name'] for i in users}


if __name__=="__main__":
    bk = Backuper(ip=mongo_ip,port=mongo_port)
    if len(sys.argv)>1 and sys.argv[1].startswith("--lsuser"):
        bk.get_users(printflag=True)
    elif len(sys.argv)>1 and sys.argv[1].startswith("--help"):
        print("""\
--lsuser: list users
--help  : print help
no arg  : backup""")
    else:
        bk.backup()
