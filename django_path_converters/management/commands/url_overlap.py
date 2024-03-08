from itertools import islice

from django.core.management.base import BaseCommand
from django.urls import get_resolver
from greenery import parse as gparse
from interegular import parse_pattern

from xeger import Xeger
from random import randint
import sys
import re
from argparse import BooleanOptionalAction
from django_path_converters.utils import strip_capture_groups

ALL = parse_pattern('[\W\w]*').to_fsm().reduce()
NONE = parse_pattern('[]').to_fsm().reduce()

def parse_regex_to_fsm(value):
    return parse_pattern(value).to_fsm().reduce()

class Command(BaseCommand):
    help = "Search if two or more URLs overlap. The exit code shows the number of overlaps."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("--seed", type=int)
        parser.add_argument("--verbose", action=BooleanOptionalAction)
        parser.add_argument("--accept", type=parse_regex_to_fsm, default=(ALL,), nargs='*')
        parser.add_argument("--reject", type=parse_regex_to_fsm, default=(NONE,), nargs='*')

    def produce_regexes(self, resolver, prefix, regex_filter=ALL):
        subregex = resolver.pattern.regex.pattern
        if subregex.startswith('^'):
            subregex = subregex[1:]
        if subregex.endswith('$'):
            subregex = subregex[:-1]
        if subregex.endswith(r'\Z'):
            subregex = subregex[:-2]
        regex = f'{prefix}{subregex}'
        if resolver.callback is not None:
            result = parse_pattern(strip_capture_groups(regex)).to_fsm().reduce()
            if not (regex_filter & result).empty():
                yield regex, [result, 0]
        for subresolver in getattr(resolver, 'url_patterns', ()):
            yield from self.produce_regexes(subresolver, regex, regex_filter=regex_filter)

    def explain_capture(self, capture_dict, _type='first', _hasnext=False):
        if capture_dict:
            explain = ', '.join(f'\x1b[32m{k}\x1b[0m=\x1b[33m{v!r}\x1b[0m' for k, v in capture_dict.items())
            sys.stderr.write(f'        with {explain} for the {_type} pattern{"; and" if _hasnext else "."}\n')
            return True

    def explain_failure(self, xeger, regex1, regex2, full1, full2):
        intersect = (regex1 & regex2).reduce()
        fail = not intersect.empty()
        reorder = False
        if fail:
            full_overlap = ''
            if (regex1 ^ regex2).empty():
                full_overlap = '\x1b[1mfully\x1b[0m '
            else:
                reorder = (regex2 - regex1).empty()
            with_example = False
            example = None
            try:
                overlap = str(gparse(strip_capture_groups(full1)) & gparse(strip_capture_groups(full2)))
                example = xeger.xeger(overlap)
                capture1 = re.match(full1, example)
                capture2 = re.match(full2, example)
                with_example = capture1 and capture2
            except:
                pass
            sys.stderr.write(f'[\x1b[31m✗\x1b[0m] patterns \x1b[34m{full1}\x1b[0m and \x1b[34m{full2}\x1b[0m {full_overlap}overlap\n')
            if with_example:
                sys.stderr.write(f'      for example with \x1b[35m{example!r}\x1b[0m\n')
                groupdict1 = capture1.groupdict()
                groupdict2 = capture2.groupdict()
                self.explain_capture(groupdict1, _hasnext=groupdict2)
                self.explain_capture(groupdict2, _type='second')
            if reorder:
                sys.stderr.write(f'    \x1b[33;40m!\x1b[0m since all captures by the second pattern are also captured by the first pattern,\n')
                sys.stderr.write(f'      the second pattern will never fire, you therefore probably should reorder the patterns.\n')
            sys.stderr.write(f'\n')
        return fail, reorder


    def handle(self, *args, seed=None, verbose=False, accept=(ALL,), reject=(NONE,), **options):
        resolver = get_resolver()
        regex_filter = (reduce(operator.or_, accept) - reduce(operator.or_, reject)).reduce()
        regexes = list(self.produce_regexes(resolver, '', regex_filter=regex_filter))
        fail = 0
        if seed is None:
            seed = randint(0, 2**64)
        xeger = Xeger(limit=1, seed=seed)  # shorter URLs, make the problem clearer

        nooverlaps = []
        reorders = {}
        for i, (full1, [regex1, subfail]) in enumerate(regexes, 1):
            for full2, regex2all in islice(regexes, i, None):
                regex2 = regex2all[0]
                hasfailed, to_reorder = self.explain_failure(xeger, regex1, regex2, full1, full2)
                if to_reorder:
                    reorders.setdefault(full2, full1)
                subfail += hasfailed
                regex2all[1] += hasfailed
            if verbose and not subfail:
                nooverlaps.append(full1)
            fail += subfail

        if reorders:
            sys.stderr.write('The following reorders are very likely:\n')
            for key, val in reorders.items():
                sys.stderr.write(f'  [\x1b[33m⇅\x1b[0m] \x1b[34m{key}\x1b[0m should be listed before \x1b[34m{val}\x1b[0m\n')
            sys.stderr.write('\n')

        if verbose:
            if nooverlaps:
                sys.stdout.write(f'\n')
                sys.stdout.write(f'patterns with no overlap found†: \n')
                for nooverlap in nooverlaps:
                    sys.stdout.write(f'  [\x1b[32m✓\x1b[0m] \x1b[34m{nooverlap}\x1b[0m\n')
                sys.stdout.write(f'† beware that the greenery package has some limitations regarding regexes, so it can not detect all overlaps.')
            sys.stdout.write(f'\n')
            sys.stdout.write(f'The examples are derived from a generator with seed \x1b[36m{seed}\x1b[0m.\n')
        status = fail // 2 + len(reorders)
        if status:
            status = ((status - 1) % 253) + 1
        exit(status)  # we count each failure twi