import requests
import random

def format_quote(data):
    quote = data['q']
    author = data['a']

    return f"""
> "{quote}"\t
>
> — *{author}*
"""

quotes_url = "https://zenquotes.io/api/quotes"
def get_quote():
    response = requests.get(quotes_url)
    data = response.json()

    x = random.randint(0,len(data))
    return format_quote(data[x])

def write_to_readme(latest, quote):

    always_text = ""
    # Get the always text
    try:
        with open("always.md", "r") as a:
            always_text = a.read()
    except FileNotFoundError:
        print("no always text.")

    try:
        with open("README.md", "w", encoding="utf-8") as rm:
            text = f"""
{always_text}

### What I'm working on
{latest}

### Daily Quote
{quote}
"""
            rm.write(text)
    except FileNotFoundError:
        print("ERROR: README.md file not found")

github_username = "jppnhmr"
github_url = f"https://api.github.com/users/{github_username}/events/public"
def get_lastest_repo():

    response = requests.get(github_url)
    events = response.json()

    for event in events:
        if event["type"] == "PushEvent":
            repo = event["repo"]["name"]
            repo = repo.split("/")[-1]

            return f"[{repo}](https://github.com/{github_username}/{repo})"


if __name__ == "__main__":

    quote = get_quote()
    latest = get_lastest_repo()

    write_to_readme(latest, quote)
