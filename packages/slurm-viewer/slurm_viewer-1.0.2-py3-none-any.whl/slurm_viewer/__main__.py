# pylint: disable=wrong-import-position
import rich.traceback

print("Slurm viewer starting")
from slurm_viewer.app import SlurmViewer
# pylint: enable=wrong-import-position


def main() -> None:
    rich.traceback.install(width=200)
    SlurmViewer().run()


if __name__ == "__main__":
    main()
