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
        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for pos in positions:
            prod = pos['product']
            quantity = pos['quantity']
            price = pos['price']
            data = StockProduct(stock=stock, product=prod, quantity=quantity, price=price)
            data.save()

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for pos in positions:
            obj, create = StockProduct.objects.update_or_create(stock=instance, product=pos['product'], defaults=pos)

        return stock
