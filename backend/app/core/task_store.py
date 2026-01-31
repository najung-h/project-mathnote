"""Task Store - JSON 파일 기반 영구 저장소"""

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TaskEncoder(json.JSONEncoder):
    """dataclass, datetime, Path 등을 JSON으로 변환"""

    def default(self, obj):
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


class TaskStore:
    """
    JSON 파일 기반 Task 저장소

    각 task를 개별 JSON 파일로 저장하여 서버 재시작 후에도 데이터 유지
    """

    def __init__(self, storage_path: str = "storage"):
        self.tasks_dir = Path(storage_path) / "tasks"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, dict] = {}
        self._load_all()

    def _get_task_path(self, task_id: str) -> Path:
        """task_id에 해당하는 JSON 파일 경로"""
        return self.tasks_dir / f"{task_id}.json"

    def _load_all(self) -> None:
        """서버 시작 시 모든 task 로드"""
        for json_file in self.tasks_dir.glob("*.json"):
            try:
                task_id = json_file.stem
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # datetime 문자열을 다시 datetime 객체로 변환
                if "created_at" in data and isinstance(data["created_at"], str):
                    data["created_at"] = datetime.fromisoformat(data["created_at"])
                self._cache[task_id] = data
            except Exception as e:
                print(f"[TaskStore] Failed to load {json_file}: {e}")
        print(f"[TaskStore] Loaded {len(self._cache)} tasks from disk")

    def _save(self, task_id: str) -> None:
        """단일 task를 JSON 파일로 저장"""
        if task_id not in self._cache:
            return

        task_path = self._get_task_path(task_id)
        with open(task_path, "w", encoding="utf-8") as f:
            json.dump(self._cache[task_id], f, cls=TaskEncoder, ensure_ascii=False, indent=2)

    def __contains__(self, task_id: str) -> bool:
        """task_id in store"""
        return task_id in self._cache

    def __getitem__(self, task_id: str) -> dict:
        """store[task_id]"""
        return self._cache[task_id]

    def __setitem__(self, task_id: str, value: dict) -> None:
        """store[task_id] = value"""
        self._cache[task_id] = value
        self._save(task_id)

    def get(self, task_id: str, default: Any = None) -> dict | Any:
        """store.get(task_id, default)"""
        return self._cache.get(task_id, default)

    def update_task(self, task_id: str, **kwargs) -> None:
        """task 필드 업데이트 후 저장"""
        if task_id in self._cache:
            self._cache[task_id].update(kwargs)
            self._save(task_id)

    def save(self, task_id: str) -> None:
        """명시적 저장 (task 내부 수정 후 호출)"""
        self._save(task_id)


# 싱글톤 인스턴스
_store: TaskStore | None = None


def get_task_store(storage_path: str = "storage") -> TaskStore:
    """TaskStore 싱글톤 인스턴스 반환"""
    global _store
    if _store is None:
        _store = TaskStore(storage_path)
    return _store
