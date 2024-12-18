import sys

def main():
    if len(sys.argv) < 2:
        print("Error: No message provided.")
        return

    message = sys.argv[1]
    # Simulate printing the message
    print(f"Printing CPDLC message: {message}")

if __name__ == "__main__":
    main()
