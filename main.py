"""
This module is where the main Flask decorator (routing?) functions go
"""

from flask import (
    Flask, g, redirect, render_template, request, session
)

import db_functions
import datetime
from datetime import timezone

from ratings_sessions import get_types_direct_primary, COMPARE_TYPE
from secret_key import SECRET_KEY

from db import get_stuff
from db import get_db

"""
@app.route('/my-route')
def my_route():
  page = request.args.get('page', default = 1, type = int)
  filter = request.args.get('filter', default = '*', type = str)
"""

username = "user"
app = Flask(__name__, static_url_path='', static_folder='static')

#password = Utils.get_password()
#Utils.test_get_password()

app.secret_key = SECRET_KEY


@app.route('/hello')
def hello():
    return "Hello, World!"


@app.route('/vibes-initiate')
def vibes_initiate():
    try:
        if session['inSession'] is True:
            return "Already in session!"
    except KeyError:
        pass

    types = get_types_direct_primary()

    session['inSession'] = True
    session['types'] = types
    now = datetime.datetime.now(timezone.utc)
    session['startTime'] = datetime.datetime.now(timezone.utc)

    db_name = "default_database"
    if app.testing:
        db_name = "test_db"

    db = get_db(db_name)

    # return "haha"
    return redirect('/vibes-session?iter=0')


@app.route('/vibes-cleanup')
def vibes_cleanup():
    session.clear()
    return render_template('/session-over')


@app.route('/session-timeout')
def session_timeout():
    return render_template("session-timeout.html")


@app.route('/vibes-session')
def vibes_session():
    cur_iter = request.args.get('curiter', default=1, type=int)
    cur_type = session['types'][cur_iter]

    start_time = session['startTime']

    now = datetime.datetime.now(timezone.utc)


    g.cur_iter = cur_iter

    seconds_elapsed = (now-start_time).total_seconds()

    if seconds_elapsed > 600:
        session.clear()
        #clear
        return redirect('/session-timeout')


    #db = get_db()
    db_name = "default_database"
    if app.testing:
        db_name = "test_db"

    db = get_db(db_name)
    print(db)

    #?curiter=0&curtype=2&c1=c1&c2=c2

    stuff = get_stuff(cur_type, db)
    if cur_type == COMPARE_TYPE.DIRECT:
        entry_choices = stuff[0]
        vibe_choice = stuff[1]

        #e in entries_rows[0]#

        entry_rows_0 = []

        c1 = entry_choices[0]
        c2 = entry_choices[1]
        v = vibe_choice
        href = "?curiter={}&curtype={}&c1={}&c2={}&v={}".format(cur_iter, cur_type, c1, c2, v)
        #######
        cur_iter = 1
        for e in entry_choices:
            entry_db = g.db.collection['entries'].find_one({'id': e})
            font_name = entry_db['name']

            ###cur_iter, cur_type, c1, c2, v, sel

            cur_href = str(href) + "&s={}".format(cur_iter)

            cur_iter += 1

            e_dict = {"style": {"font": font_name}, "href": cur_href }

            entry_rows_0.append(e_dict)

        entry_rows = [entry_rows_0]
        vibe = vibe_choice
        text = "word"
        return render_template("comparisons/multicomparison.html", entry_rows=entry_rows, vibe=vibe, text=text)

    elif cur_type == COMPARE_TYPE.RATE:
        pass

        choice_id = stuff[0]
        vibe_id = stuff[1]

        font_name = db.collection['entries'].find_one({'id': choice_id})['name']
        style = "font: {};".format(font_name)

        vibe_name = db.collection['vibes'].find_one({'id': vibe_id})['name']

        hrefs = []
        href = "?curiter={}&curtype={}&v={}&c={}".format(cur_iter, cur_type, vibe_id)
        for i in range(0, 5):
            cur_href = href + "&s={}".format(i+1)
            hrefs.append(href)

        return render_template("comparisons/rate.html", hrefs=hrefs, vibe=vibe_name, style=style)

    elif cur_type == COMPARE_TYPE.TWO_VIBE:
        ##///style, text, vibe_1, vibe_2

        entry_choice = stuff[0]
        vibes = stuff[1]

        vibe_id_1 = vibes[0]
        vibe_id_2 = vibes[1]

        entry = g.db.collection['entries'].find_one({'id': entry_choice})
        font_name = entry['name']

        vibe_name_1 = g.db.collection['vibes'].find_one({'id': vibe_id_1})
        vibe_name_2 = g.db.collection['vibes'].find_one({'id': vibe_id_2})

        style = "font: " + font_name

        href = "?curiter={}&curtype={}&v1={}&v2={}&c={}".format(cur_iter, cur_type, vibe_id_1, vibe_id_2, entry_choice)

        vibe_1 = {"href": href + "&s=" + vibe_id_1, "vibe": vibe_name_1}
        vibe_2 = {"href": href + "&s=" + vibe_id_2, "vibe": vibe_name_2}

        text = "word"

        return render_template("comparisons/twovibe.html", vstyle=style, text=text, vibe_1=vibe_1, vibe_2=vibe_2)


@app.route('/vibes-selection')
def receive_selection():
    cur_iter = request.args.get('curiter', type=int)
    cur_type = request.args.get('curtype', type=int)

    next_iter = cur_iter + 1

    db = g.db

    if cur_type == COMPARE_TYPE.DIRECT:
        c1 = request.args.get('c1', type=int)
        c2 = request.args.get('c2', type=int)
        v = request.args.get('v', type=int)

        selected_index = request.args.get('s', type=int)

        db_functions.add_direct_comparison(db, v, c1, c2, selected_index)

    elif cur_type == COMPARE_TYPE.MULTI:
        c1 = request.args.get('c1', type=int)
        c2 = request.args.get('c2', type=int)
        c3 = request.args.get('c3', default=None, type=int)
        c4 = request.args.get('c4', default=None, type=int)
        c5 = request.args.get('c5', default=None, type=int)

        choices = [c1, c2, c3, c4, c5]
        choices = [c for c in choices if c is not None]

        v = request.args.get('v', type=int)

        selected_index = request.args.get('s', type=int)

        db_functions.add_multi_result(db, v, choices, selected_index)

    elif cur_type == COMPARE_TYPE.RATE:
        v = request.args.get('v1', type=int)

        selected_index = request.args.get('s', type=int)

        db_functions.add_vibe_rating(db, v, selected_index)

    elif cur_type == COMPARE_TYPE.TWO_VIBE:
        pass

        v1 = request.args.get('v1')
        v2 = request.args.get('v2')

        c = request.args.get('c', type=int)

        selected_index = request.args.get('s', type=int)

        db_functions.add_two_vibe(db, c, v1, v2, selected_index)

    return redirect('/vibes-session?iter={0}'.format(next_iter))


if __name__ == "__main__":
    app.run()

    #app.get
    #client = app.client