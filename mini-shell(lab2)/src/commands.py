import os
import shutil
import zipfile
import tarfile
import re
import json
from pathlib import Path
from datetime import datetime
from src.logger import log_cmd, setup_logging
from src.utils import get_file_info, is_safe_path, resolve_path


class CommandHistory:
    
    def __init__(self, history_file='.his   tory'):
        self.history_file = history_file
        self.history = []
        self.undo_stack = []
        self.trash_dir = '.trash'
        self._ensure_trash_exists()
        self._load_history()
    
    def _ensure_trash_exists(self):
        if not os.path.exists(self.trash_dir):
            os.makedirs(self.trash_dir)
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add(self, cmd, cmd_type=None, args=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': cmd,
            'type': cmd_type,
            'args': args
        }
        self.history.append(entry)
        self._save_history()
    
    def add_undo(self, cmd_type, operation_info):
        self.undo_stack.append({
            'type': cmd_type,
            'info': operation_info,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_history(self, count=10):
        return self.history[-count:]
    
    def undo(self):
        if not self.undo_stack:
            return None, "История undo пуста"
        
        undo_op = self.undo_stack.pop()
        return undo_op, None


class MiniShell:
    def __init__(self):
        setup_logging()
        self.current_dir = os.path.expanduser('~')
        self.history = CommandHistory()

    def ls(self, path=None, detailed=False):
        try:
            target = resolve_path(self.current_dir, path or '.')
            items = os.listdir(target)
            
            for item in items:
                if detailed:
                    item_path = os.path.join(target, item)
                    size, mtime = get_file_info(item_path)
                    perms = oct(os.stat(item_path).st_mode)[-3:]
                    is_dir = 'd' if os.path.isdir(item_path) else '-'
                    print(f"{is_dir}{perms} {size:>10} {mtime} {item}")
                else:
                    print(item)
            
            self.history.add(f"ls {'-l' if detailed else ''} {path or '.'}", 'ls', {'path': path, 'detailed': detailed})
            log_cmd(f"ls {'-l' if detailed else ''} {path or '.'}")
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"ls {'-l' if detailed else ''} {path or '.'}", str(e))

    def cd(self, path):
        try:
            new_dir = resolve_path(self.current_dir, path)
            if not os.path.isdir(new_dir):
                raise NotADirectoryError("Каталог не существует")
            self.current_dir = new_dir
            print(self.current_dir)
            log_cmd(f"cd {path}")
            self.history.add(f"cd {path}", 'cd', {'path': path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"cd {path}", str(e))

    def chdir(self, path):
        try:
            new_dir = resolve_path(self.current_dir, path)
            if not os.path.isdir(new_dir):
                raise NotADirectoryError("Каталог не существует")
            os.chdir(new_dir)
            self.current_dir = new_dir
            print(f"Изменен каталог: {self.current_dir}")
            log_cmd(f"chdir {path}")
            self.history.add(f"chdir {path}", 'chdir', {'path': path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"chdir {path}", str(e))

    def mkdir(self, folder):
        try:
            dir_path = resolve_path(self.current_dir, folder)
            os.makedirs(dir_path)
            print(f"Создано: {folder}")
            log_cmd(f"mkdir {folder}")
            self.history.add(f"mkdir {folder}", 'mkdir', {'path': folder})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"mkdir {folder}", str(e))

    def rmdir(self, folder):
        try:
            dir_path = resolve_path(self.current_dir, folder)
            trash_path = os.path.join(self.history.trash_dir, os.path.basename(folder))
            shutil.copytree(dir_path, trash_path, dirs_exist_ok=True)
            shutil.rmtree(dir_path)
            print(f"Удалено: {folder}")
            log_cmd(f"rmdir {folder}")
            self.history.add(f"rmdir {folder}", 'rmdir', {'path': folder})
            self.history.add_undo('rmdir', {'original_path': folder, 'trash_path': trash_path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"rmdir {folder}", str(e))

    def cat(self, filepath):
        try:
            full_path = resolve_path(self.current_dir, filepath)
            if os.path.isdir(full_path):
                raise IsADirectoryError("Это директория, используйте ls для просмотра")
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
            log_cmd(f"cat {filepath}")
            self.history.add(f"cat {filepath}", 'cat', {'path': filepath})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"cat {filepath}", str(e))

    def cp(self, source, dest, recursive=False):
        try:
            src = resolve_path(self.current_dir, source)
            dst = resolve_path(self.current_dir, dest)
            
            if not os.path.exists(src):
                raise FileNotFoundError("Источник не существует")
            
            if os.path.isdir(src) and not recursive:
                raise IsADirectoryError("Используйте -r для копирования каталогов")
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            
            print(f"Скопировано: {source} → {dest}")
            log_cmd(f"cp {'-r' if recursive else ''} {source} {dest}")
            self.history.add(f"cp {'-r' if recursive else ''} {source} {dest}", 'cp', 
                           {'source': source, 'dest': dest, 'recursive': recursive})
            self.history.add_undo('cp', {'dest': dst})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"cp {'-r' if recursive else ''} {source} {dest}", str(e))

    def mv(self, source, dest):
        try:
            src = resolve_path(self.current_dir, source)
            dst = resolve_path(self.current_dir, dest)
            
            if not os.path.exists(src):
                raise FileNotFoundError("Источник не существует")
            
            original_path = src
            shutil.move(src, dst)
            print(f"Перемещено: {source} → {dest}")
            log_cmd(f"mv {source} {dest}")
            self.history.add(f"mv {source} {dest}", 'mv', {'source': source, 'dest': dest})
            self.history.add_undo('mv', {'original_path': original_path, 'new_path': dst})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"mv {source} {dest}", str(e))

    def rm(self, path, recursive=False):
        try:
            full_path = resolve_path(self.current_dir, path)
            
            if not is_safe_path(path):
                raise PermissionError("Невозможно удалить этот каталог")
            
            if not os.path.exists(full_path):
                raise FileNotFoundError("Файл не существует")
            
            if os.path.isdir(full_path):
                if not recursive:
                    confirm = input(f"Удалить директорию {path} со всем содержимым? (y/n): ")
                    if confirm.lower() != 'y':
                        print("Отменено")
                        return
                
                trash_path = os.path.join(self.history.trash_dir, os.path.basename(path))
                shutil.copytree(full_path, trash_path, dirs_exist_ok=True)
                shutil.rmtree(full_path)
            else:
                trash_path = os.path.join(self.history.trash_dir, os.path.basename(path))
                shutil.copy2(full_path, trash_path)
                os.remove(full_path)
            
            print(f"Удалено: {path}")
            log_cmd(f"rm {'-r' if recursive else ''} {path}")
            self.history.add(f"rm {'-r' if recursive else ''} {path}", 'rm', 
                           {'path': path, 'recursive': recursive})
            self.history.add_undo('rm', {'original_path': full_path, 'trash_path': trash_path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"rm {'-r' if recursive else ''} {path}", str(e))

    def zip_archive(self, source, archive_name=None):
        try:
            src = resolve_path(self.current_dir, source)
            if not os.path.exists(src):
                raise FileNotFoundError("Источник не существует")
            
            if archive_name is None:
                archive_name = os.path.basename(src) + '.zip'
            
            archive_path = resolve_path(self.current_dir, archive_name)
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                if os.path.isdir(src):
                    for root, dirs, files in os.walk(src):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(src))
                            zf.write(file_path, arcname)
                else:
                    zf.write(src, os.path.basename(src))
            
            print(f"Архив создан: {archive_name}")
            log_cmd(f"zip {source} {archive_name}")
            self.history.add(f"zip {source} {archive_name}", 'zip', 
                           {'source': source, 'archive': archive_name})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"zip {source} {archive_name}", str(e))

    def unzip_archive(self, archive_name, extract_path=None):
        try:
            archive_path = resolve_path(self.current_dir, archive_name)
            if not os.path.exists(archive_path):
                raise FileNotFoundError("Архив не найден")
            
            if extract_path is None:
                extract_path = self.current_dir
            else:
                extract_path = resolve_path(self.current_dir, extract_path)
            
            os.makedirs(extract_path, exist_ok=True)
            
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(extract_path)
            
            print(f"Архив распакован в: {extract_path}")
            log_cmd(f"unzip {archive_name} {extract_path}")
            self.history.add(f"unzip {archive_name} {extract_path}", 'unzip', 
                           {'archive': archive_name, 'path': extract_path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"unzip {archive_name}", str(e))

    def tar_archive(self, source, archive_name=None):
        try:
            src = resolve_path(self.current_dir, source)
            if not os.path.exists(src):
                raise FileNotFoundError("Источник не существует")
            
            if archive_name is None:
                archive_name = os.path.basename(src) + '.tar.gz'
            
            archive_path = resolve_path(self.current_dir, archive_name)
            
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(src, arcname=os.path.basename(src))
            
            print(f"TAR.GZ архив создан: {archive_name}")
            log_cmd(f"tar {source} {archive_name}")
            self.history.add(f"tar {source} {archive_name}", 'tar', 
                           {'source': source, 'archive': archive_name})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"tar {source} {archive_name}", str(e))

    def untar_archive(self, archive_name, extract_path=None):
        try:
            archive_path = resolve_path(self.current_dir, archive_name)
            if not os.path.exists(archive_path):
                raise FileNotFoundError("Архив не найден")
            
            if extract_path is None:
                extract_path = self.current_dir
            else:
                extract_path = resolve_path(self.current_dir, extract_path)
            
            os.makedirs(extract_path, exist_ok=True)
            
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(extract_path)
            
            print(f"Архив распакован в: {extract_path}")
            log_cmd(f"untar {archive_name} {extract_path}")
            self.history.add(f"untar {archive_name} {extract_path}", 'untar', 
                           {'archive': archive_name, 'path': extract_path})
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"untar {archive_name}", str(e))
    
    def grep(self, pattern, filepath=None, recursive=False, ignore_case=False):
        try:
            if filepath is None:
                filepath = '.'
            
            search_path = resolve_path(self.current_dir, filepath)
            
            flags = re.IGNORECASE if ignore_case else 0
            regex = re.compile(pattern, flags)
            
            matches_found = False
            
            if os.path.isfile(search_path):
                try:
                    with open(search_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                matches_found = True
                                print(f"{os.path.basename(search_path)}:{line_num}: {line.rstrip()}")
                except UnicodeDecodeError:
                    pass
            
            elif os.path.isdir(search_path):
                if recursive:
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    for line_num, line in enumerate(f, 1):
                                        if regex.search(line):
                                            matches_found = True
                                            rel_path = os.path.relpath(file_path, self.current_dir)
                                            print(f"{rel_path}:{line_num}: {line.rstrip()}")
                            except UnicodeDecodeError:
                                continue
                else:
                    for file in os.listdir(search_path):
                        file_path = os.path.join(search_path, file)
                        if os.path.isfile(file_path):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    for line_num, line in enumerate(f, 1):
                                        if regex.search(line):
                                            matches_found = True
                                            print(f"{file}:{line_num}: {line.rstrip()}")
                            except UnicodeDecodeError:
                                continue
            
            if not matches_found:
                print("Совпадений не найдено")
            
            cmd_str = f"grep {'-r' if recursive else ''} {'-i' if ignore_case else ''} '{pattern}' {filepath or '.'}"
            log_cmd(cmd_str)
            self.history.add(cmd_str, 'grep', {
                'pattern': pattern,
                'path': filepath,
                'recursive': recursive,
                'ignore_case': ignore_case
            })
        
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"grep {'-r' if recursive else ''} '{pattern}'", str(e))
    
    def history_cmd(self, count=10):
        try:
            hist = self.history.get_history(count)
            if not hist:
                print("История пуста")
                return
            
            for i, entry in enumerate(hist, 1):
                timestamp = entry.get('timestamp', 'N/A')
                cmd = entry.get('command', 'N/A')
                print(f"{i:3d}  {timestamp}  {cmd}")
            
            log_cmd(f"history {count}")
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd(f"history", str(e))

    def undo_cmd(self):
        try:
            undo_op, error = self.history.undo()
            
            if error:
                print(f"Ошибка: {error}")
                return
            
            op_type = undo_op.get('type')
            info = undo_op.get('info')
            
            if op_type == 'cp':
                if 'dest' in info and os.path.exists(info['dest']):
                    if os.path.isdir(info['dest']):
                        shutil.rmtree(info['dest'])
                    else:
                        os.remove(info['dest'])
                    print(f"Отменено: удален {info['dest']}")
            
            elif op_type == 'mv':
                if os.path.exists(info['new_path']):
                    shutil.move(info['new_path'], info['original_path'])
                    print(f"Отменено: файл возвращен в {info['original_path']}")
            
            elif op_type == 'rm':
                if os.path.exists(info['trash_path']):
                    if os.path.isdir(info['trash_path']):
                        shutil.copytree(info['trash_path'], info['original_path'], dirs_exist_ok=True)
                    else:
                        shutil.copy2(info['trash_path'], info['original_path'])
                    print(f"Отменено: файл восстановлен в {info['original_path']}")
            
            else:
                print(f"Не удается отменить операцию типа '{op_type}'")
            
            log_cmd("undo")
        
        except Exception as e:
            print(f"Ошибка: {e}")
            log_cmd("undo", str(e))

    def run(self):
        print("Мини-оболочка")
        print("Введите 'help' для справки или 'exit' для выхода")
        
        while True:
            try:
                cmd_line = input(f"\n{self.current_dir}> ").strip()
                
                if not cmd_line:
                    continue
                
                parts = cmd_line.split()
                cmd = parts[0]
                args = parts[1:]
                
                if cmd == 'exit':
                    print("До свидания!")
                    break
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd == 'ls':
                    path = None
                    for arg in args:
                        if not arg.startswith('-'):
                            path = arg
                    self.ls(path, '-l' in args)
                
                elif cmd == 'cd':
                    if args:
                        self.cd(args[0])
                
                elif cmd == 'chdir':
                    if args:
                        self.chdir(args[0])
                
                elif cmd == 'mkdir':
                    if args:
                        self.mkdir(args[0])
                
                elif cmd == 'rmdir':
                    if args:
                        self.rmdir(args[0])
                
                elif cmd == 'cat':
                    if args:
                        self.cat(args[0])
                
                elif cmd == 'cp':
                    if len(args) >= 2:
                        self.cp(args[0], args[1], '-r' in args)
                
                elif cmd == 'mv':
                    if len(args) >= 2:
                        self.mv(args[0], args[1])
                
                elif cmd == 'rm':
                    if args:
                        path = args[-1] if not args[-1].startswith('-') else args[0]
                        self.rm(path, '-r' in args)
                
                elif cmd == 'zip':
                    if args:
                        source = args[0]
                        archive_name = args[1] if len(args) > 1 else None
                        self.zip_archive(source, archive_name)
                
                elif cmd == 'unzip':
                    if args:
                        archive_name = args[0]
                        extract_path = args[1] if len(args) > 1 else None
                        self.unzip_archive(archive_name, extract_path)
                
                elif cmd == 'tar':
                    if args:
                        source = args[0]
                        archive_name = args[1] if len(args) > 1 else None
                        self.tar_archive(source, archive_name)
                
                elif cmd == 'untar':
                    if args:
                        archive_name = args[0]
                        extract_path = args[1] if len(args) > 1 else None
                        self.untar_archive(archive_name, extract_path)
                
                elif cmd == 'grep':
                    if args:
                        pattern = args[0]
                        filepath = None
                        recursive = '-r' in args
                        ignore_case = '-i' in args
                        
                        for arg in args[1:]:
                            if not arg.startswith('-'):
                                filepath = arg
                                break
                        
                        self.grep(pattern, filepath, recursive, ignore_case)
                
                elif cmd == 'history':
                    count = int(args[0]) if args else 10
                    self.history_cmd(count)
                
                elif cmd == 'undo':
                    self.undo_cmd()
                
                else:
                    print("Неизвестная команда. Введите 'help' для справки.")
            
            except KeyboardInterrupt:
                print("Программа прервана (Ctrl+C)")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

    def show_help(self):
        help_text = """

  ls [path] [-l]       - Список файлов (-l для подробного просмотра)
  cd [path]            - Смена каталога (виртуально)
  mkdir [folder]       - Создать папку
  rmdir [folder]       - Удалить папку
  cat [file]           - Показать содержимое файла
  cp [-r] src dst      - Копировать файл/папку (-r для рекурсии)
  mv src dst           - Переместить/переименовать
  rm [-r] path         - Удалить файл/папку (-r для рекурсии)
  zip source [name]    - Создать ZIP архив
  unzip archive [path] - Распаковать ZIP
  tar source [name]    - Создать TAR.GZ архив
  untar archive [path] - Распаковать TAR.GZ
  grep [-r] [-i] pattern [path]
    -r  рекурсивный поиск в подкаталогах
    -i  игнорировать регистр
  history [count]      - Показать последние N команд (по умолчанию 10)
  undo                 - Отменить последнюю операцию (cp/mv/rm)
  help                 - Эта справка
  exit                 - Выход из программы
"""
        print(help_text)