import requests
from bs4 import BeautifulSoup


def scrape_youtube_info(video_url):
    try:
        # Send an HTTP request to the YouTube video page
        response = requests.get(video_url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the video title
        title_tag = soup.find("meta", property="og:title")
        video_title = title_tag["content"] if title_tag else "Title not found"

        # Extract the video description
        description_tag = soup.find("meta", property="og:description")
        # print(f"description is {description_tag['content']}")
        video_description = (
            description_tag["content"] if description_tag else "Description not found"
        )

        return {"title": video_title, "description": video_description}

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# Example usage
youtube_url = "https://www.youtube.com/watch?v=ciLGHX_mq48&ab_channel=Badshah"
result = scrape_youtube_info(youtube_url)

if result:
    print(f"Title: {result['title']}")
    print(f"Description: {result['description']}")
