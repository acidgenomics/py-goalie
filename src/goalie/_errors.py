"""Exception classes to raise on a failed check."""


class CheckError(Exception):
    """A goalie check failed.

    Parameters
    ----------
    value : object
        Value that failed the check.
    expected : str
        Noun phrase describing what was expected, such as
        ``"a non-empty string"``.
    name : str | None
        Name of the argument or variable that holds ``value``.

    Examples
    --------
    >>> str(CheckError(1, "a string"))
    'Expected a string, got 1.'
    >>> str(CheckError(1, "a string", name="prefix"))
    'prefix must be a string, got 1.'
    """

    def __init__(self, value: object, expected: str, name: str | None = None) -> None:
        self.value = value
        self.expected = expected
        self.name = name
        if name is None:
            msg = f"Expected {expected}, got {value!r}."
        else:
            msg = f"{name} must be {expected}, got {value!r}."
        super().__init__(msg)

    def __reduce__(self) -> tuple[type["CheckError"], tuple[object, str, str | None]]:
        """Support pickling across process boundaries.

        ``BaseException`` reconstructs itself from ``args`` by default, but
        ``args`` here holds only the formatted message, not the constructor
        arguments. Without this, a re-raise across a ``multiprocessing`` or
        ``concurrent.futures`` boundary fails.

        Returns
        -------
        tuple
            Class plus constructor arguments, per the pickle protocol.
        """
        return (type(self), (self.value, self.expected, self.name))


class CheckTypeError(CheckError, TypeError):
    """A value has the wrong type.

    Examples
    --------
    >>> try:
    ...     raise CheckTypeError(1, "a string", name="prefix")
    ... except TypeError as e:
    ...     str(e)
    'prefix must be a string, got 1.'
    """


class CheckValueError(CheckError, ValueError):
    """A value has the right type but an unacceptable value.

    Examples
    --------
    >>> try:
    ...     raise CheckValueError("red", "a hex color code", name="color")
    ... except ValueError as e:
    ...     str(e)
    "color must be a hex color code, got 'red'."
    """
