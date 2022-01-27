# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# stats.wwdt.me is released under the terms of the Apache License 2.0
"""Scorekeepers Routes for Wait Wait Stats Page"""
from flask import Blueprint, current_app, redirect, render_template, url_for
import mysql.connector
from wwdtm.scorekeeper import Scorekeeper

from app.utility import redirect_url

blueprint = Blueprint("scorekeepers", __name__)


def random_scorekeeper_slug() -> str:
    """Return a random scorekeeper slug from ww_scorekeepers table"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = _database_connection.cursor(dictionary=False)
    query = ("SELECT sk.scorekeeperslug FROM ww_scorekeepers sk "
             "WHERE sk.scorekeeperslug <> 'tbd' "
             "ORDER BY RAND() "
             "LIMIT 1;")
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return result[0]


@blueprint.route("/")
def index():
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    scorekeeper = Scorekeeper(database_connection=_database_connection)
    scorekeepers = scorekeeper.retrieve_all()
    _database_connection.close()

    if not scorekeepers:
        return redirect(url_for("main.index"))

    return render_template("scorekeepers/scorekeepers.html",
                           scorekeepers=scorekeepers)


@blueprint.route("/<string:scorekeeper_slug>")
def details(scorekeeper_slug: str):
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    scorekeeper = Scorekeeper(database_connection=_database_connection)
    details = scorekeeper.retrieve_details_by_slug(scorekeeper_slug)
    _database_connection.close()

    if not details:
        return redirect(url_for("scorekeepers.index"))

    scorekeepers = []
    scorekeepers.append(details)
    return render_template("scorekeepers/single.html",
                           scorekeeper_name=details["name"],
                           scorekeepers=scorekeepers)


@blueprint.route("/all")
def all():
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    scorekeeper = Scorekeeper(database_connection=_database_connection)
    scorekeepers = scorekeeper.retrieve_all_details()
    _database_connection.close()

    if not scorekeepers:
        return redirect(url_for("scorekeepers.index"))

    return render_template("scorekeepers/all.html",
                           scorekeepers=scorekeepers)


@blueprint.route("/random")
def random():
    _slug = random_scorekeeper_slug()
    return redirect_url(url_for("scorekeepers.details",
                                scorekeeper_slug=_slug))
