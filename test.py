import os

def search_in_files(folder_path, target_string):
    """
    Search for a specific string in all .as files in a folder and its subfolders.

    :param folder_path: Path to the folder to search in
    :param target_string: String to search for
    """
    found_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".as"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if target_string in f.read():
                            found_files.append(file_path)
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

    if found_files:
        print("The string was found in the following files:")
        for file in found_files:
            print(file)
    else:
        print("The string was not found in any .as files.")

# Example usage
if __name__ == "__main__":
    folder_to_search = r'C:\Users\marie\Documents\XuanZhi9\scripts'
    string_to_search = '+ 5'

    search_in_files(folder_to_search, string_to_search)
