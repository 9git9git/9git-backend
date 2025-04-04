# 🔹 GitHub 기반 기능 개발 가이드

이 문서는 **GitHub과 JIRA를 연동한 기능을 개발 가이드**입니다.

GitHub 저장소를 포크하고, 클론하고, 변경 사항을 푸쉬하고, PR을 생성하는 순서를 설명합니다.

---

## 🖥 1. 저장소 클론(Clone)

> ✅ 클론(Clone)이란? 포크한 저장소를 내 컴퓨터에 다운로드하는 과정입니다.

1. 포크한 저장소에서 `Code` 버튼을 클릭합니다.
2. `HTTPS URL`을 복사합니다. (예: `https://github.com/your-username/project-name.git`)
3. 터미널(명령 프롬프트)을 열고, 아래 명령어를 입력합니다.

   ```bash
   git clone <https://github.com/your-username/project-name.git>
   ```

4. 클론한 폴더로 이동합니다.

---

## ✏2. 새 브랜치 생성

> ✅ 새 브랜치를 만들어 기능을 개발하는 과정입니다.

1. 새 브랜치를 생성합니다(`SCRUM-[number]-[team]-[feature]` 예시).

```bash
git checkout -b SCRUM-[number]-[team]-[feature]
```

1. 현재 브랜치를 확인합니다.

```bash
git branch
```

✅ `SCRUM-[number]-[team]-[feature]`가 선택되어 있는지 확인합니다.

---

## 💻 3. 기능 개발

> ✅ 기능 개발 후 변경된 파일을 Git에 추가하고 커밋하는 과정입니다.

1. 코드 수정 후 변경 사항을 확인합니다.

```bash
git status
```

1. 변경퇸 파일을 Git에 추가합니다.

```bash
git add .
```

1. Gitmogi 스타일을 적용하여 커밋합니다.

- 커밋 메시지 작성 가이드
  ```bash
  <gitmoji> [SCRUM-number] 작업내용
  ```

```bash
gitmoji -c
1. (방향키로 이모티콘 선택)
2. 커밋 제목 작성
3. 커밋 메세지 작성
```

---

# 🔼 4. 변경 사항 푸쉬(Push)

> ✅ **푸쉬(Push)**란? 내 컴퓨터에서 개발한 내용을 GitHub에 업로드하는 과정입니다.

```bash
git push origin SCRUM-[number]-[team]-[feature]
```

✅ 이 명령어를 실행하면 GitHub에 `SCRUM-[number]-[team]-[feature]` 브랜치가 생성됩니다.

---

# 🔁 5. Pull Request(PR) 생성

> ✅ PR(Pull Request)은 팀원에게 코드 리뷰를 요청하고, 변경 사항을 메인 저장소로 병합하는 과정입니다.

1. GitHub에서 저장소로 이동합니다.
2. `SCRUM-[number]-[team]-[feature]` 브랜치를 선택합니다.
3. `Compare & pull request` 버튼을 클릭합니다.
4. PR 제목을 작성합니다.

```bash
[SCRUM-number] 작업내용
```

1. PR 본문을 작성합니다.

```bash
## Explain this Pull Request 🙏

- Jira Issue :
- Jira URL(미정):

## What has fixed? 🛠

변경 전 내용

변경 후 내용

## Document🗒️ (Optional)

## Screenshot 📸 (Optional)

## Test Checklist ✅ (Optional)
```

1. PR을 생성하고 팀원에게 리뷰 요청합니다.
2. 코드 리뷰 후 `Merge`를 클릭하여 병합합니다.

---

## 🎯 최종 정리

| 단계            | 설명                           | 명령어                                            |
| --------------- | ------------------------------ | ------------------------------------------------- |
| **클론**        | 내 컴퓨터로 저장소 다운로드    | `git clone <저장소-URL>`                          |
| **브랜치 생성** | 새 브랜치에서 로그인 기능 개발 | `git checkout -b SCRUM-[number]-[team]-[feature]` |
| **커밋**        | 변경 사항 저장                 | `gitmoji -c "[gitmoji] [SCRUM-number] 작업내용"`  |
| **푸쉬**        | 변경 사항을 GitHub로 업로드    | `git push origin SCRUM-[number]-[team]-[feature]` |
| **PR 생성**     | 코드 리뷰 요청 후 병합         | GitHub에서 `Pull Request` 생성                    |
