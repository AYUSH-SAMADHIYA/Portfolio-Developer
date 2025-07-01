from flask import Flask, request, render_template
import random


app = Flask(__name__)

def extract_info(prompt):
    # Initialize extracted info with None values
    extracted_info = {
        "title": None,
        "name": None,
        "introduction": None,
        "skill": None,
        "contact": None,
        "education": None,
        "project": None
    }
    
    # Split prompt by semicolon to extract sections
    sections = prompt.split(";")
    for section in sections:
        # Find the first colon to separate key and value
        colon_index = section.find(":")
        if (colon_index != -1) and (len(section[:colon_index].strip())>0) and (len(section[colon_index + 1:].strip())>0):
            key = section[:colon_index].strip().lower()
            value = section[colon_index + 1:].strip()
            # Check for relevant keys
            if key in extracted_info:
                extracted_info[key] = value
    
    # Split skills into a list if available
    if extracted_info["skill"]:
        extracted_info["skill"] = [skill.strip() for skill in extracted_info["skill"].split(",")]
  
    # Split contacts into a list of dictionaries if availableṇṇṆ
    if extracted_info["contact"]:
        contacts = []
        contact_items = extracted_info["contact"].split(",")
        for item in contact_items:
            heading_details = item.split(" - ")
            if len(heading_details) == 2:
                contacts.append({
                    "heading": heading_details[0].strip(),
                    "details": heading_details[1].strip()
                })
        extracted_info["contact"] = contacts
    
    # Split education into a list of dictionaries if available
    if extracted_info["education"]:
        educations = []
        education_items = extracted_info["education"].split(",")
        for item in education_items:
            heading_details = item.split(" - ")
            if len(heading_details) == 2:
                educations.append({
                    "heading": heading_details[0].strip(),
                    "details": heading_details[1].strip()
                })
        extracted_info["education"] = educations
    
    # Split projects into a list of dictionaries if available
    if extracted_info["project"]:
        projects = []
        project_items = extracted_info["project"].split(",")
        for item in project_items:
            heading_details = item.split(" - ")
            if len(heading_details) == 2:
                projects.append({
                    "heading": heading_details[0].strip(),
                    "details": heading_details[1].strip()
                })
        extracted_info["project"] = projects
    
    return extracted_info

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        info = extract_info(prompt)
        css_file = random.choice(['style1.css', 'style2.css', 'style3.css', 'style4.css','style5.css','style6.css'])

        return render_template('base_template.html', 
                               title=info['title'], 
                               name=info['name'], 
                               introduction=info['introduction'],
                               skills=info['skill'],
                               contacts=info['contact'],
                               educations=info['education'],
                               projects=info['project'],
                               css_file=css_file)
    return """
   <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio Developer</title>
  <style>
    @import url('https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800');

    html,
    body {
      height: 100%
    }

    body {
      align-items: center;
      background: #642B73;
      background: linear-gradient(to bottom, #C6426E, #642B73);
      display: flex;
      font-family: 'Open Sans', sans;
      justify-content: center;
      overflow: hidden;
      perspective: 1800px;
      text-align: center;
      margin: 0 20px;
    }

    h1 {
      color: #3e3e42;
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -1px;
      margin-bottom: 30px;
      transform: translateZ(35px);
    }

    h3 {
      color: #eb285d;
      font-size: 16px;
      margin-bottom: 6px;
      transform: translateZ(25px);
    }

    .cards {
      background: #fff;
      border-radius: 15px;
      box-shadow: 0px 10px 20px 20px rgba(0, 0, 0, 0.17);
      display: inline-block;
      padding: 3px 35px;
      perspective: 1800px;
      text-align: center;
      transform-origin: 50% 50%;
      transform-style: preserve-3d;
      transform: rotateX(11deg) rotateY(16.5deg);
      height: 500px;
      min-width: 595px;
      position: relative;
    }

    .cards input {
      align-items: center;
      align-self: center;
    }

    .twitter__link {
      cursor: pointer;
      position: absolute;
      right: -10px;
      top: 12px;
      z-index: -1;
      background: #00aced;
      border-radius:111px;
      text-decoration: none;
      justify-content: space-between;
      font-weight: 600;
      display: flex;
      align-items: center;
      color: #fff;
      font-size: 14px;
      opacity: 0.6;
      
      &:hover {
        opacity: 1;
      }
    }
    
    .input-container textarea {
      width: 80%;
      height: 350px;
      border: none;
      outline: none;
      background: transparent;
      font-family: 'Open Sans', sans;
      font-size: 18px;
      margin-top: 20px;
      color: #3e3e42;
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }

   ::placeholder {
      color: grey;
      margin-top:70px;
      text-align:center;
      padding-top:70px;
      opacity: .5; /* Firefox */
    }

    .input-container input[type="submit"] {
      width:  auto;
      height: 40px;
      background-color: #eb285d;
      border: none;
      color: #fff;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      margin-top: 20px;
      position: absolute;
      left: 50%;
      bottom: 20px;
      transform: translateX(-50%);
      transition: background-color 0.3s ease;
      border-radius:111px;
    }
    
    .input-container input[type="submit"]:hover {
      background-color: #C6426E;
    }
    
    .twitter__icon {
      border-radius:111px;
      height: 100px;
    }

    .help-button, .example-button {
      position: absolute;
      top: 10px;
      background-color: #eb285d;
      border: none;
      color: white;
      padding: 10px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 14px;
      font-weight: bold;
      transition: background-color 0.3s ease;
    }

    .help-button:hover, .example-button:hover {
      background-color: #C6426E;
    }

    .help-button {
      left: 10px;
    }

    .example-button {
      left: 80px;
    }

    .help-note {
      display: none;
      position: absolute;
      top: 50px;
      left: 10px;
      background-color: #fff;
      color: #3e3e42;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      z-index: 10;
    }
  </style>
</head>

<body>
  <button class="help-button" onclick="toggleHelpNote()">Help</button>
  <button class="example-button" onclick="populateExample()">Example Prompt</button>
  <div class="help-note" id="help-note">
    <p>Enter your portfolio details in the format:</p>
    <ul>
      <li><strong>Title:</strong> Your page title;</li>
      <li><strong>Name:</strong> Your full name;</li>
      <li><strong>Introduction:</strong> A brief introduction about yourself;</li>
      <li><strong>Skill:</strong> Skills separated by commas;</li>
      <li><strong>Contact:</strong> Contact details in the format 'heading - details', separated by commas;</li>
      <li><strong>Education:</strong> Education details in the format 'heading - details', separated by commas;</li>
      <li><strong>Project:</strong> Project details in the format 'heading - details', separated by commas;</li>
    </ul>
    <p>END EACH SECTION WITH SEMICOLON(;)</p>
  </div>
  <div class="cards">
    <h3>ROBOAI</h3>
    <h1>PORTFOLIO DEVELOPER VERSION 0.1</h1>
    <form class="input-container" method="post" id="input-container">
      <textarea name="prompt" rows="10" cols="80" placeholder="Enter your portfolio details here..."></textarea><br>
        <input type="submit" value="Generate Portfolio">
    </form>
  </div>

  <a class="twitter__link" target="_blank"
    href="https://media.licdn.com/dms/image/D4D0BAQGdJGOpAnqYNA/company-logo_200_200/0/1696938696861?e=1726704000&v=beta&t=OXsNxkr1TlKHwrHV5KjuylgWRmfc0CZgMpp3LCXTjjs"><img
      class="twitter__icon" src="https://media.licdn.com/dms/image/D4D0BAQGdJGOpAnqYNA/company-logo_200_200/0/1696938696861?e=1726704000&v=beta&t=OXsNxkr1TlKHwrHV5KjuylgWRmfc0CZgMpp3LCXTjjs" /></a>
</body>
<script>
const cards = document.querySelector(".cards");
const images = document.querySelectorAll(".card__img");
const backgrounds = document.querySelectorAll(".card__bg");
const range = 40;

const calcValue = (a, b) => (a / b * range - range / 2).toFixed(1);

let timeout;
document.addEventListener('mousemove', ({ x, y }) => {
  if (timeout) {
    window.cancelAnimationFrame(timeout);
  }

  timeout = window.requestAnimationFrame(() => {
    const yValue = calcValue(y, window.innerHeight);
    const xValue = calcValue(x, window.innerWidth);

    cards.style.transform = `rotateX(${yValue}deg) rotateY(${xValue}deg)`;

    [].forEach.call(images, (image) => {
      image.style.transform = `translateX(${-xValue}px) translateY(${yValue}px)`;
    });

    [].forEach.call(backgrounds, (background) => {
      background.style.backgroundPosition = `${xValue * .45}px ${-yValue * .45}px`;
    })
  })
}, false);

function toggleHelpNote() {
  const helpNote = document.getElementById('help-note');
  if (helpNote.style.display === 'none' || helpNote.style.display === '') {
    helpNote.style.display = 'block';
  } else {
    helpNote.style.display = 'none';
  }
}

function populateExample() {
  const examplePrompt = `title: My Page;
name: GAJNESH SHARMA; 
introduction: I am proficient in HTML, CSS, JavaScript, and Python, among other technologies. My commitment to continuous learning and staying up-to-date with industry trends drives me to constantly improve my skill set and deliver high-quality work.;
skill: Python, Flask, HTML, CSS , JavaScript, C, C++ , Arduino, 
Wordpress ;
contact: Email - contact@example.com, Phone - 123-456-7890; education: Degree - B.Sc. in Computer Science, Certification - AWS Certified Solutions Architect ;
project: Amazon Clone - using HTML AND CSS ,Flipkart Clone - using HTML AND CSS;`;
  document.querySelector('textarea[name="prompt"]').value = examplePrompt;
}
</script>

</html>   
 """

if __name__ == '__main__':
    app.run(debug=True)
