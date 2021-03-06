# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Arizona Board of Regents
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU Lesser General Public License is in the file COPYING.

import sys

from nic import Nic
from nic_sim import NicSim

def parseCommandLine():
    import argparse
    parser = argparse.ArgumentParser(description="Run NDN-NIC simulation.")
    parser.add_argument("--comment", action="append",
                        help="ignored; may be used to identify running process")
    parser.add_argument("--bf1", default="1024",
                        help="BF-FIB configuration")
    parser.add_argument("--bf2", default="1024",
                        help="BF-CS configuration")
    parser.add_argument("--bf3", default="1024",
                        help="BF-PIT configuration")
    parser.add_argument("--nd", type=argparse.FileType('w'),
                        help="NIC decision log; stdout if unspecified")
    parser.add_argument("--bfu", type=argparse.FileType('w'),
                        help="BF update log; stdout if unspecified")
    parser.add_argument("--fib", default="DirectFib",
                        help="FIB type or expression")
    parser.add_argument("--pit", default="DirectPit",
                        help="PIT type or expression")
    parser.add_argument("--cs", default="DirectCs",
                        help="CS type or expression")
    args = parser.parse_args()
    return args

def makeBf(arg):
    """
    Create a Bloom filter from a configuration string.

    :param str arg: configuration string. Syntax:
    * m: m buckets, default count HmacHash with default hash algorithm
    * m,k: m buckets, k HmacHash with default hash algorithm
    * m,k,algo: m buckets, k HmacHash with specified hash algorithm
    * m,k,xor: m buckets, k XorHash with random polynomial terms
    * m,k,xor,file: m buckets, k XorHash with polynomial terms from file

    :return: NicBloomFilter instance
    """
    from hash_function import HmacHash, XorHash, HashGroup
    from nic_bloom_filter import NicBloomFilter

    args = arg.split(",")
    if len(args) == 1:
        return NicBloomFilter(int(args[0]))
    else:
        m, k = [ int(x) for x in args[0:2] ]
        if len(args) == 2:
            hasher = HashGroup([ HmacHash.create(m) for i in range(k) ])
        else:
            algo = args[2]
            if algo != "xor":
                hasher = HashGroup([ HmacHash.create(m, algo=algo) for i in range(k) ])
            elif len(args) == 3:
                hasher = HashGroup([ XorHash.create(m) for i in range(k) ])
            else:
                with open(args[3], "r") as polyFile:
                    hasher = HashGroup([ XorHash.create(m, polyFile=polyFile) for i in range(k) ])
        return NicBloomFilter(m, hasher)

def makeTable(nic, arg):
    import table
    if '(' not in arg:
        return getattr(table, arg)
    return eval(arg, table.__dict__, dict(nic=nic))

def run(args):
    bfFib = makeBf(args.bf1)
    bfCs = makeBf(args.bf2)
    bfPit = makeBf(args.bf3)

    ndFile = sys.stdout if args.nd is None else args.nd
    bfuFile = sys.stdout if args.bfu is None else args.bfu

    nic = Nic(bfFib, bfCs, bfPit)

    fib = makeTable(nic, args.fib)
    pit = makeTable(nic, args.pit)
    cs = makeTable(nic, args.cs)

    nicSim = NicSim(nic, fib=fib, pit=pit, cs=cs)
    nicSim.processTtt(sys.stdin, ndFile, bfuFile)

if __name__ == "__main__":
    args = parseCommandLine()
    run(args)
