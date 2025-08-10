from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code_storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model lưu trữ bài code
class CodeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)

# ✅ Phải có application context khi tạo database
with app.app_context():
    db.create_all()

# HTML template danh sách bài code
INDEX_HTML = '''
<!doctype html>
<title>Code Storage</title>
<h1>Danh sách bài code</h1>

<form method="get" action="{{ url_for('index') }}">
    <input type="text" name="q" placeholder="Tìm theo tên đề bài" value="{{ request.args.get('q', '') }}">
    <input type="submit" value="Tìm kiếm">
</form>

<a href="{{ url_for('add') }}">Thêm bài code mới</a>

<ul>
  {% for entry in entries %}
    <li>
      <strong>{{ entry.title }}</strong><br>
      <pre>{{ entry.problem }}</pre>
      <pre>{{ entry.code }}</pre>
    </li>
  {% else %}
    <li>Chưa có bài code nào.</li>
  {% endfor %}
</ul>
'''

# HTML form thêm bài code
ADD_HTML = '''
<!doctype html>
<title>Thêm bài code mới</title>
<h1>Thêm bài code mới</h1>
<form method="post" action="{{ url_for('add') }}">
    <label>Tiêu đề đề bài:<br><input type="text" name="title" required></label><br><br>
    <label>Đề bài:<br><textarea name="problem" rows="6" cols="60" required></textarea></label><br><br>
    <label>Code Python:<br><textarea name="code" rows="10" cols="60" required></textarea></label><br><br>
    <input type="submit" value="Lưu bài code">
</form>
<a href="{{ url_for('index') }}">Quay lại danh sách</a>
'''

@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    if q:
        entries = CodeEntry.query.filter(CodeEntry.title.contains(q)).all()
    else:
        entries = CodeEntry.query.all()
    return render_template_string(INDEX_HTML, entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        problem = request.form['problem'].strip()
        code = request.form['code'].strip()
        if title and problem and code:
            new_entry = CodeEntry(title=title, problem=problem, code=code)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Vui lòng điền đầy đủ thông tin", 400
    return render_template_string(ADD_HTML)

# ✅ Cấu hình chạy phù hợp với Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
