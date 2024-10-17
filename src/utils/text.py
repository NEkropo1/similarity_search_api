def parse_bool(value: str | None, default: bool = False) -> bool:
    """Parse boolean-like environment variables safely."""
    if value is None:
        return default
    return value.lower() in {"true", "1", "yes"}
