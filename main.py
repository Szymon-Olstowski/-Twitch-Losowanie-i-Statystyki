from quart import Quart, render_template, redirect, url_for,request,jsonify
import sqlite3
import threading
from twitch_bot import bot
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from datetime import datetime, timedelta
from pytz import utc
from dateutil.relativedelta import relativedelta
import os
app = Quart(__name__)

DB_NAME = "users.db"
bot_thread = None
def run_bot():
    bot.start_bot()
def stop_bot():
    bot.stop_bot()
def get_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, streamer FROM users")  
    users = c.fetchall()  
    conn.close()
    return users
def update_status(status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM status") 
    c.execute("INSERT INTO status (status) VALUES (?)", (status,))
    conn.commit()
    conn.close()
@app.route("/los")
async def los():
    usersy = get_users()
    count = len(usersy)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT status FROM status")
    status = c.fetchone()
    prefix=os.getenv("PREFIX")
    return await render_template(
        "los.html", usersy=usersy, count=count,status=status,prefix=prefix
    )
@app.route("/clear", methods=["POST"])
async def clear():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    return redirect(url_for("los")) 

@app.route("/start", methods=["POST"])
async def start():
    global bot_thread
    if not bot.running:
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
        update_status("OK")
    else:
        bot_thread = threading.Thread(target=run_bot)
        update_status("OK")
    return redirect(url_for("los"))

@app.route("/stop", methods=["POST"])
async def stop():
    global bot_thread
    bot_thread = threading.Thread(target=stop_bot)
    update_status("STOP")
    return redirect(url_for("los"))
@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/channel")
async def channel():
    return await render_template("channel_stats.html")

@app.route("/channel_stats", methods=["POST"])
async def get_channel_stats():
    data = await request.form
    login = data.get("login")
    twitch = await Twitch(
        os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET")
    )
    user = await first(twitch.get_users(logins=login))
    if user:
        user_id = user.id
        channel_info = {
            "nazwa_użytkownika": user.login,
            "opis": user.description,
            "filmy": [],
            "ilość_obserwujących": 0,
            "status": "",
        }

        stream_info = twitch.get_streams(user_id=user_id)
        async for current_stream in stream_info:
            channel_info["status"] = (
                current_stream.title
            )  
            channel_info["viewer_count"] = current_stream.viewer_count  
            channel_info["game_name"] = current_stream.game_name  
            break
        async for video in twitch.get_videos(user_id=user.id):
            formatted_created_at = video.created_at.strftime("%d-%m-%Y %H:%M:%S")
            formatted_published_at = video.published_at.strftime("%d-%m-%Y %H:%M:%S")

            channel_info["filmy"].append(
                {
                    "tytuł": video.title,
                    "link": video.url,
                    "data_utworzenia": formatted_created_at,
                    "data_publikacji": formatted_published_at,
                }
            )

        followers = await twitch.get_channel_followers(broadcaster_id=user_id)
        channel_info["ilość_obserwujących"] = followers.total

        return jsonify(channel_info)
    else:
        return jsonify({"error": "Użytkownik nie znaleziony"}), 404


@app.route("/clips")
async def clips():
    return await render_template("clips.html")


@app.route("/get_clips", methods=["POST"])
async def get_clips():
    data = await request.form
    login = data.get("login")
    started_at_str = data.get("started_at")
    ended_at_str = data.get("ended_at")

    twitch = await Twitch(
        os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET")
    )
    user = await first(twitch.get_users(logins=login))
    if user:
        user_id = user.id
        clips_info = []

        started_at = datetime.strptime(started_at_str, "%Y-%m-%dT%H:%M")
        ended_at = datetime.strptime(ended_at_str, "%Y-%m-%dT%H:%M")

        two_months_after_started_at = started_at + relativedelta(months=2)

        if ended_at > two_months_after_started_at:
            return await render_template(
                "clips.html",
                clips_info=None,
                error="Data zakończenia musi być w ciągu 2 miesięcy od daty rozpoczęcia.",
            )

        if started_at > ended_at:
            return await render_template(
                "clips.html",
                clips_info=None,
                error="Data rozpoczęcia nie może być późniejsza niż data zakończenia.",
            )

        async for clip in twitch.get_clips(
            broadcaster_id=user.id,
            started_at=started_at,
            ended_at=ended_at,
        ):
            formatted_created_at = clip.created_at.strftime("%d-%m-%Y %H:%M:%S")
            clips_info.append(
                {
                    "tytuł": clip.title,
                    "link": clip.url,
                    "data_utworzenia": formatted_created_at,
                    "data_utworzenia_raw": clip.created_at,
                    "creator_klip": clip.creator_name,
                }
            )

        clips_info.sort(key=lambda x: x["data_utworzenia_raw"], reverse=True)

        return await render_template("clips.html", clips_info=clips_info)

    else:
        return await render_template("clips.html", clips_info=None)
if __name__ == "__main__":
    app.run(host=os.getenv("HOST"))