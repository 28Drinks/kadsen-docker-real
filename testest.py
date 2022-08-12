test_list =  [
    {
        "position": "#1",
        "name": "CIABodyguard98D",
        "amount": "$1,397.08"
    },
    {
        "position": "#2",
        "name": "JPW",
        "amount": "$1,047.81"
    },
    {
        "position": "#3",
        "name": "Hidden",
        "amount": "$698.54"
    },
    {
        "position": "#4",
        "name": "oooooo",
        "amount": "$558.83"
    }]

for test in test_list:
    e = test["position"]
    print(e)

price = 360


share = 10
bet = 28

roi = share * 12
roi += bet * 12 / 2

final_roi = roi / ( price / 100)

print(final_roi)