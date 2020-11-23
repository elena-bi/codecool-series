import os
import psycopg2
import psycopg2.extras

from psycopg2.extras import RealDictCursor
import data.database_common as database_common

@database_common.connection_handler
def get_shownumbers(cursor: RealDictCursor):
    cursor.execute("select count (*) from shows")
    return cursor.fetchall()


@database_common.connection_handler
def get_shows(cursor: RealDictCursor) -> list:
 # cursor.execute(query, {'order_by': sort_by_list[order_by_col]})
 #    cursor.execute("SELECT * FROM shows")
    cursor.execute("SELECT * FROM shows")
    return cursor.fetchall()


@database_common.connection_handler
def most_ratedShows(cursor: RealDictCursor, orderby, page, page_size, order):
    offset = (int(page) -1) * int(page_size)
    if order=='asc':
        query = f"""
        SELECT title, extract(year from shows.year)::integer as release_year, runtime, round(rating,1) as rating, genre, trailer, homepage
        FROM shows join (select shows.id, string_agg(genres.name::text, ', ' order by genres.name) as genre 
        from shows 
        inner join show_genres on show_genres.show_id = shows.id 
        inner join genres on show_genres.genre_id = genres.id group by shows.id) as x on x.id = shows.id 
        order by {orderby} desc limit {page_size} offset {offset}"""
    else:
        query = f"""
            SELECT title, extract(year from shows.year)::integer as release_year, runtime, round(rating,1) as rating, genre, trailer, homepage
            FROM shows join (select shows.id, string_agg(genres.name::text, ', ' order by genres.name) as genre 
            from shows 
            inner join show_genres on show_genres.show_id = shows.id 
            inner join genres on show_genres.genre_id = genres.id group by shows.id) as x on x.id = shows.id 
            order by {orderby} asc limit {page_size} offset {offset}"""
    cursor.execute(query)
    return cursor.fetchall()



@database_common.connection_handler
def show_details(cursor: RealDictCursor, id):
    query = f"""
    SELECT title, extract(year from shows.year)::integer as release_year, (shows.runtime / 60 )::integer as hours, (shows.runtime - ((shows.runtime / 60)::integer * 60)) as minutes, round(rating,1) as rating, genre, substring(trailer, 28) as trailer, homepage 
    FROM shows 
    join (select shows.id, string_agg(genres.name::text, ', ' order by genres.name) as genre 
    from shows 
    inner join show_genres on show_genres.show_id = shows.id 
    inner join genres on show_genres.genre_id = genres.id group by shows.id) as x on x.id = shows.id 
    where shows.id = {id}
    order by rating desc limit 15 offset 0;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_actors(cursor: RealDictCursor, id):
    query=f"""
    select show_characters.show_id, string_agg(actors.name::text, ', ') as actors from actors
    join show_characters on
    show_characters.actor_id = actors.id
    where show_characters.show_id = {id}
    group by show_characters.show_id
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_seasons(cursor: RealDictCursor, id):
    query=f"""
    select seasons.title as season, seasons.overview as overview, shows.title as title from seasons
    join shows
    on shows.id = seasons.show_id
    where show_id = {id};
"""
    cursor.execute(query)
    return cursor.fetchall()
# def establish_connection(connection_data=None):
#     """
#     Create a database connection based on the :connection_data: parameter
#
#     :connection_data: Connection string attributes
#
#     :returns: psycopg2.connection
#     """
#     if connection_data is None:
#         connection_data = get_connection_data()
#     try:
#         connect_str = "dbname={} user={} host={} password={}".format(connection_data['dbname'],
#                                                                      connection_data['user'],
#                                                                      connection_data['host'],
#                                                                      connection_data['password'])
#         conn = psycopg2.connect(connect_str)
#         conn.autocommit = True
#     except psycopg2.DatabaseError as e:
#         print("Cannot connect to database.")
#         print(e)
#     else:
#         return conn
#
#
# def get_connection_data(db_name=None):
#     """
#     Give back a properly formatted dictionary based on the environment variables values which are started
#     with :MY__PSQL_: prefix
#
#     :db_name: optional parameter. By default it uses the environment variable value.
#     """
#     if db_name is None:
#         db_name = os.environ.get('MY_PSQL_DBNAME')
#
#     return {
#         'dbname': db_name,
#         'user': os.environ.get('MY_PSQL_USER'),
#         'host': os.environ.get('MY_PSQL_HOST'),
#         'password': os.environ.get('MY_PSQL_PASSWORD')
#     }
#
#
# def execute_script_file(file_path):
#     """
#     Execute script file based on the given file path.
#     Print the result of the execution to console.
#
#     Example:
#     > execute_script_file('db_schema/01_create_schema.sql')
#
#     :file_path: Relative path of the file to be executed.
#     """
#     package_directory = os.path.dirname(os.path.abspath(__file__))
#     full_path = os.path.join(package_directory, file_path)
#     with open(full_path) as script_file:
#         with establish_connection() as conn, \
#                 conn.cursor() as cursor:
#             try:
#                 sql_to_run = script_file.read()
#                 cursor.execute(sql_to_run)
#                 print("{} script executed successfully.".format(file_path))
#             except Exception as ex:
#                 print("Execution of {} failed".format(file_path))
#                 print(ex.args)
#
#
# def execute_select(statement, variables=None, fetchall=True):
#     """
#     Execute SELECT statement optionally parameterized.
#     Use fetchall=False to get back one value (fetchone)
#
#     Example:
#     > execute_select('SELECT %(title)s; FROM shows', variables={'title': 'Codecool'})
#
#     statement: SELECT statement
#
#     variables:  optional parameter dict, optional parameter fetchall"""
#     result_set = []
#     with establish_connection() as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
#             cursor.execute(statement, variables)
#             result_set = cursor.fetchall() if fetchall else cursor.fetchone()
#     return result_set
#
#
# def execute_dml_statement(statement, variables=None):
#     """
#     Execute data manipulation query statement (optionally parameterized)
#
#     :statment: SQL statement
#
#     :variables:  optional parameter dict"""
#     result = None
#     with establish_connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(statement, variables)
#             try:
#                 result = cursor.fetchone()
#             except psycopg2.ProgrammingError as pe:
#                 pass
#     return result
