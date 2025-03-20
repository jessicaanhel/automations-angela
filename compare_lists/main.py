import re


input_text = """
Archive:  Composer.zip
   Composer.app/
  Composer.app/Folder1/
  Composer.app/Folder1/Resources/Composer.icns  
  Composer.app/Folder1/Resources/TableWindow.nib  
  Composer.app/Folder1/Resources/ComposerDocument.icns  
  Composer.app/Folder1/Resources/DMGFormat@2x.icns  
  Composer.app/Folder1/Resources/ExportWindow.nib  
  Composer.app/Folder1/Resources/InfoPlistInfo.nib  
  Composer.app/Folder1/Resources/ProgressInfo.nib  
  Composer.app/Folder1/Resources/postinstall.PERL  
  Composer.app/Folder1/Resources/postupgrade.SHELL  
  Composer.app/Folder1/Resources/NoSelectionInfo.nib  
  Composer.app/Folder1/Resources/preflight.SHELL  
  Composer.app/Folder1/Resources/Base.lproj/HeadMenu.nib  
  Composer.app/Folder1/Resources/DescriptionInfo.nib  
  Composer.app/Folder1/Resources/FullTrashIcon@2x.icns  
  Composer.app/Folder1/Resources/composerWatermark.png  
"""

compare_list = [
    "Composer.app/Folder1/CodeResources",
    "Composer.app/Folder1/_CodeSignature/CodeResources",
    "Composer.app/Folder1/MacOS/Composer",
    "Composer.app/Folder1/Resources/Localizations.xml",
    "Composer.app/Folder1/Resources/DeleteConfirmation.nib",
    "Composer.app/Folder1/Resources/FullTrashIcon.icns",
    "Composer.app/Folder1/Resources/preupgrade.SHELL",
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