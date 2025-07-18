import os
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import requests
from urllib.parse import urlparse
from core.nlp_processor import extract_info
from core.pdf_generator import create_pdf_from_html

app = Flask(__name__)
app.secret_key = os.urandom(24)

def parse_manual_form(form):
    """Parses the structured data from the manual entry form."""
    data = {
        "name": form.get("name"),
        "introduction": form.get("introduction"),
        "skills": [skill.strip() for skill in form.get("skills", "").split(',') if skill.strip()],
        "contacts": [],
        "experience": [],
        "projects": [],
        "education": []
    }
    contact_items = [item.strip() for item in form.get("contacts", "").split(',') if item.strip()]
    for item in contact_items:
        if " - " in item:
            heading, details = item.split(" - ", 1)
            data["contacts"].append({"heading": heading.strip(), "details": details.strip()})

    for section_type in ["experience", "projects", "education"]:
        headings = form.getlist(f"{section_type}_headings")
        details = form.getlist(f"{section_type}_details")
        for h, d in zip(headings, details):
            if h or d:
                data[section_type].append({"heading": h, "details": d})
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    prompt_data = session.pop('prompt_data', None)

    if request.method == 'POST':
        if 'prompt' in request.form and request.form.get('prompt'):
            portfolio_data = extract_info(request.form.get('prompt'))
        else:
            portfolio_data = parse_manual_form(request.form)

        css_file = request.form.get('css_file', 'style1.css')
        primary_color = request.form.get('primary_color', '#2c3e50')
        secondary_color = request.form.get('secondary_color', '#ecf0f1')
        font_family = request.form.get('font_family', "'Poppins', sans-serif")

        return render_template(
            'portfolio.html',
            data=portfolio_data,
            css_file=css_file,
            primary_color=primary_color,
            secondary_color=secondary_color,
            font_family=font_family
        )

    return render_template('index.html', prompt_data=prompt_data)

@app.route('/import/github_url', methods=['POST'])
def import_from_github_url():
    github_url = request.form.get('github_url')
    if not github_url:
        return redirect(url_for('home'))
    try:
        path = urlparse(github_url).path
        username = path.strip('/').split('/')[0]
        if not username:
            raise ValueError("Invalid URL")
    except Exception:
        return redirect(url_for('home'))
    try:
        user_api_url = f"https://api.github.com/users/{username}"
        account_info = requests.get(user_api_url).json()
        if account_info.get('message'):
            raise ValueError("User not found")

        repos_api_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"
        repos_info = requests.get(repos_api_url).json()
        user_name = account_info.get("name") or account_info.get("login", "")
        user_bio = account_info.get("bio", "A passionate developer.")
        user_email = account_info.get("email")

        projects = [
            f"a project called '{r['name']}' ({r['description']})"
            for r in repos_info if not r.get("fork") and r.get("description")
        ]
        prompt_lines = [
            f"My name is {user_name}.",
            user_bio,
            f"You can contact me at {user_email}." if user_email else "",
            "I have worked on several projects, including " + ", ".join(projects) + "." if projects else ""
        ]
        session['prompt_data'] = "\n".join(filter(None, prompt_lines))
        return redirect(url_for('home'))
    except Exception as e:
        print(f"GitHub API Error: {e}")
        return "Failed to fetch data from GitHub.", 500

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    html_content = request.form.get('html_content')
    if not html_content:
        return "Error: No content received.", 400
    try:
        pdf_file = create_pdf_from_html(html_content, base_url=request.host_url)
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=portfolio.pdf'
        return response
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return "An error occurred while generating the PDF.", 500

# ✅ NEW: This handles form-based download from portfolio.html
@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        import json

        data = json.loads(request.form.get('data'))
        css_file = request.form.get('css_file', 'style1.css')
        primary_color = request.form.get('primary_color', '#2c3e50')
        secondary_color = request.form.get('secondary_color', '#ecf0f1')
        font_family = request.form.get('font_family', "'Poppins', sans-serif")

        # Render HTML using same template
        html_content = render_template(
            'portfolio.html',
            data=data,
            css_file=css_file,
            primary_color=primary_color,
            secondary_color=secondary_color,
            font_family=font_family
        )

        pdf_file = create_pdf_from_html(html_content, base_url=request.host_url)
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=portfolio.pdf'
        return response

    except Exception as e:
        print(f"Download PDF Error: {e}")
        return "An error occurred while creating the PDF.", 500

if __name__ == '__main__':
    app.run(debug=True)
