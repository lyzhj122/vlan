from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import getpass
from pprint import pprint
from jinja2 import Template
import yaml
import time

#efine vlan config template Jinja2 file
#define vlan parameters setting Yaml file  
TEMPLATE_FILE = 'j2-template.j2'
PARA_FILE = 'vlan.yml'



#Load template Jinja2 file and parameters Yaml file
# return 0 - Success
# return 1 - Failed
def SaveConfig (template, parameters):

    try:
        template = Template(open(template).read())
        confpara = yaml.load(open(parameters).read(),Loader=yaml.FullLoader)
        print(template.render(confpara))
        #save the rendered configuratio to file: Y-M-D-H_M_S
        savefile = template.render(confpara)
        now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
        fname= now + r"-configure.txt"
        f = open(fname, 'w')
        print(savefile,file=f)       
        return 0
    except:
        print("File Load Failed")
        return 1
    return 0    



def main():

    Host = None
    ID = None
    Passwd = None
    # input Host name or IP
    if Host == None:
       Host = input("Hostname or IP:")
       print(Host)

    # input username
    if ID == None:
       ID = input("Username:")
       print(ID)

    # input password
    if Passwd == None:
       Passwd = getpass.getpass()
       print(Passwd)

    try:
        dev = Device(host=Host, 
                     user=ID, 
                     password=Passwd)
        dev.open()
        with Config(dev) as cu:
            #run show | compare
            diff = cu.diff()
            if diff:
                cu.rollback()
            #validate configration, if error, reruen 1 (failed)
            #commit configuraion
            cu.load(template_path = TEMPLATE_FILE,template_vars = PARA_FILE, merge = True)
            try:
                cu.commit_check()
            except jnpr.junos.exception.CommitError as err:
                print("Error configuration, Please check syntax" + err)
                return 1
            else:           
                cu.commit()
                #save the configuration to file
                save = SaveConfig (TEMPLATE_FILE,PARA_FILE)
                #save failed
                if(save == 1):
                    print('Save Configure file Failed')
                    return 1;
    except jnpr.junos.exception.ConnectError as err:
        print("Error connecting : " + err)
        return 1 
    finally:
        print("Closing connection " + Host)
        dev.close()
    return 0



if __name__ == '__main__':
    main()
