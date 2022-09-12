mass = [
        [False, ['exp', ['1']], ['exp', ['2']]],
        [False, False, ['exp', ['3']]],
        [False, False, ['exp', ['4']]]
        ]                 

mass2 = list(mass)

def test(list1):
    list2 = ['r']*len(list1)
    return list2

for i in mass2:
    # определение строки, где существует более одного выхода из состояния
    find = [x for x in i if isinstance(x,list)]
    if len(find)>1:
        new_val = test(find)
        ind = 0
        for z in range(len(i)):
            if i[z]:
                i[z]=new_val[ind]
                ind+=1
    else:
        for z in range(len(i)):
            i[z] =False
    
print(mass)
print(mass2)