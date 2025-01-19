import json
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    review_title_class = event.get('reviewTitle')
    review_body_class = event.get('reviewBody')
    review_author_class = event.get('reviewAuthor')
    rating_class = event.get('rating')
    uuid = event.get('uuid')
    source_code = event.get('sourceCode')
    # bucket_name = 'extracted-reviews'

    file_name = f'{uuid}.json'
    soup = BeautifulSoup(source_code, 'html.parser')

    reviews = []
    titles = soup.find_all(class_=review_title_class)
    bodies = soup.find_all(class_=review_body_class)
    authors = soup.find_all(class_=review_author_class)
    ratings = soup.find_all(class_=rating_class)

    for i in range(min(len(titles), len(bodies), len(authors), len(ratings))):
        review = {
            "title": titles[i].get_text(strip=True),
            "body": bodies[i].get_text(strip=True),
            "author": authors[i].get_text(strip=True),
            "rating": ratings[i].get_text(strip=True)
        }
        reviews.append(review)
    return {
        'statusCode': 200,
        'body': json.dumps(reviews)
    }