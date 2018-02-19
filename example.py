# -*- coding: utf-8 -*-
import gspeech
import time
import os
import sys
import urllib.request
import json
import RPi.GPIO as GPIO
import pygame
import random
from playsound import playsound
room1_led=3
room2_led=15

servo_pin=18  # PWM pin num 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
GPIO.setup(room1_led,GPIO.OUT)
GPIO.setup(room2_led,GPIO.OUT)
p=GPIO.PWM(servo_pin,50)
p.start(0)
cnt=0
GPIO.output(room1_led,False)
GPIO.output(room2_led,False)

def play_sound(voice_str):
    client_id = "J4nyQYb8vkIhoLySTQEj"
    client_secret = "7LvKayq7sk"
    encText = urllib.parse.quote(voice_str)
    data = "speaker=mijin&speed=0&text=" + encText;
    url = "https://openapi.naver.com/v1/voice/tts.bin"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('1111.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
def sound_play():
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load('1111.mp3')
    pygame.mixer.music.play()
    time.sleep(5)
    
    
def weather_sound():
    map_name='kunsan'
    data=urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+map_name+'&APPID=98ab6e8daf80d505055cc70aea776564')
    m=data.read()
    DB=json.loads(m.decode('utf-8'))
    climate=DB['weather']
    weather=climate[0]['main']
    hot=DB['main']
    temp=hot['temp']-273.15
    kor_weather=''
    if('clear' in weather):
        kor_weather='맑          고'
    elif('haze' in weather):
        kor_weather='옅          은           안          개          가           끼          고.'
    elif('cloud' in weather or 'Cloud' in weather):
        kor_weather='구름이 끼고'
    elif('rain' in weather):
        kor_weather='비          가           오          고'
    elif('mist' in weather):
        kor_weather='안          개          가           많          이           끼          고'
    elif('snow' in weather):
        kor_weather='눈           이         오         고 '
    elif('wind' in weather):
        kor_weather='바람이 붑니다.'
    print(weather)
    weather_str='오         늘           날          씨         는           '+kor_weather+'          온                 도                  는'+str(temp)+'          도          입          니          다.'
    play_sound(weather_str)

  # webbrowser.open('1111.mp3')
    #playsound('/home/pi/Downloads/1111.mp3')
    sound_play()
    
def main():
    gsp = gspeech.Gspeech()
   
    while True:
        # 음성 인식 될때까지 대기 한다.
        
        stt = gsp.getText()
        if stt is None:
            break
        print(stt)
        time.sleep(0.01)
        if('첫 번째' in stt and '방' in stt and '켜' in stt):
            print("첫 번째 방 불 킵니다")
            str="첫               번             째           방           불               킵      니           다"
            GPIO.output(room1_led,True)
            play_sound(str)
            sound_play()
           
        if('첫 번째' in stt and '방' in stt  and '꺼' in stt):
            print("첫 번째 방 불끕니다")
            str="첫               번             째           방           불     끕      니           다"
            GPIO.output(room1_led,False)
            play_sound(str)
            sound_play()
           
        if('두 번째' in stt and '방' in  stt and '켜' in stt):
            print("두 번째 방 불킵니다")
            str="두               번             째           방           불     킵      니           다"
            GPIO.output(room2_led,True)
            play_sound(str)
            sound_play()
            
        if('두 번째' in stt and '방' in stt and '꺼' in stt):
            print("두 번째 방 불끕니다")
            str="두               번             째           방           불     끕      니           다"
            GPIO.output(room2_led,False)
            play_sound(str)
            sound_play()
           
        if('외출' in stt):
            print("모든 방 불끕니다")
            str="모               든            방           불        끕         니           다"
            GPIO.output(room2_led,False)
            GPIO.output(room1_led,False)
            play_sound(str)
            sound_play()
            
        if('날씨' in stt):
            weather_sound()
        if('메뉴' in stt or ('먹지' in stt or '음식' in stt or '먹어' in stt or '먹을' in stt)):
            food_menu=['한식','양식','중식','밥버거','햄버거','빵']
            food=random.choice(food_menu)
            str=food+' 은 어떤가요?'
            play_sound(str)
            sound_play()
            stt=gsp.getText()
            
                
            if '다른거' in stt or '딴 거' in stt:
                while '다른거' in stt or '딴거' in stt:
                    stt=gsp.getText()
                    food_index=food_menu.index(food)
                    food_menu.remove(food)
                    food=random.choice(food_menu)
                    str=food+' 은 어떤가요?'
                    play_sound(str)
                    sound_play()
                    if('그거' in stt and ('먹을래' in stt or '먹자' in stt or'먹' in stt)):
                        str='맛있게 드세요'
                        play_sound(str)
                        sound_play()
            else:
                    str='맛있게 드세요'
                    play_sound(str)
                    sound_play()
                    
     
        if('문' in stt and '열어' in stt):
            str="문을 엽니다."
            p.start(12.5)
            time.sleep(0.5)
            p.stop()
            play_sound(str)
           
        elif('문' in stt and ('닫어' in stt or '닫아' in stt)):
             p.start(7.5)
             time.sleep(0.5)
             p.stop()
             str="문을 닫습니다."
             play_sound(str)
        if ('끝내자' in stt):
            str="다음에 전원을 켜주세요. 잘있어요"
            play_sound(str)
            time.sleep(0.5)
            sound_play()
            break
            #sys.exit(1)
        stt=''

if __name__ == '__main__':
    main()