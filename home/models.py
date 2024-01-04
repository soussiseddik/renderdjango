from django.db import models

class Product(models.Model):
    patternsname = {}
    name = models.CharField(max_length=30)
    price = models.CharField(max_length=7, default='00.00')
    image = models.ImageField(upload_to= 'images/') 
    info_image1 = models.ImageField(upload_to= 'images/', default=0)
    info_image2 = models.ImageField(upload_to= 'images/', default=0) 
    allCategorys = (['phones', 'phones'], 
               ['computers','computers'], 
               ['games', 'games'], 
               ['headphones', 'headphones'], 
               ['soundcards', 'soundcards'], 
               ['microphones', 'microphones'])
    category = models.CharField(choices=allCategorys, max_length=20, default='phones')     
    caract = models.CharField(max_length=500, default='no caracters')
    def __str__(self):
        return self.name
    def get_path(self):
        return self.name.replace(' ', '-')
