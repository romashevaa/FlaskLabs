from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///routes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)


class Route(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

routes_bp = Blueprint('routes', __name__) 
api_routes = Api(routes_bp)


class RouteResource(Resource):
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        return {'id': route.id, 'name': route.name, 'length': route.length, 'difficulty': route.difficulty}

    def put(self, route_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name cannot be blank')
        parser.add_argument('length', type=float,
                            required=True, help='Length cannot be blank')
        parser.add_argument('difficulty', type=str,
                            required=True, help='Difficulty cannot be blank')

        args = parser.parse_args()
        route = Route.query.get_or_404(route_id)
        route.name = args['name']
        route.length = args['length']
        route.difficulty = args['difficulty']
        db.session.commit()
        return {'message': 'Route updated successfully'}

    def delete(self, route_id):
        route = Route.query.get_or_404(route_id)
        db.session.delete(route)
        db.session.commit()
        return {'message': 'Route deleted successfully'}


class RoutesResource(Resource):
    def get(self):
        routes = Route.query.all()
        routes_data = [{'id': route.id, 'name': route.name, 'length': route.length,
                        'difficulty': route.difficulty} for route in routes]
        return jsonify(routes_data)

    def post(self):
        try:
            if request.content_type == 'application/json':
                data = request.get_json()
            else:
                data = request.form
            if 'name' not in data or 'length' not in data or 'difficulty' not in data:
                return {'message': 'Missing required data'}, 400
            new_route = Route(
                name=data['name'], length=data['length'], difficulty=data['difficulty'])
            db.session.add(new_route)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return {'message': str(e)}, 500


api_routes.add_resource(RouteResource, '/route/<int:route_id>')
api_routes.add_resource(RoutesResource, '/routes', endpoint='routes')


@routes_bp.route('/')
def get_routes():
    routes = Route.query.all()
    return render_template('index.html', routes=routes)


@routes_bp.route('/delete/<int:route_id>', methods=['GET'])
def delete_route(route_id):
    route = Route.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for('routes.get_routes'))


@routes_bp.route('/update/<int:route_id>', methods=['GET', 'POST'])
def update_route(route_id):
    route = Route.query.get_or_404(route_id)

    if request.method == 'POST':
        route.name = request.form['name']
        route.length = request.form['length']
        route.difficulty = request.form['difficulty']
        db.session.commit()
        return redirect(url_for('routes.get_routes')) 

    return render_template('edit_route.html', route=route)


app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
