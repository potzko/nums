under_twenty = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
    'eighteen', 'nineteen', 'twenty'
]

thousand_pows = [
    '', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion'
]

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

def under_hundred(digits: int) -> str:
    assert digits < 100
    tens = [
        '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
    ]
    if digits < 21:
        return under_twenty[digits]
    
    assert 20 <digits < 100
    ten_part = tens[digits // 10]
    unit_part = digits % 10
    if unit_part == 0:
        return ten_part
    else:
        return f"{ten_part} {under_twenty[unit_part]}"

def under_thousand(digits: int) -> str:
    assert digits < 1000
    if digits < 100:
        return digit_to_num(digits)
    
    hundred_part = digits // 100
    rest_part = digits % 100
    if rest_part == 0:
        return f"{under_twenty[hundred_part]} hundred"
    else:
        return f"{under_twenty[hundred_part]} hundred and {digit_to_num(rest_part)}"

def break_into_thousands(digits: int) -> list[int]:
    parts = []
    while digits > 0:
        parts.append(digits % 1000)
        digits //= 1000
    return parts

def main():
    test_numbers = [
        0, 5, 13, 20, 25, 42, 99, 100, 105, 215, 999,
        1000, 1500, 12345, 1000000, 2000001, 3050607,
        1234567890, 1000000000000
    ]
    for number in test_numbers:
        print(f"{number}: {digit_to_num(number)}")
    print(f"total chars under a million: {sum(len(digit_to_num(n)) + 1 for n in range(1, 1000000))}") # the +1 is for lines 


if __name__ == "__main__":
    main()