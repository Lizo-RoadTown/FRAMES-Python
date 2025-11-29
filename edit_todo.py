import sys
path = sys.argv[1]
data = open(path).read()
data = data.replace('pick 4a877ff', 'edit 4a877ff', 1)
open(path, 'w').write(data)
