import os
import sys

if len(sys.argv) != 2:
	print("Missing argument: Directory")
	sys.exit()

contents = os.listdir(sys.argv[1])
for file in contents:
	if os.path.isfile(file):
		old_path_comps = os.path.abspath(file).split('/')
		old_name_comps = old_path_comps[-1].split()
		newname = old_name_comps[-1]
		new_path_comps = old_path_comps[0:-1] + [newname]
		os.rename('/'.join(old_path_comps), '/'.join(new_path_comps))
