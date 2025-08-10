from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code_storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model lưu trữ bài code
class CodeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# Template HTML trang danh sách (thêm nút xoá)
INDEX_HTML = '''
<!doctype html>
<title>Code Storage</title>
<h1>Danh sách bài code</h1>

<form method="get" action="{{ url_for('index') }}">
    <input type="text" name="q" placeholder="Tìm theo tên đề bài" value="{{ request.args.get('q', '') }}">
    <input type="submit" value="Tìm kiếm">
</form>

<a href="{{ url_for('add') }}">➕ Thêm bài code mới</a>

<ul>
  {% for entry in entries %}
    <li>
      <strong>{{ entry.title }}</strong><br>
      <pre>{{ entry.problem }}</pre>
      <pre>{{ entry.code }}</pre>
      <form method="post" action="{{ url_for('delete', entry_id=entry.id) }}" style="display:inline;">
        <button type="submit" onclick="return confirm('Bạn có chắc muốn xoá bài này?');">❌ Xoá</button>
      </form>
    </li>
  {% else %}
    <li>Chưa có bài code nào.</li>
  {% endfor %}
</ul>
'''

# Template trang thêm bài
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
<a href="{{ url_for('index') }}">⬅️ Quay lại danh sách</a>
'''

# Trang chủ
@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    if q:
        entries = CodeEntry.query.filter(CodeEntry.title.contains(q)).all()
    else:
        entries = CodeEntry.query.all()
    return render_template_string(INDEX_HTML, entries=entries)

# Thêm bài
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

# Xoá bài
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    entry = CodeEntry.query.get(entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('index'))

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
