import os


def collect_legal_files(search_directory):
    # Names of the output files
    output_license = "all_licenses.txt"
    output_notice = "all_notices.txt"

    # Statistics
    count_license = 0
    count_notice = 0

    # Lists to hold the text content
    license_data = []
    notice_data = []

    print(f"--- Starting scan in: {os.path.abspath(search_directory)} ---")

    # Walking through all directories and subdirectories
    for root, dirs, files in os.walk(search_directory):
        # Prevent the script from looking inside the .git metadata folder
        if '.git' in dirs:
            dirs.remove('.git')

        for filename in files:
            # Convert to lowercase to catch LICENSE, License, license.txt, etc.
            name_lower = filename.lower()
            full_path = os.path.join(root, filename)

            # Define search logic
            is_license = "license" in name_lower
            is_notice = "notice" in name_lower

            if is_license or is_notice:
                try:
                    # 'errors=ignore' handles any weird characters in the text files
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Create a header to separate files in the final document
                    separator = "\n" + "=" * 80 + "\n"
                    header = f"SOURCE FILE: {full_path}\n"
                    footer = "\n" + "=" * 80 + "\n"
                    entry = separator + header + separator + content + footer

                    if is_license:
                        license_data.append(entry)
                        count_license += 1
                    else:
                        notice_data.append(entry)
                        count_notice += 1

                except Exception as e:
                    print(f"Could not read {full_path}: {e}")

    # Save the combined License files
    with open(output_license, 'w', encoding='utf-8') as out_l:
        out_l.write(f"TOTAL LICENSE FILES FOUND: {count_license}\n")
        out_l.writelines(license_data)

    # Save the combined Notice files
    with open(output_notice, 'w', encoding='utf-8') as out_n:
        out_n.write(f"TOTAL NOTICE FILES FOUND: {count_notice}\n")
        out_n.writelines(notice_data)

    # Final summary to console
    print("\n" + "Check complete!")
    print(f"Found {count_license} license-related files.")
    print(f"Found {count_notice} notice-related files.")
    print(f"Results saved to: {output_license} and {output_notice}")


if __name__ == "__main__":
    # In PyCharm, '.' refers to the project root where you place this script
    target_folder = "."
    collect_legal_files(target_folder)