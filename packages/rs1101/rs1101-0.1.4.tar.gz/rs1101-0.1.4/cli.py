import rs1101.random_string as rs
import argparse


def add_length(parser):
    parser.add_argument(
        "-l",
        "--length",
        help="length of the generated random string.",
        type=int,
        default=10,
    )


def add_candidate(parser):
    parser.add_argument(
        "-c",
        "--candidate",
        help="""candidate characters,
        u for uppercase,
        l for lowercase,
        d for digist,
        p for punctuation,
        h[H] for hex
        a for all printable.""",
        choices=rs.candidate_dict.keys(),
        nargs="+",
        action="extend",
    )


def add_strength(parser):
    parser.add_argument(
        "-s",
        "--strength",
        help="evaluate the strength of an random string.",
        action="store_true",
    )


def cli_rs2int():
    parser = argparse.ArgumentParser(
        description="""Convert a random string to an integer."""
    )
    parser.add_argument("rs", help="a random string.")
    # add_length(parser)
    add_candidate(parser)
    add_strength(parser)
    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = rs.candidate_default
    # PART generate candidate
    candidate = rs.g_candidate(args.candidate)

    output = []
    # PART rs2int
    x = rs.rs2int(args.rs)
    output.append(f"{x}")

    # PART strength
    if args.strength:
        output.append(f"strength:{rs.strength(args.length,len(candidate))}")

    print("\n".join(output))


def cli_int2rs():
    parser = argparse.ArgumentParser(
        description="""Convert an integer to a random string."""
    )
    parser.add_argument("x", help="integer.", type=int)
    # add_length(parser)
    add_candidate(parser)
    add_strength(parser)
    add_length(parser)
    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = rs.candidate_default
    # PART generate candidate
    candidate = rs.g_candidate(args.candidate)

    output = []
    # PART int2rs
    s = rs.int2rs(args.x, length=args.length)
    output.append(f"{s}")

    # PART strength
    if args.strength:
        output.append(f"strength:{rs.strength(args.length,len(candidate))}")

    print("\n".join(output))


def cli_rs():
    parser = argparse.ArgumentParser(description="""generate a secret random string.""")
    add_length(parser)
    add_candidate(parser)
    add_strength(parser)

    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = rs.candidate_default

    # PART generate candidate
    candidate = rs.g_candidate(args.candidate)

    # PART generate an random string
    output = []
    s = rs.random_string(args.length, candidate)
    output.append(f"{s}")

    # PART strengt
    if args.strength:
        output.append(f"strength:{rs.strength(args.length,len(candidate))}")

    print("\n".join(output))
