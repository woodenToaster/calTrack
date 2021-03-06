from caltrack import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return "<User {}>".format(self.username)


recipes_ingredients = db.Table(
    'recipes_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id')),
    db.Column('ingr_id', db.Integer, db.ForeignKey('ingredient.ingr_id'))
)


tracker_recipes = db.Table(
    'tracker_recipes',
    db.Column('dt_id', db.Integer, db.ForeignKey('tracker.dt_id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id'))
)


tracker_ingredients = db.Table(
    'tracker_ingredients',
    db.Column('dt_id', db.Integer, db.ForeignKey('tracker.dt_id')),
    db.Column('ingr_id', db.Integer, db.ForeignKey('ingredient.ingr_id'))
)


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    ingredients = db.relationship(
        'Ingredient',
        secondary=recipes_ingredients,
        backref=db.backref('recipes', lazy='dynamic'))

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return "<Recipe {}>".format(self.name)


class Ingredient(db.Model):
    ingr_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.Float(60), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<Ingredient {}>".format(self.name)


class Tracker(db.Model):
    dt_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipes = db.relationship(
        'Recipe',
        secondary=tracker_recipes,
        backref=db.backref('trackers', lazy='dynamic')
    )
    ingredients = db.relationship(
        'Ingredient',
        secondary=tracker_ingredients,
        backref=db.backref('daily_trackers', lazy='dynamic'),
    )

    def __repr__(self):
        return "<Tracker {}>".format(self.date)

    def get_totals(self):
        return {
            'calories': self.get_total_calories(),
            'protein': self.get_total_protein(),
            'carbs': self.get_total_carbs(),
            'fat': self.get_total_fat(),
            'fiber': self.get_total_fiber()
        }

    def get_total_calories(self):
        return sum(x.calories for x in self.ingredients)

    def get_total_protein(self):
        return sum(x.protein for x in self.ingredients)

    def get_total_carbs(self):
        return sum(x.carbs for x in self.ingredients)

    def get_total_fat(self):
        return sum(x.fat for x in self.ingredients)

    def get_total_fiber(self):
        return sum(x.fiber for x in self.ingredients)
