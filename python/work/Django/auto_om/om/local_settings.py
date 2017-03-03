#-*- encoding:utf-8 -*-

"""
  新增ESXi服务器的话,
  1：需要在本文件里添加配置信息;
  2：ansible配置文件里添加ESXI机器的信息：用户名和密码;
  3：ESXi机器上需要有虚拟机模板以及创建虚拟机的python脚本;
  4: 还有各个虚拟机模板里要有修改ip的脚本，modify_ip.py
"""


#待创建的操作系统的模板信息
template_pc_info = {"10.10.3.23": 
                    {"win": {"win7": {"ip": "ip", "username": "1", "password": "1"},
                            "win8": {"ip": "ip", "username": "1", "password": "1"},
                            "win10":{"ip": "ip", "username": "1", "password": "1"}
                           }, 
                    "mac": {"10.8": {"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                            "10.9": {"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                            "10.10": {"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                            "10.11": {"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"}
                           },
                    "ubu": {"u12": {"ip": "ip", "username": "1","password": "1"},
                            "u14": {"ip": "ip", "username": "1","password": "1"}
                           }
                   },
                   "10.10.2.41":
                    {"win": {"win7": {"ip": "ip", "username": "1", "password": "1"},
                            "win8": {"ip": "ip", "username": "1", "password": "1"},
                            "win10":{"ip": "ip", "username": "1", "password": "1"}
                           }, 
                    "mac":{"10.8":{"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                           "10.9":{"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                           "10.10":{"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"},
                           "10.11":{"ip":"ip","username":"1","password":"1","subnetmask":"1","gateway":"1"}
                           },
                    "ubu": {"u12": {"ip": "ip", "username": "1","password": "1"},
                            "u14": {"ip": "ip", "username": "1","password": "1"}
                            #"u14": {"ip": "10.10.2.45", "username": "goland","password": "docker1"}
                           }
                    },

                   }
    
#vmx以及vmdk的基本信息
vm_dict = {"vmx" : {"win": {"win7": "w7yuanshi/w7yuanshi.vmx", "win8": "w8/w8.vmx", "win10": "w10/w10.vmx"},
                   "mac": {"10.8": "m10.8/m10.8vmx", "10.9": "m10.9/m10.9vmx", "10.10": "m10.10/m10.10.vmx", "10.11": "mac10.11/mac10.11vmx"},
                   "ubu": {"u12": "u12/u12.vmx", "u14": "u14/u14.vmx"}
                   },
           "vmdk": {"win": {"win7": "w7yuanshi/w7yuanshi.vmdk", "win8": "w8/w8.vmdk", "win10": "w10/w10.vmdk"},
                    "mac": {"10.8": "m10.8/m10.8vmdk", "10.9": "m10.9/m10.9vmdk", "10.10": "m10.10/m10.10.vmdk", "10.11": "mac10.11/mac10.11vmdk"},
                    "ubu": {"u12": "u12/u12.vmdk", "u14": "u14/u14.vmdk"}
                   }
          }

#""" 内存 CPU 以及硬盘大小的组合 """
list1 = {"memory": "1", "cpu": "1", "hard_disk": "15G"}
list2 = {"memory": "1", "cpu": "2", "hard_disk": "15G"}
list3 = {"memory": "2", "cpu": "4", "hard_disk": "15G"}
list4 = {"memory": "4", "cpu": "4", "hard_disk": "15G"}
select_dict = {"select1": list1, "select2": list2, "select3": list3, "select4": list4}

#ESXi服务器保存python脚本的路径的配置信息
#esxi_create_virtual_script_dict = {"10.10.3.23": "/vmfs/volumes/datastore1/xdd/create_start_virtual.py", 
#                                   "10.10.2.41": "/vmfs/volumes/datastore123/create_start_virtual.py"
#                                  }

esxi_create_virtual_script_dict = {"ip": "/vmfs/volumes/datastore1/xdd",
                                   "ip": "/vmfs/volumes/datastore123", 
                                   "create_script": "create_start_virtual.py", 
                                   "delete_script": "delete_virtual.py"
                                  }


