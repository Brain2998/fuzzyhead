
def divide_dict(dict, words):
    content=[]
    with open(dict) as f:
        content=f.readlines()
    dictName=dict[:dict.index('.txt')]
    dictLength=len(content)
    partStartIndex=0
    partEndIndex=words
    dictExceed=False
    while True:
        with open(dictName+'_'+str(partStartIndex)+'-'+str(partEndIndex-1)+'.txt', 'w') as f:
            for i in range(partStartIndex, partEndIndex):
                f.write(content[i])
        if (dictExceed):
            break
        partStartIndex=partEndIndex
        partEndIndex=partEndIndex+words
        if partEndIndex>dictLength:
            partEndIndex=dictLength
            dictExceed=True
    
#Tests
#divide_dict('38650-password-sktorrent.txt', 5000)