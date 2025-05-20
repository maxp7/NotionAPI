import notionAPI

def main():
    while True:
        if(notionAPI.checkNewEntries()):
            print("Found")


if __name__ == "__main__":
    main()