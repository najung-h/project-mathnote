# 프로젝트 구조
```
mathnote-react/
├── src/
│   ├── components/          # 재사용 컴포넌트
│   │   ├── common/          # Button, Logo, Modal
│   │   ├── welcome/         # WelcomePage 섹션들
│   │   ├── main/            # MainPage 컴포넌트들
│   │   └── upload/          # UploadModal
│   ├── constants/           # API, Config, Routes 상수
│   ├── services/            # API 서비스 레이어
│   ├── types/               # TypeScript 타입 정의
│   ├── pages/               # 페이지 컴포넌트
│   └── App.tsx              # 라우팅 설정
```

자세히는
```
mathnote-react/
├── src/
│   ├── components/          # 재사용 가능한 컴포넌트
│   │   ├── common/          # 공통 UI 컴포넌트
│   │   │   ├── Button.tsx   # 버튼 컴포넌트
│   │   │   ├── Logo.tsx     # 로고 컴포넌트
│   │   │   ├── Modal.tsx    # 모달 컴포넌트
│   │   │   └── index.ts
│   │   ├── welcome/         # Welcome 페이지 섹션 컴포넌트
│   │   │   ├── WelcomeHeader.tsx
│   │   │   ├── HeroSection.tsx
│   │   │   ├── ProblemSection.tsx
│   │   │   ├── TechSection.tsx
│   │   │   ├── OutputSection.tsx
│   │   │   ├── CTASection.tsx
│   │   │   ├── WelcomeFooter.tsx
│   │   │   └── index.ts
│   │   ├── main/            # Main 페이지 컴포넌트
│   │   │   ├── MainHeader.tsx
│   │   │   ├── VideoPlayer.tsx
│   │   │   ├── LectureInfo.tsx
│   │   │   ├── NotePreview.tsx
│   │   │   └── index.ts
│   │   ├── upload/          # 업로드 모달 컴포넌트
│   │   │   ├── UploadModal.tsx
│   │   │   └── index.ts
│   │   └── index.ts
│   ├── constants/           # 상수 정의
│   │   ├── api.ts           # API 엔드포인트, 상수
│   │   ├── config.ts        # 앱 설정 상수
│   │   ├── routes.ts        # 라우트 경로 상수
│   │   └── index.ts
│   ├── services/            # API 서비스 레이어
│   │   ├── apiClient.ts     # Axios 인스턴스
│   │   ├── videoService.ts  # Video API 서비스
│   │   ├── noteService.ts   # Note API 서비스
│   │   └── index.ts
│   ├── types/               # TypeScript 타입 정의
│   │   ├── api.ts           # API 요청/응답 타입
│   │   └── index.ts
│   ├── pages/               # 페이지 컴포넌트
│   │   ├── WelcomePage.tsx
│   │   ├── MainPage.tsx
│   │   └── index.ts
│   ├── App.tsx              # 메인 앱 컴포넌트
│   ├── main.tsx             # 엔트리 포인트
│   └── index.css            # 글로벌 스타일
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
└── vite.config.ts
```

# 실행 방법
```
# 프로젝트 폴더로 이동
cd frontend/mathnote-react

# 의존성 설치
npm install

# 개발 서버 실행 (localhost:3000)
npm run dev   # http://localhost:3000

# 빌드
npm run build
```

# 기술 스택
- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite (rolldown-vite)
- **Styling**: Tailwind CSS 3
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios
- **Math Rendering**: KaTeX
- **Markdown**: react-markdown + remark-math + rehype-katex

# API 연동 구조
|                   | 엔드포인트                             | 서비스 함수                     |
| ----------------- | -------------------------------------- | ------------------------------- |
| YouTube 영상 처리 | POST `/api/v1/videos/fetch-url`        | `videoService.fetchFromUrl()`   |
| 파일 업로드       | POST `/api/v1/videos/upload`           | `videoService.uploadFile()`     |
| 처리 시작         | POST `/api/v1/videos/{taskId}/process` | `videoService.processVideo()`   |
| 상태 조회         | GET `/api/v1/videos/{taskId}/status`   | `videoService.getStatus()`      |
| 노트 조회         | GET `/api/v1/notes/{taskId}`           | `noteService.getNote()`         |
| 다운로드          | GET `/api/v1/notes/{taskId}/download`  | `noteService.getDownloadLink()` |