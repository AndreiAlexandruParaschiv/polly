import sys

from polly import PollyPage

initial_url = sys.argv[1]

try:
    test_page = PollyPage(initial_url, allow_underscore=True)
    test_page.detect_errors()
except ValueError as e:
    print(f"Error: Could not fetch the initial URL: {initial_url}")
    print(f"Details: {e}")
    sys.exit(1)

print()
print(" ** Checking hreflang for: " + initial_url + " **")
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
    print("\tNo issues detected")
else:
    for url in test_page.alternate_urls():
        print("\t" + url + " = " + str(test_page.issues_for_url.get(url, "No issues detected")))
print()
