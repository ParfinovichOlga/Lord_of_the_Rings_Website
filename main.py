import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from sqlalchemy.orm import relationship

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

end_point = 'https://the-one-api.dev/v2/'
headers = {
    'authorization': f'Bearer {ACCESS_TOKEN}'
}

# GET INFORMATION FOR DB
# img_url = ['https://cdn.mos.cms.futurecdn.net/rnfZWUn9wvYnJa74mf6mGB-1200-80.jpg',
#            'https://upload.wikimedia.org/wikipedia/en/a/a9/The_Hobbit_trilogy_dvd_cover.jpg',
#            'https://i0.wp.com/new.hollywoodgothique.com/wp-content/uploads/2013/01/hobbit-unexpected-journey-gollum.jpg?fit=750%2C493',
#            'https://images.tntdrama.com/tnt/$dyna_params/https%3A%2F%2Fi.cdn.tntdrama.com%2Fassets%2Fimages%2F2017%2F03%2FHobbit-Desolation-ofSmaug-2048x1536.jpg',
#            'https://musicart.xboxlive.com/7/948d5100-0000-0000-0000-000000000002/504/image.jpg?w=1920&h=1080',
#            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTp-DCfkgaxhm6wkJx2vhio4UXbxQ9SPhgouHvSYBnViw&s',
#            'https://m.media-amazon.com/images/S/pv-target-images/8f8fcc7680562055d10c1baa5be07d44780ecab56acc4de6948f416665a3a805.jpg',
#            'https://images.squarespace-cdn.com/content/v1/5fbc4a62c2150e62cfcb09aa/1678145559423-2AWE6U3N37W1X27O96SZ/tileburnedin-2.jpeg']
#
# chapters = requests.get(f'{end_point}chapter', headers=headers).json()['docs']
# books = requests.get(f'{end_point}book').json()['docs']
# movies = requests.get(f'{end_point}movie',  headers=headers).json()['docs']
# quotes = requests.get(f"{end_point}/quote",  headers=headers).json()['docs']
# characters = requests.get(f'{end_point}character',  headers=headers).json()['docs']


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy()
db.init_app(app)
Bootstrap4(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250))
    chapters = relationship('Chapter', back_populates='parent_book')


class Chapter(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    book_id = db.Column(db.ForeignKey('books.id'))
    parent_book = relationship('Book', back_populates='chapters')


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    run_time_minutes = db.Column(db.Integer)
    budget_millions = db.Column(db.Integer)
    revenue_millions = db.Column(db.Integer)
    award_nomination = db.Column(db.Integer)
    award_wins = db.Column(db.Integer)
    rotten_tomatoes_score = db.Column(db.Integer)
    img_url = db.Column(db.String)
    quotes = relationship('Quote', back_populates='parent_movie')


class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.String, primary_key=True)
    dialog = db.Column(db.String)
    movie_id = db.Column(db.ForeignKey('movies.id'))
    parent_movie = relationship('Movie', back_populates='quotes')
    character_id = db.Column(db.ForeignKey('characters.id'))
    character = relationship('Character', back_populates='character_quotes')


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    race = db.Column(db.String)
    birth = db.Column(db.String)
    gender = db.Column(db.String)
    death = db.Column(db.String)
    hair = db.Column(db.String)
    height = db.Column(db.Integer)
    realm = db.Column(db.String)
    spouse = db.Column(db.String)
    character_quotes = relationship('Quote', back_populates='character')


with app.app_context():
    db.create_all()

