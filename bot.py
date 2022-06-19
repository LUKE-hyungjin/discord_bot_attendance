# -*- coding:utf-8 -*-

import token
import discord
import os
import asyncio
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
            with open("check.txt", "r+") as f:  # 파일 읽기 (만약 파일이 있을 경우)
                print("Exist")  # 데이터를 불러오기

        except FileNotFoundError:  # 파일이 없으면
            file = open("check.txt", "w")
            file.close()

        # 준비가 완료되면 콘솔 창에 "READY!"라고 표시
        print("READY")

    # 봇에 메시지가 오면 수행 될 액션

    async def on_message(self, message):
        date = datetime.today().strftime("%Y-%m-%d")
        time = datetime.today().strftime("%H:%M")

        # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
        if message.author.bot:
            return None

        # message.content = message의 내용
        if message.content == "!start":
            # 현재 채널을 받아옴
            channel = message.channel
            author = message.author.name
            # 답변 내용 구성
            # msg에 지정된 내용대로 메시지를 전송
            await message.delete()
            msg = await message.channel.send(f'{author}님 지금부터 시작합니다.')
            await asyncio.sleep(5)
            await msg.delete()
            text = f'{date}-{author}-{time}'
            with open("check.txt", "a") as f:  # 파일을 만들기
                f.write(f'{text}\n')
            return None

        if message.content == "!end":
            # 파일안에 오늘 시작한 사람이 있는지 확인
            with open("check.txt", "r") as f:  # 파일 읽기
                name = f.read()
                author = message.author.name
                if author in name:
                    line = f.readline()
                    channel = message.channel
                    # 답변 내용 구성
                    end_time = datetime.today().strftime("%H:%M")
                    text = f'{date}\n{author} : {time}~{end_time}'
                    # msg에 지정된 내용대로 메시지를 전송
                    await message.channel.send(f'{text}')
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
