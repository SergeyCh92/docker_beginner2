# from dataclasses import field
# from pyexpat import model
from itertools import product
from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class ProductSerializer(serializers.ModelSerializer):
    # positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

    def create(self, validated_data):
        print('lala')
        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        print('lala')
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for num in range(len(positions)):
            prod = positions[num]['product']
            quantity = positions[num]['quantity']
            price = positions[num]['price']
            data = StockProduct(stock=stock, product=prod, quantity=quantity, price=price)
            data.save()

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        obj_list = StockProduct.objects.filter(stock=instance)
        for pos in positions:
            for obj in obj_list:
                if obj.product == pos['product']:
                    obj.quantity = pos['quantity']
                    obj.price = pos['price']
                    obj.save()
                if pos['product'] not in [el.product for el in obj_list]:
                    prod = pos['product']
                    quantity = pos['quantity']
                    price = pos['price']
                    data = StockProduct(stock=stock, product=prod, quantity=quantity, price=price)
                    data.save()

        return stock
