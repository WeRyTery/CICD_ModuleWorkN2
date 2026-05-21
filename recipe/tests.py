from django.test import TestCase, Client
from .models import Category, Recipe
from django.urls import reverse

# Create your tests here.

def make_recipe(category, title="Cake", n = 0):
    return Recipe.objects.create(
        title = f"{title} {n}",
        description = "Tasty",
        instructions = "Eat",
        ingredients = "Caking ingredient",
        category = category,
    )

def make_category(name='Desserts'):
    return Category.objects.create(name=name)

class Main_view_tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('main')
        self.category = make_category()


    def test_main_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_main_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main.html')

    def test_main_context_has_recipes(self):
        response = self.client.get(self.url)
        self.assertIn('recipes', response.context)

    def test_main_return_max_10_recipes(self):
        for i in range(15):
            make_recipe(self.category, n = i)

        response = self.client.get(self.url)
        self.assertLessEqual(len(response.context['recipes']), 10)




class Category_details_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = make_category('Soups')
        self.other_category = make_category('Salads')
        for i in range(3):
            make_recipe(self.category, title='Soup', n=i)
        make_recipe(self.other_category, title='Caesar')

        self.url = reverse('category_detail', kwargs={'name': self.category.name})

    
    def test_category_detail_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_detail_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'category_detail.html')
    
    def test_category_detail_404_status(self):
        response = self.client.get(
            reverse('category_detail', kwargs={'name': "Dkad"})
        )
        self.assertEqual(response.status_code, 404)