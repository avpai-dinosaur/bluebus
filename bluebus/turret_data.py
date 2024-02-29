T_NERD = "nerd"
T_JOCK = "jock"
T_SCHLISSEL = "schlissel"
T_EMO = "emo"

TURRET_DATA = {
    "nerd" : {
        "bullet-img" : "",
        "bullet-speed" : 5,
        "anim-delay" : 50,
        "upgrades" : [
            # Level 1
            {
                "range" : 150,
                "cooldown" : 1500
            },
            # Level 2
            {
                "range" : 200,
                "cooldown" : 1200 
            },
            # Level 3
            {
                "range" : 250,
                "cooldown" : 1000
            }
        ]
    },
    "jock" : {
        "bullet-img" : "football.png",
        "bullet-speed" : 10,
        "anim-delay" : 50,
        "upgrades" : [
            # Level 1
            {
                "range" : 250,
                "cooldown" : 2000
            },
            # Level 2
            {
                "range" : 300,
                "cooldown" : 2000
            },
            # Level 3
            {
                "range" : 500,
                "cooldown" : 2000
            }
        ]
    },
    "emo" : {},
    "schlissel" : {
        "bullet-img" : "lonely.png",
        "bullet-speed" : 10,
        "anim-delay" : 1,
        "upgrades" : [
            # Level 1
            {
                "range" : 400,
                "cooldown" : 200
            },
            # Level 2
            {
                "range" : 500,
                "cooldown" : 100
            },
            # Level 3
            {
                "range" : 700,
                "cooldown" : 10
            }
        ]
    }
}