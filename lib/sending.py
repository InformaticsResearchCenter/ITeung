def sendingnormalize(msg):
    msg = msg.replace('\\n', '\n')
    msg = msg.strip()
    return msg