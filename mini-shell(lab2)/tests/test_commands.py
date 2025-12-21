import unittest
import os
import tempfile
import shutil
from src.commands import MiniShell

class TestMiniShell(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.shell = MiniShell()
        self.shell.current_dir = self.test_dir
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_mkdir(self):
        self.shell.mkdir('test_folder')
        folder_path = os.path.join(self.test_dir, 'test_folder')
        self.assertTrue(os.path.isdir(folder_path))
    
    def test_rmdir(self):
        folder_path = os.path.join(self.test_dir, 'test_folder')
        os.makedirs(folder_path)
        self.shell.rmdir('test_folder')
        self.assertFalse(os.path.exists(folder_path))
    
    def test_cat_file(self):
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('Hello World')
        
        self.shell.cat('test.txt')
    
    def test_cp_file(self):
        src_file = os.path.join(self.test_dir, 'source.txt')
        with open(src_file, 'w') as f:
            f.write('test content')
        
        self.shell.cp('source.txt', 'copy.txt')
        dst_file = os.path.join(self.test_dir, 'copy.txt')
        self.assertTrue(os.path.exists(dst_file))
    
    def test_mv_file(self):
        src_file = os.path.join(self.test_dir, 'old.txt')
        with open(src_file, 'w') as f:
            f.write('test')
        
        self.shell.mv('old.txt', 'new.txt')
        new_file = os.path.join(self.test_dir, 'new.txt')
        self.assertTrue(os.path.exists(new_file))
        self.assertFalse(os.path.exists(src_file))
    
    def test_rm_file(self):
        test_file = os.path.join(self.test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.shell.rm('test.txt')
        self.assertFalse(os.path.exists(test_file))
    
    def test_cd_change_directory(self):
        subfolder = os.path.join(self.test_dir, 'subfolder')
        os.makedirs(subfolder)
        
        self.shell.cd('subfolder')
        self.assertEqual(self.shell.current_dir, subfolder)
    
    def test_ls_list_files(self):
        test_file = os.path.join(self.test_dir, 'file.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.shell.ls()

if __name__ == '__main__':
    unittest.main()
