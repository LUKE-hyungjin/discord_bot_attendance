# -*- coding:utf-8 -*-

import token
import discord
import os
import asyncio
import ast
from datetime import datetime
from pytz import timezone


class chatbot(discord.Client):

    # 프로그램이 처음 실행되었을 때 초기 구성
    async def on_ready(self):
        # 상태 메시지 설정
        # 종류는 3가지: Game, Streaming, CustomActivity
        game = discord.Game("독서실 알바")

        # 계정 상태를 변경한다.
        # 온라인 상태, game 중으로 설정
        await client.change_presence(status=discord.Status.online, activity=game)

        try:  # 에러 처리
            file = open("check.txt", "r+")  # 파일 읽기 (만약 파일이 있을 경우)
            file.close()

        except FileNotFoundError:  # 파일이 없으면
            file = open("check.txt", "w")
            file.close()

        # 준비가 완료되면 콘솔 창에 "READY!"라고 표시
        print("READY")

    # txt를 받아와서 한줄의 딕셔너리로 변환
    def modify_txt():
        with open("check.txt", "r") as f:  # 파일 읽기
            line = f.read().splitlines()  # 한줄씩 리스트에 넣기
            modify_line = ""  # 문자열 선언
            with open("check.txt", "r") as f:
                count = f.read().count("}")  # }에 갯수를 통해 줄 수 세기
                for number in range(0, count):  # 줄수만큼 for문 돌리기
                    # 그 줄의 { 와 }를 없애고 뒤에 , 붙이기
                    modify_linefirst = line[number][1:-1] + ","
                    modify_line = modify_line + modify_linefirst  # 아까 선언한 문자열에 한줄씩 넣기

            modify_line = modify_line[:-1]  # 가장 마지막 , 제거
            final_line = modify_line.ljust(
                len(modify_line)+1, '}')  # 가장 끝에 } 추가

            final_line = final_line.rjust(
                len(modify_line)+2, '{')  # 처음에 { 추가
        return final_line  # 한줄의 딕셔너리 반환

    # 봇에 메시지가 오면 수행 될 액션
    async def on_message(self, message):

        # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
        if message.author.bot:
            return None

        # 시간이 어제 날짜로 저장이 되어있으면 txt파일에 남아 있는 시간을 다 출력하고 txt파일을 초기화
        try:
            with open("check.txt", "r") as f:  # 파일 읽기
                line = chatbot.modify_txt()  # 한줄 딕셔너리 가져오기
                line = ast.literal_eval(line)
                date = datetime.now(timezone('Asia/Seoul')
                                    ).strftime("%Y-%m-%d")
                time = list(line.values())
                time = time[0][:10]
                if date != time:
                    remove_items = list(line.items())
                    # 모든 줄 다 가지고 와서 출력
                    for remove_item in remove_items:
                        author = remove_item[0]
                        time = remove_item[1]
                        date = time[:10]
                        slice_time = time[-5:]
                        last_time = datetime.strptime(slice_time, "%H:%M")
                        now_time_string = datetime.now(
                            timezone('Asia/Seoul')).strftime("%H:%M")
                        now_time = datetime.strptime(now_time_string, "%H:%M")
                        hour = str(now_time - last_time)[:-6]
                        min = str(now_time - last_time)[3:-3]
                        await message.channel.send(f'{date}\n{author} : {slice_time}~{now_time_string}({hour}시간 {min}분)')
                    file = open("check.txt", "w")
                    file.close()
        except:
            pass

        if message.content == "!start":
            author = message.author.name
            # 답변 내용 구성
            # msg에 지정된 내용대로 메시지를 전송
            await message.delete()
            msg = await message.channel.send(f'{author}님 지금부터 시작합니다.')
            await asyncio.sleep(5)
            await msg.delete()
            with open("check.txt", "r") as f:  # 파일 읽기
                line = chatbot.modify_txt()
                line = ast.literal_eval(line)
                # 사용자가 이미 있으면 넘어가기
                if author in line:
                    pass
                else:
                    time = datetime.now(
                        timezone('Asia/Seoul')).strftime("%Y-%m-%d-%H:%M")
                    text = {author: time}
                    with open("check.txt", "a") as f:  # 파일을 만들기
                        f.write(f'{text}\n')
            return None

        if message.content == "!end":
            # 파일안에 오늘 시작한 사람이 있는지 확인
            author = message.author.name
            try:
                with open("check.txt", "r") as f:  # 파일 읽기
                    line = chatbot.modify_txt()
                    line = ast.literal_eval(line)
                    if author in line:
                        await message.delete()
                        time = line.get(author)
                        date = time[:10]
                        slice_time = time[-5:]
                        last_time = datetime.strptime(slice_time, "%H:%M")
                        now_time_string = datetime.now(
                            timezone('Asia/Seoul')).strftime("%H:%M")
                        now_time = datetime.strptime(now_time_string, "%H:%M")
                        hour = str(now_time - last_time)[:-6]
                        min = str(now_time - last_time)[3:-3]
                        await message.channel.send(f'{date}\n{author} : {slice_time}~{now_time_string}({hour}시간 {min}분)')
                        # 종료된 사람 txt파일에서 제거
                        with open("check.txt", "r+") as f:
                            new_f = f.readlines()
                            f.seek(0)
                            for line in new_f:
                                if "이형진" not in line:
                                    f.write(line)
                            f.truncate()

                        return None
                    else:
                        await message.delete()
                        msg = await message.channel.send("오늘 시작하지 않았습니다. !start로 시작해주세요.")
                        await asyncio.sleep(5)
                        await msg.delete()
                        return None

            except:
                await message.delete()
                msg = await message.channel.send("오늘 시작하지 않았습니다. !start로 시작해주세요.")
                await asyncio.sleep(5)
                await msg.delete()
                return None


# 프로그램이 실행되면 제일 처음으로 실행되는 함수
if __name__ == "__main__":
    # 객체를 생성
    client = chatbot()
    # TOKEN 값을 통해 로그인하고 봇을 실행
    token_path = os.path.dirname(os.path.abspath(__file__))+'/token.txt'
    t = open(token_path, "r", encoding="utf-8")
    token = t.read()
    client.run(token)
    # client.run(os.environ['token'])
