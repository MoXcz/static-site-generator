from copy_static_files import src_to_dir


def main():
    dir_public = "public/"  # delete this one
    dir_static = "static/"  # copy to this one
    src_to_dir(dir_static, dir_public)


if __name__ == "__main__":
    main()
