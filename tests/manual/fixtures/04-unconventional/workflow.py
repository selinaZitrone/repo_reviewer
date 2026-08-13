"""Non-executed fixture using embedded synthetic values."""

VALUES = [0.20, 0.25, 0.23]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


if __name__ == "__main__":
    print(mean(VALUES))
