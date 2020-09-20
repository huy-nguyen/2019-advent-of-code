These are my solutions in Python to [Advent of Code 2019](https://adventofcode.com/2019), a series of daily programming puzzles.
[MyPy](https://mypy.readthedocs.io/en/latest/index.html) is used for static typechecking and [pytest](https://docs.pytest.org/en/latest/) is used for unit testing.
This project also uses VS Code's [Remote Container Development extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) so you can have the exact same setup as I do by
- Install the extension,
- Hit F1, choose "Open Folder in Container..." and open the project root directory.

Once you're in the Dev Container, to get all the tests, hit F1 and choose "Python: Discover Tests" so that `pytest` will scan all files for unit tests and list them in the Side Bar's Test View.
From there you can run individual test or all tests if you want.
See the [docs](https://code.visualstudio.com/docs/python/testing) for more details.
Note that because the puzzle inputs (and hence expected outputs) are different for each participant, I've commented out tests that use my inputs.
