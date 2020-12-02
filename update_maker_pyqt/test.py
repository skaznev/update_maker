import os
for i in os.listdir(r'''X:\Инверсия\ФОНД\U\FUND_DB\TEST'''):
    drs = os.path.join(r'''X:\Инверсия\ФОНД\U\FUND_DB\TEST''', i)
    if not os.path.isfile(drs):
        if ('RELEASE' in drs) or ('READY_TO_RELEASE' in drs):
            continue
        for ffiles in os.listdir(drs):
            path_d = os.path.join(drs,ffiles)
            if os.path.isfile(path_d):
                if 'TR_TOOL_METADATA' in ffiles:
                    print(path_d)
        