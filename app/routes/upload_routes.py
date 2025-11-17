from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from .. import db
from ..models.project import Project
from flask_login import login_required
import os

upload_bp = Blueprint('upload', __name__, url_prefix="/upload")

# Pasta onde os arquivos serão salvos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rota para listar arquivos ativos
@upload_bp.route("/", methods=["GET"])
@login_required
def index():
    projects = Project.query.filter_by(delete_date=None).all()
    return render_template("index.html", projects=projects)

# Rota para novo upload
@upload_bp.route("/new", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        project_name = request.form.get("project_name")
        file = request.files.get("file")

        if not project_name or not file or file.filename == "":
            flash("Preencha todos os campos e selecione um arquivo!", "error")
            return redirect(url_for("upload.upload_file"))

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        new_project = Project(
            name=project_name,
            filename=file.filename,
            upload_date=datetime.now()
        )
        db.session.add(new_project)
        db.session.commit()

        flash("Arquivo enviado com sucesso!", "success")
        return redirect(url_for("upload.index"))

    return render_template("upload.html")
