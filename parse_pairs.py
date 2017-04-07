import json
import re

f = open ('heldout_pair_data.jsonlist', 'r') 
data = f.readlines()

null = None
false = False 
true = True

main_list = []
for item in range(len(data)):
	sub_dict = dict()
	json_string = json.loads(data[item])
	if json_string["op_author"] is not None:
		op_post = (json_string["op_text"]).encode('utf-8').strip()
		split = op_post.find("&gt")
		# print split
		if split!=-1: 
			op_post = op_post[:split]
	sub_dict["op_post"] = [op_post]
	pos = json_string["positive"]["comments"][0]["body"].encode('utf-8').strip()
	sub_dict["positive"] = [pos]
	neg = json_string["negative"]["comments"][0]["body"].encode('utf-8').strip()
	sub_dict["negative"] = [neg]
	main_list.append(sub_dict)

print main_list[0]