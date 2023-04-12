#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image, ImageOps, ImageFilter
import PySimpleGUI as sg
import os
barcolor = 'white'
to_size = 512
counter = 0
enlarge_only = False
sharpen = False
 
#for img in os.listdir('E:\datasets\dataset_graphic\image\9_Graphic'):
#    if img[img.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
#        counter+=1
#print (counter)
        #print (img[img.rfind(".")+1:])
            
layout = [ [sg.Text('Путь к папке',size=(10,1)), sg.InputText('',key = 'path2folder_field', enable_events=True), sg.FolderBrowse(target='path2folder_field')], #sg.Button('Найти', key = 'openfolder')],
           [sg.Text('Размер',size=(10,1)), sg.Text('512 '), sg.CB('',default=True, enable_events=True, key='cb512'), sg.Text('   768 '), sg.CB('',default=False, enable_events=True, key='cb768')],
           [sg.Radio('','R1', enable_events=True, key = 'in_width'),sg.Text('По ширине')],
           [sg.Radio('','R1', enable_events=True, key = 'in_height'),sg.Text('По высоте')],
           [sg.Radio('','R1', default=True, enable_events=True, key = 'in_size'),sg.Text('Вписать в размер')],
           [sg.CB('', key='enlarge_only'), sg.Text('Только увеличивать')],
           [sg.CB('', key='sharpen'), sg.Text('Повысить резкость')],
           [sg.CB('', key = 'fill', default = False, enable_events=True),sg.Text('Заливка цветом   '), sg.ColorChooserButton("", visible = False, size=(2, 1), target='set_line_color', button_color=(barcolor, barcolor),border_width=1, key='set_line_color_chooser'), sg.In(barcolor, size = 10, visible=False, enable_events=True, key='set_line_color')],
           [sg.Text()],
           [sg.Button('Ok'), sg.Button('Cancel'), sg.Text('Изображений в папке: '), sg.Text(counter,key = 'counter_show')]]
window = sg.Window('Великий уравнитель', layout)

def res_in_width(img, to_size, width, height, is_fill, *argv): 
    new_width = to_size
    if argv[1]:
        if new_width > width:
            wpercent = new_width/width
            new_height = int(height*wpercent)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            if argv[2]:
                img = img.filter(ImageFilter.SHARPEN)
            if is_fill:
                color = argv[0]
                expand = int((new_width-new_height)/2)
                if expand > 0:
                    border = (0, expand, 0, expand)
                    img = ImageOps.expand(img, border=border, fill=color)
                    
    else:
        wpercent = new_width/width
        new_height = int(height*wpercent)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        if argv[2]:
            img = img.filter(ImageFilter.SHARPEN)
        if is_fill:
            color = argv[0]
            expand = int((new_width-new_height)/2)
            if expand > 0:
                border = (0, expand, 0, expand)
                img = ImageOps.expand(img, border=border, fill=color)
                
        
    return (img)

def res_in_height(img, to_size, width, height, is_fill, *argv):
    new_height = to_size
    if argv[1]:
        if new_height > height:
            wpercent = new_height/height
            new_width = int(width*wpercent)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            if argv[2]:
                img = img.filter(ImageFilter.SHARPEN)
            if is_fill:
                color = argv[0]
                expand = int((new_height-new_width)/2)
                if expand > 0:
                    border = (expand, 0, expand, 0)
                    img = ImageOps.expand(img, border=border, fill=color)
    else:
        wpercent = new_height/height
        new_width = int(width*wpercent)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        if argv[2]:
            img = img.filter(ImageFilter.SHARPEN)
        if is_fill:
            color = argv[0]
            expand = int((new_height-new_width)/2)
            if expand > 0:
                border = (expand, 0, expand, 0)
                img = ImageOps.expand(img, border=border, fill=color)
    return (img)

def img_resize (path_2_folder, to_size, mode, is_fill, *argv):
    for imagefile in os.listdir(path_2_folder):
                if imagefile[imagefile.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
                    full_path = path_2_folder+'\\'+imagefile
                    img = Image.open(full_path)
                    width, height = img.size
                    
                    if mode == 'in_width':
                        img = res_in_width(img, to_size, width, height, is_fill, *argv)

                    elif mode == 'in_height':
                        img = res_in_height(img, to_size, width, height, is_fill, *argv)
                        
                    elif mode == 'in_size':
                        if width > height:
                            img = res_in_width(img, to_size, width, height, is_fill, *argv)
                        else:
                            img = res_in_height(img, to_size, width, height, is_fill, *argv)
                    img.save(full_path)


while True:
    
    event, values = window.read()
    
    if event == 'set_line_color':    
        if values[event] == "None":
            window['set_line_color_chooser'].Update(button_color=(barcolor, barcolor))
            window['set_line_color'].Update(barcolor)
        else:
            barcolor = values[event]
            window['set_line_color_chooser'].Update(button_color=(barcolor, barcolor))
            
    if event == 'fill':
        if values[event] == True:
            window['set_line_color_chooser'].Update(visible = True)
            window['set_line_color'].Update(visible = True)
        else:
            window['set_line_color_chooser'].Update(visible = False)
            window['set_line_color'].Update(visible = False)
            
    if event == 'path2folder_field':
        counter = 0
        for imag in os.listdir(values[event]):
            if imag[imag.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
                counter+=1
                window['counter_show'].Update(counter)
        #print (counter)

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
#    if event == 'openfolder':
#        path2folder = sg.popup_get_folder('Путь к папке с изображениями', no_window = True)
#        window['path2folder_field'].update(path2folder)

    if event == 'cb768':
        if values['cb768'] == True:
            window['cb512'].update(False)
        else:
            window['cb512'].update(True)
            
    if event == 'cb512':
        if values['cb512'] == True:
            window['cb768'].update(False)
        else:
            window['cb768'].update(True)
            
    if event == 'Ok':
        enlarge_only = values['enlarge_only']
        sharpen = values['sharpen']
        if values['cb768']:
            to_size = 768
        if values['cb512']:
            to_size = 512
            
        if values['in_width'] == True:
            img_resize (values['path2folder_field'], to_size, 'in_width', values['fill'], barcolor, enlarge_only, sharpen)
                    
        elif values['in_height'] == True:
            img_resize (values['path2folder_field'], to_size, 'in_height', values['fill'], barcolor, enlarge_only, sharpen)
                    
        elif values['in_size'] == True:
            img_resize (values['path2folder_field'], to_size, 'in_size', values['fill'], barcolor, enlarge_only, sharpen)

        sg.popup_ok('Done!')
        #print()
window.close()


# In[ ]:




