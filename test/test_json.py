# -*- coding: utf-8 -*-
import json
import re

json_str = """
[
	{  
		"name":"XXX",
		"url":"XXX",
		"priority":20,
		"type":1,
		"rules":[
			{   
				"type":1,  
				"url":"XXX",
				"next_page_type":0,
				"next_page_content":"XXX",
				"contents":[  
					{
						"content_type":0,
						"content_content":"XXX"
					}
				]
			},
			{   
				"type":0,  
				"url":"XXX",
				"next_page_type":0,
				"next_page_content":"XXX",
			}
		]
	},
	{  
		"name":"XXX",
		"url":"XXX",
		"priority":10,
		"type":0
	}
	
]
"""
# json_str = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", json_str)
# json_str = json_str.replace("'", "\"")

a =  json.loads(eval(json_str))