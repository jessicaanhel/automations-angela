import re
from typing import List, Tuple


def parse_string_to_list(long_string: str, pattern: str = r'(.*C.+)$') -> List[str]:
    """
    Parse a multi-line string into a list, optionally filtering lines via regex.
    Default regex extracts lines containing 'C' and anything after.
    """
    lines = long_string.strip().split('\n')
    parsed_lines = []

    for line in lines:
        match = re.search(pattern, line.strip())
        if match:
            parsed_lines.append(match.group(1).strip())

    return parsed_lines


def find_differences(list1: List[str], list2: List[str]) -> Tuple[List[str], List[str]]:
    """
    Find items unique to each list.
    Returns two lists:
    - items in list1 but not in list2
    - items in list2 but not in list1
    """
    set1 = set(list1)
    set2 = set(list2)

    unique_to_list1 = sorted(set1 - set2)
    unique_to_list2 = sorted(set2 - set1)

    return unique_to_list1, unique_to_list2


def print_differences(list_name: str, differences: List[str]) -> None:
    """
    Print the differences in a readable format.
    """
    if differences:
        print(f"\n🟠 Unique to {list_name} ({len(differences)}):")
        for item in differences:
            print(f"  - {item}")
    else:
        print(f"\n✅ No unique items in {list_name}.")


def main():
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

    # Parse and compare
    parsed_list = parse_string_to_list(list_as_string)
    only_in_compare_list, only_in_parsed_list = find_differences(compare_list, parsed_list)

    # Display results
    print_differences("compare_list", only_in_compare_list)
    print_differences("list_as_string", only_in_parsed_list)


if __name__ == "__main__":
    main()