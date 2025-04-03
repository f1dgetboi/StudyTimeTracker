import Gui
import pygame, sys 
from pygame import *
import time
import random
from datetime import date,timedelta

Gui.create_window(Gui.monitor_size[0],Gui.monitor_size[1],(255,255,255),"Time keeper")
shakai_time = 0
mainClock = pygame.time.Clock()
rika_time = 0
kokugo_time = 0
suugaku_time = 0
today = date.today()
weekday = today.isoweekday()
print(weekday)
week_study_time = [0,0,0,0]
BUTTON_COLORS = (225, 217, 209)
BUTTON_DIMENSIONS = (300,50)
LEFT = (Gui.monitor_size[0] /4 -380, Gui.monitor_size[1] /2 -250) 
MIDDLE_LEFT = (Gui.monitor_size[0] /4 *2 -400, Gui.monitor_size[1] /2 +300)
MIDDLE_RIGHT = (Gui.monitor_size[0] /4 *3 -400, Gui.monitor_size[1] /2)
RIGHT = (Gui.monitor_size[0] /4 *4 -400, Gui.monitor_size[1] /2)
shakai_button = Gui.Button(BUTTON_DIMENSIONS[0],BUTTON_DIMENSIONS[1],LEFT[0],MIDDLE_LEFT[1],BUTTON_COLORS,text="shakai start",fontsize=50,text_offset_x=20,text_offset_y=-20)
rika_button = Gui.Button(BUTTON_DIMENSIONS[0],BUTTON_DIMENSIONS[1],MIDDLE_LEFT[0],MIDDLE_LEFT[1],BUTTON_COLORS,text="rika start",fontsize=50,text_offset_x=50,text_offset_y=-20)
kokugo_button = Gui.Button(BUTTON_DIMENSIONS[0],BUTTON_DIMENSIONS[1],MIDDLE_RIGHT[0],MIDDLE_LEFT[1],BUTTON_COLORS,text="kokugo start",fontsize=50,text_offset_x=20,text_offset_y=-20)
suugaku_button = Gui.Button(BUTTON_DIMENSIONS[0],BUTTON_DIMENSIONS[1],RIGHT[0],MIDDLE_LEFT[1],BUTTON_COLORS,text="suugaku start",fontsize=50,text_offset_x=10,text_offset_y=-20)
end_button = Gui.Button(BUTTON_DIMENSIONS[0],BUTTON_DIMENSIONS[1],MIDDLE_LEFT[0] + 100,MIDDLE_LEFT[1],BUTTON_COLORS,text="End",fontsize=50,text_offset_x=150,text_offset_y=-20)
current_context =  "select menu"
timer_type = None
start = 0
r_num = random.randint(0,2)
if r_num == 1:
    r = random.randint(0,255)
    g = 255 - r
    b = random.randint(0,255)
elif r_num == 2:
    g = random.randint(0,255)
    b = 255 - g
    r = random.randint(0,255)
else:
    b = random.randint(0,255)
    r = 255 - b
    g = random.randint(0,255)
change_time = time.time()
target_color = (r,g,b)
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops= -1)

def convert_string(num):
    hours = 0
    minutes = 0
    seconds = 0
    if num >= 60:
        if num >= 3600:
            hours = num // 3600
        minutes = (num - (hours * 3600))// 60
    seconds = num - (hours * 3600) - (minutes * 60)
    return f"{hours}:{minutes}:{seconds}"

def get_study_time(subject):
        week_time = 0
        today_time = 0
        for i in range(weekday):
            day = today - timedelta(days=i)
            try:
                with open(f'{day}.txt', 'r') as f:
                    content = f.readlines()
                    if day == today:
                        if subject == "shakai":
                            today_time += int(content[1])
                        if subject == "rika":
                            today_time += int(content[2])   
                        if subject == "kokugo":
                            today_time += int(content[3])   
                        if subject == "suugaku":
                            today_time += int(content[4]) 
                    if subject == "shakai":
                        week_time += int(content[1])
                    if subject == "rika":
                        week_time += int(content[2])   
                    if subject == "kokugo":
                        week_time += int(content[3])   
                    if subject == "suugaku":
                        week_time += int(content[4])        
                print(day)
            except:
                print("No data")
        return week_time,today_time


week_study_time[0] = get_study_time("shakai")[0]
shakai_time = get_study_time("shakai")[1]
week_study_time[1] = get_study_time("rika")[0]
rika_time = get_study_time("rika")[1]
week_study_time[2] = get_study_time("kokugo")[0]
kokugo_time = get_study_time("kokugo")[1]
week_study_time[3] = get_study_time("suugaku")[0]
suugaku_time = get_study_time("suugaku")[1]

def extract_data(start_date,end_date):
    try:
        start_date = date(2008, 8, 15) 
        end_date = date(2008, 9, 15)    # perhaps date.now()

        delta = end_date - start_date   # returns timedelta

        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            print(day)
    except:
        print("No viable data")

def event_listen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open(f'{today}.txt', 'w') as f:
                #f.write(f'Y is: {testsubject.y} X is: {testsubject.x} width is: {testsubject.w} height is: {testsubject.h}')
                f.write(f'shakai:{shakai_time}, rika:{rika_time}, kokugo:{kokugo_time}, suugaku:{suugaku_time}\n{shakai_time}\n{rika_time}\n{kokugo_time}\n{suugaku_time}')
            pygame.quit()
            sys.exit()

    surf = pygame.transform.scale(Gui.screen,(Gui.monitor_size))
    Gui.display.blit(surf,(0,0))
    pygame.display.update()

