import imaplib
import email
from email.header import decode_header


# Connexion à la boîte de réception
def connect_to_email(username, password, imap_url):
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(username, password)
    mail.select("inbox")
    return mail


# Extraction des informations des e-mails
def extract_job_info(mail, limit=50):
    status, messages = mail.search(None, 'ALL')
    job_infos = []
    target_email = "alert@indeed.com"

    # Limit the number of emails to process
    email_nums = messages[0].split()
    if len(email_nums) > limit:
        email_nums = email_nums[-limit:]  # Get the last `limit` number of emails

    for num in email_nums:
        status, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Vérifier l'adresse de l'expéditeur
        from_ = msg.get("From")
        if from_:
            from_email = email.utils.parseaddr(from_)[1]
            if from_email.lower() != target_email.lower():
                continue  # Passer au prochain e-mail si l'expéditeur ne correspond pas

        # Décode le sujet de l'e-mail
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            try:
                subject = subject.decode(encoding if encoding else 'utf-8')
            except (LookupError, UnicodeDecodeError):
                subject = subject.decode('utf-8', errors='replace')  # Remplace les erreurs de décodage

        # Afficher les informations de l'e-mail
        print(f"From: {from_}")
        print(f"Subject: {subject}")
        print(f"Date: {msg.get('Date')}")

        # Afficher le corps du message
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            body = payload.decode()
                        except (LookupError, UnicodeDecodeError):
                            body = payload.decode('utf-8', errors='replace')
                        print(f"Body: {body}")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                try:
                    body = payload.decode()
                except (LookupError, UnicodeDecodeError):
                    body = payload.decode('utf-8', errors='replace')
                print(f"Body: {body}")

        print("\n" + "=" * 50 + "\n")


# Utilisation
username = "dbmx76@gmail.com"
password = "kghz sjzk sumo kbhg"
imap_url = "imap.gmail.com"


mail = connect_to_email(username, password, imap_url)
extract_job_info(mail, limit=50)
# save_to_file(job_infos)
