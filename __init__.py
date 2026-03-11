import re
from email.message import EmailMessage
from email.utils import formataddr

from CTFd.utils import get_app_config, get_config
from CTFd.utils.email.providers.smtp import get_smtp, SMTPEmailProvider


def strip_tags(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def sendmail_html(addr, text, subject):
    ctf_name = get_config("ctf_name")
    mailfrom_addr = get_config("mailfrom_addr") or get_app_config("MAILFROM_ADDR")
    mailfrom_addr = formataddr((ctf_name, mailfrom_addr))

    data = {
        "host": get_config("mail_server") or get_app_config("MAIL_SERVER"),
        "port": int(get_config("mail_port") or get_app_config("MAIL_PORT")),
    }

    username = get_config("mail_username") or get_app_config("MAIL_USERNAME")
    password = get_config("mail_password") or get_app_config("MAIL_PASSWORD")
    TLS = get_config("mail_tls") or get_app_config("MAIL_TLS")
    SSL = get_config("mail_ssl") or get_app_config("MAIL_SSL")
    auth = get_config("mail_useauth") or get_app_config("MAIL_USEAUTH")

    if username:
        data["username"] = username
    if password:
        data["password"] = password
    if TLS:
        data["TLS"] = TLS
    if SSL:
        data["SSL"] = SSL
    if auth:
        data["auth"] = auth

    smtp = get_smtp(**data)

    msg = EmailMessage()

    looks_html = "<html" in text.lower() or "</" in text.lower() or "<br" in text.lower()

    if looks_html:
        msg.set_content(strip_tags(text))
        msg.add_alternative(text, subtype="html")
    else:
        msg.set_content(text)

    msg["Subject"] = subject
    msg["From"] = mailfrom_addr
    msg["To"] = addr

    custom_smtp = bool(get_config("mail_server"))
    if custom_smtp:
        smtp.send_message(msg)
    else:
        mailsender_addr = get_app_config("MAILSENDER_ADDR")
        smtp.send_message(msg, from_addr=mailsender_addr)

    smtp.quit()
    return True, "Email sent"


def load(app):
    SMTPEmailProvider.sendmail = staticmethod(sendmail_html)
