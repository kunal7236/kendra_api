# 🏥 Jan Aushadhi Kendra API

A FastAPI-based service to store and query **Jan Aushadhi Kendra** information extracted from official PDFs.  
The API supports uploading new datasets (via PDF), searching Kendras by code, pincode, or location, and checking service status.

---

## 🚀 Features

- Upload latest **Jan Aushadhi Kendra PDF** (parses with `pdfplumber` and saves to MongoDB Atlas).
- Query Kendras by:
  - ✅ **Kendra Code**
  - ✅ **Pin Code**
  - ✅ **State + District**
- Service status endpoint to check if API is live and when data was last updated.
- MongoDB batching to handle large files (17k+ rows).
- API key protection for upload.

---

## 🔑 Authentication

- **Uploads require an API key** (`x-api-key` header).
- Set your key in `.env` file as:

```
API_KEY=your_api_key_here
MONGO_URI=your_mongo_connection_string
```

---

## 📡 Endpoints

### 1. Service Status

**`GET /status`**

Check if the service is live and see when data was last updated.

#### Example

```bash
curl https://kendra-api.onrender.com/status
```

#### Response

```json
{
  "message": "Service is live",
  "updated_at": "2025-08-05T10:42:12.123456"
}
```

---

### 2. Get by Kendra Code

**`GET /kendra/{kendra_code}`**

Retrieve details of a Kendra by its code.

#### Example

```bash
curl https://kendra-api.onrender.com/kendra/PMBJK00005
```

#### Response

```json
{
  "updated_at": "2025-08-05T10:42:12.123456",
  "results": [
    {
      "Sr.No": "1",
      "Kendra Code": "PMBJK00005",
      "Name": "B Md Arif Basha",
      "Contact": "9490477786",
      "State Name": "Andhra Pradesh",
      "District Name": "Ananthapuramu",
      "Pin Code": "515001",
      "Address": "28 635 Sangameshwara Nagar 80Feet Road, Anantapur"
    }
  ]
}
```

---

### 3. Get by Pincode

**`GET /pincode/{pincode}`**

Find Kendras in a specific pincode.

#### Example

```bash
curl https://kendra-api.onrender.com/pincode/522503
```

#### Response

```json
{
  "updated_at": "2025-08-05T10:42:12.123456",
  "results": [
    {
      "Sr.No": "4",
      "Kendra Code": "PMBJK00024",
      "Name": "Divvela Yedukondalu",
      "Contact": "8790567432",
      "State Name": "Andhra Pradesh",
      "District Name": "Guntur",
      "Pin Code": "522503",
      "Address": "Jan Aushadhi Storedoor No 7154 Shop No 7 Midde Center, Visakhapatnam(Rural)"
    }
  ]
}
```

---

### 4. Get by Location (State + District)

**`GET /location?state={state}&district={district}`**

Retrieve Kendras by state and district.

#### Example

```bash
curl "https://kendra-api.onrender.com/location?state=Andhra%20Pradesh&district=Annamayya"
```

#### Response

```json
{
  "updated_at": "2025-08-05T10:42:12.123456",
  "results": [
    {
      "Sr.No": "2",
      "Kendra Code": "PMBJK00012",
      "Name": "Reddy Lakshmi Deepak P",
      "Contact": "9177772726",
      "State Name": "Andhra Pradesh",
      "District Name": "Annamayya",
      "Pin Code": "517325",
      "Address": "Dno31531 Ctm Road, Madanapalle"
    },
    {
      "Sr.No": "3",
      "Kendra Code": "PMBJK00017",
      "Name": "E. Naga Rajesh and E. Sreedevi",
      "Contact": "9440539203",
      "State Name": "Andhra Pradesh",
      "District Name": "Annamayya",
      "Pin Code": "517325",
      "Address": "D No 1511632 Ground Floor K G Street Extention, Madanapalle"
    }
  ]
}
```

---

### 5. Upload New PDF

**`POST /upload?reset={true|false}`**

Upload a new **Jan Aushadhi PDF**.

- Use `reset=true` on the first upload to clear old data.
- Use `reset=false` for subsequent chunks (if splitting PDF).

#### Example

```bash
curl -X POST "https://kendra-api.onrender.com/upload?reset=true"   -H "x-api-key: your_api_key_here"   -F "file=@JanAushadhiKendra.pdf"
```

#### Response

```json
{
  "message": "Chunk uploaded successfully",
  "reset": true
}
```

---

## ⚡ Notes

- **Large PDFs (~862 pages, 17k rows)** are supported using batching (`batch_size=750`).
- MongoDB indexes automatically keep queries fast on:
  - `Kendra Code`
  - `Pin Code`
  - `(State Name, District Name)`
- Free-tier hosting may cause long uploads to timeout on the frontend, but the backend will still finish processing and update the DB.

---

## 👨‍💻 Author

Built with ❤️ by [@kunal7236](https://github.com/kunal7236) using FastAPI, MongoDB Atlas, and pdfplumber.

---

## 📖 Interactive API Docs

You can explore and test the API interactively using the built-in Swagger UI:

👉 [https://kendra-api.onrender.com/docs](https://kendra-api.onrender.com/docs)
