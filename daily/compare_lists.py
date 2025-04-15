import re

def extract_file_paths(input_text):
    lines = input_text.split('\n')
    file_paths = []

    for line in lines:
        match = re.search(r'(.*C.+)$', line)
        if match:
            file_paths.append(match.group(1).strip())

    return file_paths



def find_differences(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    unique_to_list1 = set1 - set2
    unique_to_list2 = set2 - set1

    return list(unique_to_list1), list(unique_to_list2)

#Define the lists to compare
list_as_string = """
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

#Call to action
string_list = extract_file_paths(list_as_string)
differencesB, differencesA = find_differences(compare_list, string_list)

print(f"unique to the compared list: {len(differencesB)}")
print(differencesB)

print(f"\nunique to the list_as_string: {len(differencesA)}")
print(differencesA)