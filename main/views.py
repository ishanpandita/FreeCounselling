from django.shortcuts import render, redirect
from .models import CounsellingEnquiry
from django.contrib import messages
import requests
import os


def send_email_via_brevo(to_email, subject, html_content):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Free Counselling",
            "email": "counselling.live@gmail.com"
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(url, json=data, headers=headers)
    return response.status_code


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        counselling_type = request.POST.get("counselling_type")
        message_text = request.POST.get("message")

        # Save to database
        CounsellingEnquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            counselling_type=counselling_type,
            message=message_text
        )

        # === USER EMAIL ===
        user_subject = "Thank you for contacting Free Counselling"

        user_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color:#333;">
            <p>Dear {name},</p>
            <p>Thank you for reaching out for <b>{counselling_type}</b> counselling.</p>
            <p>We have received your enquiry and will contact you soon.</p>
            <br>
            <p>Best regards,<br><b>Free Counselling Team</b></p>
            <br>
            <img src="https://freecounselling.life/static/images/logo(2).png" width="64" height="64"/>
          </body>
        </html>
        """

        send_email_via_brevo(email, user_subject, user_html)

        # === ADMIN EMAIL ===
        admin_subject = "New counselling enquiry received"

        admin_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color:#333;">
            <h3>New Enquiry Submitted</h3>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Counselling Type:</b> {counselling_type}</p>
            <p><b>Message:</b><br>{message_text}</p>
            <br>
            <img src="https://freecounselling.life/static/images/logo(2).png" width="64" height="64"/>
          </body>
        </html>
        """

        send_email_via_brevo("counselling.live@gmail.com", admin_subject, admin_html)

        messages.success(request, "✅ Your form has been submitted. Please check your email/spam.")
        return redirect("/")

    return render(request, "main/index.html")
