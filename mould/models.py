from django.db import models
from django.contrib.auth.models import User 

# -------------------------------------------------------------------------------
class Mould(models.Model): 

    mould_id = models.IntegerField(primary_key=True)
    mould_name = models.CharField(max_length=200)
    cavity_number = models.IntegerField()
    registered_date = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    threshold_value = models.IntegerField()
    present_count = models.IntegerField()

 
    def __str__(self): 
        return str(self.mould_id)

    def alert(self): 
        return self.threshold_value - self.present_count <= 500  


# -------------------------------------------------------------------------------- 

class MouldStatus(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_status', on_delete=models.PROTECT)
    status_update = models.DateTimeField(auto_now_add=True)
    count_increment = models.IntegerField() # daily increment. 

    def __str__(self): 
        return str(self.mould_id) 

# -----------------------------------------------------------------------------------
class MouldComment(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_chat', on_delete=models.PROTECT)
    comment_text = models.TextField()
    commented_by = models.ForeignKey(User,related_name='chat_user', on_delete=models.PROTECT)
    commented_date_time = models.DateTimeField(auto_now_add=True)




# --------------------------------------------------------------- 
class MouldData(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_data', on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    department_name = models.CharField(max_length=100) 
    product_line = models.CharField(max_length=100)  


# ---------------------------------------------------------------- 
class ProductLine(models.Model): 

    product_line_number = models.IntegerField() # numbef of product line. 
    proudct_line_name = models.CharField(max_length=100)

# ------------------------------------------------------------------ 
class Department(models.Model): 

    department_name = models.CharField(max_length=20) # name of department. 
    department_id = models.CharField(max_length=20) # id of department. 

