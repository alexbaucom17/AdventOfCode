import copy

def load_data(filename):
    with open(filename) as f:
        rules = {}
        msgs = []
        finished_rules = False
        for line in f:

            if line.strip() == "":
                finished_rules = True
                continue

            if not finished_rules:
                id, rule = line.strip().split(':')
                if rule.find('"') != -1:
                    rule = rule.strip().replace('"', '')
                    rules[int(id)] = rule
                else:
                    rule_parts = tuple([tuple([int(n) for n in r.split()]) for r in rule.strip().split('|')])
                    rules[int(id)] = rule_parts
            else:
                msgs.append(line.strip())

        return (rules,msgs)


# Checks if a given rule matches this string at the specific offset
# Returns a bool indicating if there was a match and an array of updated
# offsets that indicate how far into the string the rule has matched
def match_rule_for_id_and_offset(s, offset, id, rules):
    # If the offset is larger than the length of the string, it isn't a match
    if offset >= len(s):
        return (False, [0])

    # print("[Match Rule for Id and Offset] str: {}, id: {}, offset: {}".format(s,id,offset))

    # Check that the current substring (with offset) matches the current rule in the pattern
    match, new_offset = match_rule(s[offset:], id, rules)
    new_offsets = [o + offset for o in new_offset]

    return (match, new_offsets)


# Checks if there is a match for the given rule at all possible offset locations
# returns bool indicating if any offset had a rule match and returns a list of updated
# offsets where the match(es) occured
def match_rule_for_id(s, possible_offsets, id, rules):
    # Offsets for sub_id will hold all the offsets for this id, which could expand
    # while exploring this step of the pattern.
    new_offsets_for_sub_id = []

    # print("[Match Rule for id]            str: {}, id: {}, possible_offsets: {}".format(s,id,possible_offsets))

    # Loop over any potential offsets to see if the rule matches
    any_offset_match = False
    for offset in possible_offsets:

        match, new_offsets = match_rule_for_id_and_offset(s, offset, id, rules)

        # print("[Match Rule for id]            match: {}, offsets: {}".format(match, new_offsets))

        any_offset_match |= match
        if match:
            new_offsets_for_sub_id += new_offsets

    return (any_offset_match, new_offsets_for_sub_id)


# Checks if the given pattern of rules matches the given string
# Returns a bool indicating if there is a match and a list of 
# offsets indicating how far into the string the pattern matches
def match_rule_for_pattern(s, pattern, rules):
    # Each pattern starts at 0 offset for the current string
    current_pattern_offsets = [0]

    # print("[Match Rule for Pattern]       str: {}, pattern: {}".format(s,pattern))

    # For each id in the pattern, check if there is a match
    all_sub_rule_match = True
    for sub_rule_id in pattern:

        any_offset_match, current_pattern_offsets = match_rule_for_id(s, current_pattern_offsets, sub_rule_id, rules)

        # print("[Match Rule for Pattern]       match: {}, offsets: {}".format(any_offset_match, current_pattern_offsets))
            
        # If no id/offset combos have matched, this rule is not a match
        if not any_offset_match:
            all_sub_rule_match = False
            break

    return (all_sub_rule_match, current_pattern_offsets)


def match_rule(s, id, rules):
    rule = rules[id]

    # print("[Match Rule]                   str: {}, id: {}".format(s,id))

    # If the rule is a basic string, do the individual character check
    if isinstance(rule, str):
        return (s[0] == rule[0], [1])
    else:
        # Loop over all patterns within the role and or the results together
        any_pattern_match = False
        offsets_for_patterns = []
        for pattern in rule:

            pattern_match, pattern_offsets = match_rule_for_pattern(s, pattern, rules)

            # If all sub rules for this pattern have matched, then we can at least claim to have
            # matched a part of this rule with the given offsets. Append these offsets to any existing ones
            if pattern_match:
                any_pattern_match |= True
                offsets_for_patterns += pattern_offsets

            # print("[Match Rule]                   match: {}, offsets: {}".format(pattern_match, offsets_for_patterns))
                
        # If any part of the rule has matched, return a True match and the offsets that have been found
        if any_pattern_match:
            return (True, offsets_for_patterns)
        else:
            return (False, [0])


def check_all_msgs_match(msgs, rules):
    match = []
    for m in msgs:
        cur_match, offset = match_rule(m, 0, rules)
        if offset[0] != len(m):
            cur_match = False
        match.append(cur_match)
        if cur_match:
            print(m)

    print(match)
    print(sum(match))

def update_rules_for_pt2(rules):
    rules[8] = ((42,), (42, 8))
    rules[11] = ((42, 31), (42, 11, 31))
    return rules

if __name__ == '__main__':

    sample_data = load_data("day19/sample_input.txt")
    sample_data2 = load_data("day19/sample_input2.txt")
    data = load_data("day19/input.txt") 

    using_data = data
    rules = using_data[0]
    msgs = using_data[1]


    # check_all_msgs_match(msgs, rules)

    new_rules = update_rules_for_pt2(rules)
    #print(match_rule("aaaaabbaabaaaaababaa", 0, rules))
    check_all_msgs_match(msgs, new_rules)  