"""Notion Service - 강의 노트를 노션으로 익스포트"""

import httpx
from typing import Any, Dict, List
from app.config import settings
from app.schemas.responses import NoteResponse

class NotionService:
    NOTION_TEXT_LIMIT = 2000  # Notion API 텍스트 길이 제한

    def __init__(self):
        self.api_key = settings.NOTION_API_KEY
        self.database_id = settings.NOTION_DATABASE_ID
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def _split_text(self, text: str, limit: int = None) -> List[str]:
        """긴 텍스트를 Notion 제한에 맞게 청크로 분할"""
        if limit is None:
            limit = self.NOTION_TEXT_LIMIT
        if not text:
            return [""]
        chunks = []
        while text:
            if len(text) <= limit:
                chunks.append(text)
                break
            # 줄바꿈 기준으로 자연스럽게 자르기 시도
            split_pos = text.rfind('\n', 0, limit)
            if split_pos == -1 or split_pos < limit // 2:
                # 줄바꿈이 없거나 너무 앞에 있으면 그냥 limit에서 자름
                split_pos = limit
            chunks.append(text[:split_pos])
            text = text[split_pos:].lstrip('\n')
        return chunks

    def _create_code_blocks(self, content: str, language: str = "markdown") -> List[Dict[str, Any]]:
        """긴 코드를 여러 코드 블록으로 분할"""
        chunks = self._split_text(content)
        blocks = []
        for chunk in chunks:
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}],
                    "language": language
                }
            })
        return blocks

    def _create_paragraph_blocks(self, content: str, annotations: Dict = None) -> List[Dict[str, Any]]:
        """긴 텍스트를 여러 paragraph 블록으로 분할"""
        chunks = self._split_text(content)
        blocks = []
        for chunk in chunks:
            rich_text_item = {"type": "text", "text": {"content": chunk}}
            if annotations:
                rich_text_item["annotations"] = annotations
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [rich_text_item]
                }
            })
        return blocks

    def _create_callout_blocks(self, content: str, emoji: str = "💡", color: str = "yellow_background") -> List[Dict[str, Any]]:
        """긴 텍스트를 여러 callout 블록으로 분할"""
        chunks = self._split_text(content)
        blocks = []
        for i, chunk in enumerate(chunks):
            blocks.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}],
                    "icon": {"emoji": emoji} if i == 0 else {"emoji": "↳"},
                    "color": color
                }
            })
        return blocks

    async def create_lecture_page(self, note: NoteResponse, source_url: str | None = None) -> str:
        """
        강의 노트를 노션 데이터베이스에 새로운 페이지로 생성합니다.
        """
        url = f"{self.base_url}/pages"
        
        # 1. Properties (겉표지 정보)
        # 참고: 노션 데이터베이스에 해당 속성이 있어야 함
        properties = {
            "이름": { "title": [{"text": {"content": note.title}}] },
        }
        # 원본 영상 URL이 있으면 추가
        if source_url:
            properties["URL"] = { "url": source_url }
        
        # 2. Children (알맹이 내용)
        children = []
        
        for slide in note.slides:
            # 슬라이드 헤더
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": f"슬라이드 {slide.slide_number}"}}]
                }
            })
            
            # 타임스탬프 정보
            start_min = int(slide.timestamp_start // 60)
            start_sec = int(slide.timestamp_start % 60)
            end_min = int(slide.timestamp_end // 60)
            end_sec = int(slide.timestamp_end % 60)
            
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text", 
                        "text": {"content": f"시간: {start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"},
                        "annotations": {"italic": True, "color": "gray"}
                    }]
                }
            })

            # 슬라이드 이미지 (외부 URL)
            children.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": slide.image_url
                    }
                }
            })

            # OCR 수식 섹션
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "📊 핵심 수식 (OCR)"}}]
                }
            })
            
            # OCR 내용을 2000자 제한에 맞게 여러 블록으로 분할
            children.extend(self._create_code_blocks(slide.ocr_content, "markdown"))

            # 강의 요약 섹션
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 강의 요약"}}]
                }
            })
            
            # 요약 내용을 2000자 제한에 맞게 여러 블록으로 분할
            children.extend(self._create_paragraph_blocks(slide.audio_summary))

            # SOS 해설 (있는 경우) - 2000자 제한에 맞게 분할
            if slide.sos_explanation:
                children.extend(self._create_callout_blocks(slide.sos_explanation))

            # 구분선
            children.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })

        # 노션 API는 한 번에 최대 100개의 blocks(children)만 허용함.
        # MVP에서는 슬라이드 수가 많지 않다고 가정하고 100개로 제한.
        # 실제로는 append block children API를 추가로 호출해야 함.
        payload = {
            "parent": { "database_id": self.database_id },
            "properties": properties,
            "children": children[:100] 
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            if response.status_code != 200:
                print(f"Notion API Error: {response.text}")
                response.raise_for_status()
            
            data = response.json()
            return data.get("url", "")

notion_service = NotionService()
