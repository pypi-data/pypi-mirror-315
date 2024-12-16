[![CI Status](https://github.com/gguan/qtrade/actions/workflows/ci.yml/badge.svg)](https://github.com/gguan/qtrade/actions)
[![Python](https://img.shields.io/pypi/pyversions/qtrade.svg)](https://badge.fury.io/py/qtrade)
[![PyPI version](https://badge.fury.io/py/qtrade.svg)](https://badge.fury.io/py/qtrade)
![Coverage](https://img.shields.io/badge/coverage-97%25-green)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# QTrade

A Python library for backtesting trading strategies and applying reinforcement learning to trading.

## Features

- Backtesting engine
- Market data components
- Trading environment simulation
- Strategy development tools

## Installation

### From Source

```bash
git clone https://github.com/yourusername/qtrade.git
cd qtrade
pip install -e .
```

### Run Example

Run strategy backtest example

```bash
python examples/simply_strategy.py
```

Run reinforcement learning example

```bash
python examples/rl_example.py
```

### Requirements

- Python >= 3.7
- Dependencies listed in requirements.txt

## Project Structure

```
qtrade/
├── qtrade/              # Main package
│   ├── backtest/       # Backtesting engine
│   ├── components/     # Trading components
│   └── env/           # Trading environment
├── tests/              # Unit tests
├── examples/           # Example scripts
└── docs/              # Documentation
```

## Usage

Basic example:

```python
from qtrade import Backtest
from qtrade.components import Strategy

# Your trading logic here
```

## Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.