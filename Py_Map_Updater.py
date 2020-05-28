#ToDo List
#Adjacencies        Complete
#Definitions         Complete
#Positions          Complete
#province.bmp       Complete
#default.map        Complete

#User INPUTS
startProvicne = 2062
endProvince = 2121
newStartProvicne = 2300
#Positive X for extending the map East (Negative Unknown Effect)
XOffSet = 0
#Positive Y for extending the map South (Negative Unknown Effect)
YOffSet = 0
#Makes selection area of map smaller to reduce time significantly
ChropedMap = False
XStart = 0
YStart = 0
XEnd = 1024
YEnd = 1024


import copy
from decimal import *
from PIL import Image
from multiprocessing.pool import ThreadPool as Pool

class Map:
    max_province = 0

class proice_Map:
    max_province = 0

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    other_info = ""
    lastKnownY = -1

class ProvincePosition:
    id = 0
    pos_name = ""
    pos_city_x = 0.0
    pos_city_y = 0.0
    pos_city_r = 0.0
    pos_city_h = 0.0
    pos_unit_x = 0.0
    pos_unit_y = 0.0
    pos_unit_r = 0.0
    pos_unit_h = 0.0
    pos_councillor_x = 0.0
    pos_councillor_y = 0.0
    pos_councillor_r = 0.0
    pos_councillor_h = 0.0
    pos_text_x = 0.0
    pos_text_y = 0.0
    pos_text_r = 0.0
    pos_text_h = 0.0
    pos_port_x = 0.0
    pos_port_y = 0.0
    pos_port_r = 0.0
    pos_port_h = 0.0
    pos_wonder_x = 0.0
    pos_wonder_y = 0.0
    pos_wonder_r = 0.0
    pos_wonder_h = 0.0
    pos_wonder_costal_x = 0.0
    pos_wonder_costal_y = 0.0
    pos_wonder_costal_r = 0.0
    pos_wonder_costal_h = 0.0

class Adjacencies:
    IDfrom = 0
    IDto = 0
    adjType = ""
    IDthrough = 0
    commnet = ""
    
def province_IO(text):
    var1 = input("Input %s river procince ID: "%text)
    try:
        int(var1)
        ID = int(var1)
        return ID
    except ValueError:
        return -1

i=0
def province_ID_Set():
    var2 = input("Is this the province you want?")
    if 'y' in var2 or 't' in var2:
        print(var2)
        return True
    else:
        return False
def get_province_positions(baseMapPositions):
    PosLines = baseMapPositions.read().splitlines()
    countyList = []
    x=0 
    for line in PosLines:
        if "position=" in line:
            county = ProvincePosition()
            county.pos_name = PosLines[x-3]
            county.id = int(PosLines[x-2].lstrip().rstrip("="))

            #Get X,Y Positions
            p = []
            for t in PosLines[x].lstrip().lstrip("position={").rstrip("}").split():
                try:
                    p.append(Decimal(t))
                except ValueError:
                    pass
            #Assigne X,Y Positions
            county.pos_city_x = p[0]
            county.pos_city_y = p[1]
            county.pos_unit_x = p[2]
            county.pos_unit_y = p[3]
            county.pos_councillor_x = p[4]
            county.pos_councillor_y = p[5]
            county.pos_text_x = p[6]
            county.pos_text_y = p[7]
            county.pos_port_x = p[8]
            county.pos_port_y = p[9]

            #edge case were I am updating stuff that has not been designed for wonders
            if len(p) == 14:
                county.pos_wonder_x = p[10]
                county.pos_wonder_y = p[11]
                county.pos_wonder_costal_x = p[12]
                county.pos_wonder_costal_y = p[13]
            #Get Rotation
            r=[]
            for t in PosLines[x+1].lstrip().lstrip("rotation={").rstrip("}").split():
                try:
                    if "-" in t:
                        r.append(-1*Decimal(t.lstrip("-")))
                    else:
                        r.append(Decimal(t))
                except ValueError:
                    pass
            #Assigne Rotation
            county.pos_city_r = r[0]
            county.pos_unit_r = r[1]
            county.pos_councillor_r = r[2]
            county.pos_text_r = r[3]
            county.pos_port_r = r[4]

            #edge case were I am updating stuff that has not been designed for wonders
            if len(r) == 7:
                county.pos_wonder_r = r[5]
                county.pos_wonder_costal_r = r[6]
            #Get Hight
            h=[]
            for t in PosLines[x+2].lstrip().lstrip("height={").rstrip("}").split():
                #print(t)
                try:
                    if "-" in t:
                        h.append(-1*Decimal(t.lstrip("-")))
                    else:
                        h.append(Decimal(t))
                except ValueError:
                    pass
            #Assigne Hight
            county.pos_city_h = h[0]
            county.pos_unit_h = h[1]
            county.pos_councillor_h = h[2]
            county.pos_text_h = h[3]
            county.pos_port_h = h[4]

            #edge case were I am updating stuff that has not been designed for wonders
            if len(h) == 7:
                county.pos_wonder_h = h[5]
                county.pos_wonder_costal_h = h[6]
            #print(r)
            #print("%s, %s"%(county.pos_name, county.id))
            countyList.append(county)
        x+=1 
    return countyList
