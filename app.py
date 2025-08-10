from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model dữ liệu
class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Text, nullable=False)

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Danh sách bài code</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="container mt-4">
<h1>Danh sách bài code</h1>
<form class="mb-3" method="get" action="{{ url_for('index') }}">
  <input type="text" name="search" placeholder="Tìm theo đề bài..." value="{{ search or '' }}" class="form-control" />
</form>
<a href="{{ url_for('add') }}" class="btn btn-primary mb-3">Thêm bài mới</a>
<table class="table table-striped">
<thead>
<tr><th>ID</th><th>Đề bài</th><th>Xem</th></tr>
</thead>
<tbody>
{% for c in codes %}
<tr>
  <td>{{ c.id }}</td>
  <td>{{ c.title }}</td>
  <td><a href="{{ url_for('view', id=c.id) }}" class="btn btn-sm btn-info">Xem code</a></td>
</tr>
{% else %}
<tr><td colspan="3">Không tìm thấy bài nào.</td></tr>
{% endfor %}
</tbody>
</table>
</body>
</html>
'''

ADD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Thêm bài code</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="container mt-4">
<h1>Thêm bài code mới</h1>
<form method="post" action="{{ url_for('add') }}">
  <div class="mb-3">
    <label for="title" class="form-label">Tên đề bài</label>
    <input type="text" class="form-control" id="title" name="title" required />
  </div>
  <div class="mb-3">
    <label for="code" class="form-label">Đoạn code Python</label>
    <textarea class="form-control" id="code" name="code" rows="10" required></textarea>
  </div>
  <button type="submit" class="btn btn-success">Lưu bài</button>
  <a href="{{ url_for('index') }}" class="btn btn-secondary">Hủy</a>
</form>
</body>
</html>
'''

VIEW_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Xem bài code</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="container mt-4">
<h1>{{ code.title }}</h1>
<pre style="background:#f8f9fa; padding:15px; border-radius:5px; white-space: pre-wrap;">{{ code.code }}</pre>
<a href="{{ url_for('index') }}" class="btn btn-primary mt-3">Quay lại danh sách</a>
</body>
</html>
'''

@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        codes = Code.query.filter(Code.title.contains(search)).all()
    else:
        codes = Code.query.all()
    return render_template_string(INDEX_HTML, codes=codes, search=search)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        code = request.form['code'].strip()
        if title and code:
            new_code = Code(title=title, code=code)
            db.session.add(new_code)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template_string(ADD_HTML)

@app.route('/view/<int:id>')
def view(id):
    code = Code.query.get_or_404(id)
    return render_template_string(VIEW_HTML, code=code)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
