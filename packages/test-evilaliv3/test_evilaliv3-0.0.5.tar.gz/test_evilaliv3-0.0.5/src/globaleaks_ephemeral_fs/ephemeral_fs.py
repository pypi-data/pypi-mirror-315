import argparse
import errno
import os
import stat
from fuse import FUSE, FuseOSError, Operations
from tempfile import mkdtemp

from globaleaks_ephemeral_fs.secure_temporary_file import SecureTemporaryFile

class _EphemeralFS(Operations):
    def __init__(self, storage_directory=None):
        if storage_directory is None:
            storage_directory = mkdtemp()

        self.storage_directory = storage_directory
        self.files = {}  # Track open files and their secure temporary file handlers
        self.default_permissions = 0o660  # Default permissions for files (user read/write)
        self.uid = os.getuid()  # Current user's UID
        self.gid = os.getgid()  # Current user's GID
        self.use_ns=True

    def getattr(self, path, fh=None):
        """Return the attributes of the file or directory."""
        if path == '/':
            # Return attributes for the root directory
            st = {
                'st_mode': (stat.S_IFDIR | 0o750),
                'st_nlink': 2,
            }
        else:
            # Check if the file exists
            secure_file = self.files.get(path)

            if secure_file is None or not os.path.exists(secure_file.filepath):
                raise OSError(errno.ENOENT, "No such file or directory", path)

            # Get the file's metadata using os.stat()
            secure_file_stat = os.stat(secure_file.filepath)

            st = {
                'st_mode': (stat.S_IFREG | 0o660),
                'st_size': secure_file.size,
                'st_nlink': 1,
                'st_uid': self.uid,    # User ID
                'st_gid': self.gid,    # Group ID
                'st_atime': secure_file_stat.st_atime,
                'st_mtime': secure_file_stat.st_mtime,
                'st_ctyme': secure_file_stat.st_ctime
            }

        return st

    def readdir(self, path, fh):
        """Return the list of files in the directory."""
        return ['.', '..'] + [os.path.basename(f) for f in self.files.keys()]

    def create(self, path, mode):
        """Create a new encrypted file."""
        secure_file = SecureTemporaryFile(self.storage_directory)
        secure_file.open('w')
        self.files[path] = secure_file

        os.chmod(secure_file.filepath, self.default_permissions)
        os.chown(secure_file.filepath, self.uid, self.gid)

        return 0

    def open(self, path, flags):
        """Open an encrypted file."""
        secure_file = self.files.get(path)
        if secure_file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        mode = 'w' if (flags & os.O_RDWR or flags & os.O_WRONLY) else 'r'
        secure_file.open(mode)
        return 0

    def write(self, path, data, offset, fh):
        """Write data to the encrypted file."""
        secure_file = self.files.get(path)
        if secure_file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        secure_file.write(data)
        return len(data)

    def read(self, path, size, offset, fh):
        """Read data from the encrypted file."""
        secure_file = self.files.get(path)
        if secure_file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        os.lseek(secure_file.fd, offset, os.SEEK_SET)  # Seek to the read offset
        return secure_file.read(size)

    def release(self, path, fh):
        """Close the file."""
        secure_file = self.files.get(path)
        if secure_file:
            secure_file.close()

    def unlink(self, path):
        """Remove a file."""
        secure_file = self.files.pop(path, None)
        if secure_file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        secure_file.close()
        os.remove(secure_file.filepath)


class EphemeralFS(FUSE):
    """
    A class that mounts an ephemeral filesystem at the given mount point.
    Inherits from FUSE to provide the filesystem mounting functionality.

    Args:
        mount_point (str): The path where the filesystem will be mounted.
        storage_directory (str, optional): The directory used for storage. If None, uses a temporary directory.
        **fuse_args: Additional arguments to pass to the FUSE constructor.
    """
    def __init__(self, mount_point, storage_directory=None, **fuse_args):
        self.mount_point = mount_point
        self.storage_directory = storage_directory

        # Create the mount point directory if it does not exist
        os.makedirs(self.mount_point, exist_ok=True)

        # If a storage directory is specified, create it as well
        if self.storage_directory:
            os.makedirs(self.storage_directory, exist_ok=True)
        else:
            self.storage_directory = None  # Default to None if not provided

        # Initialize the FUSE mount with the EphemeralFS
        super().__init__(_EphemeralFS(self.storage_directory), self.mount_point, **fuse_args)
