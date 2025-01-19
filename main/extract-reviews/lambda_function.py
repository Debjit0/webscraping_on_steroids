import json
import boto3
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    review_title_class = event.get('reviewTitle')
    review_body_class = event.get('reviewBody')
    review_author_class = event.get('reviewAuthor')
    rating_class = event.get('rating')
    uuid = event.get('uuid')
    
    bucket_name = 'extracted-source-list'

    file_name = f'{uuid}.json'
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        json_content = response['Body'].read().decode('utf-8')
        existing_reviews = json.loads(json_content)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            existing_reviews = []
        else:
            raise
        
    # response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    # json_content = response['Body'].read().decode('utf-8')
    # existing_reviews = json.loads(json_content)
    
    # with open('178e4aa5-c263-46ac-877f-2d060b147701.json', 'r') as file:
    #     existing_reviews = json.load(file)
    
        
    # print(len(existing_reviews))
    reviews = []
    
    for _,review in existing_reviews.items(): 
        soup = BeautifulSoup(review, 'html.parser')

        titles = soup.find_all(class_=review_title_class)
        bodies = soup.find_all(class_=review_body_class)
        authors = soup.find_all(class_=review_author_class)
        ratings = soup.find_all(class_=rating_class)
        
        # print(titles)

        for i in range(min(len(titles), len(bodies), len(authors), len(ratings))):
            review = {
                "title": titles[i].get_text(strip=True),
                "body": bodies[i].get_text(strip=True),
                "author": authors[i].get_text(strip=True),
                "rating": ratings[i].get_text(strip=True)
            }
            reviews.append(review)

    # print(len(reviews))

    return {
        'statusCode': 200,
        'reviews_count': len(reviews),
        'reviews': json.dumps(reviews)
    }