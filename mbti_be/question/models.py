from django.db import models

class QuestionType(models.Model):
    """
    Model representing a type of question.
    """
    question_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)  # Enforces unique question types

    def __str__(self):
        return self.type
    
class Question(models.Model):
    """
    Model representing a question.
    """
    question_id = models.AutoField(primary_key=True)  # Set primary key to auto-increment
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_code = models.CharField(max_length=2)
    level = models.IntegerField()
    
class Answer(models.Model):
    """
    Model representing an answer to a question.
    """
    answer_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField()
    type_result = models.CharField(max_length=1)
    

class Personality(models.Model):
    """
    Model representing a personality type.
    """
    # personality_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=4, primary_key=True)
    description = models.TextField()
    majors = models.TextField()
    
class Major(models.Model):
    """
    Model representing a major.
    """
    major_id = models.AutoField(primary_key=True)
    major_name = models.CharField()
    type = models.ForeignKey(Personality, on_delete=models.CASCADE)
    
