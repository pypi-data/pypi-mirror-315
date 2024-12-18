# Zurich Instruments QCoDeS driver (zhinst-qcodes) Examples

This directory contains the examples for zhinst-qcodes.

We use [jupytext](https://github.com/mwouts/jupytext) to version control our
examples. Meaning that all our examples are uploaded in markdown, although they
where written in jupyter notebooks. To convert a example back into a notebook
simply do:

```
jupytext --to ipynb examples/hf2.md
```

We`ve also a skript called [generate_notebooks.sh](generate_notebooks.sh) that
automatically syncs/creates the notebooks.
