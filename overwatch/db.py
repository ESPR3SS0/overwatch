import pymongo
import subprocess


class MongoServer:
	def __init__(self):
		self.is_running = False

	def start(self):
		cmd = "mongod  >/dev/null 2>&1"
		subprocess.Popen(cmd, shell=True)
		return 
	
	def stop(self):
		cmd = "pkill mongod"
		subprocess.Popen(cmd, shell=True)
		return 

if __name__ == "__main__":
	server = MongoServer()
	server.start()
	cmd = "ps -aux | grep mongod"
	subprocess.Popen(cmd, shell=True)
	print("here")
	server.stop()
	print("done")
	subprocess.Popen(cmd, shell=True)
