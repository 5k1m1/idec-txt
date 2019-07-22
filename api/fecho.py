import os


def read_blacklist():
    return open("fblacklist.txt").read().split()


def fechoarea_count(fechoarea):
    try:
        return len(open(f"fecho/{fechoarea}", "r").read().strip().split("\n"))
    except FileNotFoundError:
        return 0


def read_fechoarea(fechoarea):
    try:
        for line in open(f"fecho/{fechoarea}.idx").read().strip().split("\n"):
            yield [fechoarea, line]
    except FileNotFoundError:
        return []


def save_file(fecho, frow, out):
    file_size = 0
    block_size = 8192
    if not os.path.exists(f"fecho/{fecho}"):
        os.mkdir(f"fecho/{fecho}")
    f = open("fecho/{0}/{1}".format(fecho, frow[1]), "wb")
    while True:
        buffer = out.read(block_size)
        if not buffer:
            break
        file_size += len(buffer)
        f.write(buffer)
    f.close()
    open(f"fecho/{fecho}.idx", "a").write(":".join(frow) + "\n")
