from abc import ABC, abstractmethod
import os
from pathlib import Path
import tempfile
import logging
from typing import Sequence

from .result import Result


class Command(ABC):
    """
    Abstract base class for command execution.

    Attributes:
        _name (str): The name of the command.
    """

    def __init__(self, name: str):
        """
        Initializes the Command with a name.

        Args:
            name (str): The name of the command.
        """
        self._name: str = name

    @property
    def name(self) -> str:
        """Returns the name of the command."""
        return self._name

    @abstractmethod
    def build(self) -> Sequence[str]:
        """Builds the command and returns a list of strings."""
        pass

    @abstractmethod
    def _validate_stdout(self, stdout: str) -> Result:
        """Validates the standard output of the command.

        Args:
            stdout (str): The standard output to validate.

        Returns:
            Result: The result of the validation.
        """
        pass

    @abstractmethod
    def _validate_stderr(self, error: str, stderr: str) -> Result:
        """Validates the standard error output of the command.

        Args:
            error (str): The error message.
            stderr (str): The standard error output to validate.

        Returns:
            Result: The result of the validation.
        """
        pass

    @abstractmethod
    def post_process(self, stdout: str, temp_dir: Path, result: Result) -> Result:
        """Processes the result after command execution.

        Args:
            temp_folder (Path): The temporary folder used during execution.
            result (Result): The result of the command execution.

        Returns:
            Result: The processed result.
        """
        pass

    def validate(self, stdout: str, stderr: str, exit_code: int | None) -> Result:
        """Validates the command execution results based on exit code.

        Args:
            stdout (str): The standard output of the command.
            stderr (str): The standard error output of the command.
            exit_code (int | None): The exit code of the command.

        Returns:
            Result: The result of the validation.
        """
        match exit_code:
            case None:
                return self._validate_stderr("Process was terminated without a return code", stderr)
            case 0:
                return self._validate_stdout(stdout)
            case 1:
                return self._validate_stderr("General error occurred during conversion", stderr)
            case 2:
                return self._validate_stderr("Misuse of shell builtins", stderr)
            case 3:
                return self._validate_stderr("Python error occurred", stderr)
            case 126:
                return self._validate_stderr("Command cannot be executed", stderr)
            case 127:
                return self._validate_stderr("Command not found", stderr)
            case 128:
                return self._validate_stderr("Invalid argument to exit", stderr)
            case n if n > 128:
                signal = n - 128
                return self._validate_stderr(f"Fatal error signal {signal}", stderr)
            case _:
                return self._validate_stderr(f"Unknown error occurred (return code: {exit_code})", stderr)

    def _find_files(self, folder: Path, extension: str) -> list[Path]:
        """Finds all files in a folder with a specific extension.

        Args:
            folder (Path): The folder to search in.
            extension (str): The file extension to look for.

        Returns:
            list[Path]: A list of file paths that match the extension.
        """
        file_paths: list[Path] = []
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.endswith(extension):
                    file_paths.append(Path(root) / filename)
        return file_paths

    def _find_file(self, name: str, folder: Path, extension: str) -> Path | None:
        """Finds a specific file by name in a folder with a specific extension.

        Args:
            name (str): The name of the file to find.
            folder (Path): The folder to search in.
            extension (str): The file extension to look for.

        Returns:
            Path | None: The path of the found file or None if not found.
        """
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.endswith(extension) and filename == name:
                    return Path(root) / filename
        return None


class BatCommand(Command):
    """
    Class for executing batch commands.

    Attributes:
        _script (str): The script to be executed.
        _temp_file_name (str | None): The name of the temporary file created.
    """

    def __init__(self, name: str, script: str):
        """
        Initializes the BatCommand with a name and script.

        Args:
            name (str): The name of the command.
            script (str): The batch script to execute.
        """
        super().__init__(name)
        self._script: str = script
        self._temp_file_name: str | None = None

    def dispose(self):
        """Cleans up the temporary file created for the batch command."""
        if self._temp_file_name:
            try:
                os.remove(self._temp_file_name)
            except OSError as e:
                logging.error(f"Error removing temporary file {self._temp_file_name}: {e}")

    def build(self) -> Sequence[str]:
        """Builds the batch command and returns the path to the temporary file.

        Returns:
            StrList: A list containing the path to the temporary batch file.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".bat") as batch_file:
            batch_file.write(self._script)
            self._temp_file_name = batch_file.name
        return [batch_file.name]
