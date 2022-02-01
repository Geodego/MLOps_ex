def find_pdb_mapping(reference_sequence, pdb_sequence):
    # Write your code here
    output = []
    prev_index = -1 # index of the previous AA in pdb_sequence
    pos_prev = -1 # position of the previous AA in pdb_sequence
    new_ref = reference_sequence
    for item in pdb_sequence:
        pdb, amino = item
        _, pos, insertion = pdb.split(".")
        pos = int(pos)
        if pos == 1:
            # no ambiguity, this is the first AA
            output.append((pdb, 0))
            pos_prev = pos
            prev_index = 0
            continue
        if pos - pos_prev <= 1:
            # there is no missing insertion code
            output.append((pdb, prev_index+1))
            pos_prev = pos
            prev_index += 1
            continue
        if not output:
            # this is the first AA in pdb_sequence and its pos is>1
            # get the index of the first possible position of the AA
            # for now we assume there is no AA inserted before that one
            new_index = reference_sequence.find(amino, pos - 1)
            if new_index == -1:
                new_index = reference_sequence.find(amino)
            output.append((pdb, new_index))
            pos_prev = pos
            prev_index = new_index
            continue
        # we are left with the case when there are missing components
        new_index = reference_sequence.find(amino, prev_index+1)
        output.append((pdb, new_index))
        pos_prev = pos
        prev_index = new_index
    return output

def test_2():
    primary = "MFVFLVLLPLVSSQCVN"
    list = [("A.4.", "F"), ("A.5.", "L"), ("A.6.", "V"), ("A.6.A", "L"), ("A.6.B", "L"), ("A.7.", "P"), ("A.12.", "Q"), ("A.13.", "C")]
    a = find_pdb_mapping(primary, list)
    print(a)

def test_3():
    primary = "MSLGAESIAINFTIS"
    list = [("A.254.", "G"), ("A.255.", "A"), ("A.256.", "E"), ("A.259.", "N"), ("A.260.", "F"), ("A.261.", "T"), ("A.262.", "I")]
    a = find_pdb_mapping(primary, list)
    print(a)


if __name__ == '__main__':
    test_3()