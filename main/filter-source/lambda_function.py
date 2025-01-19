from bs4 import BeautifulSoup, Comment
import requests

def lambda_handler(event, context):
    # Get the URL from the event input
    url = event.get('page')

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()

            # Remove all comments
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()

            cleaned_html = str(soup)
            return {
                'statusCode': 200,
                'body': cleaned_html,
                'url': url
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': f"Failed to retrieve the webpage. Status code: {response.status_code}",
                'url': url
            }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': f"An error occurred: {e}"
        }
