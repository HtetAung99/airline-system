from flask import (
    abort, Blueprint, g, redirect, request, url_for
)
from sqlalchemy import select
from flaskr.models import db, City
from flaskr.auth.routes import admin_required

city_bp = Blueprint('cities', __name__, url_prefix='/cities')


# @city_bp.get('/')
# @admin_required
def get_all_cities():
    error = None
    cities = db.session.execute(select(City)).scalars().all()
    return cities
    # return render_template('/index.html', cities=cities)


def get_city_by_id(id):
    return db.session.execute(
        select(City).filter(City.id == id)).scalar()


@city_bp.post('/new')
# @admin_required
def create_city():
    data = request.form.to_dict()
    error = None
    try:
        new_city = City(**data)
        db.session.add(new_city)
        db.session.commit()
    except Exception as e:
        print("errors", e)
        abort(500)
    return "Success", 201


@city_bp.route('/<int:id>/delete', methods=['POST'])
@admin_required
def delete_city(id):
    error = None

    try:
        db.session.delete(db.get_or_404(City, id))
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("cities.get_all_cities"))
