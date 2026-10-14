"""Pure URL normalization for GitHub repositories."""

from urllib.parse import urlsplit

_GITHUB_HOSTS = {"github.com", "www.github.com"}


def normalize_github_repository_url(repository_url: str) -> str:
    """Return a canonical GitHub repository URL or raise ``ValueError``.

    Deep links to files, branches and other repository pages all point to the
    same repository.  Network availability is checked separately.
    """
    candidate = repository_url.strip()
    if any(char in candidate for char in "\r\n\t"):
        raise ValueError("GitHub URL contains control characters")

    if "://" not in candidate:
        candidate = "https://" + candidate

    parsed = urlsplit(candidate)
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or parsed.netloc.lower() not in _GITHUB_HOSTS
    ):
        raise ValueError("Not a GitHub repository URL")

    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("GitHub repository URL must contain owner and repo")

    owner, repo = parts[:2]
    if repo.lower().endswith(".git"):
        repo = repo[:-4]

    if not owner or not repo:
        raise ValueError("Invalid GitHub repository owner or name")

    return f"https://github.com/{owner}/{repo}"
