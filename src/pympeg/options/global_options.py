from pympeg.interfaces import Options
from pympeg.utils.validation import validate_choices


class GlobalOptions(Options):

    OVERWRITE_VALUES = {True, False}
    HIDE_BANNER_VALUES = {True}
    LOGLEVEL_VALUES = {
        'quiet', 'panic', 'fatal', 'error', 'warning', 
        'info', 'verbose', 'debug', 'trace'
    }
    STATS_VALUES = {True, False}


    def __init__(
        self,
        overwrite: bool | None = None,
        hide_banner: bool | None = None,
        loglevel: str | None = None,
        stats: bool | None = None
    ) -> None:
        self._overwrite: str | None = None
        self._hide_banner: str | None = None
        self._loglevel: str | None = None
        self._stats: str | None = None

        if overwrite is not None: self.overwrite = overwrite
        if hide_banner is not None: self.hide_banner = hide_banner
        if loglevel is not None: self.loglevel = loglevel
        if stats is not None: self.stats = stats


    # ========== PROPERTY: overwrite ==========
    @property
    def overwrite(self) -> bool | None: return self._overwrite

    @overwrite.setter
    @validate_choices(OVERWRITE_VALUES)
    def overwrite(self, value: bool) -> None: self._overwrite = value

    @overwrite.deleter
    def overwrite(self) -> None: self._overwrite = None


    # ========== PROPERTY: hide_banner ==========
    @property
    def hide_banner(self) -> bool | None: return self._hide_banner

    @hide_banner.setter
    @validate_choices(HIDE_BANNER_VALUES)
    def hide_banner(self, value: bool) -> None: self._hide_banner = value

    @hide_banner.deleter
    def hide_banner(self) -> None: self._hide_banner = None


    # ========== PROPERTY: loglevel ==========
    @property
    def loglevel(self) -> str | None: return self._loglevel

    @loglevel.setter
    @validate_choices(LOGLEVEL_VALUES)
    def loglevel(self, value: str) -> None: self._loglevel = value

    @loglevel.deleter
    def loglevel(self) -> None: self._loglevel = None


    # ========== PROPERTY: stats ==========
    @property
    def stats(self) -> bool | None: return self._stats

    @stats.setter
    @validate_choices(STATS_VALUES)
    def stats(self, value: bool) -> None: self._stats = value

    @stats.deleter
    def stats(self) -> None: self._stats = None
    

    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
            args = []

            if self._overwrite is not None:
                args.append('-y' if self._overwrite else '-n')
            
            if self._hide_banner is not None:
                if self._hide_banner: 
                    args.append('-hide_banner')

            if self._loglevel is not None:
                args.extend(['-loglevel', self._loglevel])

            if self._stats is not None:
                args.append('-stats' if self._stats else '-nostats')

            return args
