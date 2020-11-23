from data import data_manager
from data.data_manager import get_seasons


def get_shows():
    return data_manager.get_shows()

def most_ratedShows(orderby='rating', page=1, page_size=15, order='desc'):
    return data_manager.most_ratedShows(orderby, page, page_size, order)


def count_shows():
    return data_manager.get_shownumbers()

def show_details(id):
    return data_manager.show_details(id)

def actors(id):
    actors = data_manager.get_actors(id)
    return actors

def seasons(id):
    return data_manager.get_seasons(id)