# CTFd HTML Email Plugin

A simple plugin for **CTFd** that enables sending **HTML emails** instead of plain-text emails.

CTFd normally sends emails as plain text. This plugin overrides the default email sender and allows sending HTML emails with a plaintext fallback for compatibility with all email clients.

## ✨ Features

* Send **HTML emails**
* Automatic **plain-text fallback**
* Uses existing **CTFd SMTP configuration**
* Lightweight and easy to install
* No changes required to CTFd core

## 📦 Installation

1. Clone or download this repository.

2. Copy the plugin folder into your CTFd plugins directory:

```
CTFd/plugins/
```

Example:

```
CTFd/plugins/CTFd-html-email-plugin/
```

3. Restart CTFd.

## ⚙️ Usage

Simply send email content containing HTML and the plugin will automatically detect it and send a **multipart email** containing:

* HTML version
* Plain text fallback

Example:

```html
<h1>Welcome to the CTF</h1>
<p>Your account has been created successfully.</p>
```

If the content is not HTML, it will be sent as a normal plaintext email.

## 🔧 How It Works

The plugin overrides the default CTFd SMTP email provider:

```
SMTPEmailProvider.sendmail
```

It detects whether the message contains HTML and sends the email using:

* `text/plain`
* `text/html`

This ensures compatibility with all mail clients.

## 📁 Project Structure

```
CTFd-html-email-plugin
│
├── README.md
├── LICENSE
└── __init__.py
```

## 🤝 Contributing

Pull requests and improvements are welcome.

If you find issues or have ideas for improvements, feel free to open an issue.

## 📜 License

This project is licensed under the MIT License.

