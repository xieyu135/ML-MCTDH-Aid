
import re

# 处理input文件
with open("input", "r") as input_file:
    input_lines = input_file.readlines()

iinput = []
input0 = []
nbasis1 = []
nbasis2 = []
input2 = []
i = 0
opt_input_file = None

for line in input_lines:
    line = line.strip('\n')  # 删除行尾的换行符

    if "mlbasis-section" in line:
        i = 1
    if "end-mlbasis-section" in line:
        i = 2
    if "end-input" in line:
        input2.append(line)
        i = 3
        break  # 退出循环

    if i == 0:
        if "name" in line and "opname" not in line:
            args = line.split("-")
            line = f"{args[0]}_opt-1"
            args = line.split(" = ")
            opt_input_file = f"{args[1]}.inp"
            print(opt_input_file)
        input0.append(line)
    elif i == 1:
        if "el" in line or "a" in line:
            nbasis1.append(0)
            nbasis2.append(0)
        else:
            args = line.split("> ")
            args = args[1].split()
            nbasis1.append(int(args[0]))
            nbasis2.append(int(args[1]))
        iinput.append(line)
    elif i == 2:
        input2.append(line)

# # 打印结果，如果需要的话
# print("Input:", iinput)
# print("Input0:", input0)
# print("Nbasis1:", nbasis1)
# print("Nbasis2:", nbasis2)
# print("Input2:", input2)

# 处理output文件 
with open("output", "r") as output_file:  
    output_lines = output_file.readlines()  
  
# 过滤掉包含 "<q>=" 的行，并将其他行存储在 output 列表中  
output = [line.strip() for line in output_lines if "<q>=" not in line]  
  
# # 打印结果，如果需要的话  
# print("Filtered Output:")  
# for line in output:  
    # print(line)
    
nbasis1Org = nbasis1[:]  # 通过切片操作复制列表内容  
nbasis2Org = nbasis2[:]  # 通过切片操作复制列表内容  

for i in range(3,len(nbasis1)):
    ## 提取natPopMax
    nb1 = nbasis1[i]
    nb2 = nbasis2[i]
    if nb1==0:
        continue
    natPopMax1 = [0] * nb1
    natPopMax2 = [0] * nb2
    n1 = int((nb1-1)/7) + 1
    n2 = int((nb2-1)/7) + 1
    for i_output, line in enumerate(output):  
        # 检查当前行是否包含 "node: *数字 " 格式的文本  
        if re.search(rf'node: *{i} ', line):  
            # 获取下一块文本的开始和结束索引  
            j1 = i_output + 1  
            j2 = i_output + n1  
              
            # 拼接指定范围内的行，并按冒号分割，然后再次按空格分割第二部分  
            line1 = ' '.join(output[j1:j2+1])  
            arg1 = line1.split(':')  
            arg1_part2 = arg1[1].split()  
              
            # 更新 natPopMax1 列表中的最大值  
            for j in range(len(arg1_part2)):  
                natPopMax1[j] = max(natPopMax1[j], float(arg1_part2[j]))  
              
            # 获取下一块文本的开始和结束索引  
            j1 = j2 + 1  
            j2 = j2 + n2  
              
            # 拼接指定范围内的行，并按冒号分割，然后再次按空格分割第二部分  
            line2 = ' '.join(output[j1:j2+1])  
            arg2 = line2.split(':')  
            arg2_part2 = arg2[1].split()  
              
            # 更新 natPopMax2 列表中的最大值  
            for j in range(len(arg1_part2)):  
                natPopMax2[j] = max(natPopMax2[j], float(arg2_part2[j]))  

    ## 获得节点基组数
    j = len(natPopMax1) - 1  
    tmp0 = natPopMax1[j]  
      
    precision = 0.05  
      
    if tmp0 < precision:  
        for j in range(len(natPopMax1) - 1, -1, -1):  
            tmp1 = natPopMax1[j]  
            if tmp1 < precision:  
                continue
            elif tmp1 >= precision:  
                nbasis1[i] = j + 2  
                break
    else:  
        kmax = 10  
        m = 2 ** (kmax - 1)  
        if tmp0 >= precision * 2 * m:  
            nbasis1[i] += kmax + 1  
        else:  
            for k in range(1, kmax + 1):  
                m = 2 ** (k - 1)  
                if tmp0 < precision * 2 * m:  
                    nbasis1[i] += k  
                    break  

    j = len(natPopMax2) - 1  
    tmp0 = natPopMax2[j]  
      
    if tmp0 < precision:  
        for j in range(len(natPopMax2) - 1, -1, -1):  
            tmp1 = natPopMax2[j]  
            if tmp1 < precision:  
                continue  # 对应 Perl 中的 next  
            elif tmp1 >= precision:  
                nbasis2[i] = j + 2  
                break  # 对应 Perl 中的 last  
    else:  
        kmax = 10  
        m = 2 ** (kmax - 1)  
        if tmp0 >= precision * 2 * m:  
            nbasis2[i] += kmax + 1  
        else:  
            for k in range(1, kmax + 1):  
                m = 2 ** (k - 1)  
                if tmp0 < precision * 2 * m:  
                    nbasis2[i] += k  
                    break
