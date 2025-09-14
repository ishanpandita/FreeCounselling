from django.shortcuts import render, redirect
from .models import CounsellingEnquiry
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        counselling_type = request.POST.get("counselling_type")
        message = request.POST.get("message")

        CounsellingEnquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            counselling_type=counselling_type,
            message=message
        )

        # === User Email ===
        user_subject = "Thank you for contacting Free Counselling"
        user_text = (
            f"Dear {name},\n\n"
            f"Thank you for reaching out for {counselling_type} counselling. "
            "We have received your enquiry and will contact you soon.\n\n"
            "Best regards,\nFree Counselling Team"
        )
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

        user_email = EmailMultiAlternatives(
            subject=user_subject,
            body=user_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        user_email.attach_alternative(user_html, "text/html")

        # === Admin Email ===
        admin_subject = "New counselling enquiry received"
        admin_text = (
            f"New enquiry submitted:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Counselling Type: {counselling_type}\n"
            f"Message:\n{message}\n"
        )
        admin_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color:#333;">
            <h3>New Enquiry Submitted</h3>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Counselling Type:</b> {counselling_type}</p>
            <p><b>Message:</b><br>{message}</p>
            <br>
            <img src="https://freecounselling.life/static/images/logo(2).png" width="64" height="64"/>
          </body>
        </html>
        """

        admin_email = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
        )
        admin_email.attach_alternative(admin_html, "text/html")

        # Send emails
        user_email.send()
        admin_email.send()

        messages.success(request, "✅ Your form has been submitted. Please check your email/spam.")
        return redirect("/")  # refresh page after saving

    return render(request, "main/index.html")
