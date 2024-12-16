# ./givemecontext/automations/format_check_test.py

import os
from pathlib import Path

from givemecontext.config import LOG_DIR_NAME, get_log_file_path, get_logs_dir
from givemecontext.utils.shell_script_runner import ShellScriptRunner


class CodeQualityAutomation:
    """
    Runs code quality checks using black, ruff, and pytest.
    Handles path validation and provides proper error handling.
    """

    @staticmethod
    def _ensure_valid_check_path(check_path: Path | str) -> Path:
        """
        Ensure we have a valid path for checking.

        Args:
            check_path: Path to validate

        Returns:
            Path: A valid Path object, falling back to current directory if needed

        Raises:
            ValueError: If the path is invalid and current directory fallback fails
        """
        try:
            path = Path(check_path).resolve()
            if not path.exists():
                # Fall back to current working directory if path doesn't exist
                print(
                    f"Warning: Path {path} does not exist, falling back to current directory"
                )
                path = Path(os.getcwd())
                if not path.exists():
                    raise ValueError(
                        f"Neither the provided path {check_path} nor the current directory exist"
                    )
            return path
        except Exception as e:
            print(f"Error resolving path {check_path}: {e}")
            current_dir = Path(os.getcwd())
            if not current_dir.exists():
                raise ValueError("Unable to find a valid path for code quality checks")
            return current_dir

    @staticmethod
    def run_with_log(check_path: Path | str) -> None:
        """
        Run code quality checks and log the output.

        Args:
            check_path: Path to run checks on

        Raises:
            FileNotFoundError: If the format check script cannot be found
            PermissionError: If the script cannot be made executable
            subprocess.CalledProcessError: If any of the quality checks fail
            IOError: If log files cannot be written
        """
        # Ensure we have a valid check path
        check_path = CodeQualityAutomation._ensure_valid_check_path(check_path)
        print(f"Running code quality checks on path: {check_path}")

        # Get the script path relative to this file
        script_dir = Path(__file__).parent
        script_path = script_dir / "format_check_test.sh"

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Ensure script is executable
        try:
            script_path.chmod(0o755)
        except Exception as e:
            raise PermissionError(f"Failed to make script executable: {e}")

        # Set up environment variables
        log_file = get_log_file_path("format_check_test_output.log")
        logs_dir = get_logs_dir()

        env_vars = {
            "GIVEMECONTEXT_LOG_FILE": log_file,
            "GIVEMECONTEXT_LOG_DIR": str(logs_dir),
            "GIVEMECONTEXT_LOG_DIR_NAME": LOG_DIR_NAME,
            "PYTHONPATH": os.getenv("PYTHONPATH", ""),
            "CHECK_PATH": str(check_path),  # Add CHECK_PATH to environment
        }

        # Initialize and run the shell script
        try:
            runner = ShellScriptRunner(str(script_path), env_vars=env_vars)
            runner.run_with_log(log_file=log_file, args=[str(check_path)])
        except Exception as e:
            print(f"Error running code quality checks: {e}")
            raise
