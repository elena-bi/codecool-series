from flask import Flask, render_template, url_for, request, redirect
import data.queries as queries
import data.data_manager
from collections import OrderedDict
from datetime import datetime
from math import ceil
# from dotenv import load_dotenv

# load_dotenv()
app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated')
@app.route('/shows/most-rated/<page>')
@app.route('/shows/most-rated/<page>/<orderby>/<order>')
def most_rated(orderby='rating', page=1, order='desc'):
    most_rated_shows = queries.most_ratedShows(
        orderby=orderby,
        page=page,
        order=order
    )

    count_shows = queries.count_shows()
    count_shows = [row['count'] for row in count_shows][0]
    total = ceil(int(count_shows) / 15)
    
    pagination_list = [
        max(0, page - 2),
        max(0, page - 1),
        page,
        min(page + 1, total),
        min(page + 2, total)
    ]

    pagination_list = [x for i, x in enumerate(pagination_list) if x > 0 and x not in pagination_list[:i]]
    pagination_list = [( url_for("most_rated", orderby=orderby, page=x, order=order), x ) for x in pagination_list]

    return render_template(
        'most_rated.html',
        shows=most_rated_shows,
        current_page=int(page),
        total=total,
        orderby=orderby,
        order=order,
        pagination_list=pagination_list
    )


@app.route("/show/<id>")
def show_details(id):
    show_details = queries.show_details(id)
    show_actors = queries.actors(id)
    show_actors = [row['actors'] for row in show_actors][0].split(',')

    seasons = queries.get_seasons(id)
    return render_template('show_details.html', shows=show_details, actors=show_actors, seasons=seasons)


def main():
    app.run(debug=False, port=8080)


if __name__ == '__main__':
    main()
