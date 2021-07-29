def write_id_para(blockName, paraId):
	#setParaMap = {'dim6': {1: 1.e+3, 3: 1.0, 9: 1.0}, 'dim62f': {11: 1.0}}
	setParaMap = {'dim6': {1: 1.e+3}, 'dim62f': {11: 1.0, 24: 1.0}}
	discardParaMap = {'dim6': [7, 8], 'dim62f': [17, 18, 20, 21], 'dim64f': [5, 9, 15, 18, 22, 24], 'dim64f2l': [11, 12, 18, 19, 20, 21]}
	parameter = '{} {} 0. \n'.format(blockName, paraId)
	if blockName in setParaMap:
		if paraId in setParaMap[blockName]:
			parameter = '{} {} {} \n'.format(blockName, paraId, setParaMap[blockName][paraId])
	if blockName in discardParaMap:
		if paraId in discardParaMap[blockName]:
			parameter = 'discard'
	return parameter

setStr = 'set param_card '
blockNameMap = {'dim6': 10, 'dim62f': 24, 'dim64f': 25, 'dim64f2l': 21, 'dim64f4l': 9}
cardList = []
for key, value in blockNameMap.items():
	for i in range(1, value + 1):
		parameter = write_id_para(key, i)
		if parameter == 'discard': continue
		lineStr = setStr + parameter
		cardList.append(lineStr)
with open("customizecards.dat", 'w') as f:
	f.writelines(cardList)