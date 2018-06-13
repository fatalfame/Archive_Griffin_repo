import os
import shutil

path = '.\sega'
destination = '.\destination'


def main():
    for dirpath,_,filenames in os.walk(path):
        for f in filenames:
            print(f)
            shutil.copy2(os.path.abspath(os.path.join(dirpath, f)), destination)


if __name__ == '__main__':
    main()
