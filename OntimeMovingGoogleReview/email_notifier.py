"""
Email notification system for OnTime Moving booking confirmations
"""
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional


class EmailNotifier:
    """Handles sending email notifications for bookings"""
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize email notifier with configuration"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.business_name = config['business']['name']
        self.business_email = config['business']['email']
        self.business_phone = config['business']['phone']
        
        # Email configuration
        self.email_config = config.get('email', {})
        self.enabled = self.email_config.get('enabled', False)
        self.smtp_server = self.email_config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.email_config.get('smtp_port', 587)
        self.smtp_username = self.email_config.get('smtp_username', '')
        self.smtp_password = self.email_config.get('smtp_password', '')
        self.from_email = self.email_config.get('from_email', self.business_email)
    
    def send_booking_confirmation(self, booking_data: Dict) -> bool:
        """
        Send booking confirmation to customer and notification to business
        
        Args:
            booking_data: Dictionary containing booking information
            
        Returns:
            True if emails sent successfully, False otherwise
        """
        if not self.enabled:
            print("⚠️  Email notifications are disabled. Enable in config.json")
            self._log_notification(booking_data)
            return False
        
        success = True
        
        # Send confirmation to customer
        try:
            self._send_customer_confirmation(booking_data)
            print(f"✓ Confirmation email sent to {booking_data['email']}")
        except Exception as e:
            print(f"✗ Failed to send customer confirmation: {e}")
            success = False
        
        # Send notification to business
        try:
            self._send_business_notification(booking_data)
            print(f"✓ Notification sent to {self.business_email}")
        except Exception as e:
            print(f"✗ Failed to send business notification: {e}")
            success = False
        
        # Always log the notification
        self._log_notification(booking_data)
        
        return success
    
    def _send_customer_confirmation(self, booking_data: Dict):
        """Send confirmation email to customer"""
        subject = f"Booking Confirmation - {self.business_name}"
        
        body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #d32f2f; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
        <h1 style="margin: 0;">{self.business_name}</h1>
        <p style="margin: 10px 0 0 0;">Booking Confirmation</p>
    </div>
    
    <div style="background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
        <h2 style="color: #d32f2f; margin-top: 0;">Thank You, {booking_data['customer_name']}!</h2>
        
        <p>We've received your moving request and will contact you shortly to confirm details.</p>
        
        <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #374151; margin-top: 0;">Booking Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Booking ID:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">#{booking_data.get('booking_id', 'Pending')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Move Date:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['move_date']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>From:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['moving_from']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>To:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['moving_to']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Move Size:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['move_size']}</td>
                </tr>
            </table>
        </div>
        
        <h3 style="color: #374151;">What's Next?</h3>
        <ol style="color: #4b5563; line-height: 1.6;">
            <li>Our team will review your booking details</li>
            <li>We'll contact you within 24 hours to confirm availability</li>
            <li>You'll receive a detailed quote and moving plan</li>
        </ol>
        
        <div style="background-color: #dbeafe; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 0; color: #1e40af;"><strong>Questions?</strong> Contact us anytime:</p>
            <p style="margin: 5px 0 0 0; color: #1e40af;">
                📞 {self.business_phone}<br>
                📧 {self.business_email}
            </p>
        </div>
        
        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
            This is an automated confirmation. Please do not reply to this email.
        </p>
    </div>
</body>
</html>
"""
        
        self._send_email(
            to_email=booking_data['email'],
            subject=subject,
            body=body
        )
    
    def _send_business_notification(self, booking_data: Dict):
        """Send new booking notification to business"""
        subject = f"🔔 New Booking Request - {booking_data['customer_name']}"
        
        notes_section = ""
        if booking_data.get('notes'):
            notes_section = f"""
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Notes:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['notes']}</td>
                </tr>
            """
        
        body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #1f2937; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
        <h1 style="margin: 0;">🚚 New Booking Request</h1>
        <p style="margin: 10px 0 0 0;">Action Required</p>
    </div>
    
    <div style="background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
        <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #374151; margin-top: 0;">Customer Information</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Name:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['customer_name']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Phone:</strong></td>
                    <td style="padding: 8px 0; color: #111827;"><a href="tel:{booking_data['phone']}">{booking_data['phone']}</a></td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Email:</strong></td>
                    <td style="padding: 8px 0; color: #111827;"><a href="mailto:{booking_data['email']}">{booking_data['email']}</a></td>
                </tr>
            </table>
        </div>
        
        <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #374151; margin-top: 0;">Move Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Booking ID:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">#{booking_data.get('booking_id', 'Pending')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Move Date:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['move_date']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>Move Size:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['move_size']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>From:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['moving_from']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6b7280;"><strong>To:</strong></td>
                    <td style="padding: 8px 0; color: #111827;">{booking_data['moving_to']}</td>
                </tr>
                {notes_section}
            </table>
        </div>
        
        <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; color: #92400e;">
                <strong>⏰ Action Required:</strong> Contact customer within 24 hours to confirm booking.
            </p>
        </div>
        
        <p style="color: #6b7280; font-size: 12px; margin-top: 30px; text-align: center;">
            Received: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
        </p>
    </div>
</body>
</html>
"""
        
        self._send_email(
            to_email=self.business_email,
            subject=subject,
            body=body
        )
    
    def _send_email(self, to_email: str, subject: str, body: str):
        """Send an email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
        
        except Exception as e:
            print(f"SMTP Error: {e}")
            raise
    
    def _log_notification(self, booking_data: Dict):
        """Log notification to file for record keeping"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'booking_id': booking_data.get('booking_id', 'Pending'),
                'customer_name': booking_data['customer_name'],
                'email': booking_data['email'],
                'phone': booking_data['phone'],
                'move_date': booking_data['move_date'],
                'status': 'notification_sent' if self.enabled else 'logged_only'
            }
            
            with open('booking_notifications.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        except Exception as e:
            print(f"Warning: Could not write to notification log: {e}")


def test_email_notifier():
    """Test the email notification system"""
    notifier = EmailNotifier()
    
    test_booking = {
        'booking_id': 999,
        'customer_name': 'Test Customer',
        'phone': '(604) 555-1234',
        'email': 'test@example.com',
        'moving_from': '123 Test St, Vancouver, BC',
        'moving_to': '456 Demo Ave, Burnaby, BC',
        'move_date': '2026-04-01',
        'move_size': '2-bedroom',
        'notes': 'This is a test booking'
    }
    
    print("Testing Email Notifier...")
    print(f"Email notifications enabled: {notifier.enabled}")
    
    if notifier.enabled:
        print(f"SMTP Server: {notifier.smtp_server}:{notifier.smtp_port}")
        print(f"From: {notifier.from_email}")
        print(f"To Business: {notifier.business_email}")
    
    result = notifier.send_booking_confirmation(test_booking)
    print(f"\nTest result: {'Success' if result else 'Failed (check config)'}")


if __name__ == "__main__":
    test_email_notifier()
