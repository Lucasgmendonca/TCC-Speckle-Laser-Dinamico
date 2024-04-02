import cv2
import os
from datetime import datetime

def captcore(vidObj, outPth, *args):
    # parameters check (existence)
    if len(args) < 4:
        print('captcore: wrong number of arguments!\n\n')
        return 1
    else:
        if isinstance(args[1], str):
            filPtt = args[1]
            imgFst = args[2]
            imgLst = args[3]
            auxArg = 4
        else:
            imgFst = args[1]
            imgLst = args[2]
            auxArg = 3

        for idxArg in range(auxArg, len(args)):
            if len(args[idxArg]) == 1:
                grbItv = args[idxArg]
            else:
                regItr = args[idxArg]

    # internal parameters (first ones)
    vidGen = vidObj.get(cv2.CAP_PROP_BACKEND) # general information
    vidRes = (int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))) # resolution
    vidFps = vidObj.get(cv2.CAP_PROP_FPS) # frames per second

    # not supplied parameters (providing default values)
    if 'filPtt' not in locals():
        filPtt = 'Img%03d.bmp'
    if 'grbItv' not in locals():
        grbItv = 1
    if 'regItr' not in locals():
        regItr = [0, 0, vidRes[0], vidRes[1]]

    # parameters check (consistency)
    if (grbItv < 1) or (grbItv > 99):
        print('captcore: frame grab interval must be a scalar between 0 and 99!\n\n')
        return 2
    if any(val < 0 for val in regItr[:4]):
        print('captcore: region of interest is not consistent!\n\n')
        return 3
    if any((regItr[0] + regItr[2], regItr[1] + regItr[3]) > vidRes):
        print('captcore: region of interest is not compatible with video resolution!\n\n')
        return 4
    
    # output directory creation (if necessary)
    if not OutPth.endswith('/'):
        OutPth += '/'
    if not os.path.exists(OutPth):
        os.makedirs(OutPth)

# internal parameters (last ones)
    imgNum = imgLst - imgFst + 1 # number of images
    smpTme = 1 / (vidFps / grbItv) # sampling time
    tmeOut = 20 * imgNum * smpTme # timeout (twenty times the estimated acquisition time)
    pthPtt = outPth.replace('\\', '\\\\') + filPtt # output file name pattern (including the file path)

# acquisition configuration
    vidObj.set(cv2.CAP_PROP_FPS, grbItv)
    vidObj.set(cv2.CAP_PROP_FRAME_COUNT, imgNum)
    vidObj.set(cv2.CAP_PROP_CONVERT_RGB, False)
    vidObj.set(cv2.CAP_PROP_FRAME_WIDTH, regItr[0])
    vidObj.set(cv2.CAP_PROP_FRAME_HEIGHT, regItr[1])
    vidObj.set(cv2.CAP_PROP_POS_X, regItr[2])
    vidObj.set(cv2.CAP_PROP_POS_Y, regItr[3])
    vidObj.set(cv2.CAP_PROP_FPS, tmeOut)



# image acquisition
    print('captcore: acquisition started, please wait!\n')
    imgList = []
    for _ in range(imgNum):
        ret, frame = vidObj.read()
        if not ret:
            print('Error reading frame. Exiting...')
            return 5
        imgList.append(frame)
    print('captcore: acquisition completed, saving the images!\n')

# image saving
    for idxImg, img in enumerate(imgList):
        filNme = pthPtt % (idxImg + imgFst)
        cv2.imwrite(filNme, img)

# information file creation
    with open(outPth + 'info.txt', 'w+') as filIdt:
        # camera general information
        filIdt.write('Camera general information:\n')
        filIdt.write(f'\t* Name: {vidObj.getBackendName()}\n')
        filIdt.write(f'\t* Resolution: {vidRes[0]} x {vidRes[1]}\n')
        filIdt.write(f'\t* Frame rate: {vidFps}\n\n')
        filIdt.write('Acquisition information:\n')
        filIdt.write(f'\t* Date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        filIdt.write(f'\t\t* HrzOff: {regItr[0]}\n')
        filIdt.write(f'\t\t* VrtOff: {regItr[1]}\n')
        filIdt.write(f'\t\t* HrzLen: {regItr[2]}\n')
        filIdt.write(f'\t\t* VrtLen: {regItr[3]}\n')
        filIdt.write(f'\t* Frame Grab Interval: first of every {grbItv} frame(s)\n')
        filIdt.write(f'\t\t* Thus, the sampling time was {smpTme} seconds\n\n')
    
    # error code
    return 0  # no error