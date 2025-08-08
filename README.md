# VibeKernel - Jupyter Kernel for Hy

A  Jupyter kernel for the [Hy language](https://hylang.org/) - a Lisp dialect embedded in Python.

**Attention: this was generated from scratch by Claude Code based on very few interactions**, see full log at [full_claude_interaction.txt]. I've verified it works for simple programs across a few cells, **but haven't reviewed the code at all**.

## Features

- Full Hy language support with Python interoperability
- Code execution with proper output handling
- Error reporting with clean tracebacks
- Basic tab completion
- Jupyter notebook integration

## Installation

1. Install the package:
```bash
pip install -e .
```

2. Install the kernel spec:
```bash
install-vibekernel --user
```

3. Start Jupyter:
```bash
jupyter notebook
# or
jupyter lab
```

4. Create a new notebook and select "Hy" as the kernel.

## Usage

You can now write Hy code in Jupyter notebooks:

```hy
;; Basic arithmetic
(+ 1 2 3)

;; Define a function
(defn factorial [n]
  (if (< n 2)
    1
    (* n (factorial (- n 1)))))

;; Use Python libraries
(import sys)
(print sys.version)

;; List comprehensions in Hy style
(list (map (fn [x] (* x x)) (range 10)))
```

## Requirements

- Python 3.8+
- Jupyter
- Hy 1.0.0+
- IPython/ipykernel

## Development

To set up for development:

1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Install kernel spec: `install-vibekernel --user`

## License

MIT License