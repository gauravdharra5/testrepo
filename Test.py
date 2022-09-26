#IS590PR - Assignment 2
#Creators: Gaurav Dharra, Shray Mishra
#Date: 01-28-2019

#Method name: readContentFromFile
#Input Parameter: file name
#Description: Opens the file and returns a file object
def readContentFromFile(fileName):
    file_object  = open(fileName,'r')
    return file_object

#Method name: processEachRowFromFile
#Input Parameter: file object, location code
#Description: Reads every line of the file at a time, processes the required data and returns a dictionary of the processed data
def processEachRowFromFile(file_object,locationCode):
    stormRecordFound = False
    numberOfStormData=0
    mapOfResults = {} # result dictionary to be returned
    counter = 0

    for eachRow in file_object.readlines():
        eachRowContent = eachRow.split(',')
        if eachRowContent[0][:2] in locationCode:
            counter+=1
            mapOfResults[counter]={'stormId':eachRowContent[0],'name': eachRowContent[1].strip(), 'maxWindSpeed':0, 'minPressure':0, 'maxPressure':0, 'noOfLandfalls':0, 'dateTimeMaxWindSpeed':''}
            numberOfStormData = int(eachRowContent[2])
            stormRecordFound = True
        else:
            numberOfStormData -=1
            eachRowContent[7] = eachRowContent[7] if int(eachRowContent[7])!=-999 else 0
            if stormRecordFound:
                mapOfResults[counter]['startDate']=eachRowContent[0]
                mapOfResults[counter]['minPressure'] = int(eachRowContent[7])
                stormRecordFound=False

            previousValue = mapOfResults[counter]['maxWindSpeed']
            mapOfResults[counter]['maxWindSpeed'] = int(eachRowContent[6]) if mapOfResults[counter]['maxWindSpeed']<int(eachRowContent[6]) else mapOfResults[counter]['maxWindSpeed']
            if(previousValue!=mapOfResults[counter]['maxWindSpeed']):
                mapOfResults[counter]['dateTimeMaxWindSpeed'] = eachRowContent[0] + ' ' + eachRowContent[1]

            mapOfResults[counter]['minPressure'] = int(eachRowContent[7]) if mapOfResults[counter]['minPressure'] > int(eachRowContent[7]) else mapOfResults[counter]['minPressure']
            mapOfResults[counter]['maxPressure'] = int(eachRowContent[7]) if mapOfResults[counter]['maxPressure'] < int(eachRowContent[7]) else mapOfResults[counter]['maxPressure']

            mapOfResults[counter]['noOfLandfalls'] = mapOfResults[counter]['noOfLandfalls']+1 if  eachRowContent[2].count('L')>0 else mapOfResults[counter]['noOfLandfalls']
            mapOfResults[counter]['year'] = eachRowContent[0][:4]

            if numberOfStormData == 0:
                mapOfResults[counter]['endDate'] = eachRowContent[0]
                mapOfResults[counter]['pressureChange'] = mapOfResults[counter]['maxPressure'] - mapOfResults[counter]['minPressure']

    return mapOfResults

#Method name: getAggregateResults
#Input Parameter: mapOfResults
#Description: Computes number of storms and hurrican level storms and returns a dictionary of aggregate result
def getAggregateResults(mapOfResults):
    mapOfAggregateResults = {}
    for eachResult in mapOfResults:
        if not mapOfResults[eachResult]['year'] in mapOfAggregateResults:
            mapOfAggregateResults[mapOfResults[eachResult]['year']]={'noOfStorms':1}
            mapOfAggregateResults[mapOfResults[eachResult]['year']]['noOfHurricaneStorms'] = 1 if mapOfResults[eachResult]['maxWindSpeed'] >= 64 else 0
        else:
            mapOfAggregateResults[mapOfResults[eachResult]['year']]['noOfStorms'] += 1
            mapOfAggregateResults[mapOfResults[eachResult]['year']]['noOfHurricaneStorms'] = mapOfAggregateResults[mapOfResults[eachResult]['year']]['noOfHurricaneStorms']+1 if mapOfResults[eachResult]['maxWindSpeed']>=64 else mapOfAggregateResults[mapOfResults[eachResult]['year']]['noOfHurricaneStorms']
    return mapOfAggregateResults

#Method name: generateOutputFile
#Input Parameter: mapOfGeneratedResults
#Description: Generates an output file from the dictionary of generated results
def generateOutputFile(mapOfGeneratedResults):
    f= open("output.txt","w+")
    headerString1 = 'Storm_System_ID Storm_Name Start_Date End_Date Maximum_Sustained_Wind(knot) Date_Time_Max_Wind Total_Pressure_Change(millibar) Number_Of_Landfall'
    headerString2 = 'Year No_of_storms No_Of_Hurricane_Storms'

    for eachLocation in mapOfGeneratedResults:
        f.write('\n'+eachLocation+'\n')
        f.write(headerString1 + '\n')
        eachIndividualResults = mapOfGeneratedResults[eachLocation]['individualResults']
        eachAggregateResults = mapOfGeneratedResults[eachLocation]['aggregateResults']
        for idx in eachIndividualResults:
            f.write(eachIndividualResults[idx]['stormId'] + ' ' + eachIndividualResults[idx]['name'] + ' ' +
                    eachIndividualResults[idx]['startDate'] + ' ' + eachIndividualResults[idx]['endDate'] + ' ' + str(
                eachIndividualResults[idx]['maxWindSpeed']) + ' ' + str(
                eachIndividualResults[idx]['dateTimeMaxWindSpeed']) + ' ' + str(
                eachIndividualResults[idx]['pressureChange']) + ' ' + str(
                eachIndividualResults[idx]['noOfLandfalls']) + '\n')

        f.write('\n' + headerString2 + '\n')
        for idx2 in eachAggregateResults:
            f.write(idx2+' '+str(eachAggregateResults[idx2]['noOfStorms'])+' '+str(eachAggregateResults[idx2]['noOfHurricaneStorms'])+'\n')

    f.close()

#Method name: main
#Input Parameter:
#Description: Synchronously calls all the methods to process result and generate output
def main():
    fileContentsToBeProcessed=['hurdat2-1851-2017-050118.txt','hurdat2-nepac-1949-2017-050418.txt']
    fileContentLocationCode=[['AL'],['EP','CP']]
    fileContentLocation = ['Atlantic', ' Northeast and North Central Pacific']
    mapOfGeneratedResults = {}

    for idx,eachFile in enumerate(fileContentsToBeProcessed):
        file_object = readContentFromFile(eachFile)
        print(file_object)
        mapOfResults = processEachRowFromFile(file_object,fileContentLocationCode[idx])
        print(mapOfResults)
        mapOfAggregateResults = getAggregateResults(mapOfResults)
        print(mapOfAggregateResults)
        mapOfGeneratedResults[fileContentLocation[idx]] = {'individualResults': mapOfResults,'aggregateResults': mapOfAggregateResults}

    print(mapOfGeneratedResults)
    generateOutputFile(mapOfGeneratedResults)


#calls the main function
if __name__ == '__main__':
    main()
