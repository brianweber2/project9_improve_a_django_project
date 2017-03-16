from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient
from .forms import MenuForm


# Test Data
menu_data1 = {
    'season': 'Summer',
    'expiration_date': '2018-03-20'
}

menu_data2 = {
    'season': 'Winter',
    'expiration_date': '2020-06-20'
}

################################
########## View Tests ##########
################################
class MenuViewsTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user',
            email='testemail@gmail.com',
            password='testing'
        )
        ingredient1 = Ingredient(name='chocolate')
        ingredient1.save()
        ingredient2 = Ingredient(name='strawberry')
        ingredient2.save()
        ingredient3 = Ingredient(name='banana')
        ingredient3.save()
        self.item1 = Item(
            name='Item 1',
            description='testing items',
            chef=self.test_user
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.menu1 = Menu.objects.create(**menu_data1)
        self.menu1.items.add(self.item1)
        self.menu2 = Menu.objects.create(**menu_data2)
        self.menu2.items.add(self.item1)

    def tearDown(self):
        self.test_user.delete()

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_create_new_menu_view_GET(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_create_new_menu_view_POST(self):
        resp = self.client.post(reverse('menu_new'))
        self.assertEqual(resp.status_code, 302)

    def test_edit_menu_view_GET(self):
        resp = self.client.get(reverse('menu_edit',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_POST(self):
        resp = self.client.post(reverse('menu_edit',
            kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)

class ItemViewsTest(TestCase):
    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail',
            kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/detail_item.html')

    def test_item_detail_view_404(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed('menu/detail_item.html')


class IngredientViewsTest(TestCase):
    pass


#################################
########## Form Tests ##########
#################################
class MenuFormsTest(TestCase):
    def test_menu_create_form_good_data(self):
        form_data = {'season': 'Winter',
            'items': self.item1,
            'expiration_date': '03/20/2020'
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Winter')
        self.assertEqual(menu.expiration_date, '03/20/2020')
        self.assertEqual(menu.items, self.item1)

    def test_menu_create_form_blank_data(self):
        form = MenuForm(data={})
        self.assertFalse(form.is_valid())


#################################
########## Model Tests ##########
#################################
class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(**menu_data1)
        self.assertEqual(menu.season, 'Summer')


