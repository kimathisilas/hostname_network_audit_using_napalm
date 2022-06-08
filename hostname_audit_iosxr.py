from napalm import get_network_driver
driver = get_network_driver('iosxr')    
with open(r'inventory.txt','r') as target:
  for line in target.readlines():
      print(line.split())
      hostname = line.split()[1]
      IP = line.split()[0]
      username = line.split()[2]
      password = line.split()[3]
      device = driver(IP,username ,password)
      try: 
          device.open() # required to load credentials
          output = device.cli(["sh running-config | i hostname"])
          for key, value in output.items():
              hostname =value.split("hostname")[-1]
          if hostname == "R1":
              print("Router has the correct Hostname Configured")
              device.close()
          else:
              print("The Hostname is  {}".format(hostname))
              device.load_merge_candidate(config='hostname R1 \n end\n')
              print(device.compare_config())
              device.commit_config()
              device.close()
      except:
            print("Failed to access the device {}".format(IP))
