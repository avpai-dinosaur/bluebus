B_WEAK = "weak"
B_MED = "medium"
B_STRONG = "strong"

ENEMY_DATA = {
    B_WEAK : {
        "img" : "bluebus.png",
        "speed" : 2,
        "health" : 5,
        "anim-delay" : 250
    },
    B_MED : {
        "img" : "orangebus.png",
        "speed" : 3,
        "health" : 10,
        "anim-delay" : 250
    },
    B_STRONG : {
        "img" : "redbus.png",
        "speed" : 4,
        "health" : 15,
        "anim-delay" : 250
    }
}

ENEMY_SPAWN_DATA = [
    {
        #1
        B_WEAK: 2,
        B_MED: 0,
        B_STRONG: 0,
    },
    {
        #2
        B_WEAK: 5,
        B_MED: 0,
        B_STRONG: 0,
    },
    {
        #3
        B_WEAK: 3,
        B_MED: 1,
        B_STRONG: 0,
    },
    {
        #4
        B_WEAK: 2,
        B_MED: 7,
        B_STRONG: 0,
    },
    {
        #5
        B_WEAK: 5,
        B_MED: 6,
        B_STRONG: 0,
    },
    {
        #6
        B_WEAK: 3,
        B_MED: 0,
        B_STRONG: 1,
    },
    {
        #7
        B_WEAK: 0,
        B_MED: 10,
        B_STRONG: 0,
    },
    {
        #8
        B_WEAK: 6,
        B_MED: 7,
        B_STRONG: 1,
    },
    {
        #9
        B_WEAK: 0,
        B_MED: 10,
        B_STRONG: 5,
    },
    {
        #10
        B_WEAK: 0,
        B_MED: 0,
        B_STRONG: 15,
    },
    {
        #11
        B_WEAK: 0,
        B_MED: 10,
        B_STRONG: 10,
    },
    {
        #12
        B_WEAK: 0,
        B_MED: 0,
        B_STRONG: 15,
    },
    {
        #13
        B_WEAK: 20,
        B_MED: 0,
        B_STRONG: 25,
    },
    {
        #14
        B_WEAK: 15,
        B_MED: 15,
        B_STRONG: 15,
    },
    {
        #15
        B_WEAK: 25,
        B_MED: 25,
        B_STRONG: 25,
    }
]