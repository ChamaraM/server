from flask import Flask
from PIL import Image
from PIL import ImageChops
import sys, time

app = Flask(__name__)

@app.route('/')
def index():
    
    
    start = time.time()
    img1 = 'bills2.jpg'
    img2 = 'bills2a.jpg'
    # ensure we're workign with images not string representations
    image1 = Image.open(img1) if isinstance(img1, str) else img1
    image2 = Image.open(img2) if isinstance(img2, str) else img2


    # First thing to do is resize image2 to be image1's dimensions
    image2 = image2.resize(image1.size, Image.BILINEAR)


    # each of these are lists of (r,g,b) values
    image1_pixels = list(image1.getdata())
    image2_pixels = list(image2.getdata())

    #print image2_pixels
    # now need to compare the r, g, b values for each image2_pixels

    # initialize vars
    i = 0
    tot_img_diff = 0
    diff_pixels = 0

    for pix1 in image1_pixels:
        pix2 = image2_pixels[i]

        r_diff = abs(pix1[0] - pix2[0])
        g_diff = abs(pix1[1] - pix2[1])
        b_diff = abs(pix1[2] - pix2[2])
        
        #print r_diff
        
        tot_pix_diff = (r_diff + g_diff + b_diff)

        if tot_pix_diff != 0:
            #print("comparing: " , pix1 , " to " , pix2)
            diff_pixels += 1
            #print diff_pixels
        i += 1

        # keep a running total of the difference of each pixel triplet
        tot_img_diff += tot_pix_diff
        
    # the greatest difference will be 765 * image1.size

    # now calculate our proprietary 'similarity score'
    # similarity = 1 - difference %
    # difference % = tot_img_diff / (image1_size * 255 * 3)
    # where the denominator is the maximum difference

    print(i)
    print(tot_img_diff)

    tot_pix = (image1.size[0] * image1.size[1]) 
    hues = 255
    channels = 3
    
    #print image1.size[0]
    #print tot_pix
    #print diff_pixels 
    #
    #img = Image.open(filename)
    #width, height = img1.size
    
    #print tot_pix
    
    img_diff = float(diff_pixels) /float( tot_pix)
    img_sim = 1 - img_diff
    #print img_diff

    #print("there were", diff_pixels , "mis-matched pixels out of a total of", tot_pix , "pixels")

    print("[PIXEL]: the two images are {:.2%} different".format(img_diff))
    print("[PIXEL]: the two images are {:.2%} similar".format(img_sim))
    
    print("Completed in {time} seconds".format(time=time.time()-start))
    
    return "Done!"

if __name__ == "__main__":
            app.run(host='0.0.0.0')