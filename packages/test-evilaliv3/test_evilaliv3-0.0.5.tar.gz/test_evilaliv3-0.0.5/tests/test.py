import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile

from globaleaks_ephemeral_fs.ephemeral_fs import EphemeralFS, mount_ephemeral_fs

class TestEphemeralFS(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file system instance before each test."""
        self.fs = EphemeralFS()
        self.test_path = '/testfile'

    def test_create_file(self):
        """Test creating a new file in the ephemeral encrypted file system."""
        # Create the file
        result = self.fs.create(self.test_path, 0o660)
        
        # Verify that the file has been added to the internal file dictionary
        self.assertIn(self.test_path, self.fs.files)
        self.assertEqual(result, 0)  # Check that the file creation returned success

    def test_write_file(self):
        """Test writing data to a file."""
        data = "This is a test."

        # Create the file first
        self.fs.create(self.test_path, 0o660)

        # Open the file for writing
        self.fs.open(self.test_path, os.O_RDWR)

        # Write data to the file
        written_length = self.fs.write(self.test_path, data, 0, None)

        # Verify that the correct number of bytes were written
        self.assertEqual(written_length, len(data))

        # Release the file after writing (flushes any remaining changes)
        self.fs.release(self.test_path, None)

        # Check the file's permissions, UID, and GID after writing
        file_attrs = self.fs.getattr(self.test_path)
        self.assertEqual(file_attrs['st_mode'] & 0o777, 0o660)  # Verify permissions
        self.assertEqual(file_attrs['st_uid'], os.getuid())     # Verify UID
        self.assertEqual(file_attrs['st_gid'], os.getgid())     # Verify GID

    def test_read_file(self):
        """Test reading data from a file."""
        data = b"This is a test."

        # Create the file first
        self.fs.create(self.test_path, 0o660)

        # Open the file for writing and write data
        self.fs.open(self.test_path, os.O_RDWR)
        self.fs.write(self.test_path, data, 0, None)

        # Release the file after writing (flushes any remaining changes)
        self.fs.release(self.test_path, None)

        # Open the file for reading
        self.fs.open(self.test_path, os.O_RDONLY)

        # Read the data from the file
        read_data = self.fs.read(self.test_path, len(data), 0, None)

        # Verify that the data read is the same as the written data
        self.assertEqual(read_data, data)

        # Release the file after reading
        self.fs.release(self.test_path, None)

    def test_readdir(self):
        """Test the directory listing."""
        # Create two files
        self.fs.create(self.test_path, 0o660)
        self.fs.create('/testfile2', 0o660)

        # Get directory contents (with file handles)
        result = self.fs.readdir('/', None)

        # Verify that the directory listing contains the files
        self.assertIn('.', result)
        self.assertIn('..', result)
        self.assertIn('testfile', result)
        self.assertIn('testfile2', result)

    def test_unlink_file(self):
        """Test removing a file."""
        # Create a file first
        self.fs.create(self.test_path, 0o660)

        # Ensure the file exists before unlinking
        self.assertIn(self.test_path, self.fs.files)

        # Unlink the file
        self.fs.unlink(self.test_path)

        # Verify that the file has been removed
        self.assertNotIn(self.test_path, self.fs.files)


class TestMountEphemeralFS(unittest.TestCase):
    @patch('os.makedirs')  # Mock os.makedirs to avoid creating directories
    @patch('fuse.FUSE')  # Mock the FUSE constructor
    def test_mount_with_storage_directory(self, mock_fuse, mock_makedirs):
        """Test mount with a provided storage_directory using temporary directories."""
        # Create temporary directories for mount point and storage directory
        mount_point = tempfile.mkdtemp()
        storage_directory = tempfile.mkdtemp()

        try:
            # Call the function
            mount_ephemeral_fs(mount_point, storage_directory)

            # Check that os.makedirs was called for both mount_point and storage_directory
            mock_makedirs.assert_any_call(mount_point, exist_ok=True)
            mock_makedirs.assert_any_call(storage_directory, exist_ok=True)

            # Ensure FUSE was called with the correct arguments
            mock_fuse.assert_called_once_with(
                mock.ANY,  # EphemeralFS instance
                mount_point,
                **{}  # Assuming no additional fuse_args were passed
            )
        finally:
            # Clean up temporary directories
            os.rmdir(mount_point)
            os.rmdir(storage_directory)

    @patch('os.makedirs')  # Mock os.makedirs to avoid creating directories
    @patch('fuse.FUSE')  # Mock the FUSE constructor
    def test_mount_without_storage_directory(self, mock_fuse, mock_makedirs):
        """Test mount with no storage_directory (default to None) using temporary directories."""
        # Create a temporary directory for the mount point
        mount_point = tempfile.mkdtemp()

        try:
            # Call the function
            mount_ephemeral_fs(mount_point)

            # Check that os.makedirs was called only for mount_point
            mock_makedirs.assert_called_once_with(mount_point, exist_ok=True)

            # Ensure FUSE was called with the correct arguments
            mock_fuse.assert_called_once_with(
                mock.ANY,  # EphemeralFS instance
                mount_point,
                **{}  # Assuming no additional fuse_args were passed
            )
        finally:
            # Clean up temporary directory
            os.rmdir(mount_point)

    @patch('os.makedirs')  # Mock os.makedirs to avoid creating directories
    @patch('fuse.FUSE')  # Mock the FUSE constructor
    def test_fuse_called_with_storage_directory(self, mock_fuse, mock_makedirs):
        """Test that FUSE is called with the correct storage directory using temporary directories."""
        # Create temporary directories for mount point and storage directory
        mount_point = tempfile.mkdtemp()
        storage_directory = tempfile.mkdtemp()

        try:
            # Call the function with additional fuse_args
            mount_ephemeral_fs(mount_point, storage_directory)

            # Ensure FUSE was called with the correct storage_directory argument
            mock_fuse.assert_called_once_with(
                MagicMock(storage_directory=storage_directory),  # EphemeralFS with storage_directory
                mount_point
            )
        finally:
            # Clean up temporary directories
            os.rmdir(mount_point)
            os.rmdir(storage_directory)

if __name__ == '__main__':
    unittest.main()
