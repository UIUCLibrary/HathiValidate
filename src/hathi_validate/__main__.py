"""Bootstrap for running the package as an executable."""

import sys

import hathi_validate.cli


def main() -> None:
    """Entry point for starting the cli scripts."""
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest  # type: ignore
        sys.exit(pytest.main(sys.argv[2:]))
    # elif len(sys.argv) > 1 and "--gui" in sys.argv:
    #     try:
    #         hathi_validate.gui.main()
    #     except ImportError:
    #         print("Feature not currently installed", file=sys.stderr)
    else:
        hathi_validate.cli.main()


if __name__ == '__main__':
    main()
