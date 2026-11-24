# basecalc

Convert integers between binary, octal, decimal, and hexadecimal, and evaluate simple bitwise operations, without opening a full programming shell. For programmers, students, and anyone who reads values in more than one base.

## Quickstart

```
python3 basecalc.py --help
python3 basecalc.py convert 0xff --to dec
```

## Usage

```
usage: basecalc.py [-h] {convert,op} ...

  convert VALUE [--from {bin,oct,dec,hex}] [--to {bin,oct,dec,hex}]
      VALUE may carry a prefix (0b, 0o, 0x) or a suffix letter (b, o, d, h);
      --from wins when both are present. --to defaults to hex. Output is
      printed bare, with a 0b/0o/0x prefix for non-decimal bases.
  op {and,or,xor,shl,shr} A B
      Prints the result in dec, hex, and bin. For shl/shr, B is the shift
      count. Negative operands are rejected.
```

## Examples

```
$ python3 basecalc.py convert 0xff --to dec
255

$ python3 basecalc.py convert 255 --to bin
0b11111111

$ python3 basecalc.py convert -255 --to hex
-0xff

$ python3 basecalc.py op and 12 10
dec: 8
hex: 0x8
bin: 0b1000

$ python3 basecalc.py op shl 1 8
dec: 256
hex: 0x100
bin: 0b100000000
```

## Configuration

None — all options are command-line flags.

## Limitations

Integers only — no fractions, no floating point, no expressions. Bitwise operations accept non-negative operands only. Python integers are arbitrary precision, so very large values work, but output is not grouped or padded.

## License

MIT — see `LICENSE`.

By Dr. Brent Allen Jensen, Radical Blueprinting Research.

## Support this work

If this tool saved you time, you can support more open work like it:

- **BTC:** `15McijPo79Zx58NGyEf2PvaPtGqGmpztWn`
- **ETH:** `0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B`

Thank you.
