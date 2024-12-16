import argparse
from globaleaks_ephemeral_fs.ephemeral_fs import EphemeralFS

def main():
    parser = argparse.ArgumentParser(description="GLOBALEAKS EPHEMERAL FS")
    parser.add_argument('mount_point', help="Path to mount the filesystem")
    parser.add_argument('--storage_directory', '-s', help="Optional storage directory. Defaults to a temporary directory.")
    args = parser.parse_args()

    EphemeralFS(args.mount_point, args.storage_directory, nothreads=True, foreground=True)


if __name__ == '__main__':
    main()
