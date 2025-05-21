import argparse
from ..base_module.base_cli import CLIParser, add_common_cli_args, get_common_cli_args
from .lab8_branch import Lab8Branch, INT_TYPES, DEFAULT_START_LEN, DEFAULT_DEEP


LAB2_DEFAULT_INT_TYPE = "int64"

def create_task_lab8(args) -> Lab8Branch:
    task = Lab8Branch(
        n=args.n,
        deep=args.deep,
        student_id=args.id,
        **get_common_cli_args(args),
    )
    return task

def add_cli_args_lab8(parser: argparse.ArgumentParser):
    add_common_cli_args(parser)
    parser.add_argument('--n', type=int, default=DEFAULT_START_LEN, help="Number of functions")
    parser.add_argument('--deep', type=float, default=DEFAULT_DEEP, help="Main path depth coefficient")
    parser.add_argument("--answer", type=str, default="")
    parser.set_defaults(func=create_task_lab8)

Lab8CLIParser = CLIParser(
    name="lab8_branch",
    add_cli_args=add_cli_args_lab8,
)