# print(nbasis1)
# print(nbasis2)
## 确定mode节点的基组数
i = 3  
mode = []
nbasis_mode = []
while i <= len(nbasis1) - 1:  
    if nbasis1[i] == 0:  
        line = iinput[i]  
        args = line.split("[")  # 分割字符串  
        args = args[1].split("]")  # 再次分割字符串并取第二个部分  
        mode.append(args[0])  # 将结果添加到mode列表  
        nbasis_mode.append(nbasis1[i - 1])  # 将结果添加到nbasis_mode列表  
        i += 1  
          
        # 检查下一个元素是否为0，并做相应处理  
        if nbasis1[i] == 0:  
            line = iinput[i]  
            args = line.split("[")  
            args = args[1].split("]")  
            mode.append(args[0])  
            nbasis_mode.append(nbasis2[i - 2])
            i += 1  
        else:  
            i += 1  
            line = iinput[i]  
            args = line.split("[")  
            args = args[1].split("]")  
            mode.append(args[0])  
            nbasis_mode.append(nbasis2[i - 1])  # 注意索引调整  
            i += 1  
              
            line = iinput[i]  
            args = line.split("[")  
            args = args[1].split("]")  
            mode.append(args[0])  
            nbasis_mode.append(nbasis2[i - 2])  # 注意索引调整  
            i += 1  
    else:  
        i += 1  

pairs = zip(mode, nbasis_mode)
pairs = sorted(pairs, key=lambda x:x[1], reverse=True)
nbasis_mode = [ nbasis for m, nbasis in pairs ]
mode = [ m for m, nbasis in pairs ]
print(pairs)
'''
n = len(nbasis_mode) - 1  
for j in range(1, n + 1):
    a = nbasis_mode.pop(j - 1)
    b = mode.pop(j - 1)  
      
    for i in range(j - 2, -1, -1):  
        if nbasis_mode[i] > a:  
            # 使用insert在指定索引处插入元素，类似于Perl中的splice  
            nbasis_mode.insert(i + 1, a)  
            mode.insert(i + 1, b)  
            break  # 对应Perl中的last  
        else:  
            if i > 0:  
                continue  # 对应Perl中的next  
            else:  
                nbasis_mode.insert(i, a)  
                mode.insert(i, b)  
'''

sum_ = sum(nbasis_mode)  # 计算列表元素的总和  
sum_half = sum_ / 2  # 计算总和的一半  
sum1 = 0  # 用于在循环中累加元素  
index = []  # 用于存储满足条件的索引  
  
for i in range(len(nbasis_mode)):  
    nb = nbasis_mode[i]  
    sum1 += nb  
    if sum1 > sum_half:  
        # 判断索引是否满足整除条件  
        if i // 2 == (i - 1) // 2:  
            index.append(i)  
            break
        else:  
            i += 1  # 手动递增索引，因为Python的for循环不会允许直接修改循环变量  
            if i < len(nbasis_mode):  # 确保索引没有超出列表范围  
                nb = nbasis_mode[i]  
                sum1 += nb  
                index.append(i)  
                break

sum1_half = sum1 / 2  # 计算sum1的一半  
sum2 = 0  # 用于在循环中累加元素  

