# 보토리 기여 부분 설명

## Merge전 체크사항

[ ] Image 처리태그와의 호환성 (n줄 이상 혹은 n자 이상의 이미지를 포함하는 메세지)

[ ] 데이터베이스에 `LongTextChannel` 추가 여부

## 용어

| 용어 (실사용) | 설명                        |
| ------------- | --------------------------- |
| 원본          | 작성자가 작성한 글          |
| 사본 (Orig)   | 작성자가 작성한 글의 복사본 |
| 정보 (Info)   | 글의 메타데이터(글쓴이 등)  |
| 단축된 (Tiny) | 단축된 글                   |
| 글            | = 메세지 (혼용)             |

* 사본의 경우 copy등을 이름을 사용해야 하나 다른 코드와의 이름 규칙 일치를 위해 `Orig`사용

## 변수

| 변수                   | desc                     | other          |
| ---------------------- | ------------------------ | -------------- |
| LongTextChannel        | 사본 글 저장 채널        | DB에 추가 필요 |
| LongMsgOrigInfoEmbed   | 사본 글 정보 임베드      |                |
| LongMsgOrigInfoMessage | 사본 글 정보 메세지 객체 |                |
| LongMsgOrigContent     | 사본 글 내용             |                |
| LongMsgOrigEmbed       | 사본 글 임베드           |                |
| LongMsgOrigMessage     | 사본 글 메세지 객체      |                |
| LongMsgTinyEmbed       | 단축된 글 임베드         |                |
| LongMsgTinyMessage     | 단축된 글 메세지 객체    |                |

