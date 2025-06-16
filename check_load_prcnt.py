#!/usr/bin/env python3

# SEE: https://www.scoutapm.com/blog/understanding-load-averages
# SEE: https://docs.python.org/3/library/os.html#os.getloadavg
# SEE: https://docs.python.org/3/library/os.html#os.cpu_count

import argparse
import os

parser = argparse.ArgumentParser(
    prog='check_load_prcnt',
    description='Check CPU load with percentage values',
    epilog='License MIT. Copyright Michaelshof Gem gGmbH.'
)
parser.add_argument("--wload1", type=int, required=True, help="Warning for load1 in percent")
parser.add_argument("--wload5", type=int, required=True, help="Warning for load5 in percent")
parser.add_argument("--wload15", type=int, required=True, help="Warning for load15 in percent")
parser.add_argument("--cload1", type=int, required=True, help="Critical for load1 in percent")
parser.add_argument("--cload5", type=int, required=True, help="Critical for load5 in percent")
parser.add_argument("--cload15", type=int, required=True, help="Critical for load15 in percent")
args = parser.parse_args()

codes_label = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]
loads_label = ("load1", "load5", "load15")
loads = (load1, load5, load15) = os.getloadavg()
cpu_cnt = os.cpu_count()

load1_prcnt = load1 / cpu_cnt * 100
load5_prcnt = load5 / cpu_cnt * 100
load15_prcnt = load15 / cpu_cnt * 100
loads_prcnt = (load1_prcnt, load5_prcnt, load15_prcnt)

warns = (warn1, warn5, warn15) = (args.wload1, args.wload5, args.wload15)
crits = (crit1, crit5, crit15) = (args.cload1, args.cload5, args.cload15)

codes = []
msgs = []
perfs_data = []
for idx in range(0, 3):
    warn = warns[idx]
    crit = crits[idx]
    load = loads[idx]
    load_prcnt = loads_prcnt[idx]
    load_label = loads_label[idx]
    perfs_data.append("'%s_prcnt'=%.3f%%;%i;%i" % (load_label, load_prcnt, warn, crit))
    if load_prcnt >= crit:
        codes.append(2)
        msgs.append("%s is critical with %.2f / %.1f %%" % (load_label, load, load_prcnt))
    elif load_prcnt >= warn:
        codes.append(1)
        msgs.append("%s is warning with %.2f / %.1f %%" % (load_label, load, load_prcnt))

code = 0 if len(codes) == 0 else max(codes)
code_label = codes_label[code]
msg = "wonderful" if len(msgs) == 0 else ", ".join(msgs)
perf_data = " ".join(perfs_data)
output = "%s - %s|%s" % (code_label, msg, perf_data)

print(output)
exit(code)

