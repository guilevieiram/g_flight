from email.mime.text import MIMEText


message = MIMEText("uhuuuul")
message["Subject"] = "G-Flight cheap flights alert!"
msg=MIMEText(message).as_string()

print(msg)