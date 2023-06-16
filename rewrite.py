import os


def write_actions(actions, newF):
    newF.write("Actions:\n")
    for item in actions:
        newF.write(f'"{item}" is an action.\n')
    newF.write("\n")


def write_mechanisms(mechanisms, newF):
    newF.write("Mechanisms:\n")
    for line in mechanisms:
        k, v = line.strip().split(": ")
        if "|" in v:
            v = v.split(" | ")
            newF.write(f'"{k}" if ')
            newF.write(' or '.join([f'"{item}"' for item in v[:-1]]))
            newF.write(f' or "{v[-1]}"\n')
        else:
            newF.write(f'"{k}" if "{v}"\n')
    newF.write("\n")


def write_utilities(utilities, newF):
    newF.write("Utilities:\n")
    utils = utilities.strip().split("\n")
    utils = [item.strip() for item in utils]
    utils = [item.split(": ") for item in utils][::-1]
    while len(utils) > 0:
        a = utils.pop()
        b = utils.pop()
        if int(a[1]) > int(b[1]):
            newF.write(f'"{a[0]}" is good\n')
            newF.write(f'"{b[0]}" is bad\n')
        else:
            newF.write(f'"{a[0]}" is bad\n')
            newF.write(f'"{b[0]}" is good\n')
    newF.write("\n")


def write_best_choice(utilities, newF):
    utilities = utilities.strip().split("\n")
    utilities = [item.strip().split(": ") for item in utilities]
    maximum = float("-inf")
    key = None
    for k, v in utilities:
        if int(v) > maximum:
            maximum = int(v)
            key = k
    newF.write(f'The best choice is "{key}" with {maximum} score.\n\n')


def write_intention(mechanisms, best_choice, newF):
    intention_conseq = []
    for line in mechanisms:
        k, v = line.strip().split(": ")
        if "|" in v:
            v = v.split(" | ")
            if best_choice in v:
                intention_conseq.append(k)
        else:
            if v == best_choice:
                intention_conseq.append(k)
    for line in mechanisms:
        k, v = line.strip().split(": ")
        if "|" in v:
            v = v.split(" | ")
            for item in v:
                if item in intention_conseq and k not in intention_conseq:
                    intention_conseq.append(k)
        else:
            if v in intention_conseq and k not in intention_conseq:
                intention_conseq.append(k)
    newF.write(f'The intention of this problem for action "{best_choice}", consequences: ')
    newF.write(" --> ".join([f'"{item}"' for item in intention_conseq]))
    newF.write(".\n")


def main():
    input_dir = "input"
    output_dir = "output"
    path = sorted(os.listdir(input_dir))

    for file in path:
        # load input file
        with open(os.path.join(input_dir, file)) as f:
            data = f.read().split("\n\n")

        # create file for output
        with open(os.path.join(output_dir, f'{file}-output.txt'), "w") as newF:
            des = data[0]
            newF.write(f"{des}:\n\n")

            write_actions(data[1].strip().split("\n"), newF)
            write_mechanisms(data[2].strip().split("\n"), newF)
            write_utilities(data[3], newF)
            write_best_choice(data[3], newF)
            write_intention(data[2].strip().split("\n"), key, newF)

    print("Outputs saved successfully in output directory...")


if __name__ == "__main__":
    main()