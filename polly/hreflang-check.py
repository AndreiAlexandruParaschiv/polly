import sys
import os
import csv # Added
from datetime import datetime # Added
from polly import PollyPage

# Define CSV headers globally or pass them around
CSV_HEADERS = [
    "URL", "Fetch_Status", "Fetch_Details",
    "No_Return_Tags_Status", "No_Return_Tags_Details",
    "Non_Retrievable_Pages_Status", "Non_Retrievable_Pages_Details",
    "Canonical_Conflicts_Status", "Canonical_Conflicts_Details",
    "Multiple_Entries_For_Codes_Status", "Multiple_Entries_For_Codes_Details",
    "Multiple_X-Default_Tags_Status", "Multiple_X-Default_Tags_Details",
    "Hreflang_Key_Errors_Status", "Hreflang_Key_Errors_Details",
    "URL_Errors_Status", "URL_Errors_Details",
    "Is_X_Default_Page"
]

def check_single_url(url_to_check, csv_writer): # Added csv_writer
    """Fetches and checks hreflang data for a single URL and writes to CSV."""
    row_data = {header: "" for header in CSV_HEADERS}
    row_data["URL"] = url_to_check

    try:
        test_page = PollyPage(url_to_check, allow_underscore=True)
        test_page.detect_errors()
        row_data["Fetch_Status"] = "OK"
    except ValueError as e:
        print(f"Error: Could not fetch URL: {url_to_check}")
        print(f"Details: {e}")
        print("-" * 40)
        row_data["Fetch_Status"] = "FAIL"
        row_data["Fetch_Details"] = str(e)
        if csv_writer: # Ensure csv_writer is not None
             csv_writer.writerow(row_data)
        return

    # ... (console printing remains the same for now) ...
    print()
    print(f" ** Checking hreflang for: {url_to_check} **")
    print()

    print("Alternative URLs:")
    if not test_page.alternate_urls():
        print("\tNone")
    else:
        print("\t" + "\n\t".join(test_page.alternate_urls()))
    print()
    print("No return tag error pages:")
    if not test_page.no_return_tag_pages():
        print("\tNone")
    else:
        print("\t" + "\n\t".join(test_page.no_return_tag_pages()))
    print()
    print("Non-retrievable pages:")
    if not test_page.non_retrievable_pages():
        print("\tNone")
    else:
        print("\t" + "\n\t".join(test_page.non_retrievable_pages()))
    print()
    print("Canonical conflict pages:")
    if not test_page.canonical_conflict_pages():
        print("\tNone")
    else:
        print("\t" + "\n\t".join(test_page.canonical_conflict_pages()))
    print()
    print("Codes with multiple entries:")
    if not test_page.hreflang_keys_with_multiple_entries:
        print("\tNone")
    else:
        print("\t" + "\n\t".join(test_page.hreflang_keys_with_multiple_entries))
    print()
    print("Is this page the default:")
    print("\t" + str(test_page.is_default))
    print()
    print("Are there multiple defaults present:")
    print("\t" + str(test_page.has_multiple_defaults))
    print()
    print("hreflang keys:")
    if not test_page.hreflang_keys:
        print("\tNone")
    else:
        print("\t" + ", ".join(test_page.hreflang_keys))
    print()
    print("Languages:")
    if not test_page.languages:
        print("\tNone")
    else:
        print("\t" + ", ".join(test_page.languages))
    print()
    print("Regions:")
    if not test_page.regions:
        print("\tNone")
    else:
        print("\t" + ", ".join(test_page.regions))
    print()

    print("Errors by hreflang_key:")
    if not test_page.hreflang_keys:
        print("\tNo issues detected")
    else:
        for hreflang_key in test_page.hreflang_keys:
            print("\t" + hreflang_key + " = " + str(test_page.issues_for_key.get(hreflang_key, "No issues detected")))
    print()

    print("Errors by url:")
    if not test_page.alternate_urls():
        # If alternate_urls is empty, but there might be general errors for the initial URL itself,
        # this logic might need refinement based on how PollyPage stores errors for the initial URL
        # if no alternates are found. For now, this matches previous behavior.
        # Consider if issues_for_url can have the initial_url as a key if no alternates.
        all_urls_to_check_for_errors = [url_to_check] + test_page.alternate_urls()
        found_errors_for_initial = False
        for u in all_urls_to_check_for_errors:
            if test_page.issues_for_url.get(u):
                print("\t" + u + " = " + str(test_page.issues_for_url.get(u)))
                found_errors_for_initial = True
        if not found_errors_for_initial:
             print("\tNo issues detected")

    else:
        for url_key in test_page.alternate_urls(): # Iterate through known alternate URLs
             # Also include the initial URL if it has reported errors
            if test_page.issues_for_url.get(url_key):
                 print("\t" + url_key + " = " + str(test_page.issues_for_url.get(url_key, "No issues detected")))
            # To ensure initial URL's own errors are shown if not in alternates
        if test_page.issues_for_url.get(url_to_check) and url_to_check not in test_page.alternate_urls() :
            print("\t" + url_to_check + " = " + str(test_page.issues_for_url.get(url_to_check)))


    # Populate CSV data
    if test_page.no_return_tag_pages():
        row_data["No_Return_Tags_Status"] = "FAIL"
        row_data["No_Return_Tags_Details"] = "; ".join(test_page.no_return_tag_pages())
    else:
        row_data["No_Return_Tags_Status"] = "OK"

    if test_page.non_retrievable_pages():
        row_data["Non_Retrievable_Pages_Status"] = "FAIL"
        row_data["Non_Retrievable_Pages_Details"] = "; ".join(test_page.non_retrievable_pages())
    else:
        row_data["Non_Retrievable_Pages_Status"] = "OK"

    if test_page.canonical_conflict_pages():
        row_data["Canonical_Conflicts_Status"] = "FAIL"
        row_data["Canonical_Conflicts_Details"] = "; ".join(test_page.canonical_conflict_pages())
    else:
        row_data["Canonical_Conflicts_Status"] = "OK"

    if test_page.hreflang_keys_with_multiple_entries:
        row_data["Multiple_Entries_For_Codes_Status"] = "FAIL"
        row_data["Multiple_Entries_For_Codes_Details"] = "; ".join(test_page.hreflang_keys_with_multiple_entries)
    else:
        row_data["Multiple_Entries_For_Codes_Status"] = "OK"

    if test_page.has_multiple_defaults:
        row_data["Multiple_X-Default_Tags_Status"] = "FAIL"
        row_data["Multiple_X-Default_Tags_Details"] = "Multiple x-default tags found"
    else:
        row_data["Multiple_X-Default_Tags_Status"] = "OK"

    # Consolidate issues_for_key
    key_errors = {k: v for k, v in test_page.issues_for_key.items() if v}
    if key_errors:
        row_data["Hreflang_Key_Errors_Status"] = "FAIL"
        row_data["Hreflang_Key_Errors_Details"] = str(key_errors)
    else:
        row_data["Hreflang_Key_Errors_Status"] = "OK"

    # Consolidate issues_for_url
    url_errors = {k: v for k, v in test_page.issues_for_url.items() if v}
    if url_errors: # Check if there are any actual errors
        row_data["URL_Errors_Status"] = "FAIL"
        # Ensure the initial URL's own errors are captured if not in alternates explicitly
        initial_url_error = test_page.issues_for_url.get(url_to_check)
        all_url_errors_details = {}
        if initial_url_error:
             all_url_errors_details[url_to_check] = initial_url_error
        for alt_url in test_page.alternate_urls():
            error = test_page.issues_for_url.get(alt_url)
            if error:
                all_url_errors_details[alt_url] = error
        row_data["URL_Errors_Details"] = str(all_url_errors_details) if all_url_errors_details else ""
        if not all_url_errors_details: # If after filtering, no errors, then OK
            row_data["URL_Errors_Status"] = "OK"

    else: # No keys in issues_for_url initially
        row_data["URL_Errors_Status"] = "OK"


    row_data["Is_X_Default_Page"] = str(test_page.is_default)

    # Console printing (can be kept or removed/made optional later)
    # ... (existing print statements for details) ...
    print("No return tag error pages:")
    if not test_page.no_return_tag_pages(): print("\tNone")
    else: print("\t" + "\n\t".join(test_page.no_return_tag_pages()))
    print()
    print("Non-retrievable pages:")
    if not test_page.non_retrievable_pages(): print("\tNone")
    else: print("\t" + "\n\t".join(test_page.non_retrievable_pages()))
    print()
    print("Canonical conflict pages:")
    if not test_page.canonical_conflict_pages(): print("\tNone")
    else: print("\t" + "\n\t".join(test_page.canonical_conflict_pages()))
    print()
    print("Codes with multiple entries:")
    if not test_page.hreflang_keys_with_multiple_entries: print("\tNone")
    else: print("\t" + "\n\t".join(test_page.hreflang_keys_with_multiple_entries))
    print()
    print("Is this page the default:")
    print("\t" + str(test_page.is_default))
    print()
    print("Are there multiple defaults present:")
    print("\t" + str(test_page.has_multiple_defaults))
    print()
    print("hreflang keys:")
    if not test_page.hreflang_keys: print("\tNone")
    else: print("\t" + ", ".join(test_page.hreflang_keys))
    print()
    print("Languages:")
    if not test_page.languages: print("\tNone")
    else: print("\t" + ", ".join(test_page.languages))
    print()
    print("Regions:")
    if not test_page.regions: print("\tNone")
    else: print("\t" + ", ".join(test_page.regions))
    print()
    print("Errors by hreflang_key:")
    if not test_page.hreflang_keys and not key_errors : print("\tNo issues detected") # check key_errors as well
    else:
        for hreflang_key in test_page.hreflang_keys: # Iterate all keys
            print("\t" + hreflang_key + " = " + str(test_page.issues_for_key.get(hreflang_key, "No issues detected")))
        # Print errors for keys not in hreflang_keys but in issues_for_key (if any, though unlikely with current polly.py)
        for hreflang_key in key_errors:
            if hreflang_key not in test_page.hreflang_keys:
                 print("\t" + hreflang_key + " (error only) = " + str(key_errors[hreflang_key]))
    print()
    print("Errors by url:")
    # Logic for printing URL errors to console
    urls_with_printed_errors = set()
    initial_url_console_error = test_page.issues_for_url.get(url_to_check)
    if initial_url_console_error:
        print(f"\t{url_to_check} = {initial_url_console_error}")
        urls_with_printed_errors.add(url_to_check)

    has_alternate_url_errors = False
    for alt_url in test_page.alternate_urls():
        error = test_page.issues_for_url.get(alt_url)
        if error:
            print(f"\t{alt_url} = {error}")
            urls_with_printed_errors.add(alt_url)
            has_alternate_url_errors = True

    if not initial_url_console_error and not has_alternate_url_errors and not test_page.alternate_urls():
         # This case means no alternates and no error for initial URL was found by .get()
         # but issues_for_url might still be non-empty if polly.py populates it weirdly.
         # However, standard case is no errors printed if nothing found.
         is_empty_issues_for_url = True
         for url_key_check in test_page.issues_for_url: # Check if issues_for_url has any content at all
             if test_page.issues_for_url[url_key_check]:
                 is_empty_issues_for_url = False
                 break
         if is_empty_issues_for_url:
            print("\tNo issues detected")


    print("\n" + "-" * 40 + "\n")

    if csv_writer: # Ensure csv_writer is not None
        csv_writer.writerow(row_data)


