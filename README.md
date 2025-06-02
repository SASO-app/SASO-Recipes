
# Receipt OCR API (FastAPI)

This app lets you upload a receipt image and returns the store name, date, and total amount using OCR.

### Endpoint:
POST `/parse`

Form-data:
- file: (upload receipt image)

### Response:
```json
{
  "store": "Biltema",
  "date": "2025-05-02",
  "total": "478.90"
}
```
