from cli.interface import app
from pathlib import Path
from organizer.scanner import Scanner
from config import load_config
from collections import defaultdict



def run(source: Path, dest: Path, dry_run: bool) -> None:
    # function where main logic will be placed. Called from interface.py
    # print(f"Source: {source}")
    # print(f"Destination: {dest}")
    # print(f"Dry run: {dry_run}")

    config = load_config()
    if source:
        config["source"] = source
    if dest:
        config["dest"] = dest

    config["dry_run"] = dry_run

    print(f"Scanning files in: {source}")

    scanner = Scanner(source)
    files = scanner.scan()
    
    # we are grouping files by size
    size_map = defaultdict(list)
    for file in files:
        size_map[file.size].append(file)
    
    # now we grouping based on hashes, aka same content
    duplicates = []
    for size, group in size_map.items():
        if len(group) > 1:
            hash_map = defaultdict(list)
            for file in group:
                file_hash = file.compute_hash()
                hash_map[file_hash].append(file)
                
            for dup_group in hash_map.values():
                if len(dup_group) > 1:
                    duplicates.append(dup_group)
                    
    if duplicates:
        print("Found duplicate files:")
        for group in duplicates:
            print(" - Duplicate set:")
            for file in group:
                print(f"{file.path}")
    else:
        print("No duplicates found.")
        

    # print(f"Found {len(files)} files.")
    # for file in files[:10]:
    #     print(file)


def main():
    app()


if __name__ == "__main__":
    main()
