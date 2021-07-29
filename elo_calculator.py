"""Elo Calculator"""


def calculate_new_ratings(r1, r2, winner, k=32):
    R1 = 10.0**(r1/400.)
    R2 = 10.0**(r2/400.)

    expected_score1 = R1/(R1+R2)
    expected_score2 = R2/(R1+R2)

    if winner == 0:
        S1 = 1
        S2 = 0

    elif winner == 1:
        pass
        S1 = 0
        S2 = 1

    else:
        S1 = .5
        S2 = .5

    new_r1 = r1 + k*(S1 - expected_score1)
    new_r2 = r2 + k*(S2 - expected_score2)

    return new_r1, new_r2
