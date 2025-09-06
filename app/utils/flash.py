from fastapi import Request
from typing import List, Dict, Optional

def flash(request: Request, message: str, category: str = "info"):
    """
    Lưu flash message vào session (hiển thị ở request sau).
    """
    flashes: List[Dict[str, str]] = request.session.get("flash", [])
    flashes.append({"message": message, "category": category})
    request.session["flash"] = flashes


def get_flashed_messages(request: Request, with_categories: bool = True) -> List:
    """
    Lấy và xóa flash messages từ session.
    """
    flashes: List[Dict[str, str]] = request.session.pop("flash", [])

    if with_categories:
        return [(msg["category"], msg["message"]) for msg in flashes]
    else:
        return [msg["message"] for msg in flashes]