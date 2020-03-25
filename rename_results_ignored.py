import os

if __name__=='__main__':
    results_dir='results-new/'
    dirlist = os.listdir(results_dir)
    for csv in dirlist:
        if '不含' in csv:
            name=csv.split('.')[0].split('_')
            os.rename(results_dir+csv,results_dir+name[0]+'_'+name[1]+'.csv')
            continue 
        name=csv.split('.')[0].split('_')[0]
        os.rename(results_dir+csv,results_dir+ name+'.csv')