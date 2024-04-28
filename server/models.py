from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        
        # check if name already exists
        if Author.query.filter_by(name = name).first():
            raise ValueError("Name already exists")
        return name

    @validates('phone_number')
    def validates_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Input phone number")
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone_number)!=10 :
            raise ValueError("Phone number must be 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validates_title(self,key,title):
        if not title:
            raise ValueError("Title input required")
        
        clickbait_phrases = ["Won't Believe","Secret","Top","Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
                raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title

    @validates('content')
    def validates_content(self, key, content):
        if len(content)<250 :
            raise ValueError("Content must be 250 characters")
        return content

    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary)>250 :
            raise ValueError("Summary must not be more than 250 characters")
        return summary
    
    @validates('category')
    def validates_category(self,key,category):
        if category !='Fiction' and category != 'Non-Fiction':
            raise ValueError("Post category should be either Fiction or Non-Fiction.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
