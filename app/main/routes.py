import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db
from app.main import bp
from app.models import Project, Image
from app.main.forms import ProjectForm, ImageUploadForm, ExifEditForm
from app.main.exif_utils import ExifManager

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('main/index.html', title='Home', projects=projects)

@bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                        description=form.description.data,
                        user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully.')
        return redirect(url_for('main.project', project_id=project.id))
    return render_template('main/create_project.html', title='New Project', form=form)

@bp.route('/project/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    return render_template('main/project.html', title=project.name, project=project)

@bp.route('/project/<int:project_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_image(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    form = ImageUploadForm()
    if form.validate_on_submit():
        if 'image' not in request.files:
            flash('No image file')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            image = Image(
                filename=filename,
                original_filename=file.filename,
                title=form.title.data,
                description=form.description.data,
                keywords=form.keywords.data,
                copyright=form.copyright.data,
                author=form.author.data,
                created_date=form.created_date.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                project_id=project.id
            )
            
            db.session.add(image)
            db.session.commit()
            
            # Write EXIF data to the image
            exif_data = {
                'title': image.title,
                'description': image.description,
                'copyright': image.copyright,
                'author': image.author,
                'created_date': image.created_date,
                'latitude': image.latitude,
                'longitude': image.longitude
            }
            
            ExifManager.write_exif(filepath, exif_data)
            
            flash('Image uploaded successfully')
            return redirect(url_for('main.project', project_id=project_id))
    
    return render_template('main/upload_image.html', title='Upload Image',
                         project=project, form=form)

@bp.route('/project/<int:project_id>/image/<int:image_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_image(project_id, image_id):
    project = Project.query.get_or_404(project_id)
    image = Image.query.get_or_404(image_id)
    
    if project.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    form = ExifEditForm()
    if request.method == 'GET':
        form.title.data = image.title
        form.description.data = image.description
        form.keywords.data = image.keywords
        form.copyright.data = image.copyright
        form.author.data = image.author
        form.created_date.data = image.created_date
        form.latitude.data = image.latitude
        form.longitude.data = image.longitude
    
    if form.validate_on_submit():
        image.title = form.title.data
        image.description = form.description.data
        image.keywords = form.keywords.data
        image.copyright = form.copyright.data
        image.author = form.author.data
        image.created_date = form.created_date.data
        image.latitude = form.latitude.data
        image.longitude = form.longitude.data
        
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
        exif_data = {
            'title': image.title,
            'description': image.description,
            'copyright': image.copyright,
            'author': image.author,
            'created_date': image.created_date,
            'latitude': image.latitude,
            'longitude': image.longitude
        }
        
        if ExifManager.write_exif(image_path, exif_data):
            db.session.commit()
            flash('Image metadata updated successfully.')
            return redirect(url_for('main.view_image', project_id=project_id, image_id=image_id))
        else:
            flash('Error updating image metadata.')
    
    return render_template('main/edit_image.html', title='Edit Image', form=form,
                         project=project, image=image)

@bp.route('/project/<int:project_id>/image/<int:image_id>')
@login_required
def view_image(project_id, image_id):
    project = Project.query.get_or_404(project_id)
    image = Image.query.get_or_404(image_id)
    
    if project.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    return render_template('main/view_image.html', title=image.title or 'View Image',
                         project=project, image=image)

@bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/project/<int:project_id>/image/<int:image_id>/download')
@login_required
def download_image(project_id, image_id):
    project = Project.query.get_or_404(project_id)
    image = Image.query.get_or_404(image_id)
    
    if project.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                             image.filename,
                             as_attachment=True,
                             download_name=image.original_filename)