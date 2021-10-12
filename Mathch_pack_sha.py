import os, sys, time




# read app list
packList = []
csvFile = "/home/zicheng18/data2/az/data"
packFile = "crawlPack_10111115.txt"
curtime = time.strftime("%Y-%m-%d-%H-%M-%S")
#print('Current Time: ', curtime)
outputPath = curtime+"output.csv"

outputFile = open(outputPath, 'w+')
print("package,sha256", file=outputFile)


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
print('[Main] Match csv File...')
flush()
f = open(csvFile, 'r')
i = 0
#sha256_0 ,sha1_1,md5_2,dex_date_3,apk_size_4,pkg_name_5,vercode_6,vt_detection_7,vt_scan_date_8,dex_size_9,markets_10
#0000003B455A6C7AF837EF90F2EAFFD856E3B5CF49F5E27191430328DE2FA670,9C14D537A7ADB4CFC43D291352F73E05E0CCDD4A,3EDFC78AB53521942798AD551027D04F,2016-04-05 17:58:46,10386469,"com.zte.bamachaye",121,0,2016-06-15 15:26:44,4765888,anzhi

for line in f:
    lineArray = line.rstrip().split  #no matter \r or \n
    market = line[10]
    tempPack = line[5][1:-1]
    if tempPack in packList and market=="play.google.com":
        sha256 = line[0]
        vt_scan_date_str = line[8]
        if pack in appMap.keys():
            storedDate_str = appTimeMap[pack]
            vt_scan_date = datetime.strptime(vt_scan_date_str, "%Y-%m-%d %H:%M:%S")
            storedDate = datetime.strptime(storedDate_str, "%Y-%m-%d %H:%M:%S")
            if vt_scan_date > storeDate:
                appMap[pack] = sha256
                appTimeMap[pack] = vt_scan_date
        else:
            appMap[pack] = sha256
            appTimeMap[pack] = vt_scan_date_str
    #TODO pkg is empty here
if f:
    f.close()

print(appMap, file=outputFile)
if outputFile:
    outputFile.close()
