"""
დაწერერეთ პროგრამა რომელის მეშვეობითაც მომხმარებელი შეძლებს შეამოწმოს, ხელმისაწვდომია თუ არა მატარებელში,
კონკრეტულ ვაგონში კონკრეტული, ადგილი. მომხმარებელს უნდა შეეძლოს შეიტანოს ვაგონისა და ადგილის ნომერი.
იმ შემთხვევაში, თუ არჩეული ადგილი დაკავებულია, შესთავაზეთ უახლოესი ადგილი და თუ ვაგონში არ არის თავისუფალი ადგილები,
პროგრამამ გააგრძელოს ძიება სხვა ვაგონებში სანამ არ იპოვის თავისუფალ ადგილს. გამოიყენეთ ქვემოთ მოცემული დიქშენერი.

p.s
ვაგონის ნომერია key ხოლო ამავე ვაგონის data არის value
"""

data = {
    1: [
        { "seat_name": "a1", "isTaken": True },
        { "seat_name": "a2", "isTaken": False },
        { "seat_name": "a3", "isTaken": True },
        { "seat_name": "a4", "isTaken": True },
        { "seat_name": "a5", "isTaken": False },
    ],
    2: [
        { "seat_name": "b1", "isTaken": False },
        { "seat_name": "b2", "isTaken": False },
        { "seat_name": "b3", "isTaken": True },
        { "seat_name": "b4", "isTaken": False },
        { "seat_name": "b5", "isTaken": True },
    ],
    3: [
        { "seat_name": "c1", "isTaken": False },
        { "seat_name": "c2", "isTaken": True },
        { "seat_name": "c3", "isTaken": True },
        { "seat_name": "c4", "isTaken": True },
        { "seat_name": "c5", "isTaken": False },
    ],
}

