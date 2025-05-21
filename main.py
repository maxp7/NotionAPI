import notionAPI
import time
def main():
    while True:
        print("...")
        if(notionAPI.checkNewEntries()):
            print(notionAPI.fetchedResults)
        time.sleep(1)

if __name__ == "__main__":
    main()