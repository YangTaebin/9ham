import smtplib
from email.mime.text import MIMEText

checker="hello world!"

s = smtplib.SMTP("smtp.gmail.com", 587)
s.ehlo()
s.starttls()
s.login("9hamofficial@gmail.com", "cxnyfeizoiascqpi")
msg = MIMEText("안녕하십니까\n해당 이메일을 통한 본인인증 확인 메일이 전송되었습니다.\n본인인증 창에 아래 인증번호를 입력해주세요.\n\n"+str(checker)+"\n\n저희 9ham 서비스를 이용해주셔서 감사합니다.")
msg["Subject"] = "9ham 본인인증 확인용 이메일"
s.sendmail("9hamofficial@gmail.com", "taebinjjang@gmail.com", msg.as_string())
s.quit()
print("이메일 전송 완료")