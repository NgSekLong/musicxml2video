import math
start=-0.875
interval=1.05946305

print('Select All:')
for i in range(-49,48):
    if i > 0:
        value = math.pow(interval, abs(i)) - 1
    else:
        value =  math.pow(1 / interval, abs(i)) - 1
    value = round(value, 5)
    value *= 100
    #print ("The value when i=" + str(i) + " is:" + str(value) )

    print('ChangePitch:Percentage="'+str(value)+'" SBSMS="1"')
    print('ExportMp3:\nUndo:\nRedo:')
