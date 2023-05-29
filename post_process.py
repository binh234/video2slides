import imagehash
import os
from collections import deque
from PIL import Image


def find_similar_images(
    base_dir, hash_size=8, hashfunc=imagehash.dhash, queue_len=5, threshold=4
):
    snapshots_files = sorted(os.listdir(base_dir))

    hash_dict = {}
    hash_queue = deque([], maxlen=queue_len)
    duplicates = []
    num_duplicates = 0

    print("---" * 5, "Finding similar files", "---" * 5)

    for file in snapshots_files:
        read_file = Image.open(os.path.join(base_dir, file))
        comp_hash = hashfunc(read_file, hash_size=hash_size)
        duplicate = False

        if comp_hash not in hash_dict:
            hash_dict[comp_hash] = file
            # Compare with hash queue to find out potential duplicates
            for img_hash in hash_queue:
                if img_hash - comp_hash <= threshold:
                    duplicate = True
                    break

            if not duplicate:
                hash_queue.append(comp_hash)
        else:
            duplicate = True

        if duplicate:
            print("Duplicate file: ", file)
            duplicates.append(file)
            num_duplicates += 1

    print("\nTotal duplicate files:", num_duplicates)
    print("-----" * 10)
    return hash_dict, duplicates


def remove_duplicates(
    base_dir, hash_size=8, hashfunc=imagehash.dhash, queue_len=5, threshold=4
):
    _, duplicates = find_similar_images(
        base_dir,
        hash_size=hash_size,
        hashfunc=hashfunc,
        queue_len=queue_len,
        threshold=threshold,
    )

    if not len(duplicates):
        print("No duplicates found!")
    else:
        print("Removing duplicates...")

        for dup_file in duplicates:
            file_path = os.path.join(base_dir, dup_file)

            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("Filepath: ", file_path, "does not exists.")

        print("All duplicates removed!")

    print("***" * 10, "\n")


if __name__ == "__main__":
    remove_duplicates("sample_1")
