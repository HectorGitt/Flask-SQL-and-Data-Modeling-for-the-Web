#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from request_handler import Request
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('VenueGenre', backref='venue',lazy=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue',lazy=True)
    
    def __repr__(self):
        return f'{self.name}'

class Artist(db.Model):
    __tablename__ = 'Artist'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('ArtistGenre', backref='artist',lazy=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist',lazy=True)
    def __repr__(self):
        return f'{self.name}'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
      return f'{self.artist_id} {self.venue_id}'
    
    
class Genre(db.Model):
    __tablename__ = 'Genre'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    #model relationships
    artist_genre = db.relationship('ArtistGenre', backref='genre', lazy=True)
    venue_genre = db.relationship('VenueGenre', backref='genre', lazy=True)
    
    def __repr__(self):
        return f'{self.name}'
    
class ArtistGenre(db.Model):
    __tablename__ = 'artist_genre'
    
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('Genre.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    
    def __repr__(self):
      return f'{Genre.query.filter_by(id=self.genre_id).first().name}'
    
class VenueGenre(db.Model):
    __tablename__ = 'venue_genre'
    
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('Genre.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
        return f'{Genre.query.filter_by(id=self.genre_id).first().name}'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.all()
  cities = []
  states = []
  #using set to avoid duplicate data
  location = set()
  data = []
  #save cities and states in location set
  for venue in venues:
    location.add((venue.city,venue.state))
  print(location)
  #group data by location
  for place in location:
    data.append({
      'city':place[0],
      'state':place[1],
      'venues':Venue.query.filter_by(city=place[0],state=place[1]),
    })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  #append list of result to array
  venues_arr = []
  for venue in venues:
    venues_arr.append({
      'id':venue.id,
      'name': venue.name,
    })
  #added count to response data
  response = {
    'count':len(venues_arr),
    'data': venues_arr,
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  #request handler class
  Req = Request()
  data = Req.model_control(venue, 'venue')
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    #request handler class
    Req = Request()
    venue, genres = Req.request_control(form,Venue, 'venue')
    db.session.add(venue)
    db.session.commit()
    for i in genres:
      #if genre does not exist
      if bool(Genre.query.filter_by(name=i).first()) is False:
        #save genre in db
        genre = Genre(name=i)
        db.session.add(genre)
        db.session.commit()
      else:
        #get genre if exist
        genre = Genre.query.filter_by(name=i).first()
      #Attach genre to venue
      venue_genre = VenueGenre(genre_id=genre.id, venue_id=venue.id)
      db.session.add(venue_genre)
      db.session.commit()
      # TODO: modify data to be the data object returned from db insertion
    name = venue.name
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., 
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    print(sys.exc_info())
    flash('An error occurred. Venue ' + name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except():
    db.session.rollback()
  finally:
    db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  artists_arr = []
  #append list of result to array
  for artist in artists:
    artists_arr.append({
      'id':artist.id,
      'name': artist.name,
    })
  #added count to response data
  response = {
    'count':len(artists_arr),
    'data': artists_arr,
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(id=artist_id).first()
  #request handler class
  Req = Request()
  data = Req.model_control(artist, 'artist')

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter_by(id=artist_id).first()
  #request handler class
  Req = Request()
  Req.edit_get(form,artist, 'artist')
  artist_genres = ArtistGenre.query.filter_by(artist_id=artist.id).all()
  genre_arr = []
  #append genre to array and render on template
  for artist_genre in artist_genres:
    genre = Genre.query.filter_by(id=artist_genre.genre_id).first()
    genre_arr.append(genre.name)
  form.genres.data = genre_arr
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    #request handler class
    Req = Request()
    Req.edit_post(form, artist, 'artist')
    artist_genre = ArtistGenre.query.filter_by(artist_id=artist.id).all()
    for each in artist_genre:
      db.session.delete(each)
    db.session.commit()
    genres = form.genres.data
    for i in genres:
          #if genre does not exist
      if bool(Genre.query.filter_by(name=i).first()) is False:
        #save genre in db
        genre = Genre(name=i)
        db.session.add(genre)
        db.session.commit()
      else:
        #get genre if exist
        genre = Genre.query.filter_by(name=i).first()
      #Attach genre to artist
      artist_genre = ArtistGenre(genre_id=genre.id, artist_id=artist.id)
      db.session.add(artist_genre)
      db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter_by(id=venue_id).first()
  #request handler class
  Req = Request()
  Req.edit_get(form,venue, 'venue')
  venue_genres = VenueGenre.query.filter_by(venue_id=venue.id).all()
  genre_arr = []
  #append genre to array and render on template
  for venue_genre in venue_genres:
    genre = Genre.query.filter_by(id=venue_genre.genre_id).first()
    genre_arr.append(genre.name)
  form.genres.data = genre_arr
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    #request handler class
    Req = Request()
    Req.edit_post(form, venue, 'venue')
    venue_genre = VenueGenre.query.filter_by(venue_id=venue.id).all()
    for each in venue_genre:
      db.session.delete(each)
    db.session.commit()
    genres = form.genres.data
    for i in genres:
      #if genre does not exist
      if bool(Genre.query.filter_by(name=i).first()) is False:
        #save genre in db
        genre = Genre(name=i)
        db.session.add(genre)
        db.session.commit()
      else:
        #get genre if exist
        genre = Genre.query.filter_by(name=i).first()
      #Attach genre to venue
      venue_genre = VenueGenre(genre_id=genre.id, venue_id=venue.id)
      db.session.add(venue_genre)
      db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))



#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  try:
    # TODO: insert form data as a new Artist record in the db, instead
    form = ArtistForm()
    Req = Request()
    artist, genres = Req.request_control(form,Artist,'artist')
    db.session.add(artist)
    db.session.commit()
    genres = form.genres.data
    for i in genres:
      #if genre does not exist
      if bool(Genre.query.filter_by(name=i).first()) is False:
        #save genre in db
        genre = Genre(name=i)
        db.session.add(genre)
        db.session.commit()
      else:
        #get genre if exist
        genre = Genre.query.filter_by(name=i).first()
      #Attach genre to artist
      artist_genre = ArtistGenre(genre_id=genre.id, artist_id=artist.id)
      db.session.add(artist_genre)
      db.session.commit()
      # TODO: modify data to be the data object returned from db insertion
    name = artist.name
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + name + ' could not be listed.')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = [] 
  for show in shows:
    # append shows to list
    data.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:
    # TODO: insert form data as a new Show record in the db, instead
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    artist = Artist.query.filter_by(id=artist_id).first()
    if artist.seeking_venue:
      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      print(show)
      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    else:
      flash('Artist not seeking for shows')
  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('Show was not succesfully listed')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
