from api.cricket_api import get_live_matches

def test():
    matches = get_live_matches()

    if not matches:
        print("API Failed")
        return

    print(f"Total Matches: {len(matches)}\n")

    for m in matches[:5]:
        print(m)


if __name__ == "__main__":
    test()