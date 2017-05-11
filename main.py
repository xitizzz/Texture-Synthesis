from efros import efros_algorithm
import settings as st
import time


def main():
    img_names = ["T1.gif", "T2.gif", "T3.gif", "T4.gif", "T5.gif"]
    log = open("Log.txt", "wb")
    for img in img_names:
        for i in [5, 9, 11, 15, 21]:
            print img
            st.set_window(i)
            start = time.time()
            efros_algorithm(str(st.input_path+img), i, 200, 200, img.split('.')[0]+"_W"+str(i)+".gif")
            end = time.time()
            log.write("Texture {:s} \t Windows Size {:d} \t Time {:.2f} sec".format(img, i, (end-start)))
            print "Finished in "+str(end-start)+" seconds"
    log.close()


if __name__ == "__main__":
    main()

