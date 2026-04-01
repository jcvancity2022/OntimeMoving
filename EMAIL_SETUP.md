# Email Notification Setup Guide

## Overview
The OnTime Moving system now includes automated email notifications for booking confirmations. When a customer submits a booking:

1. **Customer receives**: A professional confirmation email with booking details
2. **Business receives**: A notification email with customer info and action items
3. **System logs**: All notifications are logged to `booking_notifications.log`

## Current Status
✅ Email notification system installed  
⚠️ **Email notifications are DISABLED by default** (requires configuration)

## Quick Setup (Gmail Example)

### Step 1: Enable in config.json
Edit `config.json` and update the email section:

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_username": "your-email@gmail.com",
  "smtp_password": "your-app-password",
  "from_email": "info@ontime-moving.com"
}
```

### Step 2: Get Gmail App Password
**Important**: Regular Gmail passwords won't work. You need an App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Security → 2-Step Verification (must be enabled)
3. App passwords → Generate new password
4. Select "Mail" and "Windows Computer"
5. Copy the 16-character password (no spaces)
6. Use this password in `config.json`

### Step 3: Restart Server
```bash
python server.py
```

### Step 4: Test
```bash
python email_notifier.py
```

## Using Other Email Services

### Office 365 / Outlook
```json
"smtp_server": "smtp.office365.com",
"smtp_port": 587,
"smtp_username": "your-email@outlook.com",
"smtp_password": "your-password"
```

### Custom SMTP Server
```json
"smtp_server": "mail.yourdomain.com",
"smtp_port": 587,
"smtp_username": "notifications@yourdomain.com",
"smtp_password": "your-password"
```

## What Happens Without Email Enabled

Even with emails disabled, the system:
- ✅ Still accepts and saves bookings normally
- ✅ Logs all notifications to `booking_notifications.log`
- ⚠️ Displays console warnings about disabled emails
- ℹ️ Won't fail or crash

## Email Templates

### Customer Confirmation Email
- Professional green-themed design matching the website
- Displays booking ID, move date, addresses, and size
- Includes "What's Next?" steps
- Shows business contact information

### Business Notification Email
- Clear action-required format
- Complete customer contact info (clickable phone/email)
- Full move details
- Request timestamp

## Troubleshooting

### "Authentication failed"
- Verify you're using an App Password (not regular password)
- Check 2-Step Verification is enabled for Gmail
- Ensure smtp_username matches the email exactly

### "Connection refused"
- Check smtp_server and smtp_port are correct
- Verify firewall isn't blocking port 587
- Try port 465 with SSL if 587 fails

### Emails not arriving
- Check spam/junk folders
- Verify email addresses are correct
- Review `booking_notifications.log` for errors
- Test with `python email_notifier.py`

### "Module not found: email.mime"
- This is built into Python, no installation needed
- If error persists, Python installation may be corrupt

## Viewing Notification Logs

All notifications (sent or not) are logged:
```bash
type booking_notifications.log
```

Each log entry shows:
- Timestamp
- Booking ID
- Customer info
- Status (notification_sent or logged_only)

## Security Best Practices

1. **Never commit credentials**: Add `config.json` to `.gitignore`
2. **Use App Passwords**: Don't use your main email password
3. **Restrict access**: Keep SMTP credentials secure
4. **Monitor logs**: Review `booking_notifications.log` regularly

## Production Recommendations

For production use, consider:
- **Dedicated email service**: SendGrid, Mailgun, AWS SES
- **Email queues**: Handle high volume without delays
- **Delivery tracking**: Monitor bounce rates and deliverability
- **Professional domain**: Use info@yourdomain.com instead of Gmail

## Support

If you need help setting up email notifications:
1. Check this guide first
2. Review `booking_notifications.log` for error details
3. Test with `python email_notifier.py`
4. Verify config.json syntax is valid JSON

---

**Ready to enable?** Edit `config.json` → Set `"enabled": true` → Add SMTP credentials → Restart server