def get_province_deff(baseMapDefinition):
    deffMap = baseMapDefinition.read().splitlines()
    deffList = []
    x=0
    for line in deffMap:
        if "province;red;green;blue;x;x" in line:
            continue
        else:
            if x<14000:
                tmpline = line.split(';')
                try:
                    county = ProvinceDefinition()
                    county.red = int(tmpline[1])
                    county.id = int(tmpline[0])
                    county.green = int(tmpline[2])
                    county.blue = int(tmpline[3])
                    county.name = tmpline[4]
                    county.other_info = tmpline[5]
                    deffList.append(county)
                except IndexError:
                    pass
        x +=1
    return deffList
def get_adjacencies(baseMapAdjacencies):
    adjMap = baseMapAdjacencies.read().splitlines()
    adjList = []
    x=0
    for line in adjMap:
        if "From;To;Type;Through;" in line:
            continue
        else:
            tmpline = line.split(';')
            try:
                adj = Adjacencies()
                adj.IDto = int(tmpline[1])
                adj.IDfrom = int(tmpline[0])
                adj.adjType = tmpline[2]
                adj.IDthrough = int(tmpline[3])
                adj.comment = tmpline[8]
                adjList.append(adj)
            except IndexError:
                pass
    return adjList

i=0
def write_positons(countyList, XOffSet, YOffSet):
    outputPositions = open("Output Map\positions_tmp.txt", "w",encoding='utf-8',errors='ignore')
    ThreePlaces = Decimal(10) ** -3
    for county in countyList:
        #print(county.pos_name)
        outputPositions.write(county.pos_name)
        outputPositions.write("\n\t%g="%county.id)
        outputPositions.write("\n\t{")
        #X,Y Positions
        outputPositions.write("\n\t\tposition={")

        outputPositions.write("%s "%(county.pos_city_x.quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(county.pos_city_y.quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(county.pos_unit_x.quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(county.pos_unit_y.quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(county.pos_councillor_x.quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(county.pos_councillor_y.quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(county.pos_text_x.quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(county.pos_text_y.quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(county.pos_port_x.quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(county.pos_port_y.quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(Decimal(county.pos_wonder_x).quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s "%(Decimal(county.pos_wonder_y).quantize(ThreePlaces)+YOffSet))
        outputPositions.write("%s "%(Decimal(county.pos_wonder_costal_x).quantize(ThreePlaces)+XOffSet))
        outputPositions.write("%s"%(Decimal(county.pos_wonder_costal_y).quantize(ThreePlaces)+YOffSet))

        outputPositions.write("}")
        #Rotations
        outputPositions.write("\n\t\trotation={")
       
        outputPositions.write("%s "%county.pos_city_r.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_unit_r.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_councillor_r.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_text_r.quantize(ThreePlaces))
        outputPositions.write("%s "%Decimal(county.pos_port_r).quantize(ThreePlaces))
        outputPositions.write("%s "%Decimal(county.pos_wonder_r).quantize(ThreePlaces))
        outputPositions.write("%s"%Decimal(county.pos_wonder_costal_r).quantize(ThreePlaces))

        outputPositions.write("}")
        #Height
        outputPositions.write("\n\t\theight={")
       
        outputPositions.write("%s "%county.pos_city_h.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_unit_h.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_councillor_h.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_text_h.quantize(ThreePlaces))
        outputPositions.write("%s "%county.pos_port_h.quantize(ThreePlaces))
        outputPositions.write("%s "%Decimal(county.pos_wonder_h).quantize(ThreePlaces))
        outputPositions.write("%s"%Decimal(county.pos_wonder_costal_h).quantize(ThreePlaces))

        outputPositions.write("}")

        outputPositions.write("\n\t}\n")
    outputPositions.close()
#temp for merging old ports into new positions
def write_positons2(countyList, countyList2, XOffSet, YOffSet):
    outputPositions = open("Output Map\positions2_tmp.txt", "w",encoding='utf-8',errors='ignore')
    ThreePlaces = Decimal(10) ** -3
    for county in countyList:
        for county2 in countyList2:
            if county2.id == county.id:
                if county2.id == 447 or (county2.id >720 and county2.id <806) or county2.id ==968 or (county2.id>1244 and county2.id<1261) or county2.id==1345 or (county.id>1500 and county.id<1504):
                    outputPositions.write(county.pos_name)
                    outputPositions.write("\n\t%g="%county.id)
                    outputPositions.write("\n\t{")
                    #X,Y Positions
                    outputPositions.write("\n\t\tposition={")

                    outputPositions.write("%s "%(county.pos_city_x.quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(county.pos_city_y.quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(county.pos_unit_x.quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(county.pos_unit_y.quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(county.pos_councillor_x.quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(county.pos_councillor_y.quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(county.pos_text_x.quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(county.pos_text_y.quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(county2.pos_port_x.quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(county2.pos_port_y.quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(Decimal(county.pos_wonder_x).quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s "%(Decimal(county.pos_wonder_y).quantize(ThreePlaces)+YOffSet))
                    outputPositions.write("%s "%(Decimal(county.pos_wonder_costal_x).quantize(ThreePlaces)+XOffSet))
                    outputPositions.write("%s"%(Decimal(county.pos_wonder_costal_y).quantize(ThreePlaces)+YOffSet))

                    outputPositions.write("}")
                    #Rotations
                    outputPositions.write("\n\t\trotation={")
       
                    outputPositions.write("%s "%county.pos_city_r.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_unit_r.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_councillor_r.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_text_r.quantize(ThreePlaces))
                    outputPositions.write("%s "%Decimal(county2.pos_port_r).quantize(ThreePlaces))
                    outputPositions.write("%s "%Decimal(county.pos_wonder_r).quantize(ThreePlaces))
                    outputPositions.write("%s"%Decimal(county.pos_wonder_costal_r).quantize(ThreePlaces))

                    outputPositions.write("}")
                    #Height
                    outputPositions.write("\n\t\theight={")
       
                    outputPositions.write("%s "%county.pos_city_h.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_unit_h.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_councillor_h.quantize(ThreePlaces))
                    outputPositions.write("%s "%county.pos_text_h.quantize(ThreePlaces))
                    outputPositions.write("%s "%county2.pos_port_h.quantize(ThreePlaces))
                    outputPositions.write("%s "%Decimal(county.pos_wonder_h).quantize(ThreePlaces))
                    outputPositions.write("%s"%Decimal(county.pos_wonder_costal_h).quantize(ThreePlaces))

                    outputPositions.write("}")

                    outputPositions.write("\n\t}\n")
    outputPositions.close()

def write_Definitions(deffList):
    outputDeff = open("Output Map\definition.csv", "w",encoding='utf-8',errors='ignore')
    outputDeff.write("province;red;green;blue;x;x")
    for county in deffList:
        outputDeff.write("\n%g;"%county.id)
        outputDeff.write("%g;"%county.red)
        outputDeff.write("%g;"%county.green)
        outputDeff.write("%g;"%county.blue)
        outputDeff.write("%s;"%county.name)
        outputDeff.write("%s"%county.other_info)
    outputDeff.close()
def write_Adjacencies(adjList):
    outputAdj = open("Output Map\\adjacencies_tmp.csv", "w",encoding='utf-8',errors='ignore')
    outputAdj.write("From;To;Type;Through;-1;-1;-1;-1;Comment")
    for county in adjList:
        outputAdj.write("\n%g;"%county.IDfrom)
        outputAdj.write("%g;"%county.IDto)
        outputAdj.write("%s;"%county.adjType)
        outputAdj.write("%g;"%county.IDthrough)
        outputAdj.write("-1;-1;-1;-1;%s"%county.comment)
    outputAdj.close()
def write_DefaultMap(updaetdDefaultMapList):
    outputdeffault = open("Output Map\\default_tmp.map", "w",encoding='utf-8',errors='ignore')
    for line in updaetdDefaultMapList:
        tmpLine = ""
        for index in line:
            tmpLine += str("%s "%index)
        outputdeffault.write("%s\n"%tmpLine)
    outputdeffault.close()

def threaded_DrawProvinces(x1,x2,y1,y2,z,smallCountyListNames,newSmallCountyListNames,pixMNR,pixNew):
    print("%s - %g / %g"%(smallCountyListNames[z].name,z,len(smallCountyListNames)))
    provinceEnd = False
    for y in  range(y1,y2):
        if provinceEnd:
            break
        else:
            for x in range(x1,x2):
                #print(smallCountyListNames[z].red)
                if pixMNR[x,y] == (smallCountyListNames[z].red, smallCountyListNames[z].green, smallCountyListNames[z].blue):
                    pixNew[x,y] = copy.deepcopy((newSmallCountyListNames[z].red, newSmallCountyListNames[z].green, newSmallCountyListNames[z].blue, 255))
                    #print("%i, %i, %i"%(x,y,z))
                    #print(pixNew[x,y])
                    #print(z)
                    smallCountyListNames[z].lastKnownY = y
                    #print(y)

            if smallCountyListNames[z].lastKnownY > -1 and y > smallCountyListNames[z].lastKnownY + (y2 * 1/64):
                #print("poped:\t%s" %smallCountyListNames[z].name)
                provinceEnd = True
                print("Poped\t %s - %g / %g"%(smallCountyListNames[z].name,z,len(smallCountyListNames)))
                break
    i=0

def draw_UpdatedProvinces(MNRMapProvinces, smallCountyListNames, newSmallCountyListNames):
    pixMNR = MNRMapProvinces.load()
    img = Image.new(MNRMapProvinces.mode, MNRMapProvinces.size, 'white')
    pixNew = img.load()
    if ChropedMap:
        x1,y1=XStart,YStart
        x2,y2=XEnd,YEnd
    else:
        x1,y1=0,0
        x2,y2=MNRMapProvinces.size[0],MNRMapProvinces.size[1]
    z=0
    #print(len(smallCountyListNames))

    pool_size = 10
    pool = Pool(pool_size)

    while z < len(smallCountyListNames):
        pool.apply_async(threaded_DrawProvinces,(x1,x2,y1,y2,z,smallCountyListNames,newSmallCountyListNames,pixMNR,pixNew,))
        z+=1
    pool.close()
    pool.join()

    img.show()
    img.save("Output Map//province_tmp.bmp")
    img.close()


startSet = False
endSet = False
newStartSet = False
bUpdateMap = True


baseMapDefinition = open("Base Map\definition.csv",'r',encoding='utf-8',errors='ignore')
baseMapDefinition2 = open("MNR Map\definition.csv",'r',encoding='utf-8',errors='ignore')
baseMapPositions = open("Base Map\positions.txt",'r',encoding='utf-8',errors='ignore')
MNRMapPositions = open("MNR Map\positions.txt",'r',encoding='utf-8',errors='ignore')
MNRMapAdjacencies = open("MNR Map\\adjacencies.csv",'r',encoding='utf-8',errors='ignore')

MNRDefaultMap = open("MNR Map\default.map",'r',encoding='utf-8',errors='ignore')

try:
    MNRMapProvinces = Image.open("MNR Map\\provinces.bmp")
except:
    print("province map missing will not run map updater")
    bUpdateMap = False

#print(baseMapDefinition.readlines())

#get the starting/ending province IDs for the MNR map and the new postion they will be moved to
if False: #on/off switch
    while startSet is False:
        while startProvicne < 1:
            startProvicne = province_IO("starting")
        startSet = province_ID_Set()
        if startSet is False:
            startProvicne = 0
    i=0
    while endSet is False:
        while endProvince < 1:
            endProvince = province_IO("starting")
        endSet = province_ID_Set()
        if endSet is False:
            endProvince = 0
    i=0
    while newStartSet is False:
        while newStartProvicne < 1:
            newStartProvicne = province_IO("starting")
        newStartSet = province_ID_Set()
        if newStartSet is False:
            newStartProvicne = 0
    i=0
    print("you entered %s" %startProvicne)

#get the map postion information for each province
countyList = get_province_positions(baseMapPositions)
countyList2 = get_province_positions(MNRMapPositions)

#get the map deffinition informaiton for each province
deffList = get_province_deff(baseMapDefinition)
deffList2 = get_province_deff(baseMapDefinition2)

#get the Adjacencies information
adjList2 = get_adjacencies(MNRMapAdjacencies)

#Grab all provinces that will be effected by change
smallCountyListNames = []
for county in deffList2:
    #print("%s, %s"%(county.id,startProvicne))
    if county.id >= startProvicne and county.id <= endProvince:
        smallCountyListNames.append(county)
        #print(county.name)

i=0
#Set province name in new spot
startingDiffrence = newStartProvicne - startProvicne 
newEndProvince = startingDiffrence + endProvince 
newSmallCountyListNames = []
if True:
    for county in deffList:
        if county.id >= newStartProvicne and county.id <= newEndProvince:
            county.name = (smallCountyListNames[i]).name  
            #print("%g, %g, %s"%(i,county.id,county.name))
            county.other_info = (smallCountyListNames[i]).other_info
            newSmallCountyListNames.append(county)
            i +=1
i=0

#change province IDs for positions
countyListMNR = []
for county in countyList2:
    if county.id >= startProvicne and county.id <= endProvince:
        county.id = county.id + startingDiffrence
        countyListMNR.append(county)
        #print(county.id)

i=0
#get lines containing province ID in default.map

defaultMapList = []
defaultMap = MNRDefaultMap.read().splitlines()
for line in defaultMap:
    j= startProvicne
    newTmpLine = ""
    while j <= endProvince+1:
        if str(j) in line:
            if line not in defaultMapList:
                defaultMapList.append(line)
                #print(line)
        j +=1
i=0
#update lines in default map
updaetdDefaultMapList = []
for line in defaultMapList:
    tmpLine = line.split(" ")
    tmpLineList= []
    for index in tmpLine:
        try:
            tmpID = int(index.lstrip().rstrip())
            if tmpID >= startProvicne and tmpID <= endProvince+1:
                index = int(index.lstrip().rstrip()) + startingDiffrence
            #print(index)
        except ValueError:
            pass
        tmpLineList.append(index)
    updaetdDefaultMapList.append(tmpLineList)
    #print(tmpLineList)
i=0
#get and update lines containing province ID in adjancies.csv
NewAdjList = []
for county in adjList2:
    tmpTrue = False
    if county.IDfrom >= startProvicne and county.IDfrom <= endProvince:
        county.IDfrom += startingDiffrence
        tmpTrue = True
    if county.IDto >= startProvicne and county.IDto <= endProvince:
        county.IDto += startingDiffrence
        tmpTrue = True
    if county.IDthrough >= startProvicne and county.IDthrough <= endProvince:
        county.IDthrough += startingDiffrence
        tmpTrue = True
    if tmpTrue:
        NewAdjList.append(county)

i=0


write_positons(countyListMNR, XOffSet, YOffSet)
#write_positons2(countyList, countyList2, XOffSet, YOffSet)
write_Definitions(newSmallCountyListNames)
write_Definitions(deffList)
#write_Adjacencies(adjList2)
write_Adjacencies(NewAdjList)
write_DefaultMap(updaetdDefaultMapList)

#change province map color
if bUpdateMap:
    draw_UpdatedProvinces(MNRMapProvinces, smallCountyListNames, newSmallCountyListNames)