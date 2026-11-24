#!/usr/bin/env python3
"""
Base calculator for converting integers between binary, octal, decimal, and hexadecimal,
and evaluating simple bitwise operations.

Usage examples:
    $ python basecalc.py convert 0xff --to dec
    255

    $ python basecalc.py op and 12 10
    dec: 8
    hex: 0x8
    bin: 0b1000
"""

import argparse
import sys


BASES = {'bin': 2, 'oct': 8, 'dec': 10, 'hex': 16}


def parse_value(value_str, from_base=None):
    """Parse a value string with optional prefix/suffix into an integer.

    When from_base ('bin'/'oct'/'dec'/'hex') is given it wins; a matching
    0b/0o/0x prefix is still stripped before parsing.
    """
    value_str = value_str.strip()
    if not value_str:
        raise ValueError("Empty value")

    sign = 1
    if value_str.startswith('-'):
        sign = -1
        value_str = value_str[1:]
    elif value_str.startswith('+'):
        value_str = value_str[1:]

    if from_base is not None:
        num_str = value_str
        for prefix in ('0b', '0o', '0x'):
            if num_str.lower().startswith(prefix):
                num_str = num_str[2:]
                break
        base = BASES[from_base]
        if not num_str:
            raise ValueError(f"Empty number in {value_str}")
        try:
            return sign * int(num_str, base)
        except ValueError as e:
            raise ValueError(f"Invalid {base}-digit value: {value_str}") from e

    if value_str.startswith('0b') or value_str.endswith('b'):
        if value_str.startswith('0b'):
            num_str = value_str[2:]
        else:
            num_str = value_str[:-1]
        base = 2
    elif value_str.startswith('0o') or value_str.endswith('o'):
        if value_str.startswith('0o'):
            num_str = value_str[2:]
        else:
            num_str = value_str[:-1]
        base = 8
    elif value_str.startswith('0x') or value_str.endswith('h'):
        if value_str.startswith('0x'):
            num_str = value_str[2:]
        else:
            num_str = value_str[:-1]
        base = 16
    else:
        num_str = value_str
        base = 10
    
    if not num_str:
        raise ValueError(f"Empty number in {value_str}")
    
    try:
        return sign * int(num_str, base)
    except ValueError as e:
        raise ValueError(f"Invalid {base}-digit value: {value_str}") from e


def format_value(value, base):
    """Format an integer value for the specified base."""
    if base == 'bin':
        return bin(value)
    elif base == 'oct':
        return oct(value)
    elif base == 'hex':
        return hex(value)
    elif base == 'dec':
        return str(value)
    else:
        raise ValueError(f"Unknown base: {base}")


def cmd_convert(args):
    """Handle the convert subcommand."""
    try:
        value = parse_value(args.value, args.from_base)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    to_base = args.to_base if args.to_base else 'hex'
    
    try:
        result = format_value(value, to_base)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_op(args):
    """Handle the op subcommand."""
    try:
        a = parse_value(args.a)
        b = parse_value(args.b)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    
    if a < 0 or b < 0:
        print("Error: Negative operands not allowed", file=sys.stderr)
        sys.exit(2)
    
    op_name = args.operation.lower()
    
    if op_name == 'and':
        result = a & b
    elif op_name == 'or':
        result = a | b
    elif op_name == 'xor':
        result = a ^ b
    elif op_name == 'shl':
        result = a << b
    elif op_name == 'shr':
        result = a >> b
    else:
        print(f"Error: Unknown operation: {op_name}", file=sys.stderr)
        sys.exit(2)
    
    print(f"dec: {result}")
    print(f"hex: {hex(result)}")
    print(f"bin: {bin(result)}")


def main():
    parser = argparse.ArgumentParser(
        description='Base calculator for converting integers and evaluating bitwise operations.'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert subcommand
    convert_parser = subparsers.add_parser('convert', help='Convert between bases')
    convert_parser.add_argument('value', help='Value to convert (with optional prefix/suffix)')
    convert_parser.add_argument('--from', dest='from_base', choices=['bin', 'oct', 'dec', 'hex'],
                                help='Source base')
    convert_parser.add_argument('--to', dest='to_base', choices=['bin', 'oct', 'dec', 'hex'],
                                help='Target base (default: hex)')
    convert_parser.set_defaults(func=cmd_convert)
    
    # Op subcommand
    op_parser = subparsers.add_parser('op', help='Evaluate bitwise operations')
    op_parser.add_argument('operation', choices=['and', 'or', 'xor', 'shl', 'shr'],
                           help='Bitwise operation to perform')
    op_parser.add_argument('a', help='First operand')
    op_parser.add_argument('b', help='Second operand (or shift count for shl/shr)')
    op_parser.set_defaults(func=cmd_op)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
