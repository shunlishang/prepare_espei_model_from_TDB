import re, os 
import numpy as np
import json
import glob
from bisect import bisect_left, insort
###################################################################################
def find_model_from_eachline(aa_lines, phase):
    for line in aa_lines:         
        if line == '': continue
        if line[0] == '$': continue    
        if 'CONST' in line:
            cc = line.split()
            pp = cc[1]; pp = re.split(':', pp)[0]           
            if pp == phase: 
                #print('here=pp, cc[1]=', pp)                
                if pp+':' in cc[1]:  
                    pp2 = pp+':'; print('pp2=', pp2)
                    line2=re.sub(pp2, phase, line)
                else:                
                    line2=line                                                                 
                aa=re.sub(r'%', '', line2)                
                #print('line=', aa)
                dd = aa.split(':')
                model = dd[1:-1]                 
                #print('model=', dd, model)
    return model  
    
######
def dedup(seq):
    # Remove duplicates. Preserve order first seen. Assume orderable, but not hashable elements'
    result = []
    seen = []
    for x in seq:
        i = bisect_left(seen, x)
        if i == len(seen) or seen[i] != x:
            seen.insert(i, x)
            result.append(x)
    return result
##------------
   
def To_write_json_file(in_dict, out_json_file):
    with open(out_json_file, 'w') as f:
        f.write('{\n')
        f.write('  "components": ')
        f.write(json.dumps(in_dict.get('components')))
        f.write(',\n  "refdata": ');               
        f.write(json.dumps(in_dict.get('refdata')))
        f.write(',\n  "phases": {'); 
        ###########
        mykey = [k for k in in_dict.get('phases').keys()]
        #mykey = in_dict.get('phases').keys() this one is NOT what I wanted
        #print('mykey===', mykey)
        nn=len(mykey)-1
        for i in range(nn):
            f.write('\n    "'+mykey[i]+'": \n       ')                        
            f.write(json.dumps(in_dict.get('phases').get(mykey[i])))
            f.write(',')
        f.write('\n    "'+mykey[-1]+'": \n       ') 
        f.write(json.dumps(in_dict.get('phases').get(mykey[-1]))) 
        #########
        f.write('\n  }')
        f.write('\n}')
        f.write('\n')
    f.close()

####
def To_write_phases_file(mykey, out_text_file):
    with open(out_text_file, 'w') as f:
        f.write('\n')
        f.write('all_phase_names:')                
        nn=len(mykey)
        for i in range(nn):
            if type(mykey[i][1]) == str:
                f.write('\n  - ' + mykey[i][1] + '  # no. ' + str(mykey[i][0]))
            if type(mykey[i][1]) == list:
                #print('mykey[i][1]=',mykey[i][1])
                f.write('\n  - [' + mykey[i][1][0] + ', ' + mykey[i][1][1] + ']  # no. ' + str(mykey[i][0]))
        f.write('\n')
        f.write('\nphase_list:')
        for i in range(nn):
            if type(mykey[i][1]) == str:
                f.write('\n  - ' + str(mykey[i][0]) + '  # for phase ' + mykey[i][1])
            if type(mykey[i][1]) == list:
                f.write('\n  - ' + str(mykey[i][0]) + '  # for phase ['+ mykey[i][1][0] + ', ' + mykey[i][1][1] + ']')
        f.write('\n')
    f.close()

####
def find_order_disorder_phases(line):
    cc = line.split();  # print('xxxxcc=', cc)
    #print('find_odo_phases in func, cc4, cc6:', cc[4], cc[6])
    disphase = cc[6].split(',')[0]
    #print('find_odo_phases in func:', cc[4], dd)
    return disphase, cc[4]

## end of funcitons    end of funcitons  end of funcitons  end of funcitons   
###############################################################################
###############################################################################
    
current_directory_files = os.listdir('.')
for fname in current_directory_files:
    asdf = fname[-4:].upper(); # print('file name=', asdf)
    if asdf == '.TDB':
        tdbfile = fname
        break
