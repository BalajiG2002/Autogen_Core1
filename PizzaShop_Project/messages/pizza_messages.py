from dataclasses import dataclass
from typing import List

@dataclass
class CustomerQuestion:
    """Message for customer questions"""
    question: str
    customer_name: str

@dataclass
class PizzaOrder:
    """Message for pizza orders"""
    pizza_type: str
    customer_name: str
    special_requests: str

@dataclass
class DeliveryRequest:
    """Message for delivery requests"""
    order_id: str
    address: str
    customer_phone: str
    estimated_time: int

@dataclass
class PaymentRequest:
    """Message for payment processing"""
    amount: float
    payment_method: str
    customer_name: str
