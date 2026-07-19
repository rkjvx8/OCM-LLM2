import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request

from site_data import articles, services, training_events

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "false").lower() in {"1", "true", "yes"}
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "no-reply@vanguardchangesolutions.com")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "ryanjacobson2@gmail.com")


@app.route("/")
def home():
    return render_template("index.html", services=services, articles=articles, events=training_events[:2])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services_page():
    return render_template("services.html", services=services)


@app.route("/training")
def training():
    return render_template("training.html", events=training_events)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    success = False
    message = ""
    if request.method == "POST":
        submitted = True
        name = request.form.get("name", "there").strip() or "there"
        sender_email = request.form.get("email", "").strip()
        topic = request.form.get("topic", "General inquiry").strip()
        body_text = request.form.get("message", "").strip()

        email_message = EmailMessage()
        email_message["Subject"] = f"New inquiry from {name} — {topic}"
        email_message["From"] = EMAIL_SENDER
        email_message["To"] = EMAIL_RECIPIENT
        if sender_email:
            email_message["Reply-To"] = sender_email

        email_message.set_content(
            f"Name: {name}\n"
            f"Email: {sender_email or 'Not provided'}\n"
            f"Topic: {topic}\n\n"
            f"Message:\n{body_text or 'No message provided.'}\n"
        )

        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
                if SMTP_USE_TLS:
                    smtp.starttls()
                if SMTP_USER and SMTP_PASSWORD:
                    smtp.login(SMTP_USER, SMTP_PASSWORD)
                smtp.send_message(email_message)
            success = True
            message = f"Thanks for reaching out, {name}. Your message has been sent."
        except Exception:
            success = False
            message = "There was a problem sending your message. Please try again later or email ryanjacobson2@gmail.com directly."

    return render_template("contact.html", submitted=submitted, success=success, message=message)


@app.route("/ocm-llm")
def ocm_llm():
    return render_template("ocm_llm.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=port, debug=debug)