#  FILL THE TABLES WITH DATA
# with app.app_context():
#     for book in books:
#         new_book = Book(id=book['_id'], name=book['name'])
#         db.session.add(new_book)
#         db.session.commit()
#     for chapter in chapters:
#         new_chapter = Chapter(id=chapter['_id'], name=chapter['chapterName'], book_id=chapter['book'])
#         db.session.add(new_chapter)
#         db.session.commit()
#     for movie in movies:
#         new_movie = Movie(id=movie['_id'], name=movie['name'], run_time_minutes=movie['runtimeInMinutes'],
#                           budget_millions=movie['budgetInMillions'],
#                           revenue_millions=movie['boxOfficeRevenueInMillions'],
#                           award_nomination=movie['academyAwardNominations'], award_wins=movie['academyAwardWins'],
#                           img_url=img_url[movies.index(movie)], rotten_tomatoes_score=movie['rottenTomatoesScore'])
#         db.session.add(new_movie)
#         db.session.commit()
#     for quote in quotes:
#         new_quote = Quote(id=quote['_id'], dialog=quote['dialog'], movie_id=quote['movie'],
#                       character_id=quote['character'])
#         db.session.add(new_quote)
#         db.session.commit()
#     for character in characters:
#         new_character = Character(id=character['_id'], name=character['name'], url=character['wikiUrl'],
#                                   race=character['race'], birth=character['birth'], gender=character['gender'],
#                                   death=character['death'], hair=character['hair'], height=character['height'],
#                                   realm=character['realm'], spouse=character['spouse'])
#         db.session.add(new_character)
#         db.session.commit()


@app.route("/")
def home():
    movie_series = db.session.execute(db.select(Movie).where(Movie.id.in_(['5cd95395de30eff6ebccde56', '5cd95395de30eff6ebccde57']))).scalars()
    return render_template("index.html", movies=movie_series)


@app.route("/books")
def all_books():
    result = db.session.execute(db.select(Book)).scalars()
    return render_template("books.html", books=result)


@app.route("/movies")
def all_movies():
    result = db.session.execute(db.select(Movie)).scalars()
    return render_template('movies.html', movies=result)


@app.route("/characters")
def all_characters():
    result = {
                "Ainur": db.session.execute(db.select(Character).where(Character.race == 'Ainur')).scalars(),
                "Black Uruk": db.session.execute(db.select(Character).where(Character.race == 'Black Uruk')).scalars(),
                "Dragons": db.session.execute(db.select(Character).where(Character.race.in_(['Dragon', 'Dragons']))).scalars(),
                "Dwarves": db.session.execute(db.select(Character).where(Character.race.in_(['Dwarf', 'Dwarves']))).scalars(),
                "Eagles": db.session.execute(db.select(Character).where(Character.race.in_(['Eagle', 'Eagles', 'Great Eagles']))).scalars(),
                "Elves": db.session.execute(db.select(Character).where(Character.race.in_(['Elf', 'Elves']))).scalars(),
                "Ents": db.session.execute(db.select(Character).where(Character.race.in_(['Ent', 'Ents']))).scalars(),
                "Orcs": db.session.execute(db.select(Character).where(Character.race.in_(['Orc', ' Orc', 'Orcs']))).scalars(),
                "God": db.session.execute(db.select(Character).where(Character.race == 'God')).scalars(),
                "Great Spiders": db.session.execute(db.select(Character).where(Character.race == 'Great Spiders')).scalars(),
                "Half-elven": db.session.execute(db.select(Character).where(Character.race == 'Half-elven')).scalars(),
                "Hobbits": db.session.execute(db.select(Character).order_by(Character.name).where(Character.race.in_(['Hobbit', 'Hobbits']))).scalars(),
                "Human": db.session.execute(db.select(Character).where(Character.race.in_(['Human', 'Men']))).scalars(),
                "Maiar": db.session.execute(db.select(Character).where(Character.race == 'Maiar')).scalars(),
                "Uruk-hai": db.session.execute(db.select(Character).where(Character.race.in_(['Uruk-hai', 'Uruk-hai,Orc']))).scalars()
        }
    return render_template('characters.html', result=result)


@app.route("/<book_id>/chapter")
def all_chapters(book_id):
    requested_book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    return render_template("chapters.html", book=requested_book)


@app.route("/<movie_id>/quote")
def quotes(movie_id):
    requested_movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    return render_template("quotes.html", movie=requested_movie)


@app.route("/search", methods=['POST'])
def search_character():
    if request.method == 'POST':
        requested_character = db.session.execute(db.select(Character).where(Character.name == request.form["character"].title())).scalar()
        if requested_character:
            return redirect(url_for('show_character', character_id=requested_character.id))
        else:
            return redirect(url_for('all_characters'))


@app.route("/characters/<character_id>")
def show_character(character_id):
    character = db.session.execute(db.select(Character).where(Character.id == character_id)).scalar()
    return render_template('character_info.html', character=character)


if __name__ == '__main__':
    app.run(debug=True, port=502)
