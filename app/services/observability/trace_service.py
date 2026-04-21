class TraceService:
    def log(self, event: str, data: dict | None = None) -> None:
        payload = data or {}
        print(f"[LYRA TRACE] {event} -> {payload}")