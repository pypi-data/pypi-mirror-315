import asyncio
from tempfile import TemporaryDirectory
from pathlib import Path
from typing import Sequence, Protocol

from .result import Result


class CommandProtocol(Protocol):
    def build(self) -> Sequence[str]: ...
    def validate(self, stdout: str, stderr: str, exit_code: int | None) -> Result: ...
    def post_process(self, stdout: str, temp_dir: Path, result: Result) -> Result: ...
    def dispose(self): ...

    @property
    def name(self) -> str: ...


CommandSet = dict[str, Sequence[CommandProtocol]]


class Runner:
    """
    A class to execute commands asynchronously and handle their results.
    """

    @staticmethod
    async def execute(command: CommandProtocol, clean: bool = True) -> Result:
        """
        Execute a single command and return the result.

        Args:
            command (CommandProtocol): The command to execute.

        Returns:
            Result: The result of the command execution.
        """
        cmd_list = command.build()

        with TemporaryDirectory(delete=clean) as temp_dir:
            if not cmd_list:
                return Result(name=command.name, success=False, message="Command list is empty")

            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=temp_dir,
            )

            stdoutData, stderrData = await process.communicate()

            stdout = stdoutData.decode("utf-8", errors="ignore")
            stderr = stderrData.decode("utf-8", errors="ignore")

            result = command.validate(stdout, stderr, process.returncode)
            command.dispose()

            if not result.success:
                return result

            return command.post_process(stdout, Path(temp_dir), result)

    @staticmethod
    async def _execute_command(command: CommandProtocol, temp_dir: Path) -> Result:
        """
        Execute a command in a specified temporary directory.

        Args:
            command (CommandProtocol): The command to execute.
            temp_dir (Path): The path to the temporary directory.

        Returns:
            Result: The result of the command execution.
        """
        cmd_list = command.build()

        if not cmd_list:
            return Result(name=command.name, success=False, message="Command list is empty")

        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
        )

        stdoutData, stderrData = await process.communicate()

        stdout = stdoutData.decode("utf-8", errors="ignore")
        stderr = stderrData.decode("utf-8", errors="ignore")

        result = command.validate(stdout, stderr, process.returncode)

        if not result.success:
            return result

        return command.post_process(stdout, Path(temp_dir), result)

    @staticmethod
    async def execute_set(
        commands: CommandSet,
        clean: bool = True,
        wait_time: float = 2,
        batch_size: int = 10,
    ) -> list[Result]:
        """
        Execute a set of commands in batches and return their results.

        Args:
            commands (dict[str, Sequence[CommandProtocol]]): A dictionary where keys are command names
            and values are sequences of commands to execute.
            wait_time (float): Time to wait between command executions in seconds.
            batch_size (int): Number of commands to execute in each batch.

        Returns:
            list[Result]: A list of results from the executed commands.
        """
        results: list[Result] = []
        with TemporaryDirectory(delete=clean) as temp_dir:

            for command_list in commands.values():
                for i in range(0, len(command_list), batch_size):
                    batch = command_list[i : i + batch_size]
                    tasks = [Runner._execute_command(command, Path(temp_dir)) for command in batch]
                    try:
                        results.extend(await asyncio.gather(*tasks))
                    except Exception as e:
                        return [Result(name="Error", success=False, message=str(e))]

                    await asyncio.sleep(wait_time)

        for command in commands.values():
            for cmd in command:
                cmd.dispose()

        return results
