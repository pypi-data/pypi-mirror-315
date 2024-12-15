#!/usr/bin/env python3
# Version 0.0.6
import os
import sys

def print_directory_tree(start_path, ignore_dirs=None, prefix="", output_file=None):
    """
    Dizin yapısını ağaç benzeri bir şekilde yazdırır veya dosyaya yazar.
    """
    if ignore_dirs is None:
        ignore_dirs = {".git", "node_modules"}

    # Mevcut dizindeki öğeleri al
    contents = os.listdir(start_path)
    dirs = [d for d in contents if os.path.isdir(os.path.join(start_path, d)) and d not in ignore_dirs]
    files = [f for f in contents if os.path.isfile(os.path.join(start_path, f))]

    # Öğeleri sırala
    all_items = sorted(dirs) + sorted(files)

    # Her öğeyi işle
    for i, item in enumerate(all_items):
        connector = "└── " if i == len(all_items) - 1 else "├── "
        line = prefix + connector + item
        if output_file:
            output_file.write(line + "\n")
        else:
            print(line)

        # Eğer klasörse, içini tarayalım
        if os.path.isdir(os.path.join(start_path, item)):
            new_prefix = prefix + ("    " if i == len(all_items) - 1 else "│   ")
            print_directory_tree(os.path.join(start_path, item), ignore_dirs, new_prefix, output_file)

def main():
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "."

    # Dizin yapısını ağaç şeklinde yazdır
    print_directory_tree(target_dir)

if __name__ == "__main__":
    main()