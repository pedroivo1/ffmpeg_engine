from pympeg.interfaces import Options


class GlobalOptions(Options):

    OVERWRITE_VALUES = {"no", "yes"}
    LOGLEVEL_VALUES = {
        "quiet", "panic", "fatal", "error", "warning", 
        "info", "verbose", "debug", "trace"
    }
    BOOLEAN_VALUES = {"yes", "no"}


    def __init__(
        self,
        overwrite: str | None = None,
        hide_banner: str | None = None,
        loglevel: str | None = None,
        stats: str | None = None,
    ) -> None:
        self._overwrite: str | None = None
        self._hide_banner: str | None = None
        self._loglevel: str | None = None
        self._stats: str | None = None

        if overwrite is not None:
            self.overwrite = overwrite
        if hide_banner is not None:
            self.hide_banner = hide_banner
        if loglevel is not None:
            self.loglevel = loglevel
        if stats is not None:
            self.stats = stats


    @property
    def overwrite(self) -> str | None:
        return self._overwrite
    
    @overwrite.setter
    @Options.valida_lista(BOOLEAN_VALUES)
    def overwrite(self, value) -> None:
        self._overwrite = value

    @overwrite.deleter
    def overwrite(self) -> None:
        self._overwrite = None

    @property
    def hide_banner(self) -> str | None:
        return self._hide_banner
    
    @hide_banner.setter
    @Options.valida_lista({'yes'})
    def hide_banner(self, value: str) -> None:
        self._hide_banner = value

    @hide_banner.deleter
    def hide_banner(self) -> None:
        self._hide_banner = None

    @property
    def loglevel(self) -> str | None:
        return self._loglevel
    
    @loglevel.setter
    @Options.valida_lista(LOGLEVEL_VALUES)
    def loglevel(self, value: str) -> None:
        self._loglevel = value

    @loglevel.deleter
    def loglevel(self) -> None:
        self._loglevel = None
    
    @property
    def stats(self) -> str | None:
        return self._stats

    @stats.setter
    @Options.valida_lista(BOOLEAN_VALUES)
    def stats(self, value: str) -> None:
        self._stats = value

    @stats.deleter
    def stats(self) -> None:
        self._stats = None

    def generate_command_args(self) -> list:
        args = []

        if self._overwrite is not None:
            args.append("-y" if self._overwrite == "yes" else "-n")

        if self._hide_banner is not None:
            args.append("-hide_banner")

        if self._loglevel is not None:
            args.extend(["-loglevel", self._loglevel])

        if self._stats is not None:
            args.append("-stats" if self._stats == "yes" else "-nostats")

        return args
