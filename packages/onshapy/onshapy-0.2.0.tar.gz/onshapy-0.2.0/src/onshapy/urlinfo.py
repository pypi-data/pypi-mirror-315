import re


class UrlInfo:
    documentId: str | None = None
    workspaceId: str | None = None
    elementId: str | None = None

    def __init__(self, url: str) -> None:
        match = re.search(r"\/(?:documents|d)\/(\w+)(?:\/|$)", url, re.IGNORECASE)
        if match:
            self.documentId = match.group(1)

        match = re.search(r"\/w\/(\w+)(?:\/|$)", url, re.IGNORECASE)
        if match:
            self.workspaceId = match.group(1)

        match = re.search(r"\/e\/(\w+)(?:\/|$)", url, re.IGNORECASE)
        if match:
            self.elementId = match.group(1)
