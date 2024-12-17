from .cli.cli import init


try:
    get_ipython
    init()
except NameError:
    pass
