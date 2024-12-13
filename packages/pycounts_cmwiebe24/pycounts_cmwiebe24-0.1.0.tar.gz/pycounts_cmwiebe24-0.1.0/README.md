# pycounts_cmwiebe24

This is a simple package I am developing to teach myself about python package development.

## Installation

```bash
$ pip install pycounts_cmwiebe24
```

## Usage

`pycounts_cmwiebe24` can be used to count words in a text file and plot results
as follows:

```python
from pycounts_cmwiebe24.pycounts_cmwiebe24 import count_words
from pycounts_cmwiebe24.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pycounts_cmwiebe24` was created by Caleb Wiebe. Caleb Wiebe retains all rights to the source and it may not be reproduced, distributed, or used to create derivative works.

## Credits

`pycounts_cmwiebe24` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
