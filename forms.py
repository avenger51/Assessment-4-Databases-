"""Forms for playlist app."""

from wtforms import SelectField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired  


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField("Playlist Name", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    # Add the necessary code to use this form


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Title", validators=[InputRequired()])
    artist = StringField("Artist", validators=[InputRequired()])
    # Add the necessary code to use this form


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE 
#seems you need an existing song to get from the drop down..
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""
    #song = StringField('Song To add', validators=[InputRequired()])  <--this just adds playlist_songs without linking?
    song = SelectField('Song To Add', coerce=int, choices=[])


