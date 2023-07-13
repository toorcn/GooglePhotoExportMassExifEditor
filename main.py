import os
# For python Modules
import datetime
import sys
sys.path.append("./pyModules")
# exif Module import
from exif import Image
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

folder_path = ".\process"

loop = 0
processedCount = 0
dtOriginalEXIFCount = 0
print("[VRBL] Processing " + str(len(os.listdir(folder_path))) + " files.")
while True:
    tempProcessedCount = 0
    # get all files in folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        file_prefix = file_path[10:13]
        if file_name[-3:] == "mp4" or file_name[-3:] == "dng":
            print("Unsupported type: " + file_name)
            continue
        # if file_name[-3:] == "dng":
        #     with open(file_path, 'rb') as image_file:
        #         image = Image(image_file)
        #     print('DNG - ' + image.has_exif)
        #     continue
        retrieved_date = ""
        if file_prefix == "IMG":
            rYear = file_path[14:18]
            rMonth = file_path[18:20]
            rDate = file_path[20:22]
            rHour = file_path[23:25]
            rMinute = file_path[25:27]
            rSecond = file_path[27:29]
            retrieved_date = f"{rYear}:{rMonth}:{rDate} {rHour}:{rMinute}:{rSecond}"
        if file_prefix == "PXL":
            rYear = file_path[14:18]
            rMonth = file_path[18:20]
            rDate = file_path[20:22]
            rHour = str(int(file_path[23:25]) + 8)
            rMinute = file_path[25:27]
            rSecond = file_path[27:29]

            if int(rHour) > 24:
                rHour = str(int(rHour) - 24)
                tempRetrieved_date = f"{rYear}-{rMonth}-{rDate} {rHour}:{rMinute}:{rSecond}"
                # print("trd" + tempRetrieved_date)
                dt = parse(tempRetrieved_date, yearfirst=True)
                print(tempRetrieved_date, dt)
                dt2 = relativedelta(days=1)
                dt3 = dt + dt2
                print(dt, dt3)
                
                retrieved_date = tempRetrieved_date
            else:
                retrieved_date = f"{rYear}:{rMonth}:{rDate} {rHour}:{rMinute}:{rSecond}"

            # retrieved_date = f"{rYear}:{rMonth}:{rDate} {rHour}:{rMinute}:{rSecond}"
        if file_prefix == "Scr":
            rYear = file_path[21:25]
            rMonth = file_path[26:28]
            rDate = file_path[29:31]
            rHour = file_path[32:34]
            rMinute = file_path[35:37]
            rSecond = file_path[38:40]
            retrieved_date = f"{rYear}:{rMonth}:{rDate} {rHour}:{rMinute}:{rSecond}"
        if file_prefix == "sha":
            rYear = file_path[21:25]
            rMonth = file_path[26:28]
            rDate = file_path[29:31]
            rHour = file_path[32:34]
            rMinute = file_path[35:37]
            rSecond = file_path[38:40]
            retrieved_date = f"{rYear}:{rMonth}:{rDate} {rHour}:{rMinute}:{rSecond}"
        if retrieved_date == "":
            print("Unknown type: " + file_name)
            continue
        
        try:
            dt = parse(retrieved_date, False)
            # print(dt.date().day)
        except:
            print(f"Date could not be parsed: ({retrieved_date}) {file_name}")
            continue

        try:
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as image_file:
                    image = Image(image_file)

                modifiedFlag = False

                # if no EXIF then add
                if (not image.has_exif) or (not hasattr(image, "datetime_original")):
                    image.datetime_original = retrieved_date
                    modifiedFlag = True

                if modifiedFlag:
                    with open(file_path, 'wb') as new_image_file:
                        new_image_file.write(image.get_file())
                    print(f"[VRBL] Processed ({file_prefix}) ({file_name[-20:]}) to ({retrieved_date})")
                    tempProcessedCount += 1
                    continue
                    
        except:
            print("Error processing " + file_path)
            
    loop += 1   
    if tempProcessedCount == 0:
        noDateCount = len(os.listdir(folder_path)) - (processedCount + dtOriginalEXIFCount)
        print(f"[VRBL] Processed ({str(processedCount)}/{str(len(os.listdir(folder_path)))}) files, {noDateCount} undated. With {loop} passes.")
        break
    else:
        processedCount += tempProcessedCount
        print(f"Looping again. Last processed count: {str(processedCount)}")

    # print(f"[Debug]: {image.has_exif} | {file_name}")
    # if image.list_all():
    
    # print("datetime " + image.datetime)
    # if callable(image.list_all()):
    #     print("L")
    #     print(image.list_all())
    # if hasattr(image, "datetime"):
    #     print("datetime " + image.datetime)
    # elif hasattr(image, "datetime_original"):
    #     print("datetimeOriginal " + image.datetime_original)
    # else:
    #     0
    #     # print(getattr(image))
    # print("\n")

    # 

    # if hasattr(image, "datetime_original"):
    #     print(file_name[-20:] + " " + image.datetime_original)
    #     print("skip dtO")
    #     continue
    # if hasattr(image, "datetime"):
    #     print(file_name[-20:] + " " + image.datetime)
    #     print("skip dt")
    #     continue
    # if not hasattr(image, "datetime"):
    #     if (not hasattr(image, "datetime_original")) and file_prefix == "PXL":
    #         image.datetime_original = retrieved_date
    #         modifiedFlag = True
    #     elif file_prefix == "IMG" or file_prefix == "Scr":
    #         image.datetime = retrieved_date
    #         modifiedFlag = True
            
    # 
    
    # # change IMG or Scr
    # if (file_prefix == "IMG" or file_prefix == "Scr") and image.list_all() == []:
    #     image.datetime = retrieved_date
    #     print("mod1")
    #     modifiedFlag = True
    # # print(f"1 {modifiedFlag}")

    # if ( (not hasattr(image, "datetime_original")) and file_prefix == "PXL") and not modifiedFlag:
    #     image.datetime_original = retrieved_date
    #     modifiedFlag = True
    # # print(f"2 {modifiedFlag}")

    # if (file_prefix == "IMG" or file_prefix == "Scr") and image.list_all() == []:
    #     image.datetime = retrieved_date
    #     with open(file_path, 'wb') as new_image_file:
    #         new_image_file.write(image.get_file())
    #     print(f"Processed ({file_prefix}) ({file_name[20:]}) to ({retrieved_date})")
    #     processedCount += 1
    #     continue

    # if (not hasattr(image, "datetime_original")):
    #     image.datetime_original = retrieved_date
    #     with open(file_path, 'wb') as new_image_file:
    #         new_image_file.write(image.get_file())
    #     print(f"Processed ({file_prefix}) ({file_name[20:]}) to ({retrieved_date})")
    #     processedCount += 1
    #     continue