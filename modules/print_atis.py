import sys

if len(sys.argv) < 2:
    print("No ATIS content provided!")
    sys.exit(1)

content = sys.argv[1]
print(f"Printing ATIS Data: {content}")
