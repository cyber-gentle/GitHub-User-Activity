from urllib.request import urlopen
import sys
import json



def fetch_activity(username: str) -> list[dict] | str:
    if not username:
        return "User name cannot be empty"

    users_api_url = f"https://api.github.com/users/{username}/events"

    with urlopen(users_api_url, timeout=10) as response:
        return json.load(response)




def format_event(events: list[dict]) -> str:
    messages = []

    for event in events:
        event_type = event["type"]
        repository = event["repo"]["name"]
        payload = event["payload"]
        action = payload.get("action")

        match event_type:
            case "IssuesEvent":
                issue_number = payload["issue"]["number"]
                messages.append(
                    f"{action.capitalize()} issue #{issue_number} in {repository}"
                )

            case "PushEvent":
                commits = payload.get("size")
                if commits is not None:
                    messages.append(
                        f"Pushed {commits} commits to {repository}"
                    )
                else:
                    messages.append(
                        f"Pushed commits to {repository}"
                    )

            case "WatchEvent":
                if action == "started":
                    messages.append(f"Starred {repository}")

            case "CreateEvent":
                ref_type = payload.get("ref_type")
                ref = payload.get("ref")

                if ref:
                    messages.append(
                        f"Created {ref_type} '{ref}' in {repository}"
                    )
                else:
                    messages.append(
                        f"Created {ref_type} in {repository}"
                    )

            case "PullRequestEvent":
                pr = payload.get("pull_request", {})
                pr_number = payload.get("number")

                if action == "closed" and pr.get("merged"):
                    action = "merged"

                if action:
                    messages.append(
                        f"{action.capitalize()} pull request #{pr_number} in {repository}"
                    )

            case "ForkEvent":
                messages.append(f"Forked {repository}")

            case "IssueCommentEvent":
                messages.append(
                    f"Commented on an issue in {repository}"
                )

            case "ReleaseEvent":
                messages.append(
                    f"{action.capitalize()} a release in {repository}"
                    if action else f"Release activity in {repository}"
                )

            case _:
                messages.append(
                    f"{event_type} in {repository}"
                )

    return "\n".join(messages) if messages else "No recent activity found."



def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <github_username>")
        return

    user_name = sys.argv[1].lower()
    events = fetch_activity(user_name)

    activity = format_event(events)
    print(activity)

   
    

if __name__ == "__main__":
    main()



        
