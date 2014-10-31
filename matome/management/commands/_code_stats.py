# -*- coding: utf-8 -*-

import os
import re


class CodeStatisticsCalculator(object):

    PATTERNS = {
        'py': {
            'line_comment': re.compile('^\s*#'),
            'class': re.compile('\s*class\s+[_A-Z]'),
            'method': re.compile('\s*def\s+[_a-z]'),
        },
        'js': {
            'line_comment': re.compile(r'^\s*//'),
            'begin_block_comment': re.compile(r'^\s*/\*'),
            'end_block_comment': re.compile(r'\*/'),
            'method': re.compile('function(\s+[_a-zA-Z][\da-zA-Z]*)?\s*\('),
        },
        'coffee': {
            'line_comment': re.compile('^\s*#'),
            'begin_block_comment': re.compile('^\s*###'),
            'end_block_comment': re.compile('^\s*###'),
            'class': re.compile('^\s*class\s+[_A-Z]'),
            'method': re.compile('[-=]>'),
        }
    }

    def __init__(self, lines=0, code_lines=0, classes=0, methods=0):
        self.lines = lines
        self.code_lines = code_lines
        self.classes = classes
        self.methods = methods

    def add(self, code_statistics_calculator):
        self.lines += code_statistics_calculator.lines
        self.code_lines += code_statistics_calculator.code_lines
        self.classes += code_statistics_calculator.classes
        self.methods += code_statistics_calculator.methods

    def add_by_file_path(self, file_path):
        with open(file_path) as f:
            self.add_by_io(f, CodeStatisticsCalculator._file_type(file_path))

    def add_by_io(self, io, file_type):
        if file_type in CodeStatisticsCalculator.PATTERNS:
            patterns = CodeStatisticsCalculator.PATTERNS[file_type]
        else:
            patterns = {}

        comment_started = False

        empty_line_pattern = re.compile('^\s*$')

        for line in io.readlines():
            self.lines += 1
            if comment_started:
                if 'end_block_comment' in patterns and patterns['end_block_comment'].match(line):
                    comment_started = False
                continue
            else:
                if 'begin_block_comment' in patterns and patterns['begin_block_comment'].match(line):
                    comment_started = True
                    continue

            if 'class' in patterns and patterns['class'].match(line):
                self.classes += 1

            if 'method' in patterns and patterns['method'].match(line):
                self.methods += 1

            if not empty_line_pattern.match(line) and 'line_comment' not in patterns or not patterns['line_comment'].match(line):
                """空行でなく、言語的にラインコメントが定義されていないか、ラインコメント形式でない。"""
                self.code_lines += 1

    @staticmethod
    def _file_type(file_path):
        return re.sub(re.compile("\A\."), '', os.path.splitext(file_path)[-1]).lower()


class CodeStats(object):
    TEST_TYPES = ['Controller tests',
                  'Helper tests',
                  'Model tests',
                  'Mailer tests',
                  'Integration tests',
                  'Functional tests (old)',
                  'Unit tests (old)']

    def __init__(self, pairs):
        self.pairs = pairs
        self.statistics = self._calculate_statistics()
        if len(self.pairs) > 1:
            self.total = self._calculate_total()
        else:
            self.total = 0
        self._print_stack = []

    @property
    def result(self):
        represents = []
        represents.append(CodeStats._splitter())
        represents.append(CodeStats._header())
        represents.append(CodeStats._splitter())
        for pair in self.pairs:
            represents.append(CodeStats._line(pair[0], self.statistics[pair[0]]))
        represents.append(CodeStats._splitter())

        if self.total:
            represents.append(CodeStats._line("Total", self.total))
            represents.append(CodeStats._splitter())

        represents.append(self._code_test_stats())

        return '\n'.join(represents)

    def _calculate_statistics(self):
        return {
            pair[0]: self._calculate_category_statistics(pair[-1]) for pair in self.pairs
        }

    def _calculate_category_statistics(self, targets, regex=re.compile('.*\.(py|js|coffee)$')):
        stats = CodeStatisticsCalculator()

        for path in targets:
            if regex.match(path):
                stats.add_by_file_path(path)

        return stats

    def _calculate_total(self):
        stats = CodeStatisticsCalculator()
        for pair in self.pairs:
            stats.add(pair[-1])
        return stats

    def _calculate_code(self):
        code_loc = 0
        for stats_key in self.statistics:
            if stats_key not in CodeStats.TEST_TYPES:
                code_loc += self.statistics[stats_key].code_lines
        return code_loc

    def _calculate_tests(self):
        code_loc = 0
        for stats_key in self.statistics:
            if stats_key in CodeStats.TEST_TYPES:
                code_loc += self.statistics[stats_key].code_lines
        return code_loc

    @staticmethod
    def _header():
        return "| Name                 | Lines |   LOC | Classes | Methods | M/C | LOC/M |"

    @staticmethod
    def _splitter():
        return "+----------------------+-------+-------+---------+---------+-----+-------+"

    @staticmethod
    def _line(name, statistics):
        m_over_c = (float(statistics.methods) / statistics.classes) if statistics.classes != 0 else 0.0
        loc_over_m = (float(statistics.code_lines) / statistics.methods) - 2 if statistics.methods != 0 else 0.0

        line_format = "".join([
            "| {name:20} ",
            "| {lines:5} ",
            "| {code_lines:5} ",
            "| {classes:7} ",
            "| {methods:7} ",
            "| {m_over_c:3.1f} ",
            "| {loc_over_m:5.1f} |"
        ])

        return line_format.format(
            name=name,
            lines=statistics.lines,
            code_lines=statistics.code_lines,
            classes=statistics.classes,
            methods=statistics.methods,
            m_over_c=m_over_c,
            loc_over_m=loc_over_m
        )

    def _code_test_stats(self):
        code = self._calculate_code()
        tests = self._calculate_tests()
        result_format = "  Code LOC: {code}     Test LOC: {tests}     Code to Test Ratio: 1:{:.1f}"
        return result_format.format(tests / code, code = code, tests = tests)
