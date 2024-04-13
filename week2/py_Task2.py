bookedrecord = []

def book(consultants, hour, duration, criteria):
    availableconsultants = ["Jenny", "John", "Bob"]
    for booking in bookedrecord:
        start = booking["start"]
        end = booking["end"]
        if hour < end and hour + duration > start:
            if booking["consultant"] in availableconsultants:
                availableconsultants.remove(booking["consultant"])
    if not availableconsultants:
        print("No Service")
        return None


    if criteria == "price":
        availableconsultants.sort(key=lambda consultant: next((c["price"] for c in consultants if c["name"] == consultant), float('inf')))
    elif criteria == "rate":
        availableconsultants.sort(key=lambda consultant: next((c["rate"] for c in consultants if c["name"] == consultant), float('-inf')), reverse=True)

    print(availableconsultants[0])

    bookedrecord.append({"consultant": availableconsultants[0], "start": hour, "end": hour + duration})





consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John