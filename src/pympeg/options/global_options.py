from pympeg.interfaces import Options


class GlobalOptions(Options):
    def __init__(
        self,
        overwrite: str | None = None,
        hide_banner: str | None = None,
        loglevel: str | None = None,
        stats: str | None = None,
    ) -> None:
        self.overwrite = overwrite
        self.hide_banner = hide_banner
        self.loglevel = loglevel
        self.stats = stats

    def generate_command_args(self) -> list:
        args = []

        if self.overwrite is not None:
            overwrite_map = {"no": "-n", "yes": "-y"}
            if self.overwrite in overwrite_map:
                args.append(overwrite_map[self.overwrite])
            else:
                self._log_invalid_value("overwrite", self.overwrite)

        if self.hide_banner is not None:
            if self.hide_banner == "yes":
                args.append("-hide_banner")
            else:
                self._log_invalid_value("hide_banner", self.hide_banner)

        if self.loglevel is not None:
            valid_levels = {
                "quiet",
                "panic",
                "fatal",
                "error",
                "warning",
                "info",
                "verbose",
                "debug",
                "trace",
            }
            if self.loglevel in valid_levels:
                args.extend(["-loglevel", self.loglevel])
            else:
                self._log_invalid_value("loglevel", self.loglevel)

        if self.stats is not None:
            stats_map = {"yes": "-stats", "no": "-nostats"}
            if self.stats in stats_map:
                args.append(stats_map[self.stats])
            else:
                self._log_invalid_value("stats", self.stats)

        return args
