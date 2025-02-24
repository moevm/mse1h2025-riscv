import argparse
from ..base_module.base_cli import CLIParser, add_common_cli_args, get_common_cli_args
from .lab10_test import Lab10Test, INT_TYPES


LAB2_DEFAULT_INT_TYPE = "int64"

def create_task_lab10(args) -> Lab10Test:
    task = Lab10Test(
        a2_class=args.a2, a3_class=args.a3,
        a2_min=args.a2_min, a2_max=args.a2_max,
        a3_min=args.a3_min, a3_max=args.a3_max,
        **get_common_cli_args(args),
    )
    return task

def add_cli_args_lab10(parser: argparse.ArgumentParser):
    add_common_cli_args(parser)
    parser.add_argument('--a2', type=str, choices=INT_TYPES.keys(), default=LAB2_DEFAULT_INT_TYPE)
    parser.add_argument('--a3', type=str, choices=INT_TYPES.keys(), default=LAB2_DEFAULT_INT_TYPE)
    parser.add_argument('--a2-min', type=int)
    parser.add_argument('--a2-max', type=int)
    parser.add_argument('--a3-min', type=int)
    parser.add_argument('--a3-max', type=int)
    parser.set_defaults(func=create_task_lab10)

Lab10CLIParser = CLIParser(
    name="lab10_test",
    add_cli_args=add_cli_args_lab10,
)
