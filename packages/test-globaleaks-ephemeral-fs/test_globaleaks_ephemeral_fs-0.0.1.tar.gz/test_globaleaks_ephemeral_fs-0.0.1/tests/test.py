import errno
import os
import shutil
import unittest
from tempfile import mkdtemp
from unittest.mock import patch
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20
from globaleaks_ephemeral_fs import EphemeralFile, EphemeralOperations, EphemeralFS

TEST_PATH='TESTFILE.TXT'
TEST_DATA=b'This is a test.'


class TestEphemeralFile(unittest.TestCase):
    def setUp(self):
        self.storage_dir = mkdtemp()
        self.ephemeral_file = EphemeralFile(self.storage_dir)

    def tearDown(self):
        shutil.rmtree(self.storage_dir)

    def test_create_and_write_file(self):
        with self.ephemeral_file.open('w') as file:
            file.write(TEST_DATA)

        self.assertTrue(os.path.exists(self.ephemeral_file.filepath))

    def test_encryption_and_decryption(self):
        with self.ephemeral_file.open('w') as file:
            file.write(TEST_DATA)

        with self.ephemeral_file.open('r') as file:
            decrypted_data = file.read()

        self.assertEqual(decrypted_data, TEST_DATA)

    def test_file_cleanup(self):
        file_path = self.ephemeral_file.filepath
        del self.ephemeral_file
        self.assertFalse(os.path.exists(file_path))


class TestEphemeralOperations(unittest.TestCase):
    def setUp(self):
        TEST_PATH = '/testfile'
        self.storage_dir = mkdtemp()
        self.operations = EphemeralOperations(self.storage_dir)

    def tearDown(self):
        for file in self.operations.files.values():
            os.remove(file.filepath)
        os.rmdir(self.storage_dir)

    def test_create_file(self):
        self.operations.create(TEST_PATH, 0o660)
        self.assertIn(TEST_PATH, self.operations.files)

    def test_open_existing_file(self):
        self.operations.create(TEST_PATH, 0o660)
        self.operations.open(TEST_PATH, os.O_RDONLY)

    def test_write_and_read_file(self):
        # Create the file first
        self.operations.create(TEST_PATH, 0o660)

        # Open the file for writing and write data
        self.operations.open(TEST_PATH, os.O_RDWR)
        self.operations.write(TEST_PATH, TEST_DATA, 0, None)

        # Release the file after writing (flushes any remaining changes)
        self.operations.release(TEST_PATH, None)

        # Open the file for reading
        self.operations.open(TEST_PATH, os.O_RDONLY)

        # Read the data from the file
        read_data = self.operations.read(TEST_PATH, len(TEST_DATA), 0, None)

        # Verify that the data read is the same as the written data
        self.assertEqual(read_data, TEST_DATA)

        # Release the file after reading
        self.operations.release(TEST_PATH, None)


    def test_unlink_file(self):
        self.operations.create(TEST_PATH, 0o660)
        self.assertIn(TEST_PATH, self.operations.files)

        self.operations.unlink(TEST_PATH)
        self.assertNotIn(TEST_PATH, self.operations.files)

    def test_file_not_found(self):
        with self.assertRaises(OSError) as context:
            self.operations.open('/nonexistentfile', os.O_RDONLY)
        self.assertEqual(context.exception.errno, errno.ENOENT)

if __name__ == '__main__':
    unittest.main()

