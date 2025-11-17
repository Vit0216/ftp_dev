from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from .. import db
from ..models.project import Project
from flask_login import login_required
import os

delete_bp = Blueprint('delete', __name__, url_prefix="/delete")

UPLOAD_FOLDER = "uploads"

@delete_bp.route("/", methods=["GET", "POST"])
@login_required
def delete_file():
    if request.method == "POST":
        project_name = request.form.get("project_name")

        if not project_name:
            flash("Informe o nome do projeto!", "error")
            return redirect(url_for("delete.delete_file"))

        project = Project.query.filter_by(name=project_name).first()

        if not project:
            flash("Projeto não encontrado!", "error")
            return redirect(url_for("delete.delete_file"))

        filepath = os.path.join(UPLOAD_FOLDER, project.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

        project.delete_date = datetime.now()
        db.session.commit()

        flash("Arquivo deletado com sucesso!", "success")
        return redirect(url_for("delete.delete_file"))

    return render_template("delete.html")
