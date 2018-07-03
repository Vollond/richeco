import re
 
results2 = "(180,)"
results2 = ''.join(str(e) for e in results2)
#results2 = (str(results2))
results2 = re.findall(r'\d*\d', (str(results2)))
			
print(results2[0]) # ['the', 'the']