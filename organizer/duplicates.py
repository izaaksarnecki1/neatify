from collections import defaultdict
from send2trash import send2trash

def find_duplicates(files):
    size_map = defaultdict(list)
    for file in files:
        size_map[file.size].append(file)

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
    
    return duplicates

def delete_duplicates(duplicates, dry_run: bool, delete_mode: str):
    for group in duplicates:
        if delete_mode == "clean" or delete_mode == "c":
            group.sort(key=lambda f: (len(str(f.path.name)), f.path.name))  # sort by last modified
            keep = group[0]
            to_delete = group[1:]
            print(f"\nKeeping (clean): {keep.path}")
        elif delete_mode == "manual" or delete_mode == "m":
            print("Duplicate group:\n")
            for idx, fr in enumerate(group):
                print(f"{idx}: {fr.path}")
            choice = input("Enter the number of the file to keep (ENTER to skip): ")
            if choice == "":
                print("\nSkipped group.\n")
                continue
            try:
                keep = group[int(choice)]
                to_delete = [f for f in group if f != keep]
            except (IndexError, ValueError):
                print("Invalid choice. Skipping group.\n")
                continue
        else:
            continue  # skip deletion in "none" mode

        for file in to_delete:
            if dry_run:
                print(f"[DRY RUN] Would send to trash: {file.path}\n")
            else:
                try:
                    send2trash(str(file.path))
                    print(f"Sent to trash: {file.path}")
                except Exception as e:
                    print(f"Failed to delete {file.path}: {e}\n")
                    

def process_duplicates(files, dry_run: bool, delete_mode: str):   
    duplicates = find_duplicates(files)

    if duplicates:
        for group in duplicates:
            print("\n - Duplicate set:")
            for file in group:
                print(f"{file.path}")
        if delete_mode is None:
            delete_mode = input("\nEnter delete mode (clean | manual): \n").strip().lower()

        if delete_mode in ["clean", "c", "manual", "m"]:
            delete_duplicates(duplicates, dry_run, delete_mode)
    else:
        print("No duplicates found.\n")
