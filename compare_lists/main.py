import re


input_text = """
  Composer.app/Folder1/Resources/Base.lproj/HeadMenu.nib  
  Composer.app/Folder1/Resources/DescriptionInfo.nib  
  Composer.app/Folder1/Resources/FullTrashIcon@2x.icns  
  Composer.app/Folder1/Resources/composerWatermark.png  
"""

compare_list = [
    "Composer.app/Folder1/Resources/permissionsGradient.png",
    "Composer.app/Folder1/Resources/DownloadCheck.SHELL",
    "Composer.app/Folder1/Resources/DescriptionPlistInfo.nib",
    "Composer.app/Folder1/Resources/HeadComposerWindow.nib/keyedobjects-110000.nib",
]

def extract_file_paths(input_text):
    lines = input_text.split('\n')
    file_paths = []

    for line in lines:
        match = re.search(r'(.*C.+)$', line)
        if match:
            file_paths.append(match.group(1).strip())

    return file_paths

input_list = extract_file_paths(input_text)

def find_differences(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    unique_to_list1 = set1 - set2
    unique_to_list2 = set2 - set1

    return list(unique_to_list1), list(unique_to_list2)

differencesB, differencesA = find_differences(compare_list, input_list)

print(f"unique to the compared list: {len(differencesB)}")
print(differencesB)

print(f"\nunique to the input_text: {len(differencesA)}")
print(differencesA)