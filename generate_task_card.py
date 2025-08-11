
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
from flask import Flask, send_file
import io
import os

# ===== 任務清單 =====
tasks = [
    "任務1：與貓貓大人合照",
    "任務2：與一位異性玩家合照",
    "任務3：與一位同性玩家合照",
    "任務4：在幫會領地任何角落，與一個可互動的家具（例如椅子）合照",
    "任務5：擺出任何表情並拍照",
    "任務6：在世界頻打上貓窩萬歲，並截圖",
    "任務7：在貓窩幫會頻道講一句話，並截圖",
    "任務8：在貓窩幫會頻道打上「我愛XX堂（自己的堂）」，並截圖",
    "任務9：到貓窩幫會領地-低血堂的領域拍照",
    "任務10：到貓窩幫會領地-棉花堂的領域拍照",
    "任務11：到貓窩幫會領地-龍發堂的領域拍照",
    "任務12：到貓窩幫會領地-天線堂的領域拍照",
    "任務13：在逆水寒任何一艘船上拍照",
    "任務14：與幫會任務小廚娘合照",
    "任務15：與幫會領地中的貓掌印合照",
    "任務16：與幫會領地木樁合照",
    "任務17：與幫會領地中MEOW大招牌合照",
    "任務18：與江湖門派-相思門的執劍人合照 (江湖門派NPC)",
    "任務19：與江湖門派-平天門的武德長者合照 (江湖門派NPC)",
    "任務20：與江湖門派-無念門的無念淨者合照 (江湖門派NPC)",
    "任務21：與江湖門派-逍遙門的水妲嬌合照 (江湖門派NPC)",
    "任務22：與江湖門派-丐幫的傳功長老合照 (江湖門派NPC)",
    "任務23：與江湖門派-龍門客棧的引路人合照 (江湖門派NPC)",
    "任務24：與幫會領地中的貓合照(看板、燈飾或是幫派貨運地板告示)",
    "任務25：前往大相國寺(714,1267)使用祈福動作與大雄寶殿拍照",
    "任務26：前往鑑石壇(1451,1468)使用許願動作與鑑石台拍照",
    "任務27：前往杭州(746,1380)與靈隱寺合照",
    "任務28：前往杭州(783,819)與雷峰塔合照",
    "任務29：前往磁州(881,145)油菜花田中與風車合照",
    "任務30：前往磁州(1040,791)與孔子合照",
    "任務31：前往三清山(1146,802)與NPC葉哀禪合照",
    "任務32：前往三清山(1122,741)與鶴合照",
    "任務33：前往桃溪村(938,1066)與桃溪小舖的桃婆婆合照",
    "任務34：前往桃溪村(996,1159)與兵器舖的唐大鑄合照",
    "任務35：前往鏡湖(731,324)與登天梯合照",
    "任務36：前往鏡湖(414,516)與鞦韆合照",
    "任務37：前往滄州(1202,1112)在吊橋上使用扔球動作並拍照",
    "任務38：前往滄州(1186,996)與鐵血大牢大門合照",
    "任務39：前往白帝城(705902)與棋盤牆合照",
    "任務40：前往白帝城(837,783)與地球儀合照",
    "任務41：前往白帝城(485,808)與神相課業導師合照",
    "任務42：前往藥王谷(567,542)與寫有藥王谷的大石合照",
    "任務43：前往藥王谷(603,296)與素問課業導師合照",
    "任務44：前往東極海(433,637)與六把劍合照",
    "任務45：前往東極海(310,773)與漩渦合照",
    "任務46：前往東極海(572,624)與碎夢課業導師合照",
    "任務47：前往碧血營(599,396)與鐵衣課業導師合照",
    "任務48：前往碧血營(242,696)與血河課業導師合照",
    "任務49：前往藥王谷(450,367)與九靈課業導師合照",
    "任務50：前往東極海(542,658)與龍吟課業導師合照",
]

# ===== 畫文字的函數 =====
def draw_multiline_text(draw, text, font, max_width, start_x, start_y, line_spacing=4):
    lines = []
    wrapper = textwrap.TextWrapper(width=40)
    raw_lines = wrapper.wrap(text)

    for raw_line in raw_lines:
        if draw.textbbox((0, 0), raw_line, font=font)[2] > max_width:
            temp_line = ""
            for char in raw_line:
                if draw.textbbox((0, 0), temp_line + char, font=font)[2] <= max_width:
                    temp_line += char
                else:
                    lines.append(temp_line)
                    temp_line = char
            if temp_line:
                lines.append(temp_line)
        else:
            lines.append(raw_line)

    y = start_y
    for line in lines:
        draw.text((start_x, y), line, font=font, fill="black")
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        y += line_height + line_spacing

    return y - start_y

# ===== 任務卡生成函數 =====
def generate_task_card():
    chosen_tasks = random.sample(tasks, 9)

    width, height = 900, 900
    card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(card)

    grid_size = width // 3
    font = ImageFont.truetype("msjhl.ttc", 24)

    for i, task in enumerate(chosen_tasks):
        x = (i % 3) * grid_size
        y = (i // 3) * grid_size
        draw.rectangle([x, y, x + grid_size, y + grid_size], outline="gray", width=3)
        padding = 10
        max_text_width = grid_size - 2 * padding
        start_x = x + padding
        start_y = y + padding
        draw_multiline_text(draw, task, font, max_text_width, start_x, start_y)

    return card

# ===== Flask API =====
app = Flask(__name__)

@app.route("/draw", methods=["GET"])
def draw_card():
    card = generate_task_card()
    img_io = io.BytesIO()
    card.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))