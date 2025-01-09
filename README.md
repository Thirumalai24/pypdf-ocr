# Superbill Processor

## Run on local machine
uvicorn main --reload 
http://127.0.0.1:8000/extract-pdf


## Run Docker Container

To run the Docker container, use the following command:

step 1: Build the Docker image.

```sh
docker build -t superbill-ocr .
```
Step 2: Run the Docker Container.

```sh
docker run -d -p 8000:8000 superbill-ocr
```

## API Details

### Description
  This endpoint extracts structured data from a PDF file uploaded via a multipart/form-data request. It validates the API key provided in the x-api-key header and checks if the uploaded file is a PDF. Upon successful extraction, it returns the extracted data in JSON format.

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/extract-pdf' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_SECRET_KEY' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.pdf'

```

## Endpoints

### Ping Api Request
```sh
GET http://0.0.0.0:8000/ping
```
### Response 
```sh
{
    "ping": "pong"
}
```
### Extract-pdf Api Request
```sh 
POST http://0.0.0.0:8000/extract-pdf
```

### Headers
  x-api-key: Your API key for authorization.

### Request Body
  file: The PDF file to be processed.

### Responses
  200 OK: Successful extraction. Returns JSON data.
  400 Bad Request: Invalid file type or missing file.
  401 Unauthorized: Invalid API key.
  500 Internal Server Error: Server error occurred during processing.

## EXAMPLE

### Request
```sh
POST /extract-pdf
Host: 0.0.0.0:8000
Content-Type: multipart/form-data
x-api-key: YOUR_SECRET_KEY

[@/path/to/your/file.pdf]
```
##Sample pdf
[receipt (1).pdf](https://github.com/user-attachments/files/18357744/receipt.1.pdf)

### Response 
```sh
{
  "client": {
      "rawData": "Emily Cavanaugh, DOB: 09/01/1984, (847) 521-0057, emily.n.cavanaugh@gmail.com",
      "name": "Emily Cavanaugh",
      "dob": "09/01/1984",
      "mob": "(847) 521-0057",
      "email": "emily.n.cavanaugh@gmail.com"
  },
  "insured": null,
  "responsibleparty": null,
  "provider": {
      "rawData": "Catherine Boyce,NPI: #1437216272,(773) 983-8444,Info@evanstoncounseling.com,License: LCSW #149-007739",
      "name": "Catherine Boyce",
      "npi": "#1437216272",
      "mob": "(773) 983-8444",
      "email": "Info@evanstoncounseling.com"
  },
  "practice": {
      "rawData": "Tax ID: 87-4255693,NPI: 1679234165",
      "taxId": "87-4255693",
      "npi": "1679234165"
  },
  "diagnosisCodes": [
      {
          "rawData": "1 F43.20 - Adjustment disorder, unspecified",
          "dx": "1",
          "diagnosisCode": "F43.20",
          "description": "Adjustment disorder, unspecified"
      }
  ],
  "services": [
      {
          "rawData": "05/01/2024 02 90791-95 1 Psychiatric Diagnostic Evaluation 1 $300 $300",
          "date": "05/01/2024",
          "pos": "02",
          "serviceCode": "90791",
          "modifiers": "95",
          "dx": "1",
          "units": "1",
          "fee": "300",
          "paid": "300"
      },
      {
          "rawData": "05/06/2024 02 90837-95 1 Psychotherapy, 60 min 1 $300 $300",
          "date": "05/06/2024",
          "pos": "02",
          "serviceCode": "90837",
          "modifiers": "95",
          "dx": "1",
          "units": "1",
          "fee": "300",
          "paid": "300"
      },
      {
          "rawData": "05/13/2024 02 90837-95 1 Psychotherapy, 60 min 1 $300 $300",
          "date": "05/13/2024",
          "pos": "02",
          "serviceCode": "90837",
          "modifiers": "95",
          "dx": "1",
          "units": "1",
          "fee": "300",
          "paid": "300"
      },
      {
          "rawData": "05/21/2024 02 90837-95 1 Psychotherapy, 60 min 1 $300 $300",
          "date": "05/21/2024",
          "pos": "02",
          "serviceCode": "90837",
          "modifiers": "95",
          "dx": "1",
          "units": "1",
          "fee": "300",
          "paid": "300"
      },
      {
          "rawData": "06/03/2024 02 90837-95 1 Psychotherapy, 60 min 1 $300 $300",
          "date": "06/03/2024",
          "pos": "02",
          "serviceCode": "90837",
          "modifiers": "95",
          "dx": "1",
          "units": "1",
          "fee": "300",
          "paid": "300"
      }
  ],
  "totalFees": "$1,500.00",
  "totalPaid": "$1,500.00"
}
```



