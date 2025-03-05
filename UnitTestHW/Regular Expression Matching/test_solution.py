import pytest
from solution import Solution

@pytest.fixture
def solution():
    return Solution()

testcases = [
    # s, p, expected_res
    ["", "", True],
    ["aa", "a", False],
    ["aa", "a*", True],
    ["ab", ".*", True],
    ["aab", "c*a*b", True],
    ["aaa", "ab*a*c*a", True]
]

@pytest.mark.parametrize(["s", "p", "expected"], testcases)
def test_thing(solution, s, p, expected):
    assert solution.isMatch(s, p) == expected

@pytest.mark.xfail
def test_broken_solution(solution):
    assert solution.isMatch("a", ".*.") == True 