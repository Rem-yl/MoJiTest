from typing import List


def expand_range_list(range_str: str) -> List[int]:
    result = []
    for part in range_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return result
