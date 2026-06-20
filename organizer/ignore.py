import fnmatch
from pathlib import Path


class Ignorer:
    """Decides which files and directories to skip during scanning.

    Rules come from config (`ignore.names`, `ignore.patterns`) and may be
    augmented at the CLI. `include_hidden=True` disables the implicit
    dotfile rule so users can still organize hidden files on demand.
    """

    def __init__(
        self,
        names: list[str] | None = None,
        patterns: list[str] | None = None,
        include_hidden: bool = False,
    ):
        self.names = set(names or [])
        self.patterns = list(patterns or [])
        self.include_hidden = include_hidden

    @classmethod
    def from_config(
        cls,
        config: dict,
        extra_patterns: list[str] | None = None,
        include_hidden: bool = False,
    ) -> "Ignorer":
        section = config.get("ignore") or {}
        patterns = list(section.get("patterns") or [])
        if extra_patterns:
            patterns.extend(extra_patterns)
        return cls(
            names=section.get("names"),
            patterns=patterns,
            include_hidden=include_hidden,
        )

    def should_skip_dir(self, path: Path) -> bool:
        return self._match(path.name)

    def should_skip_file(self, path: Path) -> bool:
        return self._match(path.name)

    def _match(self, name: str) -> bool:
        if not self.include_hidden and name.startswith("."):
            return True
        if name in self.names:
            return True
        return any(fnmatch.fnmatch(name, pat) for pat in self.patterns)
