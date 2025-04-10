def calculate_progress_rate(completed_goal: int, total_goal: int) -> float:
    """
    완료 목표 수와 전체 목표 수를 기반으로 진행률을 계산
    예: 7 / 10 → 70.00%
    """
    if total_goal == 0:
        return 0.00
    return round((completed_goal / total_goal) * 100, 2)
