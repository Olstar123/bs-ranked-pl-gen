import requests
import json
import time

url = "https://scoresaber.com/api/leaderboards"
params = {
    "ranked": "true",
    "category": "3",
    "sort": "0",
    "unique": "false",
    "page": "1"
}

# Clear the files at the start
open("hashes.temp", "w").close()
open("playlist.bplist", "w").close()

songs_data = []
start_time = time.time()

while True:
    response = requests.get(url, params=params)
    data = response.json()

    if not data["leaderboards"]:
        break

    for song in data["leaderboards"]:
        song_hash = song["songHash"]
        song_stars = song["stars"]
        song_data = {"hash": song_hash, "/stars": song_stars}
        songs_data.append(song_data)
        print(song_hash)

        with open("hashes.temp", "a") as file:
            file.write(song_hash + "\n")

    params["page"] = str(int(params["page"]) + 1)

end_time = time.time()
elapsed_time = (end_time - start_time) * 1000

# Save the song hashes to the playlist file
playlist_data = {
    "playlistTitle": "Scoresaber Ranked ({date})".format(date=time.strftime("%Y-%m-%d")),
    "playlistDescription": "All ranked maps on Scoresaber so you can download them easily!",
    "playlistAuthor": "Olstar123",
    "songs": [{"hash": song_data["hash"]} for song_data in songs_data],
    "image": ""
}

print(playlist_data)

with open("playlist.bplist", "w") as file:
    json.dump(playlist_data, file, indent=2)

# Print some nice info at the end :)
print("==============================================")
print("All " + str(len(songs_data)) + " song hashes have been gathered.")
print("Time taken: " + str(round(elapsed_time)) + "ms")
print("Playlist saved to playlist.bplist")
print("==============================================")
