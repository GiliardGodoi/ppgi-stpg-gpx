# -*- coding: utf-8 -*-

import re
import os
from collections import defaultdict

problems_class = {
        'b' : {'max' : 18},
        'c' : {'max' : 20},
        'd' : {'max' : 20},
        'e' : {'max' : 20},
        'others' : ['dv80.txt', 'dv160.txt', 'dv320.txt']
    }

def generate_file_names(key = None):

    if isinstance(problems_class[key], list) :
        for item in problems_class[key]:
            yield item

    elif isinstance(problems_class[key], dict) :
        counter = 1
        MAX = problems_class[key]['max']
        while counter <= MAX :
            yield f"stein{key}{counter}.txt"
            counter += 1

## ================================================

class SteinerTreeProblem(object):
    '''
        The main purpose for this class is represent in memory the Steiner Problem's instance in memory.
    '''

    def __init__(self):
        self.nro_nodes = 0
        self.nro_edges = 0
        self.nro_terminals = 0
        self.graph = defaultdict(dict)
        self.terminals = list()

        self.name = None
        self.remark = None
        self.creator = None
        self.file_name = None


class Reader(object):
    '''
        This class parses the Steiner Tree Problem instance's file and fill the Steiner Tree Problem class above.

        Based on Bruna Osti's propose
        from: <https://github.com/brunaostii/Steiner_Tree>
    '''

    def __init__(self):
        self.STP = SteinerTreeProblem()

    def parser(self, fileName):
        self.STP.file_name = fileName

        with open(fileName, 'r') as file :
            for line in file :
                if "SECTION Comment" in line :
                    self._parser_section_comment(file)

                elif "SECTION Graph" in line :
                    self._parser_section_graph(file)

                elif "SECTION Terminals" in line :
                    self._parser_section_terminals(file)

        return self.STP

    def _parser_section_comment(self,file):
        for line in file:
            _list = re.findall(r'"(.*?)"',line)
            if "Name" in line :
                _name = _list[0] if len(_list) else "Name unviable"
                self.STP.name = _name

            elif "Creator" in line :
                _creator = _list[0] if len(_list) else "Creator unviable"
                self.STP.creator = _creator

            elif "Remark" in line :
                remark = _list[0] if len(_list) else "Creator unviable"
                self.STP.remark = remark

            elif "END" in line:
                break

    def _parser_section_graph(self, file):
        for line in file:
            if line.startswith("E ") :
                entries = re.findall(r'(\d+)', line)
                vetor = [ e for e in entries if e.isdecimal() ]

                assert len(vetor) == 3, "The line must to have three values"
                v, w, peso = vetor

                v = int(v)
                w = int(w)
                peso = int(peso)

                self.STP.graph[v][w] = peso
                self.STP.graph[w][v] = peso

            elif line.startswith("Nodes"):
                nodes = re.findall(r'Nodes (\d+)$', line)
                self.STP.nro_nodes = int(nodes[0]) if len(nodes) else -1

            elif line.startswith("Edges"):
                edges = re.findall(r'Edges (\d+)$', line)
                self.STP.nro_edges = int(edges[0]) if len(edges) else -1

            elif "END" in line :
                break

    def _parser_section_terminals(self,file):

        for line in file:
            if line.startswith("T "):
                _string = re.findall(r"(\d+)$", line)
                v_terminal = int(_string[0]) if len(_string) == 1 else -1
                self.STP.terminals.append(v_terminal)

            elif line.startswith("Terminals"):
                terminal = re.findall(r'Terminals (\d+)$', line)
                self.STP.nro_terminals = int(terminal[0]) if len(terminal) else -1

            elif "END" in line:
                break


class ReaderORLibrary():
    '''
    Read a Steiner Tree Problem instance from a OR-Library file format.

    For more details visit <http://people.brunel.ac.uk/~mastjjb/jeb/orlib/steininfo.html>
    '''
    def __init__(self):
        pass

    def __define_stp(self, file_name : str):

        STP = SteinerTreeProblem()

        index = 0
        if '\\' in file_name:
            index = file_name.rfind('\\') + 1

        STP.file_name = file_name[index:]

        if STP.file_name.startswith("stein"):
            # "An SST-based algorithm for the Steiner problem in graphs" Networks 19 (1989) 1-16.
            STP.name = STP.file_name.strip('steinx.').upper()
            STP.creator = "J. E. Beasley"
            STP.remark = "Sparse graph with random weights"
        elif STP.file_name.startswith("dv") :
            ##"Efficient path and vertex exchange in Steiner tree algorithms", Networks 29, 89-105 (1997)
            STP.name = STP.file_name.upper()
            STP.creator = "C. Duin and S. Voss"
            STP.remark = "Incidence weights problems"

        return STP


    def parser(self, file_name):

        if not os.path.exists(file_name):
            raise FileExistsError(f'{file_name} does not exists')

        STP = self.__define_stp(file_name)

        with open(file_name, 'r') as FILE:
            # number of vertices, number of edges
            line = FILE.readline()
            entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
            assert len(entries) == 2, "First line isn't equal 2 numbers"

            STP.nro_nodes = entries[0]
            STP.nro_edges = entries[1]

            # for each edge: the end vertices and the cost of the edge
            counter = 0
            while counter < STP.nro_edges:
                line = FILE.readline()
                entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
                assert len(entries) == 3, f'Edge line has not 3 values. Line {(counter + 1)}'
                u = entries[0]
                v = entries[1]
                weight = entries[2]

                STP.graph[u][v] = weight
                STP.graph[v][u] = weight
                counter += 1

            # number of vertices to be connected together
            line = FILE.readline()
            entry = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
            assert len(entry) == 1, "Number of terminals have to be just one"
            STP.nro_terminals = entry[0]

            # the vertex numbers for the vertices that are to be connected together
            line = FILE.readline()

            # for some problems' instance, the terminals are represented in more than one line
            terminals = list()
            while line:
                entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
                terminals.extend(entries)
                line = FILE.readline()

            assert len(terminals) == entry[0], "Numer of terminals is not ok"
            STP.terminals = terminals

        return STP
