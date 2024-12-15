# Email SMTP
Handles sending emails using SMTP

# Install
```
pip install email-smtp
```

# Requires
email-smtp requires python 3.10 or higher

# Using

```python
from em import send, valid

def send_email(to, subject, text, html):

	if valid(to):
		send(to, subject, {
			'text': text,
			'html': html
		})
```

# Options

| Name | Type | Description |
| ---- | ---- | ----------- |
| `attachments` | str[] \| {'body': str, 'filename'}[] | A list of attachments to add to the email |
| `bcc` | str \| str[] | One or more e-mail addresses to send a blind carbon copy to |
| `cc` | str \| str[] | One or more e-mail addresses to send a carbo copy to |
| `from` | str | The e-mail address to show as having sent the e-mail |
| `html` | str | The HTML version of the e-mail to send, this or `text` must be set |
| `reply-to` | str | The e-mail address to mark as receiving any replies |
| `text` | str | The text version of the e-mail to send, this or `html` must be set |
| `unsubscribe` | str | The URL to add to the header for the receiver to be able to unsubscribe |