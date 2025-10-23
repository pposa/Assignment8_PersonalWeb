from flask import Flask, render_template, url_for, request, redirect
import os
from DAL import get_projects, insert_project

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def projects():
    # Fetch projects; if DB is empty, optionally seed from known images
    rows = get_projects(limit=100)

    if not rows:
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
        seeds = []
        # Seed EY Case Competition if images exist
        ey_imgs = []
        for fname in ['EY1.png', 'EY2.png']:
            if os.path.exists(os.path.join(static_dir, fname)):
                ey_imgs.append(fname)
        if ey_imgs:
            for img in ey_imgs:
                insert_project({
                    'Title': 'EY Case Competition',
                    'Description': 'Case competition entry demonstrating strategic digital transformation with supporting visuals.',
                    'ImageFileName': img,
                })

        # Seed Patient Transparency Prototype if images exist
        hosp_imgs = []
        for fname in ['image (2).png', 'image (3).png']:
            if os.path.exists(os.path.join(static_dir, fname)):
                hosp_imgs.append(fname)
        if hosp_imgs:
            for img in hosp_imgs:
                insert_project({
                    'Title': 'Patient Transparency Prototype',
                    'Description': 'Mobile app prototype improving patient transparency on wait times, costs, and billing.',
                    'ImageFileName': img,
                })

        rows = get_projects(limit=100)

    # Group rows by Title to collate multiple images per project
    grouped = {}
    for r in rows:
        title = r.get('Title')
        if title not in grouped:
            grouped[title] = {
                'Title': title,
                'Description': r.get('Description', ''),
                'Images': []
            }
        img = r.get('ImageFileName')
        if img:
            grouped[title]['Images'].append(img)

    projects_list = list(grouped.values())
    return render_template('projects.html', projects=projects_list)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/add_project', methods=['POST'])
def add_project():
    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    image_filename = (request.form.get('image_filename') or '').strip()

    if title and image_filename:
        insert_project({
            'Title': title,
            'Description': description,
            'ImageFileName': image_filename,
        })
    # After insert, redirect to projects page so it's immediately visible
    return redirect(url_for('projects'))

if __name__ == '__main__':
    # Bind to all interfaces so the app is reachable when running inside Docker
    app.run(host='0.0.0.0', port=5002, debug=True)
