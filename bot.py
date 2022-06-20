# -*- coding:utf-8 -*-

import token
import discord
import os
import asyncio
import ast
from datetime import datetime


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

    # 봇에 메시지가 오면 수행 될 액션

    def modify_txt():
        with open("check.txt", "r") as f:  # 파일 읽기
            line = f.readline()
            modify_linefirst = line[1:-2] + ","
            while line:
                line = f.readline()
                modify_line = line[1:-2] + ","
                modify_linefirst = modify_linefirst + modify_line
            final_line = modify_linefirst[:-2]
            final_line = final_line.ljust(len(final_line)+1, '}')
        final_line = final_line.rjust(len(final_line)+1, '{')
        return final_line

    async def on_message(self, message):

        # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
        if message.author.bot:
            return None

        with open("check.txt", "r") as f:  # 파일 읽기
            line = chatbot.modify_txt()
            line = ast.literal_eval(line)
            print(line)
            date = datetime.today().strftime("%Y-%m-%d")
            time = list(line.values())
            time = time[0][:10]
            if date != time:
                remove_items = list(line.items())
                for remove_item in remove_items:
                    author = remove_item[0]
                    time = remove_item[1]
                    date = time[:10]
                    slice_time = time[-5:]
                    now_time = datetime.today().strftime("%H:%M")
                    hour = int(datetime.today().strftime("%H"))
                    min = int(datetime.today().strftime("%M"))
                    await message.channel.send(f'{date}\n{author} : {slice_time}~{now_time}({hour}시간 {min}분)')
            file = open("check.txt", "w")
            file.close()

        if message.content == "!start":
            author = message.author.name
            # 답변 내용 구성
            # msg에 지정된 내용대로 메시지를 전송
            await message.delete()
            msg = await message.channel.send(f'{author}님 지금부터 시작합니다.')
            await asyncio.sleep(5)
            await msg.delete()
            time = datetime.today().strftime("%Y-%m-%d-%H:%M")
            text = {author: time}
            with open("check.txt", "a") as f:  # 파일을 만들기
                f.write(f'{text}\n')
            return None

        if message.content == "!end":
            # 파일안에 오늘 시작한 사람이 있는지 확인
            author = message.author.name
            with open("check.txt", "r") as f:  # 파일 읽기
                line = ast.literal_eval(f.readline())
                print(line)
                print(author)
                if author in line:
                    time = line.get(author)
                    date = time[:10]
                    slice_time = time[-5:]
                    now_time = datetime.today().strftime("%H:%M")
                    hour = int(datetime.today().strftime("%H"))
                    min = int(datetime.today().strftime("%M"))
                    await message.channel.send(f'{date}\n{author} : {slice_time}~{now_time}({hour}시간 {min}분)')
                    return None

                else:
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
