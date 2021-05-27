import tekore as tk

playlist_id_1 = "https://open.spotify.com/playlist/75owcABGoeuoEFRf2wUfsf?si=adf27c2c8fb24fa2"[34:56]
playlist_id_2 = "https://open.spotify.com/playlist/6JOs2fcbRUcs5hxLW2LHgP?si=6285314918624162"[34:56]

request_max = 1337

if __name__ == '__main__':
    # Get valid token and authorize
    client_id = "3f8c2582f87e46c498d4482aa8ea3b3c"
    client_secret = "8820e18c331f4e449e27f49d0ff66a07"
    redirect_uri = "http://localhost/"
    conf = (client_id, client_secret, redirect_uri)
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    Spotify = tk.Spotify(token)

    # Enter playlist links and cut out anything but Spotify ID
    playlist_id_temp = input("Playlist 1 Link: ")[34:56]
    if playlist_id_temp != "":
        playlist_id_1 = playlist_id_temp
    playlist_id_temp = input("Playlist 2 Link: ")[34:56]
    if playlist_id_temp != "":
        playlist_id_2 = playlist_id_temp

    # Fetch playlists belonging to given Spotify IDs
    playlist_1 = []
    playlist_2 = []
    print("\nGathering playlist information...")
    for offset in range(0, request_max, 100):
        playlist_1 += Spotify.playlist_items(playlist_id_1, as_tracks=True, offset=offset)["items"]
    for offset in range(0, request_max, 100):
        playlist_2 += Spotify.playlist_items(playlist_id_2, as_tracks=True, offset=offset)["items"]
    print("Done!\n")

    # Simplify playlist format
    playlist_1_simple = set()
    playlist_2_simple = set()
    for song in playlist_1:
        playlist_1_simple.add(song["track"]["artists"][0]["name"] + " - " + song["track"]["name"])
    for song in playlist_2:
        playlist_2_simple.add(song["track"]["artists"][0]["name"] + " - " + song["track"]["name"])

    # Select mode
    mode = input("[unite, intersect, difference]\nSelect mode: ")

    output = set()
    if mode == "unite":
        output = playlist_1_simple.union(playlist_2_simple)
    elif mode == "intersect":
        output = playlist_1_simple.intersection(playlist_2_simple)
    elif mode == "difference":
        output = playlist_1_simple.difference(playlist_2_simple)
    else:
        print("Invalid mode error. Possible options: [unite, intersect, difference]")

    # Output
    output = sorted(output)
    for song in output:
        print(song)
    print("\n")
    print("Playlist 1 Length: " + str(len(playlist_1_simple)))
    print("Playlist 2 Length: " + str(len(playlist_2_simple)))
    if mode == "unite":
        print("Combined length: " + str(len(output)))
    elif mode == "intersect":
        print("Intersected length: " + str(len(output)))
    elif mode == "difference":
        print("Difference length: " + str(len(output)))