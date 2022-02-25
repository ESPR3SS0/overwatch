from overwatch import PullService 
from pathlib import Path


f_name = "config.cfg"
f_p = Path(f_name).resolve()

service = PullService(f_p)

service.Start()
