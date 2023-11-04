from flask import Flask, redirect, render_template, url_for
#from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
#from flask_bootstrap import Bootstrap Not working 11/3 5:14

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

#replaced below in favor of above
#connect_db(app)
#db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#debug = DebugToolbarExtension(app) #removed because it never works


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
   
    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()

    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:
    
    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()

    if form.validate_on_submit():  
      

        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        #removed below as it's a 'manual add'
        #new_playlist = Playlist(
        #    name=name,
        #    description=description
        #    )
    
        db.session.add(new_playlist)
        db.session.commit()

        return redirect("/")
    else:
    
        return render_template("new_playlist.html", form=form)
    
@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    
    
    playlist = Playlist.query.get(playlist_id)
    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id).all()
    song_details = [Song.query.get(song.song_id) for song in playlist_songs]

    return render_template("playlist.html", playlist=playlist, songs=song_details)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    form = SongForm()

    if form.validate_on_submit():  
        new_song = Song(title=form.title.data, artist=form.artist.data)
  
    
        db.session.add(new_song)
        db.session.commit()

        return redirect("/")
    else:
    
        return render_template("new_song.html", form=form)
    
@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get(song_id)
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    return render_template("song.html", song=song)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    form.song.choices = [(song.id, song.title) for song in Song.query.order_by('title').all()]

    if form.validate_on_submit():  
        add_song= PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)

        db.session.add(add_song)
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", form=form, playlist=playlist, playlist_id=playlist_id)
  
    
    
    ##commented out below...not sure what it's for yet 11/3 11:46
    ## BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#
    ## THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS
#
    #playlist = Playlist.query.get_or_404(playlist_id)
    #form = NewSongForPlaylistForm()
#
    ## Restrict form to songs not already on this playlist
#
    #curr_on_playlist = ...
    #form.song.choices = ...
#
    #if form.validate_on_submit():
#
    #      # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#
    #      return redirect(f"/playlists/{playlist_id}")
#
    #return render_template("add_song_to_playlist.html",
    #                         playlist=playlist,
    #                         form=form)
#