#########
my_file=open(tdbfile,'r')       # open TDB to read 
textp  = my_file.read()         # read TDB file        

aa_lines = textp.split('\n');   #print( 'len of aa_lines = ', len(aa_lines))

nn=0; myphase=[]; myratio =[]; mymodel=[]; myodo = []; list_all_odo =[]; list_ordered = []
for line in aa_lines:   
    if line == '': continue
    if line[0] == '$': continue
    if ' PHASE ' in line or '/nPHASE ' in line: 
        cc = line.split(); #print('xxxxcc=', cc)
        pp = cc[1]; pp = re.split(':', pp)[0]
        ratio = cc[4:-1];  #print('here, ratio=', ratio)
        ratio = [float(x) for x in ratio]  
        mmm = find_model_from_eachline(aa_lines, pp)   # cc[1] may with :
        myphase.append(pp)
        myratio.append(ratio)
        mymodel.append(mmm)
    if ' GES ' in line and ' DIS' in line:
        phase1, phase2 = find_order_disorder_phases(line)  # disorder phase first, ordered second
        myodo.append([phase1, phase2])
        list_all_odo.extend([phase1, phase2])
        list_ordered.append(phase2)

#print('myphase=', myphase)
#print('myratio=', myratio)
#print('mymodel=', mymodel)
print(); print('list_ordered = ', list_ordered)

if len(myodo) > 0:
    print(); print('disorder-order phases=', myodo); #print('disorder-order ALL phases=', list_all_odo)
    print()

newmodel=[]; elems=[]
for i in range(len(mymodel)):
    aa=[]         
    for k in range(len(mymodel[i])):
        bb=mymodel[i][k].split(',')                
        bb = [x.replace(' ', '') for x in bb]
        aa.append(bb)
        elems.extend(bb)
    newmodel.append(aa)    
        
#print('new_model=', newmodel)
#print('all-elems=', elems)

#unique_elem = set(elems)
#unique_elem = [x for x in unique_elem]

unique_elem = dedup(elems)
unique_elem = sorted(unique_elem)
print('unique_elem=', unique_elem); print()

##===================================================
dict_phase={}
for i in range(len(myphase)):
    jj = 0
    for k in range(len(myodo)):
        if myphase[i] == myodo[k][1]:
            jj = 1
            here_odo = myodo[k]
            print(); print('find odo phases =', here_odo)
            break
    if jj == 0:
        dict1 = dict(sublattice_model=newmodel[i], sublattice_site_ratios=myratio[i])
    if jj == 1:
        dict1 = dict(sublattice_model=newmodel[i], sublattice_site_ratios=myratio[i], disorder_order=here_odo)

    dict_phase[myphase[i]] = dict1
    #print('xxx=', phase1, len(phase1))
   
print('*** number of total phases = ', len(dict_phase)); print()
#print('here_dict_phase=', dict_phase)

my_final_dict = dict(components=unique_elem, refdata='SGTE91', phases=dict_phase)

out_json_file = 'INPUT+MODEL.json'
To_write_json_file(my_final_dict, out_json_file)

###################
out_text_file = 'phase_list_for_reference.txt'
mykey = [k for k in my_final_dict.get('phases').keys()]
mykey_num=[]; n=0
for i in range(len(mykey)):
    if mykey[i] not in list_all_odo:
        n = n + 1
        mykey_num.append([n, mykey[i]])
for j in range(len(myodo)):
    n = n +1
    mykey_num.append([n, myodo[j]])
####
print(); print('mykey_num=', mykey_num)

To_write_phases_file(mykey_num, out_text_file)


####################
#
print()
print('###############################')
print('The TDB file used in this code is:', tdbfile)
print('NOTE: I read the first TDB file in this folder')
print()
print('update 2019-12-17: write down some notes, add odo information')
print()
print('##### THE END #####')
print()
