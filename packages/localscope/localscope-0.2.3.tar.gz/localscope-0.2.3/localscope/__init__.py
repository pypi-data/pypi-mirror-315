import builtins
import dis
import functools as ft
import inspect
import logging
import textwrap
import types
from typing import Any, Callable, Dict, Iterable, Optional, Set, Union


LOGGER = logging.getLogger(__name__)


def localscope(
    func: Optional[Union[types.FunctionType, types.CodeType]] = None,
    *,
    predicate: Optional[Callable] = None,
    allowed: Optional[Union[Iterable[str], str]] = None,
    allow_closure: bool = False,
):
    """
    Restrict the scope of a callable to local variables to avoid unintentional
    information ingress.

    Args:
        func : Callable whose scope to restrict.
        predicate : Predicate to determine whether a global variable is allowed in the
            scope. Defaults to allow any module.
        allowed: Names of globals that are allowed to enter the scope.
        allow_closure: Allow access to non-local variables from the enclosing scope.

    Attributes:
        mfc: Decorator allowing *m*\\ odules, *f*\\ unctions, and *c*\\ lasses to enter
            the local scope.

    Examples:

        Basic example demonstrating the functionality of localscope.

        >>> a = 'hello world'
        >>> @localscope
        ... def print_a():
        ...     print(a)
        Traceback (most recent call last):
        ...
        localscope.LocalscopeException: `a` is not a permitted global (file "...",
            line 1, in print_a)

        The scope of a function can be extended by providing an iterable of allowed
        variable names or a string of space-separated allowed variable names.

        >>> a = 'hello world'
        >>> @localscope(allowed=['a'])
        ... def print_a():
        ...     print(a)
        >>> print_a()
        hello world

        The predicate keyword argument can be used to control which `values` are allowed
        to enter the scope (by default, only modules may be used in functions).

        >>> a = 'hello world'
        >>> allow_strings = localscope(predicate=lambda x: isinstance(x, str))
        >>> @allow_strings
        ... def print_a():
        ...     print(a)
        >>> print_a()
        hello world

        Localscope is strict by default, but :code:`localscope.mfc` can be used to allow
        modules, functions, and classes to enter the function scope: a common use case
        in notebooks.

        >>> class MyClass:
        ...     pass
        >>> @localscope.mfc
        ... def create_instance():
        ...     return MyClass()
        >>> create_instance()
        <MyClass object at 0x...>

    Notes:

        The localscope decorator analyses the decorated function (and any dependent code
        blocks) at the time of declaration because static analysis has a minimal impact
        on performance and it is easier to implement.
    """
    # Set defaults and construct partial if the callable has not yet been provided for
    # parameterized decorators, e.g., @localscope(allowed={"foo", "bar"}). This is a
    # thin wrapper around the actual implementation `_localscope`. The wrapper
    # reconstructs an informative traceback.
    if isinstance(allowed, str):
        allowed = allowed.split()
    allowed = set(allowed) if allowed else set()
    predicate = predicate or inspect.ismodule
    if not func:
        return ft.partial(
            localscope,
            allow_closure=allow_closure,
            allowed=allowed,
            predicate=predicate,
        )

    return _localscope(
        func,
        allow_closure=allow_closure,
        allowed=allowed,
        predicate=predicate,
        _globals={},
    )


class LocalscopeException(RuntimeError):
    """
    Raised when a callable tries to access a non-local variable.
    """

    def __init__(
        self,
        message: str,
        code: types.CodeType,
        instruction: dis.Instruction,
        lineno: Optional[int] = None,
    ) -> None:
        source = None
        lineno = instruction.starts_line if lineno is None else lineno
        if lineno is not None:
            # Add the source code if we can find it.
            try:
                # Get the source, dedent, re-indent, and add a marker where the
                # error occurred.
                lines, start = inspect.getsourcelines(code)
                lines = textwrap.dedent("".join(lines)).split("\n")
                text = "\n".join(
                    f"{no:3}: {line}" for no, line in enumerate(lines, start=start)
                )
                lines = textwrap.indent(text, "    ").split("\n")
                offset = lineno - start
                lines[offset] = "--> " + lines[offset][4:]

                # Don't show all lines of the source.
                lines = lines[max(0, offset - 2) : offset + 3]
                source = "\n".join(lines)
            except OSError:  # pragma: no cover
                pass
        message = (
            f'{message} (file "{code.co_filename}", line {lineno}, in {code.co_name})'
        )
        if source:
            message = f"{message}\n{source}"
        super().__init__(message)


def _localscope(
    func: Union[types.FunctionType, types.CodeType],
    *,
    predicate: Callable,
    allowed: Set[str],
    allow_closure: bool,
    _globals: Dict[str, Any],
):
    """
    Args:
        ...: Same as for the wrapper :func:`localscope`.
        _globals : Globals associated with the root callable which are passed to
            dependent code blocks for analysis.
    """

    # Extract global variables from a function
    # (https://docs.python.org/3/library/types.html#types.FunctionType) or keep the
    # explicitly provided globals for code objects
    # (https://docs.python.org/3/library/types.html#types.CodeType).
    if isinstance(func, types.FunctionType):
        code = func.__code__
        _globals = {**func.__globals__, **inspect.getclosurevars(func).nonlocals}
    else:
        code = func

    # Add function arguments to the list of allowed exceptions. We only take
    # `code.co_argcount + code.co_kwonlyargcount` variables because `code.co_varnames`
    # contains all local variables.
    has_varargs = 1 if code.co_flags & inspect.CO_VARARGS else 0
    allowed.update(
        code.co_varnames[: code.co_argcount + code.co_kwonlyargcount + has_varargs]
    )

    # Construct set of forbidden operations. The first accesses global variables. The
    # second accesses variables from the outer scope.
    forbidden_opnames = {"LOAD_GLOBAL"}
    if not allow_closure:
        forbidden_opnames.add("LOAD_DEREF")

    LOGGER.info("analysing instructions for %s...", func)
    lineno = None
    for instruction in dis.get_instructions(code):
        LOGGER.info(instruction)
        if instruction.starts_line is not None:
            lineno = instruction.starts_line
        name = instruction.argval
        if instruction.opname in forbidden_opnames:
            # Variable explicitly allowed by name or in `builtins`.
            if name in allowed or hasattr(builtins, name):
                continue
            # Complain if the variable is not available.
            if name not in _globals:
                raise LocalscopeException(
                    f"`{name}` is not in globals", code, instruction, lineno
                )
            # Check if variable is allowed by value.
            value = _globals[name]
            if not predicate(value):
                raise LocalscopeException(
                    f"`{name}` is not a permitted global", code, instruction, lineno
                )
        elif instruction.opname == "STORE_DEREF":
            # Store a new allowed variable which has been created in the scope of the
            # function.
            allowed.add(name)

    # Deal with code objects recursively after adding the current arguments to the
    # allowed exceptions
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            _localscope(
                const,
                _globals=_globals,
                allow_closure=True,
                predicate=predicate,
                allowed=allowed,
            )

    return func


def _allow_mfc(x):
    return inspect.ismodule(x) or inspect.isfunction(x) or inspect.isclass(x)


localscope.mfc = localscope(predicate=_allow_mfc)  # type: ignore[attr-defined]
