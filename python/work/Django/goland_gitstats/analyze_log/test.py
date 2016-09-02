temp_file = "temp_log.txt"

fp = open(temp_file, "r")
all_lines = fp.readlines()
fp.close()

for i in all_lines[:55]:
    print i

print len(all_lines)