for i in range(len(nbasis_mode)):  
    nb = nbasis_mode[i]  
    sum2 += nb  
    if sum2 > sum1_half:  
        # 判断索引是否满足整除条件  
        if i // 2 == (i - 1) // 2:  
            index.append(i)  
            break  # 对应Perl中的last  
        else:  
            i += 1  # 手动递增索引，因为Python的for循环不会允许直接修改循环变量  
            if i < len(nbasis_mode):  # 确保索引没有超出列表范围  
                nb = nbasis_mode[i]  
                sum2 += nb  
                index.append(i)  
                break  # 对应Perl中的last  

sum1_half = (sum_ - sum1) / 2  # 计算剩余部分的一半  
sum2 = 0  # 用于在循环中累加元素  
  
# 从index列表中的第一个元素索引的下一个位置开始遍历  
for i in range(index[0] + 1, len(nbasis_mode)):  
    nb = nbasis_mode[i]  
    sum2 += nb  
    if sum2 > sum1_half:  
        # 判断索引是否满足整除条件  
        if i // 2 == (i - 1) // 2:  
            index.append(i)  
            break  # 对应Perl中的last  
        else:  
            i += 1  # 手动递增索引，因为Python的for循环不会允许直接修改循环变量  
            if i < len(nbasis_mode):  # 确保索引没有超出列表范围  
                nb = nbasis_mode[i]  
                sum2 += nb  
                index.append(i)  
                break  # 对应Perl中的last  
   
index.sort()
index.insert(0, -1)  
#print(mode)
index.append(len(mode) - 1)  
print(index)


kmax = 10  
nlayer1 = None  # 初始化nlayer1，假设没有找到合适的值  
for i in range(1, kmax + 1):  
    m = 2 ** i  # 计算2的i次方  
    if len(index)-1 == m:  # 如果index列表的长度等于m  
        nlayer1 = i  # 将i赋值给nlayer1  
        break  # 找到后退出循环  
 
opt = open(opt_input_file, 'w')

for item in input0:  
    opt.write(str(item) + '\n')   
opt.write('mlbasis-section\n')  
opt.write('0> {} {}\n'.format(nbasis1Org[1], nbasis2Org[1]))  
opt.write('  1> [el]\n')  
  
imode = 0  
  
for j in range(1, len(index)):  
    for i in range(nlayer1, 0, -1):  
        m = 2 ** i  
        if (j - 1) % m == 0:  
            ilayer = nlayer1 - i + 1  
            i1 = ilayer  
            opt.write('  ' * i1 + f"{ilayer}> 6 6\n")  
  
    nmode_tmp = index[j] - index[j - 1]  
    kmax = 10  
    for i in range(1, kmax + 1):  
        m = 2 ** i  
        if nmode_tmp <= m:  
            nlayer_tmp = i  
            m2 = m // 2  
            nmode_extra = nmode_tmp - m2  
            break  
  
    nmode1 = m2 - nmode_extra  
    for imode_tmp in range(1, nmode_tmp + 1):  
        if imode_tmp <= nmode1:  
            n = nlayer_tmp  
            imode0 = imode_tmp - 1  
        else:  
            n = nlayer_tmp + 1  
            imode0 = imode_tmp + nmode1 - 1  
        for i in range(n - 1, 0, -1):  
            m = 2 ** i  
            if imode0 % m == 0:  
                ilayer2 = n - i  
                i1 = nlayer1 + ilayer2  
                if i > 1:  
                    opt.write('  ' * i1 + f"{i1}> 6 6\n")  
                else:  
                    nb1 = nbasis_mode[imode]  
                    nb2 = nbasis_mode[imode + 1]  
                    # opt.write('  ' * i1 + f"{i1}> {nb1} {nb1}\n")  
                    opt.write('  ' * i1 + f"{i1}> 6 6\n")  
          
        i1 = n + nlayer1  
        opt.write('  ' * i1 + f"{i1}> [{mode[imode]}]\n")  
        # tmp = str(imode + 1) + 'a'  
        # opt.write('  ' * i1 + f"{i1}> [{tmp}]\n")  
        imode += 1  

for i in range(len(input2)):  
    opt.write(f"{input2[i]}\n")  

opt.close()  


