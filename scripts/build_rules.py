import esmre
import re


parser = re.compile(r"(?P<rec>\w+) <- (?P<prefix>\w+) \((?P<support>\w+), (?P<confidence>\w+)")

with open("../data/gen_result.dat", "r") as f:
    for _l in f:
        line = _l.strip()

        print i