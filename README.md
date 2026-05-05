# QR Attendance — Matrix Master

A Django-based QR code attendance system. Admins generate a time-limited QR code per session; students scan it to register their attendance.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Usage

| Role | Steps |
|------|-------|
| Admin | Go to `/qr-generator/` → Generate QR code → Show it to students |
| Student | Scan QR code with phone → Login → Confirm attendance |
| External | Open the shareable link provided by admin (no login needed) |

## URLs

| URL | Description |
|-----|-------------|
| `/` | Login page |
| `/qr-generator/` | Admin: generate QR code (staff only) |
| `/dates/` | Admin: view all sessions and attendees (staff only) |
| `/view-students/<token>/` | Public attendance list |
| `/admin/` | Django admin — add/delete students and sessions |

## Notes

- QR codes are valid for **2 hours** from generation
- For mobile scanning, run with `0.0.0.0:8000` and access via your machine's local IP (not `localhost`)
- Students must be created in `/admin/` before they can log in
