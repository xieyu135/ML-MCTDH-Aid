
import re

from tree import rebuildRightTreeLines
#from primitive_cvg import npbasisCvg

pop_thre = 0.99999
input_f = open("input", "r")
output_f = open("output", "r")
new_input_file = ""

input0 = []
input1 = []
input2 = []
nbasis = []
nbranch_node = []
natPopMax = []
output = []

i = 0
while True:
    line = input_f.readline()
    if not line:
        break
    line = line.rstrip()

    if "mlbasis-section" in line and "end-mlbasis-section" not in line:
        input0.append(line)
        i = 1
        line = input_f.readline().rstrip()

    if "end-mlbasis-section" in line:
        i = 2

    if "end-input" in line:
        input2.append(line)
        break

    if i == 0:
        if "name " in line and "opname" not in line:
            # print(line)
            args = line.split("-")
            if len(args)<2:
                itmp = 1
            else:
                itmp = int(args[1]) + 1
            line = f"{args[0]}-{itmp}"
            args = line.split(" = ")
            new_input_file = f"{args[1]}.inp"
        input0.append(line)
    elif i == 1:
        if "el" in line or "a" in line:
            nbasis.append([0])
            nbranch_node.append(0)
        else:
            args = line.split("> ")
            args = args[1].split(" ")
            nbranch = len(args)
            nbasis.append(args)
            nbranch_node.append(nbranch)
        input1.append(line)
    elif i == 2:
        input2.append(line)
# print(nbasis)
# print(nbranch_node)
# for line in input0:
    # print(line)
# for line in input1:
    # print(line)
# for line in input2:
    # print(line)
input_f.close()

output = output_f.readlines()
output = [line.rstrip() for line in output]
# output = 

for inode in range(len(nbasis)):
    nb = nbasis[inode][0]
    if nb==0:
        # natPopMax[inode] = 0
        natPopMax.append(0)
        continue
    else:
        natPopMax.append([])
    for j in range(len(nbasis[inode])):
        nb = int(nbasis[inode][j])
        natPopMax[inode].append([])
        for k in range(nb):
            # natPopMax[inode][j][k] = 0
            natPopMax[inode][j].append(0)
# print(natPopMax)

i_output = 0
#print(len(output))
for i_output in range(len(output)):
    line = output[i_output]
    if "node:" in line:
        res  = re.findall(r'node: *([0-9]+)', line)
        inode1 = int(res[0])
        inode = inode1 - 1
        for j in range(len(nbasis[inode])):
            nb = nbasis[inode][j]
            nb = int(nb)
            n = (nb - 1) // 7 + 1
            iop = i_output + 1
            ied = i_output + n
            line1 = "".join(output[iop:ied + 1])
            arg = line1.split(":")[1].split()
            arg = [float(x) for x in arg]
            for k in range(len(arg)):
                tmp = natPopMax[inode][j][k]
                tmp = max(arg[k], tmp)
                natPopMax[inode][j][k] = tmp
            i_output = ied

precision0 = 0.0005
for inode in range(1, len(natPopMax)):
    if nbasis[inode][0] == 0:
        continue
    elif nbasis[inode + 1][0] == 0:
        precision = precision0
    else:
        precision = precision0 * 10
    for j in range(len(natPopMax[inode])):
        for k in range(len(natPopMax[inode][j]) - 1, 0, -1):
            tmp = natPopMax[inode][j][k]
            tmp1 = natPopMax[inode][j][k - 1]
            if tmp < precision and tmp1 < precision:
                continue
            elif tmp < precision and tmp1 >= precision:
                nbasis[inode][j] = k + 1
                break
            else:
                kmax = 10
                m = 2 ** (kmax - 1)
                if tmp >= precision * 2 * m:
                    nbasis[inode][j] = k + kmax + 1
                else:
                    for im in range(1, kmax + 1):
                        m = 2 ** (im - 1)
                        if tmp < precision * 2 * m:
                            nbasis[inode][j] = k + 1 + im
                            break
# print(nbasis)
for inode in range(1, len(nbasis)):
    if nbasis[inode][0] == 0:
        continue
    line = " ".join(map(str, nbasis[inode]))
    args = input1[inode].split(">")
    input1[inode] = args[0] + "> " + line
# print(input1)
input1 = rebuildRightTreeLines(input1)
# print(input1)
new_input_f = open(new_input_file, "w")
for line in input0:
    new_input_f.write(line + "\n")
for i in range(len(nbasis)):
    # print(input1[i])
    new_input_f.write(f'{input1[i]}\n')
for line in input2:
    new_input_f.write(f'{line}\n')
new_input_f.close()
output_f.close()


#npbasisCvg(new_input_file, pop_thre)