def change_over_time(end_color,start_time):
    current_color = (255,255,255)
    current_color = (int((end_color[0] / 60)*abs(time.time()-start_time)),int((end_color[1] / 60)*abs(time.time() -start_time)),int((end_color[2] / 60)*abs(time.time() -start_time)))
    print(current_color)
    return current_color
def drawtoScreen():
    global current_context, shakai_time,rika_time,kokugo_time,suugaku_time,start,timer_type,change_time,target_color,loop_time
    Gui.screen.fill((255,255,255)) 
    if current_context == "select menu":
        shakai_frame = Gui.buy_frame(LEFT[0], LEFT[1], BUTTON_COLORS, f"shakai day: {convert_string(shakai_time)}", f"shakai week: {convert_string(week_study_time[0])}", "image.png")
        rika_frame = Gui.buy_frame(MIDDLE_LEFT[0], LEFT[1], BUTTON_COLORS, f"rika day: {convert_string(rika_time)}", f"rika week: {convert_string(week_study_time[1])}", "image.png")
        kokugo_frame = Gui.buy_frame(MIDDLE_RIGHT[0], LEFT[1], BUTTON_COLORS, f"kokugo day: {convert_string(kokugo_time)}", f"kokugo week: {convert_string(week_study_time[2])}", "image.png")
        suugaku_frame = Gui.buy_frame(RIGHT[0], LEFT[1], BUTTON_COLORS, f"suugaku day: {convert_string(suugaku_time)}", f"suugaku week: {convert_string(week_study_time[3])}", "image.png")
        shakai_frame.draw()
        rika_frame.draw()
        kokugo_frame.draw()
        suugaku_frame.draw()
        shakai_button.draw()
        rika_button.draw()
        kokugo_button.draw()
        suugaku_button.draw()
        shakai_button.check_clicks()
        rika_button.check_clicks()
        kokugo_button.check_clicks()
        suugaku_button.check_clicks()  
        if rika_button.clicked:
            timer_type = "rika"
            current_context = "timer_screen"
            rika_button.clicked = False
            start = time.time()
            loop_time = 1
        if shakai_button.clicked:
            timer_type = "shakai"
            current_context = "timer_screen"
            start = time.time()
            shakai_button.clicked = False
            loop_time = 1
        if kokugo_button.clicked:
            timer_type = "kokugo"
            current_context = "timer_screen"
            start = time.time()
            kokugo_button.clicked = False
            loop_time = 1
        if suugaku_button.clicked:
            timer_type = "suugaku"
            current_context = "timer_screen"
            start = time.time()
            suugaku_button.clicked = False
            loop_time = 1
    if current_context == "timer_screen":
        end_button.draw()
        end_button.check_clicks()
        current = time.time()
        sum_time = int(current - start)
        if (sum_time % 60) == 0 :
            r_num = random.randint(0,2)
            if r_num == 1:
                r = random.randint(0,255)
                g = 255 - r
                b = random.randint(0,255)
            elif r_num == 2:
                g = random.randint(0,255)
                b = 255 - g
                r = random.randint(0,255)
            else:
                b = random.randint(0,255)
                r = 255 - b
                g = random.randint(0,255)

            target_color = (r,g,b)
            change_time = current
        print(target_color)
        Gui.screen.fill(change_over_time(target_color,change_time)) 
        text_color = (255 - change_over_time(target_color,change_time)[0],255 - change_over_time(target_color,change_time)[1],255-change_over_time(target_color,change_time)[2])
        if timer_type == "rika":
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 ,f"Day time:{convert_string(rika_time + sum_time)}")
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 +100,f"week time:{convert_string(week_study_time[1] + sum_time)}")
        if timer_type == "shakai":
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 ,f"Day time:{convert_string(shakai_time + sum_time)}")
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 +100,f"week time:{convert_string(week_study_time[0] + sum_time)}")
        if timer_type == "suugaku":
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 ,f"Day time:{convert_string(suugaku_time + sum_time)}")
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 +100,f"week time:{convert_string(week_study_time[3] + sum_time)}")
        if timer_type == "kokugo":
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 ,f"Day time:{convert_string(kokugo_time + sum_time)}")
            Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 +100,f"week time:{convert_string(week_study_time[2] + sum_time)}")
        Gui.create_center_text(Gui.DEFAULT_FONT,100,text_color,Gui.monitor_size[0]/2,Gui.monitor_size[1]/2 -100,f"study session:{convert_string(sum_time)}")

        if end_button.clicked == True:
            if timer_type == "rika":
                rika_time += sum_time
                week_study_time[1] += sum_time
            if timer_type == "shakai":
                shakai_time += sum_time
                week_study_time[0] += sum_time
            if timer_type == "suugaku":
                suugaku_time += sum_time
                week_study_time[3] += sum_time
            if timer_type == "kokugo":
                kokugo_time += sum_time
                week_study_time[2] += sum_time
            current_context = "select menu"
            end_button.clicked = False
        


def main():
    while True:
        drawtoScreen()
        event_listen()
        mainClock.tick(30)
main()