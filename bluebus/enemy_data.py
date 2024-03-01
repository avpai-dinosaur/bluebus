B_WEAK = "weak"
B_MED = "medium"
B_STRONG = "strong"

ENEMY_DATA = {
    B_WEAK : {
        "img" : "bus.png",
        "speed" : 2,
        "health" : 5,
        "anim-delay" : 50
    },
    B_MED : {
        "img" : "bus2.png",
        "speed" : 3,
        "health" : 7,
        "anim-delay" : 50
    },
    B_STRONG : {
        "img" : "bus3.png",
        "speed" : 1,
        "health" : 15,
        "anim-delay" : 50
    }
}

ENEMY_SPAWN_DATA = [
    {
        #1
        B_WEAK: 1,
        B_MED: 0,
        B_STRONG: 0,
    },
    {
        #2
        B_WEAK: 0,
        B_MED: 1,
        B_STRONG: 0,
    },
    {
        #3
        B_WEAK: 0,
        B_MED: 0,
        B_STRONG: 1,
    },
    # {
    #     #4
    #     B_WEAK: 30,
    #     B_MED: 15,
    #     B_STRONG: 0,
    # },
    # {
    #     #5
    #     B_WEAK: 5,
    #     B_MED: 20,
    #     B_STRONG: 0,
    # },
    # {
    #     #6
    #     B_WEAK: 15,
    #     B_MED: 15,
    #     B_STRONG: 4,
    # },
    # {
    #     #7
    #     B_WEAK: 20,
    #     B_MED: 25,
    #     B_STRONG: 5,
    # },
    # {
    #     #8
    #     B_WEAK: 10,
    #     B_MED: 20,
    #     B_STRONG: 15,
    # },
    # {
    #     #9
    #     B_WEAK: 15,
    #     B_MED: 10,
    #     B_STRONG: 5,
    # },
    # {
    #     #10
    #     B_WEAK: 0,
    #     B_MED: 100,
    #     B_STRONG: 0,
    # },
    # {
    #     #11
    #     B_WEAK: 5,
    #     B_MED: 10,
    #     B_STRONG: 12,
    # },
    # {
    #     #12
    #     B_WEAK: 0,
    #     B_MED: 15,
    #     B_STRONG: 10,
    # },
    # {
    #     #13
    #     B_WEAK: 20,
    #     B_MED: 0,
    #     B_STRONG: 25,
    # },
    # {
    #     #14
    #     B_WEAK: 15,
    #     B_MED: 15,
    #     B_STRONG: 15,
    # },
    # {
    #     #15
    #     B_WEAK: 25,
    #     B_MED: 25,
    #     B_STRONG: 25,
    # }
]