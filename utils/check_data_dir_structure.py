from pathlib import Path


path = Path("root_data/blackoutu742-1980")


# Needs a following folders 
#    - competitive
#    - complete
#    - profile 
#    - characters

required_dirs = [ "competitive", "complete", "profile", "characters"]

dir_in_root = []

def check_for_expected_dirs( required, root_dir):

	for item in path.iterdir():
		if not item.is_file():
			dir_in_root.append(item)
	current = [ x.name for x in dir_in_root ]
	
	for d in required:
		if d not in current:
			return False 
	
	return True

if __name__ == "__main__":
	path = Path("root_data/blackoutu742-1980")
	required_dirs = [ "competitive", "complete", "profile", "characters"]
	good_dir_struct = check_for_expected_dirs( required_dirs, path)
	print("The dicrotry stat is: {}".format(good_dir_struct))
