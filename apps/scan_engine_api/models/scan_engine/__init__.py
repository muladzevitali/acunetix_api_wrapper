from .reports import Report
from .results import Result
from .scans import (Scan, scan_profiles)
from .targets import (Target, target_criticality, scan_speeds)


class SearchEngine(Target, Scan, Result, Report):
    pass
