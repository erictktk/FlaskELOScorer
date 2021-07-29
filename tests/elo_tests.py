import elo_calculator
import ratings_sessions


def generator_test():
    the_list = ratings_sessions.get_type_direct_primary()

    assert len(the_list) >= 50
    assert len(the_list) < 80

    assert 5 not in the_list


def elo_tests():
    pass

    x_score = 800
    y_score = 800

    x_score, y_score = elo_calculator.calculate_new_ratings(x_score, y_score)

    assert x_score > y_score

    a_score = 800
    b_score = 800
    c_score = 800

    ### a should win
    ### b should be last
    ### c should be second

    match_0 = [0, 1, 0]
    match_1 = [1, 0, 1]
    match_2 = [1, 2, 1]
    match_3 = [0, 2, 0]

    a_score, b_score = elo_calculator.calculate_new_ratings(a_score, b_score, 0)
    b_score, a_score = elo_calculator.calculate_new_ratings(b_score, a_score, 1)
    b_score, c_score = elo_calculator.calculate_new_ratings(b_score, c_score, 1)
    a_score, c_score = elo_calculator.calculate_new_ratings(a_score, c_score, 0)

    assert a_score > b_score
    assert a_score > c_score
    assert c_score > b_score
