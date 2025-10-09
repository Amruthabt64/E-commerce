from flask import Flask
from extensions import db, cors,jwt
from auth.routes import auth_bp
from products.routes import products_bp
from Cart.routes import cart_bp
from Orders.routes import orders_bp
# from products.routes import products_bp
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:password@localhost:3306"

# Configure database (adjust user, password, and db name as per your setup)
app.config['SQLALCHEMY_BINDS'] = {
    'auth': 'mysql+pymysql://root:password@localhost/auth_db',
    'products': 'mysql+pymysql://root:password@localhost/products_db',
    'cart': 'mysql+pymysql://root:password@localhost/cart_db',
    'orders': 'mysql+pymysql://root:password@localhost/orders_db'
}
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
# ✅ Initialize extensions
db.init_app(app)
cors.init_app(app)
jwt.init_app(app)

# ✅ Register blueprints

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
