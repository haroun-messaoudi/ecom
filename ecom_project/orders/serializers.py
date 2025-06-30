from rest_framework import serializers
from .models import Order, OrderItem, Wilaya, Commune
from products.serializers import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity','price']
        read_only_fields = ['id','price']
    def validate(self, attrs):
        if attrs['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if attrs['quantity'] > attrs['product'].stock:
            raise serializers.ValidationError("Insufficient stock for this variant.")
        
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    # We need to expose delivery_type, wilaya, commune
    delivery_type = serializers.ChoiceField(
        choices=(("A Domicile", "A Domicile"), ("Bureau", "Bureau"))
    )
    # Assuming wilaya and commune are ForeignKeys in Order → we use PrimaryKeyRelatedField
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'costumer_name',
            'costumer_phone',
            'order_date',
            'delivery_type',
            'delivery_fees',
            'wilaya',
            'commune',
            'order_status',
            'total_amount',
            'items',
        ]
        read_only_fields = ['id', 'order_date', 'total_amount', 'order_status']

    def validate(self, data):
        """
        Enforce that if delivery_type == "A Domicile",
        then wilaya and commune cannot be null/omitted.
        """
        delivery_type = data.get('delivery_type')
        wilaya = data.get('wilaya')
        commune = data.get('commune')
        if wilaya is None:
            raise serializers.ValidationError({
                'wilaya': "This field is required"
            })

        # if delivery_type == "A Domicile":
        #     if commune is None:

        #         raise serializers.ValidationError({
        #            "commune":"This field is required when delivery_type is 'A Domicile'."

        #         })

        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Prepare items for bulk_add_items
        bulk_items = []
        for item_data in items_data:
            # item_data['product'] is a Product instance due to ModelSerializer
            bulk_items.append({
                "product": item_data["product"],
                "quantity": item_data["quantity"],
            })

        # Use bulk_add_items for efficient creation
        order.bulk_add_items(bulk_items)

        # total_amount is updated
        return order