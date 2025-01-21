## Overview

The Review Extraction API is designed to extract product reviews dynamically from any given product page. The API features

- Browser automation frameworks **(Playwright)**
- Large Language Models (LLMs) for dynamic CSS selector identification **(Gemini 1.5 Flash)**
- Pagination handling to retrieve all reviews

---

## System Architecture

### Basic Workflow Diagram
![diagram-export-19-01-2025-20_09_35](https://github.com/user-attachments/assets/bd571997-fe75-461b-82c9-f827452a6563)

### Flow:

- The page URL is taken as input through the API, and the HTML content is filtered to remove unwanted tags and unnecessary elements. **AWS Lambda** is used to handle this processing step.
- An **LLM (Gemini 1.5 Flash)** is utilized to dynamically identify the class name of the reviews section in the filtered HTML.
- An **AWS EC2 instance** is deployed to create a virtual machine environment for running **Playwright**. EC2 is used because **AWS Lambda** does not support Chromium, which is required to execute Playwright.
- A UUID is generated on the EC2 instance, and parallel tasks are executed using the “execute reviews” function defined in `uuid.json`.
- The extracted reviews are written to an **AWS S3 bucket** for secure and scalable storage.
- The stored reviews can be retrieved from the **S3 bucket** upon request.

### Components:

- **Filter Source Code:** The pipeline starts by taking a URL as input. It then uses a library like Beautiful Soup to filter the HTML source code of the webpage, likely extracting relevant information.
- **Trigger EC2 Instance:** The filtered data is then used to trigger an EC2 instance. This instance appears to run a Playwright script, which is a browser automation library. The EC2 instance is responsible for navigating through the website, clicking pagination buttons, and extracting source code from multiple pages.
- **Generate JSON:** The extracted source code from each page is processed and saved as JSON files on an S3 storage bucket.
- **Extract Reviews:** The pipeline then takes the UUIDs of the generated JSON files and executes a Lambda function in parallel for each UUID. This Lambda function extracts the reviews from the source code and saves them to another S3 bucket.

---
## API Specification
- The first api is used to trigger the STEP FUNCTION and the api will return an unique ARN or ProcessID. 
- The second api is used to fetch the OUTPUT from the JSON File Stored in S3.
- (Since we are on the free-tier of AWS, the timeout for each api is 29 seconds,therefore we had to use two different endpoints)

---
## API1 Specification
- https://ecgzhmjm9e.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?page=LINKTOTHEURL   -> returns the ARN
- https://o2crc9xy03.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?executionArn=ARN    -> returns the JSON Output

### Response Format
```
{
  "exexutionARN: xxx
  "status": pipeline is executing
  "url" : xxx
}
```

---

## API2 Specification
- https://o2crc9xy03.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?executionArn=ARN    -> returns the JSON Output
### Response Format
```
{
  "reviews_count": 100,
  "reviews": [
    {
      "title": "Review Title",
      "body": "Review body text",
      "rating": 5,
      "reviewer": "Reviewer Name"
    }
  ]
}
```

---
### Technologies Used
- Python
- Google Gemini Flash 1.5
- Aws Lambda
- Aws EC2
- Aws S3
- Aws Step Function
- Aws Api Gateway

---
## Websites Tested
- https://2717recovery.com/products/recovery-cream
- https://www.trustpilot.com/

- https://www.shopclues.com/combo-of-2-my-chetan-9-w-round-2-pin-led-bulb-white-153526540.html
- https://www.shopclues.com/chamria-hing-wati-digestive-mouth-freshner-200-gm-can-pack-of-2-153514795.html
---
## Demo Output
<img width="1792" alt="Screenshot 2025-01-20 at 2 08 49 PM" src="https://github.com/user-attachments/assets/428a16a7-c5ce-4371-88b5-b2e0347b3211" />

## Deployed Website
- https://unique-sunflower-b40dd4.netlify.app/
