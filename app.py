from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiptvummcyikgi:1e2b0f26d79acb617b0a2478ba89fad6a3f440de318b12ba43a477f34f14381d@ec2-99-80-200-225.eu-west-1.compute.amazonaws.com:5432/dabk0kq2g03fqa'
db = SQLAlchemy(app)




class Brand(db.Model):
	__tablename__ = 'brand'
	name = db.Column(db.String(50), primary_key=True, nullable=False)
	brand = db.relationship('Car')


class Car(db.Model):
	__tablename__ = 'car'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(50), unique=True, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	brand = db.Column(db.String(50),db.ForeignKey('brand.name'))


db.create_all()



@app.route('/<table>/', methods=['post'])
def add(table):
	if table == "Car":
		gid = request.form.get('gid')
		name = request.form.get('name')
		price = request.form.get('price')
		brand = request.form.get('brand')
		new = Car(id = gid, name = name, price = price, brand = brand)
	elif table == "Brand":
		name = request.form.get('name')
		new = Brand(name = name)
	try:
		db.session.add(new)
		db.session.commit()
	except Exception:
		if table == "Car":
			return redirect(url_for('read_table_car'))
		elif table == "Brand":
			return redirect(url_for('read_table_brand'))
	if table == "Car":
		return redirect(url_for('read_table_car'))
	elif table == "Brand":
		return redirect(url_for('read_table_brand'))

@app.route('/<table>/Update', methods=['post'])
def update(table):
	if table == "Car":
		name = request.form.get('Name')
		price = request.form.get('Price')
		brand = request.form.get('Brand')
		gid = request.form.get('Id')
		x = db.session.query(Car).get(gid)
		x.name = name
		x.price = price
		x.brand = brand
	elif table == "Brand":
		name = request.form.get('Name')
		x = db.session.query(Brand).get(name)
		x.name = name
	try:
		db.session.commit()
	except Exception:
		if table == "Car":
			return redirect(url_for('read_table_car'))
		elif table == "Brand":
			return redirect(url_for('read_table_brand'))
	if table == "Car":
		return redirect(url_for('read_table_car'))
	elif table == "Brand":
		return redirect(url_for('read_table_brand'))

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)

@app.route('/Car')
def read_table_car():
	data = Car.query.all()
	return render_template('index.html', data=data,table="Car")

@app.route('/Brand')
def read_table_brand():
	data = Brand.query.all()
	return render_template('index_brand.html', data=data,table="Brand")

@app.route('/<table>/delete/<name>')
def delete(table,name):
	if table == "Car":
		data = Car.query.all()
	elif table == "Brand":
		data = Brand.query.all()
	else:
		return redirect(url_for('hello'))
	for d in data:
		if d.name == name:
			db.session.delete(d)
			db.session.commit()
	if table == "Car":
		return redirect(url_for('read_table_car'))
	elif table == "Brand":
		return redirect(url_for('read_table_brand'))
	else:
		return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run()
