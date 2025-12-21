import unittest
import os
import tempfile
import shutil
from src.utils import resolve_path, is_safe_path, get_file_info

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_resolve_path_parent(self):
        result = resolve_path('/home/user/folder', '..')
        expected = '/home/user'
        self.assertEqual(result, expected)
    
    def test_resolve_path_home(self):
        result = resolve_path('/home/user/folder', '~')
        expected = os.path.expanduser('~')
        self.assertEqual(result, expected)
    
    def test_resolve_path_relative(self):
        result = resolve_path('/home/user', 'folder')
        expected = '/home/user/folder'
        self.assertEqual(result, expected)
    
    def test_is_safe_path_safe(self):
        self.assertTrue(is_safe_path('my_folder'))
        self.assertTrue(is_safe_path('file.txt'))
    
    def test_is_safe_path_unsafe(self):
        self.assertFalse(is_safe_path('..'))
        self.assertFalse(is_safe_path('/'))
    
    def test_get_file_info(self):
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        size, mtime = get_file_info(test_file)
        self.assertEqual(size, 4)
        self.assertIsNotNone(mtime)

if __name__ == '__main__':
    unittest.main()
