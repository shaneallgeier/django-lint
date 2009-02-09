#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-lint -- Static analysis tool for Django projects and applications
# Copyright (C) 2008-2009 Chris Lamb <chris@chris-lamb.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from pylint import checkers, lint
from optparse import OptionParser

from DjangoLint import AstCheckers

def main():
    usage = """ %prog [options] target

    Django Lint is a tool that statically analyses Django projects and
    applications, checking for programming errors and bad code smells. For
    example, it reports nullable "CharField" fields, as well as reporting for
    unspecified options in settings.py.

    The `target` argument is mandatory and can specify either a directory
    containing a Django project, a single application or a single file.
    """.rstrip()

    parser = OptionParser(usage=usage)
    parser.add_option(
        '-r',
        '--reports',
        dest='report',
        action='store_true',
        default=False,
        help='generate report',
    )

    options, args = parser.parse_args()

    if len(args) != 1:
        raise parser.error("The 'target' argument is mandatory")

    target = os.path.abspath(args[0])

    if not os.path.exists(target):
        raise parser.error(
            "The specified target (%r) does not exist" \
                % target
        )

    path = target
    while True:
        flag = False
        for django_file in ('manage.py', 'models.py', 'urls.py'):
            if os.path.exists(os.path.join(path, django_file)):
                sys.path.insert(0, os.path.dirname(path))
                flag = True
                break
        if flag:
            break

        path = os.path.dirname(path)

        if path == '/':
            raise parser.error(
                "The specified target (%r) does not appear to be part of a " \
                "Django application" % target
            )

    linter = lint.PyLinter()
    linter.set_option('reports', options.report)
    checkers.initialize(linter)

    for msg in ('C0111', 'C0301'):
        linter.disable_message(msg)

    AstCheckers.register(linter)
    linter.check([target])

    return 0

if __name__ == "__main__":
    sys.exit(main())