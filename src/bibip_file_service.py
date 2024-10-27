from os import path

ROW_LENGTH = 500


class FileService:
    def __init__(self, root_directory_path: str):
        self.root_directory_path = root_directory_path

    def _format_path(self, filename: str) -> str:
        return path.join(self.root_directory_path, filename)

    def read_file(self, filename: str) -> list[list[str]]:
        if path.exists(self._format_path(filename)):
            split_lines = []
            with open(self._format_path(filename), "r") as f:
                for line in f.readlines():
                    split_line = line.strip().split(",")
                    if split_line[-1] == 'False':
                        split_lines.append(split_line)

                return split_lines
        return []

    def write_file(self,
                   filename: str,
                   position_in_data_file: int,
                   line: str) -> None:
        with open(self._format_path(filename), "r+") as f:
            f.seek(position_in_data_file * (ROW_LENGTH + 2))
            f.write(line.ljust(ROW_LENGTH))

    def rewrite_file(self,
                     filename: str,
                     lines: list[str]) -> None:
        with open(self._format_path(filename), "w") as f:
            for line in lines:
                f.write(line + "\n")

    def get_line_from_file(self,
                           filename: str,
                           position_in_data_file: int) -> list[str] | None:
        if path.exists(self._format_path(filename)):
            with open(self._format_path(filename), "r") as f:
                f.seek(position_in_data_file * (ROW_LENGTH + 2))
                line = f.readline().strip().split(',')
                if line[-1] == 'False':
                    return line
        return None

    def append_file(self, row: str, filename: str) -> None:
        with open(self._format_path(filename), "a") as f:
            f.write(row.ljust(ROW_LENGTH) + '\n')
