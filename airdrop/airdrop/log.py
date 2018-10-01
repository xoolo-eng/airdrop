import syslog
from datetime import datetime


class Log(object):
    """docstring for Log"""
    use_syslog = False

    def __init__(self, path_file=None, syslog_facility=None):
        if syslog_facility:
            facility = None
            if syslog_facility == "LOG_LOCAL0":
                facility = syslog.LOG_LOCAL0
            elif syslog_facility == "LOG_LOCAL1":
                facility = syslog.LOG_LOCAL1
            elif syslog_facility == "LOG_LOCAL2":
                facility = syslog.LOG_LOCAL2
            elif syslog_facility == "LOG_LOCAL3":
                facility = syslog.LOG_LOCAL3
            elif syslog_facility == "LOG_LOCAL4":
                facility = syslog.LOG_LOCAL4
            elif syslog_facility == "LOG_LOCAL5":
                facility = syslog.LOG_LOCAL5
            elif syslog_facility == "LOG_LOCAL6":
                facility = syslog.LOG_LOCAL6
            elif syslog_facility == "LOG_LOCAL7":
                facility = syslog.LOG_LOCAL7
            else:
                raise ValueError("log.py:30. Error syslog Facilities.")
            syslog.openlog(
                ident="AIRDROP",
                logoption=syslog.LOG_PID,
                facility=facility
            )
            self.use_syslog = True
        elif path_file:
            self.log_file = open(path_file, "a")
        else:
            raise ValueError("log.py:40. The log file is not defined.")

    def emerg(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_EMERG,
                " [EMERG]   {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [EMERG]   {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def alert(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_ALERT,
                " [ALERT]   {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [ALERT]   {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def crit(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_CRIT,
                " [CRIT]    {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [CRIT]    {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def err(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_ERR,
                " [ERR]     {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [ERR]     {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def warning(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_WARNING,
                " [WARNING] {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [WARNING] {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def notice(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_NOTICE,
                " [NOTICE]  {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [NOTICE]  {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def info(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_INFO,
                " [INFO]    {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [INFO]    {1}\n".format(
                    datetime.today(),
                    message
                )
            )

    def debug(self, message):
        if self.use_syslog:
            syslog.syslog(
                syslog.LOG_DEBUG,
                " [DEBUG]   {}".format(message)
            )
        else:
            self.log_file.write(
                "{0}: [DEBUG]   {1}\n".format(
                    datetime.today(),
                    message
                )
            )


# LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, LOG_NOTICE, LOG_INFO, LOG_DEBUG
# EMERG, ALERT, CRIT, ERR, WARNING, NOTICE, INFO, DEBUG
# emerg, alert, crit, err, warning, notice, info, debug
