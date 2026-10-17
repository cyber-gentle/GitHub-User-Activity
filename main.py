from urllib.request import urlopen
import sys
import json



def fetch_activity(username: str) -> list[dict] | str:
    if not username:
        return "User name cannot be empty"

    users_api_url = f"https://api.github.com/users/{username}/events"

    with urlopen(users_api_url, timeout=10) as response:
        return json.load(response)




def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <github_username>")
        return

    user_name = sys.argv[1].lower()
    events = fetch_activity(user_name)

    # activity = format_event(events)
    # print(activity)

   
    

if __name__ == "__main__":
    main()



        
