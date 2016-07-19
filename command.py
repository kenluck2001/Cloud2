import os
from fabric.api import local, settings, abort, run, cd

def fixCredential():
    CREDENTIAL_DIR = "~/.aws/"
    delCMD = 'rm -rf ' + CREDENTIAL_DIR
    local(delCMD)
    mkCMD = 'mkdir ' + CREDENTIAL_DIR
    local(mkCMD)

    with cd(CREDENTIAL_DIR):
        SETTING_DIR = os.getcwd() + "/settings/*"
        cp_CMD = "cp -R "+ SETTING_DIR +" " + CREDENTIAL_DIR 
        local(cp_CMD)
        local("rm -rf *~ ")

fixCredential()




os.system("python server2.py")
