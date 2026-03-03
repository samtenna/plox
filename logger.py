class Logger:
    def __init__(self) -> None:
        pass

    @staticmethod
    def error(line: int, message: str):
        Logger.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
