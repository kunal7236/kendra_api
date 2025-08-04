# Jan Aushadhi Kendra API

A FastAPI-based service to extract and serve Jan Aushadhi Kendra data from PDF to MongoDB.

## 🔧 Setup

- Add your `.env` file with:
```
API_KEY=your_secret_api_key
MONGO_URI=your_mongodb_connection_string
```

## 🚀 Endpoints

### ✅ Public Routes

- `GET /location?state=...&district=...`  
  → Returns Kendras by state and district.

- `GET /pincode/{pincode}`  
  → Returns Kendras for a pincode.

- `GET /kendra/{kendra_code}`  
  → Returns data for a specific Kendra.

- `GET /status`  
  → Returns last updated time.

### 🔐 Admin Route

- `POST /upload`  
  Uploads a new PDF and updates the database.  
  Requires header:
  ```
  Authorization: Bearer YOUR_API_KEY
  ```

## 📦 Example Query

```bash
curl https://yourdomain.com/location?state=Bihar&district=Patna
```
