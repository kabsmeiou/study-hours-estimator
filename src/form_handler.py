from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange


class StudentForm(FlaskForm):
  name=StringField("Name", validators=[InputRequired(), Length(min=1, max=16, message='Name must be between 1 and 16 characters')])

  # integer fields
  attendance=IntegerField("Attendance Percentage", validators=[InputRequired(), NumberRange(min=0, max=100, message='Minimum input: 0, Maximum input: 100')])
  sleep_hours=IntegerField("Hours of Sleep", validators=[InputRequired(), NumberRange(min=0, message='Minimum input: 0')])
  previous_scores=IntegerField("Previous Exam Score", validators=[InputRequired(), NumberRange(min=0, max=100, message='Minimum input: 0, Maximum input: 100')])
  tutoring_sessions=IntegerField("Number of Tutoring Sessions", validators=[InputRequired(), NumberRange(min=0, message='Minimum input: 0')])
  physical_activity=IntegerField("Number of Physical Activities", validators=[InputRequired(), NumberRange(min=0, message='Minimum input: 0')])
  exam_score=IntegerField("Target Exam Score", validators=[InputRequired(), NumberRange(min=0, max=100, message='Minimum input: 0, Maximum input: 100')])

  # categorical fields (select type)
  parental_involvement=SelectField(u"Level of Parental Involvement",
                                   validators=[InputRequired()], 
                                   choices=[('medium', 'Medium'), 
                                            ('high', 'High'), 
                                            ('low', 'Low')])
  access_to_resources=SelectField(u"Level of Access to Resources",
                                  validators=[InputRequired()], 
                                  choices=[('medium', 'Medium'), 
                                            ('high', 'High'), 
                                            ('low', 'Low')])
  internet_access=SelectField(u"Access to Internet",
                                  validators=[InputRequired()], 
                                 choices=[('yes', 'Yes'),
                                          ('no', 'No')])
  extracurricular_activities=SelectField(u"Has Extra Curricular Activities", 
                                         validators=[InputRequired()],
                                         choices=[('no', 'No'), 
                                            ('yes', 'Yes')])
  motivation_level=SelectField(u"Motivation Level", 
                               validators=[InputRequired()],
                               choices=[('medium', 'Medium'), 
                                          ('high', 'High'), 
                                          ('low', 'Low')])
  family_income=SelectField(u"Estimated Family Income",
                            validators=[InputRequired()],
                            choices=[('medium', 'Medium'), 
                                          ('high', 'High'), 
                                          ('low', 'Low')])
  teacher_quality=SelectField(u"Teaching Quality of Professor", 
                              validators=[InputRequired()],
                              choices=[('medium', 'Medium'), 
                                          ('high', 'High'), 
                                          ('low', 'Low')])
  school_type=SelectField(u"School type", 
                          validators=[InputRequired()],
                          choices=[('private', 'Private'), 
                                            ('public', 'Public')])
  peer_influence=SelectField(u"Peer influence", 
                             validators=[InputRequired()],
                             choices=[('neutral', 'Neutral'), 
                                          ('positive', 'Positive'), 
                                          ('negative', 'Negative')])
  learning_disabilities=SelectField(u"Has learning disabilities", 
                                    validators=[InputRequired()],
                                    choices=[('no', 'No'), 
                                            ('yes', 'Yes')])
  distance_from_home=SelectField(u"School's distance from home", 
                                 validators=[InputRequired()],
                                 choices=[('moderate', 'Moderate'), 
                                          ('near', 'Near'), 
                                          ('far', 'Far')])
  parental_education_level=SelectField(u"Parent's Education Level", 
                                       validators=[InputRequired()],
                                       choices=[('college', 'College'), 
                                          ('postgraduate', 'Postgraduate'), 
                                          ('high_school', 'High School')])
  gender=SelectField(u"Gender", 
                     validators=[InputRequired()],
                     choices=[('male', 'Male'),
                              ('female', 'Female')])
  
  submit = SubmitField('Predict Hours Needed', render_kw={'class': 'button-6'})