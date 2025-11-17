from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from .. import db
from ..models.project import Project
from flask_login import login_required
import os

update_bp = Blueprint('update', __name__, url_prefix="/update")

UPDATE_FOLDER = "updates"
os.makedirs(UPDATE_FOLDER, exist_ok=True)

@update_bp.route("/", methods=["GET", "POST"])
@login_required
def update_file():
    if request.method == "POST":
        project_name = request.form.get("project_name")
        file = request.files.get("file")

        if not project_name or not file or file.filename == "":
            flash("Preencha todos os campos e selecione um arquivo!", "error")
            return redirect(url_for("update.update_file"))

        filepath = os.path.join(UPDATE_FOLDER, file.filename)
        file.save(filepath)

        project = Project.query.filter_by(name=project_name).first()
        if project:
            project.filename = file.filename
            project.update_date = datetime.now()
        else:
            project = Project(
                name=project_name,
                filename=file.filename,
                update_date=datetime.now()
            )
            db.session.add(project)

        db.session.commit()

        flash("Arquivo atualizado com sucesso!", "success")
        return redirect(url_for("update.update_file"))

    return render_template("update.html")
