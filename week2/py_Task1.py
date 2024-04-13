def find_and_print(messages, current_station):
    green_line = [
        "Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing",
        "Songjiang Nanjing", "Zhongshan", "Beimen", "Ximen", "Xiaonanmen",
        "Chiang Kai-Shek Memorial Hall", "Guting", "Taipower Building",
        "Gongguan", "Wanlong", "Jingmei", "Dapinglin", "Qizhang",
        "Xindian City Hall", "Xindian"
    ]

    min_distance = float('inf')
    nearest_friend = ""
    friend_station_index = None

    if current_station == "Xiaobitan":
        # 在 Xiaobitan 站的處理邏輯
        for friend, friend_message in messages.items():
            if "Xiaobitan" in friend_message:
                nearest_friend = friend
            else:
                for word in friend_message.split():
                    if word in green_line:
                        friend_station_index = green_line.index(word)
                        distance = abs(green_line.index("Qizhang") - friend_station_index)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_friend = friend
                            break

    else:
        # 在其他站的處理邏輯
        for friend, friend_message in messages.items():
            distance = None

            # 朋友在綠線 "Xiaobitan"，特殊處理
            if "Xiaobitan" in friend_message:
                # 計算到 "Qizhang" 的距離
                to_qizhang_distance = abs(green_line.index(current_station) - green_line.index("Qizhang"))

                # 計算到 "Xiaobitan" 的距離
                distance = to_qizhang_distance + 1
            else:
                # 朋友在綠線主線
                 for station in green_line:
                    if station in friend_message:
                        friend_station_index = green_line.index(station)
                        # 計算朋友站點到目標站點的距離
                        distance = abs(green_line.index(current_station) - friend_station_index)
                        break

            # 最終選擇是根據所有朋友的距離比較的
            if distance is not None and distance < min_distance:
                min_distance = distance
                nearest_friend = friend

    print(nearest_friend)


messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
}


find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

