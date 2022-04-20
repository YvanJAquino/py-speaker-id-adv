sample = {
    "thing": {
        "inner": {
            "solution": "YES!"
        }, 
        "outer": [] # [{"answer": "yes"}, {"other": "no"}]
    }
}

print(sample.get("thing").get("outer")[4])