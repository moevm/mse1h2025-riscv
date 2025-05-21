import argparse
from ..base_module.base_cli import CLIParser, add_common_cli_args, get_common_cli_args
from .lab9_first import Lab9First, INT_TYPES, DEFAULT_START_LEN, DEFAULT_DEEP


LAB9_DEFAULT_INT_TYPE = "int64"

def create_task_lab9(args) -> Lab9First:
    task = Lab9First(
        n=args.n,
        deep=args.deep,
        answer=args.answer,
        interactive=args.interactive_init,
        print_task_when_i=args.print_task_when_interactive,
        **get_common_cli_args(args),
    )
    return task

def add_cli_args_lab9(parser: argparse.ArgumentParser):
    add_common_cli_args(parser)
    parser.add_argument('--n', type=int, default=DEFAULT_START_LEN, help="Number of functions")
    parser.add_argument('--deep', type=float, default=DEFAULT_DEEP, help="Main path depth coefficient")
    parser.add_argument("--answer", type=str, default="")
    parser.add_argument("-i", "--interactive-init", action='store_true')
    parser.add_argument("--print-task-when-interactive", action='store_true')
    parser.set_defaults(func=create_task_lab9)

Lab9CLIParser = CLIParser(
    name="lab9_first",
    add_cli_args=add_cli_args_lab9,
)
