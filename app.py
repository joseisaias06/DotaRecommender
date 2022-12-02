import pandas as pd

from flask import Flask, render_template, session, redirect, url_for

from utils.draft import Draft
from utils.forms import DotaForm
from utils.variables import dict_id

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DotaForm()
    if form.validate_on_submit():
        session['user_id'] = form.user_id.data
        session['side'] = form.side.data
        session['radiant_hero_1'] = form.radiant_hero_1.data
        session['radiant_hero_2'] = form.radiant_hero_2.data
        session['radiant_hero_3'] = form.radiant_hero_3.data
        session['radiant_hero_4'] = form.radiant_hero_4.data
        session['radiant_hero_5'] = form.radiant_hero_5.data
        session['dire_hero_1'] = form.dire_hero_1.data
        session['dire_hero_2'] = form.dire_hero_2.data
        session['dire_hero_3'] = form.dire_hero_3.data
        session['dire_hero_4'] = form.dire_hero_4.data
        session['dire_hero_5'] = form.dire_hero_5.data

        cantidad_heroes_radiant = 0
        cantidad_heroes_dire = 0

        if session['radiant_hero_1'] != 'not yet':
            cantidad_heroes_radiant += 1
        if session['radiant_hero_2'] != 'not yet':
            cantidad_heroes_radiant += 1
        if session['radiant_hero_3'] != 'not yet':
            cantidad_heroes_radiant += 1
        if session['radiant_hero_4'] != 'not yet':
            cantidad_heroes_radiant += 1
        if session['radiant_hero_5'] != 'not yet':
            cantidad_heroes_radiant += 1

        if session['dire_hero_1'] != 'not yet':
            cantidad_heroes_dire += 1
        if session['dire_hero_2'] != 'not yet':
            cantidad_heroes_dire += 1
        if session['dire_hero_3'] != 'not yet':
            cantidad_heroes_dire += 1
        if session['dire_hero_4'] != 'not yet':
            cantidad_heroes_dire += 1
        if session['dire_hero_5'] != 'not yet':
            cantidad_heroes_dire += 1

        if abs(cantidad_heroes_dire - cantidad_heroes_radiant) > 1:
            return render_template('home.html', form=form,
                                   error='La cantidad de héroes elegidos por cada equipo debe ser igual o diferir en 1')

        if session['side'] == 'Radiant' and cantidad_heroes_radiant < cantidad_heroes_dire:
            return render_template('home.html', form=form,
                                   error='La cantidad de héroes Dire debe ser menor o igual a la cantidad de héroes '
                                         'Radiant')

        if session['side'] == 'Dire' and cantidad_heroes_radiant > cantidad_heroes_dire:
            return render_template('home.html', form=form,
                                   error='La cantidad de héroes Radiant debe ser menor o igual a la cantidad de '
                                         'héroes Dire')

        # Check if a hero is repeated and not yet
        heroes = [session['radiant_hero_1'], session['radiant_hero_2'], session['radiant_hero_3'],
                  session['radiant_hero_4'], session['radiant_hero_5'], session['dire_hero_1'],
                  session['dire_hero_2'], session['dire_hero_3'], session['dire_hero_4'], session['dire_hero_5']]

        for hero in heroes:
            if heroes.count(hero) > 1 and hero != 'not yet':
                return render_template('home.html', form=form,
                                       error='No se puede elegir el mismo héroe más de una vez')

        return redirect(url_for("solution"))

    return render_template('home.html', form=form)


@app.route('/solution/')
def solution():
    if session['side'] == "Radiant":
        player = 0
    else:
        player = 1

    user_id = session['user_id']
    message_user = ''

    state = [list(filter(lambda x: x != 'not yet',
                         [session['radiant_hero_1'],
                          session['radiant_hero_2'],
                          session['radiant_hero_3'],
                          session['radiant_hero_4'],
                          session['radiant_hero_5']])),
             list(filter(lambda x: x != 'not yet',
                         [session['dire_hero_1'],
                          session['dire_hero_2'],
                          session['dire_hero_3'],
                          session['dire_hero_4'],
                          session['dire_hero_5']]))]

    state = [[int(s) for s in sublist] for sublist in state]

    avail_moves = [i for i in range(138) if
                   i not in [0, 24, 115, 116, 117, 118, 122, 124, 125, 127, 130, 131, 132, 133, 134]]
    avail_moves = set([i for i in avail_moves if i not in state[0] + state[1]])

    d = Draft(state=state, avail_moves=avail_moves, player=player)
    p = d.get_player()
    output = p.get_move()

    # Read csv and concat outputs
    # Cut Output Heroes in 50
    output_series = pd.Series(output[:50])

    # Get User Data and concat with output
    if user_id is True:
        try:
            df = pd.DataFrame(output_series, columns=['hero_id'])

            # Get the index and set in a column reversed
            df['position'] = output_series.index
            df['position'] = df['position'].apply(lambda x: 49 - x)

            # Normalize position column
            df['position'] = df['position'] + 1
            df['position'] = df['position'].div(50)

            player_data = pd.read_csv('Player_heroes.csv')
            player_data = player_data[player_data['hero_id'].isin(output_series)]
            player_data = player_data.drop(player_data[player_data.games < 6].index)

            # Win Rate Metric of Player
            player_data['win_rate'] = player_data['win'] / player_data['games']

            # Get Final Results. The Best Hero is the one with the highest win rate and the Highest position(Reversed)
            resultado = df.merge(player_data, left_on='hero_id', right_on='hero_id')
            resultado['score'] = resultado['position'] * resultado['win_rate']

            resultado.sort_values(by=['score'], ascending=False, inplace=True)
            resultado_names = [dict_id[hero] for hero in resultado['hero_id']]

        except:
            resultado_names = [dict_id[hero] for hero in output_series]
            message_user = 'No se pudo obtener información de tu historial de partidas. Verifique el ID de usuario ' \
                           'ingresado. '

    else:

        resultado_names = [dict_id[hero] for hero in output_series]

    return render_template('solution.html', list_heroes=resultado_names, user_id=user_id, message_user=message_user)


# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
    app.run(debug=True)
