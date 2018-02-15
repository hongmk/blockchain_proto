# 입력된 block의 해시값을 리턴함
# 적용 해시알고리즘 : sha256

import hashlib, json, sys

def getHash(block=""):

	if type(block)!=str:
		block = json.dumps(block,sort_keys=True)

	if sys.version_info.major == 2:
		return unicode(hashlib.sha256(block).hexdigest(),'utf-8')
	else:
		return hashlib.sha256(str(block).encode('utf-8')).hexdigest()

if __name__ == "__main__":
	a = getHash('1')
	print(a)
