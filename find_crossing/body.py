import  os
files_crossing  = ''
path_stock      = r'''X:\Инверсия\ФОНД\U\FUND_DB\TEST'''
def execute(LIST_OBJECTS):
    global files_crossing
    files_crossing = ''
    def find_file(FILE):
        print('ПОИСК ФАЙЛА')
        global files_crossing
        global path_stock
        # А теперь немного ада, но лень было делать по уму, все равно скоро отомрет
        if not FILE in ['',' ','  ']:
            for i in os.listdir(path_stock):
                verion_folder = os.path.join(path_stock, i)
                if (not os.path.isfile(verion_folder)) and not (('RELEASED' == i.upper())):
                    if 'READY_TO_RELEASE' == i.upper():
                        path_stock_r = os.path.join(path_stock, i) 
                        for i_r in os.listdir(path_stock_r):
                            verion_folder_r = os.path.join(path_stock_r, i_r)    
                            if not os.path.isfile(verion_folder_r): 
                                for file_of_version in os.listdir(verion_folder_r):
                                    root_file_vers = os.path.join(verion_folder_r,file_of_version)
                                    if os.path.isfile(root_file_vers):
                                        if file_of_version.lower() == FILE.lower():
                                            files_crossing += '\nПересечение      : ' + i_r + '\\' + file_of_version
                    else:
                        for file_of_version in os.listdir(verion_folder):
                            root_file_vers = os.path.join(verion_folder,file_of_version)
                            if os.path.isfile(root_file_vers):
                                if file_of_version.lower() == FILE.lower():
                                    files_crossing += '\nПересечение      : ' + i + '\\' + file_of_version

    for i in LIST_OBJECTS:
        find_file(i)
    return files_crossing