"""Utility Function Tests"""

import pytest

from app.utils.time_utils import (
    seconds_to_timestamp,
    timestamp_to_seconds,
    format_duration,
    find_segment_for_timestamp,
)


class TestSecondsToTimestamp:
    """seconds_to_timestamp 함수 테스트"""

    def test_seconds_only(self):
        """60초 미만"""
        assert seconds_to_timestamp(45) == "00:45"

    def test_minutes_and_seconds(self):
        """분 + 초"""
        assert seconds_to_timestamp(125) == "02:05"

    def test_hours_minutes_seconds(self):
        """시 + 분 + 초"""
        assert seconds_to_timestamp(3725) == "01:02:05"

    def test_zero(self):
        """0초"""
        assert seconds_to_timestamp(0) == "00:00"

    def test_float_input(self):
        """소수점 입력 (정수로 변환)"""
        assert seconds_to_timestamp(65.7) == "01:05"


class TestTimestampToSeconds:
    """timestamp_to_seconds 함수 테스트"""

    def test_mm_ss_format(self):
        """MM:SS 형식"""
        assert timestamp_to_seconds("02:30") == 150.0

    def test_hh_mm_ss_format(self):
        """HH:MM:SS 형식"""
        assert timestamp_to_seconds("01:30:45") == 5445.0

    def test_seconds_only(self):
        """초만 입력"""
        assert timestamp_to_seconds("45") == 45.0

    def test_with_decimals(self):
        """소수점 포함"""
        assert timestamp_to_seconds("01:30.5") == 90.5


class TestFormatDuration:
    """format_duration 함수 테스트"""

    def test_seconds_only(self):
        """초만 표시"""
        assert format_duration(45) == "45s"

    def test_minutes_and_seconds(self):
        """분 + 초"""
        assert format_duration(125) == "2m 5s"

    def test_hours_minutes_seconds(self):
        """시 + 분 + 초"""
        assert format_duration(3725) == "1h 2m 5s"

    def test_zero(self):
        """0초"""
        assert format_duration(0) == "0s"

    def test_exact_hour(self):
        """정확히 1시간"""
        assert format_duration(3600) == "1h"

    def test_exact_minute(self):
        """정확히 1분"""
        assert format_duration(60) == "1m"


class TestFindSegmentForTimestamp:
    """find_segment_for_timestamp 함수 테스트"""

    @pytest.fixture
    def sample_segments(self):
        """샘플 세그먼트"""
        return [
            (0.0, 60.0),    # 0
            (60.0, 120.0),  # 1
            (120.0, 180.0), # 2
        ]

    def test_find_first_segment(self, sample_segments):
        """첫 번째 세그먼트에서 찾기"""
        result = find_segment_for_timestamp(30.0, sample_segments)
        assert result == 0

    def test_find_middle_segment(self, sample_segments):
        """중간 세그먼트에서 찾기"""
        result = find_segment_for_timestamp(90.0, sample_segments)
        assert result == 1

    def test_find_last_segment(self, sample_segments):
        """마지막 세그먼트에서 찾기"""
        result = find_segment_for_timestamp(150.0, sample_segments)
        assert result == 2

    def test_boundary_start(self, sample_segments):
        """세그먼트 시작 경계 - 첫 번째 매칭 세그먼트 반환"""
        # 60.0은 첫 번째 세그먼트 끝(0.0-60.0)과 두 번째 세그먼트 시작(60.0-120.0) 모두에 포함
        # 함수는 첫 번째 매칭 세그먼트를 반환
        result = find_segment_for_timestamp(60.0, sample_segments)
        assert result == 0

    def test_boundary_end(self, sample_segments):
        """세그먼트 끝 경계"""
        result = find_segment_for_timestamp(180.0, sample_segments)
        assert result == 2

    def test_not_found(self, sample_segments):
        """세그먼트에 없는 타임스탬프"""
        result = find_segment_for_timestamp(200.0, sample_segments)
        assert result is None

    def test_empty_segments(self):
        """빈 세그먼트 리스트"""
        result = find_segment_for_timestamp(30.0, [])
        assert result is None
