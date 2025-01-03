from ..models import *
from ..extensions import db
from ..services.plots import *
from flask import Blueprint, render_template
import logging

analytics = Blueprint('analytics', __name__)


@analytics.route("/user_analytics")
def user_analytics():
    logging.debug(f"query all: {db.session.query(Track).all()}") #*can i access db here? i can import
    df = get_table_from_db(db, Lyrics)

    bargraph_fig = generate_bar_chart(df, "detected_language")
    linegraph_fig = generate_line_chart_lyrics(df, "detected_language")

    bargraph_html = generate_fig_html(bargraph_fig)
    linegraph_html = generate_fig_html(linegraph_fig)

    return render_template('user_analytics.html', plot1_html = bargraph_html, plot2_html = linegraph_html)