import os
for file in os.listdir():
    if file.endswith('.ui'):
        os.system('pyside6-uic {} > ui_{}.py'.format(file,file[:-3]))