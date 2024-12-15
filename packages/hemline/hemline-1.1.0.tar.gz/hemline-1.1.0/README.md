This is yet another python library for creating frames around your terminal
output.

It creates a frame around text, wrapping the text to fit into the frame.

The implementation follows clean code principles such as single responsibility
principle, and dependency injection.


# Install

    pip install hemline

# Documentation

See [jnthnhrr.github.io/python-hemline](https://jnthnhrr.github.io/python-hemline)


# Use

```python3
from hemline import Frame

frame = Frame()
text = "This is some text"
framed = frame.format(text)
```

You will find more detailed examples in the documentation.