def main():
    urls_to_process = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    default_config_file = os.path.join(project_root, "urls_to_check.txt")

    if len(sys.argv) > 1:
        argument = sys.argv[1]
        if argument.lower().endswith(".txt") and os.path.isfile(argument):
            print(f"Reading URLs from specified file: {argument}")
            try:
                with open(argument, 'r') as f:
                    urls_to_process = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"Error: Specified file not found: {argument}")
                sys.exit(1)
            except Exception as e:
                print(f"Error reading file {argument}: {e}")
                sys.exit(1)
        elif "://" in argument: # Basic check for a URL
            urls_to_process.append(argument)
        else:
            print(f"Argument '{argument}' is not a valid URL or a .txt file. Trying default config.")
            if os.path.isfile(default_config_file):
                print(f"Reading URLs from default config file: {default_config_file}")
                try:
                    with open(default_config_file, 'r') as f:
                        urls_to_process = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    print(f"Error reading default config file {default_config_file}: {e}")
                    sys.exit(1)
            else:
                print(f"Default config file not found at {default_config_file}.")
                print("Usage: python3 hreflang-check.py [url | path/to/urls.txt]")
                sys.exit(1)

    else: # No arguments provided, use default config file
        if os.path.isfile(default_config_file):
            print(f"No arguments provided. Reading URLs from default config file: {default_config_file}")
            try:
                with open(default_config_file, 'r') as f:
                    urls_to_process = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"Error reading default config file {default_config_file}: {e}")
                sys.exit(1)
        else:
            print(f"Default config file not found at {default_config_file}.")
            print("Usage: python3 hreflang-check.py [url | path/to/urls.txt]")
            print("Alternatively, create a 'urls_to_check.txt' file in the project root directory.")
            sys.exit(1)


    if not urls_to_process:
        print("No URLs to process.")
        sys.exit(0)

    # Create results directory
    results_dir = os.path.join(project_root, "results")
    os.makedirs(results_dir, exist_ok=True)

    # CSV file setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"hreflang_results_{timestamp}.csv"
    csv_filepath = os.path.join(results_dir, csv_filename)

    print(f"Results will be saved to: {csv_filepath}")

    csv_file = None
    csv_writer_obj = None
    try:
        csv_file = open(csv_filepath, 'w', newline='', encoding='utf-8')
        csv_writer_obj = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        csv_writer_obj.writeheader()

        for url in urls_to_process:
            check_single_url(url, csv_writer_obj) # Pass writer

    except IOError as e:
        print(f"Error writing to CSV file {csv_filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV operations: {e}")
    finally:
        if csv_file:
            csv_file.close()
            print(f"Finished processing. Results saved to: {csv_filepath}")


if __name__ == "__main__":
    main()
