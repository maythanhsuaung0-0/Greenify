import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(to_email, approve, seller_name, seller_password):
    # company email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'your.greenify@gmail.com'
    smtp_password = 'xvaqcjfbqcpzgjns'

    from_email = smtp_username
    subject = 'Approval mail for your Greenify seller account'
    message = MIMEMultipart()
    body = f"""
    
    Dear {seller_name}, </br>
    
    <p>We hope this email finds you well. We appreciate your interest in joining our platform as a seller, and we are delighted to inform you that your seller account registration has been approved.</p>
    
    <p>
    You can log in to Greenify seller account using: </br>
    Seller Email: {to_email} </br>
    Seller Password: <u>{seller_password}</u>
    </p>

    <p>You can now log in to your seller account and start listing your products on our platform. We believe that your offerings will be a valuable addition to our marketplace, and we look forward to a successful and collaborative partnership.
    </p>
    <p>To access your seller dashboard, please click on the following link: </br>
    
     <a href="http://127.0.0.1:5000/staff/login">Greenify seller dashboard</a></p>
    
    <p>If you have any questions or need assistance with setting up your account, please do not hesitate to reach out to our support team at this email address.
    Thank you for choosing to be a part of our community. We wish you every success in your endeavors as a seller on our platform.
    </p>
    Best regards,</br>
    
    Greenify"""
    if not approve:
        subject = "Rejection of Seller Account Registration"
        body = """

        Dear Seller,
        
        We hope this email finds you well. Thank you for your interest in becoming a seller on our platform. After careful consideration of your application, we regret to inform you that your seller account registration has been declined.
        
        Our platform is dedicated to promoting businesses that prioritize sustainability, and we appreciate your initiative to be a part of this community. However, based on our evaluation, it seems that the products you intend to sell or the description provided does not sufficiently demonstrate a commitment to sustainability, which is a priority for our website.
        
        We encourage you to review your product offerings and provide a more detailed description of how your business aligns with sustainable practices. If you make the necessary adjustments, we invite you to reapply for a seller account in the future.
        
        Thank you for your understanding. If you have any questions or would like further clarification, please feel free to reach out to our support team at this email address.
        
        We appreciate your interest in our platform and wish you success in your endeavors.
        
        Best regards,
        
        Greenify"""
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(from_email, to_email, message.as_string())
