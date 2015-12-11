# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Arizona Board of Regents
# Author: Teng Liang <philoliang@email.arizona.edu>
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

from utility import getPrefixes

class NaiveFib:
    def __init__(self, nic):
        self.nic = nic

    def insert(self, prefix):
        self.nic.bf1.add(prefix, "FIB1")

    def erase(self, prefix):
        self.nic.bf1.remove(prefix, "FIB1")

class NaivePit:
    def __init__(self, nic):
        self.nic = nic

    def insert(self, prefix):
        self.nic.bf1.add(prefix, "PIT1")

    def erase(self, prefix):
        self.nic.bf1.remove(prefix, "PIT1")

class NaiveCs:
    def __init__(self, nic):
        self.nic = nic

    def insert(self, name):
        prefixes = getPrefixes(name)
        for prefix in prefixes:
            self.nic.bf2.add(prefix, "CS2")

    def erase(self, name):
        prefixes = getPrefixes(name)
        for prefix in prefixes:
            self.nic.bf2.remove(prefix, "CS2")

Fib = NaiveFib
Pit = NaivePit
Cs = NaiveCs