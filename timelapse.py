import cv2
import os
import sys
#from matplotlib import pyplot as plt

def print_progress(percent):
    s = ''
    for x in range(0,100,2): 
        if x < percent: s = s + '='
        else: s = s + ' '
    ss = '[' + s + '] ' + '%02d'%percent + ' %\r'                
    sys.stdout.write( ss )
    sys.stdout.flush()    

def equalize_image(im):
    H, S, V = cv2.split(cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    eq_V = cv2.equalizeHist(V)
    eq_im = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2BGR)
    return eq_im    

def make_video(folder, vid_path, fps=20, eq=True):
    images = os.listdir(folder)
    size = cv2.imread(folder+'/'+images[0]).shape[:2]
    size = (size[1], size[0])
    print 'Size: ', size
    print 'Length: ', len(images)/float(fps), 's'
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    out = cv2.VideoWriter(vid_path, fourcc, float(fps), size)

    i=0
    percent=0
    print_progress(0)
    for img in images:
        im = cv2.imread(folder+'/'+img) 
        im = equalize_image(im)
        out.write(im)

        oldpercent = percent
        percent = int(100 * i/float(len(images)))
        i = i + 1
        if oldpercent != percent:
            print_progress(percent)
    out.release()
    print_progress(100)
    print '\n'

if __name__ == '__main__':
    make_video( sys.argv[1], sys.argv[1]+".avi", sys.argv[2] )
