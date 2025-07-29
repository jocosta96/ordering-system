from typing import List, Optional


from src.application.repositories.order_repository import OrderRepository
from src.application.repositories.product_repository import ProductRepository
from src.application.repositories.ingredient_repository import IngredientRepository
from src.application.repositories.customer_repository import CustomerRepository
from src.application.dto.implementation.order_dto import (
    OrderCreateRequest,
    OrderUpdateRequest,
    PaymentRequest,
    PaymentRequestDTO,
    PaymentRequestResponse,
    OrderResponse,
    OrderListResponse,
    PaymentStatusResponse
)
from src.entities.order import Order, OrderItem
from src.entities.value_objects.order_status import OrderStatus


class OrderCreateUseCase:
    """Use case for creating a new order"""

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        ingredient_repository: IngredientRepository,
        customer_repository: CustomerRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.ingredient_repository = ingredient_repository
        self.customer_repository = customer_repository

    def execute(self, request: OrderCreateRequest) -> OrderResponse:
        """Execute the order creation use case"""
        # Validate customer exists
        customer = self.customer_repository.find_by_id(request.customer_internal_id)
        if not customer:
            raise ValueError(f"Customer with ID {request.customer_internal_id} not found")

        # Business rule: Customer must be able to place orders
        if not customer.can_place_order():
            raise ValueError("Customer does not meet requirements to place orders")

        # Build order items
        order_items = []
        for item_request in request.order_items:
            # Get product - only allow active products for new orders
            product = self.product_repository.find_by_id(item_request.product_internal_id, include_inactive=False)
            if not product:
                raise ValueError(f"Product with ID {item_request.product_internal_id} not found or is deactivated")
            
            # Additional validation: ensure product is active for new orders
            if not product.is_active:
                raise ValueError(f"Product with ID {item_request.product_internal_id} is deactivated and cannot be added to new orders")

            # Get additional ingredients - only allow active ingredients for new orders
            additional_ingredients = []
            for ing_id in item_request.additional_ingredient_internal_ids:
                ingredient = self.ingredient_repository.find_by_id(ing_id, include_inactive=False)
                if not ingredient:
                    raise ValueError(f"Ingredient with ID {ing_id} not found or is deactivated")
                if not ingredient.is_active:
                    raise ValueError(f"Ingredient with ID {ing_id} is deactivated and cannot be added to new orders")
                additional_ingredients.append(ingredient)

            # Get remove ingredients - only allow active ingredients for new orders
            remove_ingredients = []
            for ing_id in item_request.remove_ingredient_internal_ids:
                ingredient = self.ingredient_repository.find_by_id(ing_id, include_inactive=False)
                if not ingredient:
                    raise ValueError(f"Ingredient with ID {ing_id} not found or is deactivated")
                if not ingredient.is_active:
                    raise ValueError(f"Ingredient with ID {ing_id} is deactivated and cannot be removed from new orders")
                remove_ingredients.append(ingredient)

            # Create order item
            order_item = OrderItem(
                order_internal_id=0,  # Will be set by Order entity
                product=product,
                additional_ingredient=additional_ingredients,
                remove_ingredient=remove_ingredients
            )
            order_items.append(order_item)

        # Create order
        order = Order.create(
            customer_internal_id=request.customer_internal_id,
            order_items=order_items
        )

        # Set start date
        order.set_start_date()

        # Save order
        created_order = self.order_repository.create(order)

        return OrderResponse.from_entity(created_order)


class OrderReadUseCase:
    """Use case for reading order information"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_internal_id: int) -> Optional[OrderResponse]:
        """Execute the order read use case"""
        order = self.order_repository.get_by_id(order_internal_id)
        if not order:
            return None

        return OrderResponse.from_entity(order)


class OrderListUseCase:
    """Use case for listing orders"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, skip: int = 0, limit: int = 100) -> OrderListResponse:
        """Execute the order list use case"""
        orders = self.order_repository.list_all(skip=skip, limit=limit)
        return OrderListResponse.from_entity(orders, skip, limit)


class OrderUpdateUseCase:
    """Use case for updating an order"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_internal_id: int, request: OrderUpdateRequest) -> Optional[OrderResponse]:
        """Execute the order update use case"""
        order = self.order_repository.get_by_id(order_internal_id)
        if not order:
            return None

        # Update status if provided
        if request.status:
            order.status = OrderStatus.create(request.status)

        # Update order items if provided
        if request.order_items:
            # This would require more complex logic to rebuild order items
            # For now, we'll just update the status
            pass

        # Save updated order
        updated_order = self.order_repository.update(order)

        return OrderResponse.from_entity(updated_order)


class OrderStatusUpdateUseCase:
    """Use case for updating order status"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_internal_id: int, status: str) -> Optional[OrderResponse]:
        """Execute the order status update use case"""
        order = self.order_repository.update_status(order_internal_id, status)
        if not order:
            return None

        return OrderResponse.from_entity(order)


class OrderPaymentProcessUseCase:
    """Use case for processing order payment"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_internal_id: int, payment_request: PaymentRequest) -> Optional[OrderResponse]:
        """Execute the order payment processing use case"""
        payment_data = {
            'transaction_id': payment_request.transaction_id,
            'approval_status': payment_request.approval_status,
            'date': payment_request.date,
            'message': payment_request.message
        }

        order = self.order_repository.process_payment(order_internal_id, payment_data)
        if not order:
            return None

        return OrderResponse.from_entity(order)


class OrderPaymentStatusUseCase:
    """Use case for getting order payment status"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_internal_id: int) -> Optional[PaymentStatusResponse]:
        """Execute the order payment status use case"""
        order = self.order_repository.get_by_id(order_internal_id)
        if not order:
            return None

        return PaymentStatusResponse.from_entity(order)


class OrderPaymentRequestUseCase:
    """Use case for requesting payment for an order"""

    def __init__(self, order_repository: OrderRepository, qr_payment_repository):
        self.order_repository = order_repository
        self.qr_payment_repository = qr_payment_repository

    def execute(self, order_internal_id: int, payment_request: PaymentRequestDTO) -> PaymentRequestResponse:
        """Execute the order payment request use case"""
        # Get order to validate it exists and get its value
        order = self.order_repository.get_by_id(order_internal_id)
        if not order:
            raise ValueError(f"Order with ID {order_internal_id} not found")

        # Validate that order hasn't been paid yet
        if order.has_payment_verified:
            raise ValueError("Order has already been paid")

        # Use the order's actual value
        amount = order.value.value
        
        # Request payment through QR payment repository
        payment_response = self.qr_payment_repository.request_payment(
            order_id=payment_request.order_internal_id,
            amount=amount
        )
        
        # Convert JSONResponse to dict for serialization
        payment_response_dict = {
            "status_code": payment_response.status_code,
            "content": payment_response.body.decode() if hasattr(payment_response, 'body') else str(payment_response.content)
        }
        
        return PaymentRequestResponse(
            order_id=order_internal_id,
            amount=amount,
            payment_response=payment_response_dict
        )


class OrderCancelUseCase:
    """Use case for canceling an order"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        
    def execute(self, order_internal_id: int) -> bool:
        """Execute the order cancel use case"""
        return self.order_repository.cancel(order_internal_id)





class OrderByStatusUseCase:
    """Use case for getting orders by status"""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, status: str) -> List[OrderResponse]:
        """Execute the order by status use case"""
        orders = self.order_repository.get_by_status(status)
        return [OrderResponse.from_entity(order) for order in orders] 