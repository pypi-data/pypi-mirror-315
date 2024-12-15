from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_single_char():
    regexEnumerator = RegexEnumerator(r'(a)')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)

def test_single_char_class():
    regexEnumerator = RegexEnumerator(r'([a])')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)

def test_multiple_char_class():
    regexEnumerator = RegexEnumerator(r'([a-c])')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)

def test_single_char_with_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)