import os, sys, time, datetime

# read app list

csvFile = "/home/zicheng18/data2/az/data"
curtime = time.strftime("%Y-%m-%d-%H-%M-%S")
# print('Current Time: ', curtime)

catPath = "group"
outputDir = "output"
finishedPath = outputDir+"/Finished.txt"
catFileList = os.listdir(catPath)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  new folder... %s ---" % path)

#Read finished list
finishedList = []
if os.path.exists(finishedPath):
    f = open(finishedPath, 'r')
    for line in f:
        finishedCat = line.rstrip()
        finishedList.append(finishedCat)
    if f:
        f.close()

for cat in catFileList:
    if cat == "Finished.txt":
        continue
    if cat[:-4] in finishedList:
        print("Skip"+cat)
        continue
    packList = []
    packFile = catPath + "/" + cat
    outputPath = outputDir + "/" + cat[:-4] + ".csv"

    outputFile = open(outputPath, 'w+')
    outputFile.write("package,sha256,vercode")
    if outputFile:
        outputFile.close()


    def flush():
        sys.stdout.flush()


    print('[Main] Read pack File...')
    f2 = open(packFile, 'r')
    for line in f2:
        pack = line.rstrip().split("\t")[0]  # no matter \r or \n
        packList.append(pack)
    if f2:
        f2.close()

    appMap = {}
    appTimeMap = {}
    vercodeMap = {}
    print('[Main] Match csv File...')
    flush()
    f = open(csvFile, 'r')
    i = 0
    # sha256_0 ,sha1_1,md5_2,dex_date_3,apk_size_4,pkg_name_5,vercode_6,vt_detection_7,vt_scan_date_8,dex_size_9,markets_10
    # 0000003B455A6C7AF837EF90F2EAFFD856E3B5CF49F5E27191430328DE2FA670,9C14D537A7ADB4CFC43D291352F73E05E0CCDD4A,3EDFC78AB53521942798AD551027D04F,2016-04-05 17:58:46,10386469,"com.zte.bamachaye",121,0,2016-06-15 15:26:44,4765888,anzhi

    for line in f:
        lineArray = line.rstrip().split(",")  # no matter \r or \n
        market = lineArray[10]
        tempPack = lineArray[5][1:-1]
        # print(tempPack)
        if tempPack in packList:
            if market == "play.google.com":
                sha256 = lineArray[0]
                vt_scan_date_str = lineArray[8]
                verCode = lineArray[6]
                if not verCode == "":
                    verCode = int(verCode)
                else:
                    verCode = 0
                # vt_scan_date = datetime.datetime.strptime(vt_scan_date_str, "%Y-%m-%d %H:%M:%S")
                # storedDate = datetime.datetime.strptime(storedDate_str, "%Y-%m-%d %H:%M:%S")

                if tempPack in appMap.keys():
                    maxVercode = vercodeMap[tempPack]
                    if verCode > maxVercode:
                        appMap[tempPack] = sha256
                        appTimeMap[tempPack] = vt_scan_date_str
                        vercodeMap[tempPack] = verCode
                else:
                    i = i + 1
                    print(cat, i, tempPack)
                    appMap[tempPack] = sha256
                    vercodeMap[tempPack] = int(verCode)
                    appTimeMap[tempPack] = vt_scan_date_str
        # TODO pkg is empty here
    if f:
        f.close()

    outputFile = open(outputPath, 'a+')
    for pack in appMap.keys():
        result = "%s,%s,%d" % (pack, appMap[pack], vercodeMap[pack])
        outputFile.write(result + "\n")
    if outputFile:
        outputFile.close()

    with open(finishedPath, "a") as finishedFile:
        finishedFile.write(cat + "\n")
    if finishedFile:
        finishedFile.close()
