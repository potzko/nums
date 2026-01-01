import functools
from collections import Counter

under_twenty = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
    'eighteen', 'nineteen', 'twenty'
]

thousand_pows = [
    '', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion'
]

tens = [
    '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
]

def line_on_page(digits: int) -> str:
    return digit_to_num(digits) + '\n'

def digit_to_num(digits: int) -> str:
    if 0 <= digits <= 20:
        return under_twenty[digits]
    if 21 <= digits < 100:
        return under_hundred(digits)
    if 100 <= digits < 1000:
        return under_thousand(digits)
    parts = break_into_thousands(digits)
    word_parts = []
    for idx, part in enumerate(parts):
        if part == 0:
            continue
        part_word = under_thousand(part)
        if thousand_pows[idx]:
            part_word += f" {thousand_pows[idx]}"
        word_parts.append(part_word)
    return ' '.join(reversed(word_parts))

@functools.cache
def under_hundred(digits: int) -> str:
    assert digits < 100
    if digits < 21:
        return under_twenty[digits]
    
    assert 20 < digits < 100
    ten_part = tens[digits // 10]
    unit_part = digits % 10
    if unit_part == 0:
        return ten_part
    else:
        return f"{ten_part} {under_twenty[unit_part]}"

@functools.cache
def under_thousand(digits: int) -> str:
    assert digits < 1000
    if digits < 100:
        return digit_to_num(digits)
    
    hundred_part = digits // 100
    rest_part = digits % 100
    if rest_part == 0:
        return f"{under_twenty[hundred_part]} hundred"
    else:
        # comment out either the british or american style line below
        return f"{under_twenty[hundred_part]} hundred and {digit_to_num(rest_part)}" #british style
        # return f"{under_twenty[hundred_part]} hundred {digit_to_num(rest_part)}" #american style

def break_into_thousands(digits: int) -> list[int]:
    parts = []
    while digits > 0:
        parts.append(digits % 1000)
        digits //= 1000
    return parts

def main():
    #tests
    assert line_on_page(0) == 'zero\n'
    assert line_on_page(5) == 'five\n'
    assert line_on_page(13) == 'thirteen\n'
    assert line_on_page(20) == 'twenty\n'
    assert line_on_page(25) == 'twenty five\n'
    assert line_on_page(42) == 'forty two\n'
    assert line_on_page(99) == 'ninety nine\n'
    assert line_on_page(100) == 'one hundred\n'
    assert line_on_page(105) in ['one hundred five\n', 'one hundred and five\n']
    assert line_on_page(215) in ['two hundred fifteen\n', 'two hundred and fifteen\n']
    assert line_on_page(999) in ['nine hundred ninety nine\n', 'nine hundred and ninety nine\n']
    assert line_on_page(1000) in ['one thousand\n', 'one thousand\n']
    assert line_on_page(1500) in ['one thousand five hundred\n', 'one thousand five hundred\n']
    assert line_on_page(12345) in ['twelve thousand three hundred forty five\n', 'twelve thousand three hundred and forty five\n']
    assert line_on_page(1000000) in ['one million\n', 'one million\n']
    assert line_on_page(1123123) in ['one million one hundred twenty three thousand one hundred twenty three\n', 'one million one hundred and twenty three thousand one hundred and twenty three\n']
    assert line_on_page(2000001) in ['two million one\n', 'two million one\n']
    assert line_on_page(3050607) in ['three million fifty thousand six hundred seven\n', 'three million fifty thousand six hundred and seven\n']
    assert line_on_page(1234567890) in ['one billion two hundred thirty four million five hundred sixty seven thousand eight hundred ninety\n', 'one billion two hundred and thirty four million five hundred and sixty seven thousand eight hundred and ninety\n']
    assert line_on_page(1234567890123) in ['one trillion two hundred thirty four billion five hundred sixty seven million eight hundred ninety thousand one hundred twenty three\n', 'one trillion two hundred and thirty four billion five hundred and sixty seven million eight hundred and ninety thousand one hundred and twenty three\n']

    def get_text(n: int = 1_000_001) -> str:
        return (line_on_page(i) for i in range(n))
    
    print(f"total chars under a million: {sum(len(word) for word in get_text())}")
    print(f"total letters under a million: {sum(len([i for i in word if not i in [' ', '\n']]) for word in get_text())}")
    print(f"total spaces and new lines under a million: {sum(len([i for i in word if i in [' ', '\n']]) for word in get_text())}")
    seen = set()
    for i in range(1000001):
        word = line_on_page(i)
        chars = set(word)
        if chars - seen != set():
            print(f"the first number where the letters {chars - seen} appear is {i}")
        seen = seen | chars
    print(f"unique chars used: {seen}")
    print(f"number of unique chars used: {len(seen)}")
    char_counts = Counter()
    for i in range(1000001):
        char_counts.update(line_on_page(i))
    print(f"character counts: {char_counts}")

if __name__ == "__main__":
    main()
