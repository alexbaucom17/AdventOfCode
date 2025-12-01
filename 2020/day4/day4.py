def load_data(filename):
    with open(filename) as f:
        data = []
        cur_passport = []
        for line in f:
            line = line.rstrip()
            if line == "":
                data.append(cur_passport)
                cur_passport = []
            else:
                cur_passport.append(line)

        data.append(cur_passport)
        return data

def parse_passport(passport_data):
    output = {}
    for line in passport_data:
        for field in line.split():
            key,value = field.split(":")
            output[key] = value
    return output


def validate_expected_fields(passport, expected_fields):
    for f in expected_fields:
        if f not in passport.keys():
            return False
    return True


def count_valid_passports_simple(data):
    num_valid = 0
    expected_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for passport_data in data:
        passport = parse_passport(passport_data)
        if validate_expected_fields(passport, expected_fields):
            num_valid += 1
    return num_valid


def validate_field(key, value):
    if key == "byr":
        return int(value) >= 1920 and int(value) <= 2002
    elif key == "iyr":
        return int(value) >= 2010 and int(value) <= 2020
    elif key == "eyr":
        return int(value) >= 2020 and int(value) <= 2030
    elif key == "hgt":
        if "cm" in value:
            idx = value.find("cm")
            num = int(value[:idx])
            return num >= 150 and num <= 193
        elif "in" in value:
            idx = value.find("in")
            num = int(value[:idx])
            return num >= 59 and num <= 76
        else:
            return False
    elif key == "hcl":
        return len(value) == 7 and value[0] == '#'
    elif key == "ecl":
        return value in ["amb","blu","brn","gry","grn","hzl","oth"]
    elif key == "pid":
        return len(value) == 9
    elif key == "cid":
        return True


def count_valid_passports_advanced(data):
    num_valid = 0
    expected_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for passport_data in data:
        passport = parse_passport(passport_data)
        if validate_expected_fields(passport, expected_fields):
            valid = True
            for key,value in passport.items():
                if not validate_field(key,value):
                    valid = False
            if valid:
                num_valid += 1
    return num_valid


if __name__ == '__main__':

    sample_data = load_data("day4/sample_input.txt")
    data = load_data("day4/input.txt")

    # part 1
    print(count_valid_passports_simple(data))

    # part 2
    sample_invalid = load_data("day4/sample_invalid_pt2.txt")
    sample_valid = load_data("day4/sample_valid_pt2.txt")
    print(count_valid_passports_advanced(data))
