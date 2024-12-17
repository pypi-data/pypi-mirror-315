def urljoin(*args: str) -> str:
    from urllib.parse import urljoin

    if not args:
        return ""

    if len(args) == 1:
        return args[0]
    base = args[0]
    for part in args[1:]:
        if base:
            base = base.rstrip("/") + "/"
            part = part.lstrip("/")
        base = urljoin(base, part)

    return base
