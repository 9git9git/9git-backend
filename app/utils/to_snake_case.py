import re


def camel_to_snake(text: str) -> str:
    """camelCase를 snake_case로 변환합니다."""

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)

    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
