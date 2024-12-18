import sys

if len(sys.argv) < 2:
    print("No content provided!")
    sys.exit(1)

content = sys.argv[1]
print(f"Printing CPDLC Message: {content}")
