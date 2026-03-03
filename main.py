import argparse

from scanner import Scanner


class PLox:
    def __init__(self):
        self.had_error = False

    def _run_repl(self):
        while True:
            line = input("> ")
            self._run(line)

            self.had_error = False

    def _run_file(self, file_name: str):
        with open(file_name, "r") as f:
            contents = f.read()
            self._run(contents)

        if self.had_error:
            exit(1)

    def _run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)


if __name__ == "__main__":
    interpreter = PLox()
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()

    if not args.file:
        print("Run REPL")
    else:
        print("Running file")
