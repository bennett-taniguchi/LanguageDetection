for x in range(1000):
    colNames = r.readline().replace('\n','').split('",')
    if(len(colNames) == 2): classified = classify(colNames[0])
    elif(len(colNames) == 3): classified = classify(colNames[1])
    if(not classified): wrong += 1
    

print(wrong)
