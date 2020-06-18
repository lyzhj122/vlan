from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import getpass
from pprint import pprint
from jinja2 import Template
import yaml

#efine vlan config template Jinja2 file
#define vlan parameters setting Yaml file  
TEMPLATE_FILE = 'template.j2'
PARA_FILE = 'vlan.yml'
#def main():
    

host = None
uname = None
pw = None
# input Host name or IP
if host == None:
    host = input("Hostname or IP:")
    print(host)

# input username
if uname == None:
    uname = input("Username:")
    print(uname)

# input password
if pw == None:
    pw = getpass.getpass()
    print(pw)

#connect to NETCONF and open connection
dev = Device(host=host, user=uname, password=pw)
dev.open()

#load cofigure file from yaml
confpara = yaml.load(open(PARA_FILE).read())
#pprint(confpara)

#enter configuration mode
#cu = Config(dev)


#below for testing render
template = Template(open(TEMPLATE_FILE).read())
f = open('output.txt', 'w')
print (template.render(confpara),file=f)




#run show | compare
diff = cu.diff()


#load Jingja2 template , and vars need to be rendered into the template
with Config(dev) as cu:

    cu.load(template_path=TEMPLATE_FILE, template_vars=confpara, format='txt') 

    template = Template(TEMPLATE_FILE)
    template.render(vlan_vars)
    #check syntax
    cu.commit_check()
    #commit configuraion
    cu.commit()

#close connection
#dev.close()







#if __name__ == '__main__':
#    main()
