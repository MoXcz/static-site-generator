from os import listdir, mkdir, path
from shutil import copy, rmtree


def clean_dir(dir):
    if path.exists(dir):
        rmtree(dir)
    mkdir(dir)


def src_to_dir(src, dir):
    clean_dir(dir)
    if path.exists(src) and path.exists(dir):  # verify the paths do exist
        src_dirs = src.split("/")
        for i in range(len(src_dirs)):  # remove whitespaces from source path
            if src_dirs[i] == "":
                src_dirs.pop(i)

        if len(src_dirs) > 1:
            dir = f"{dir}{src_dirs[1]}"  # adjust destination path
            mkdir(dir)  # create directory

        for entry in listdir(src):  # iterate files inside source directory
            entry = path.join(src, entry)  # adjust path (test.txt -> text/test.txt)
            if path.isfile(entry):
                copy(entry, dir)
            elif not path.isfile(entry):
                src_to_dir(entry, dir)
    print("It worked!")
