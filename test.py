import re
 
silly_string = "the c12312312at in the hat"
pattern = "\d*\d"
a = re.findall(pattern, silly_string)
a = ''.join(str(e) for e in a)

print(a) # ['the', 'the']