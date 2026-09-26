import asyncio
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.db.base import Base
from app.db.database import engine, session
from app.models.policy import PolicyChunk
from app.services.embedding import get_embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import app.models

POLICY_TEXT = """
AI SHOE STORE - COMPANY POLICIES

GENERAL STORE INFORMATION

Our store sells shoes for men, women, and children. Customers can browse available shoes,
check prices, search for products, and place orders after creating an account and logging in.
All orders are associated with the authenticated customer's account.

ACCOUNT POLICY

Customers must create an account using a username and password before placing an order.
Customers are responsible for keeping their account credentials private.
Customers should never share their password or JWT access token with another person.
The store will use account information only for providing store services and managing orders.

PRODUCT POLICY

Every product displayed in the store has a product ID, product name, and price.
Product availability depends on the products currently stored in the inventory.
Prices displayed by the store are the current listed prices.
Customers should check the available product information before placing an order.

ORDER POLICY

Customers must be logged in before placing an order.
An order belongs to the user whose authenticated JWT was used when creating the order.
Customers can place an order directly through the store API or by asking the AI assistant
to place an order for them.
The AI assistant can place an order only when it can identify the requested product.
If the requested product cannot be identified, the assistant should ask the customer
for more information instead of creating an incorrect order.

ORDER CANCELLATION POLICY

Customers should contact store support if they want to cancel an order.
Cancellation depends on the current stage of the order.
An order that has already been shipped may not be eligible for cancellation.

RETURN POLICY

Customers may request a return according to the store's return conditions.
Returned shoes should be unused, unworn, and in suitable condition.
The customer should keep the original packaging and product information when requesting
a return whenever possible.
The store may reject a return if the product has been significantly used or damaged
after delivery.

EXCHANGE POLICY

Customers may request an exchange when the received shoe has a valid size or product issue.
Exchange requests depend on product availability.
If the requested replacement size is unavailable, the customer may need to choose another
available size or use the applicable return process.

REFUND POLICY

Refunds are processed after the returned product is received and checked.
The refund amount depends on the applicable store return conditions.
Processing time can vary depending on the payment method and financial institution.
Customers should contact support if a refund has not appeared after the expected processing
period.

DAMAGED PRODUCT POLICY

Customers should contact support as soon as possible if a shoe arrives damaged.
Customers should provide the order information and, when requested, photographs showing
the damage.
The support team will review the issue and determine the appropriate resolution.

WRONG PRODUCT POLICY

If a customer receives a different product from the one ordered, the customer should
contact support with the order ID and product details.
The store may arrange a return and replacement after verifying the order.

SHIPPING POLICY

Orders are prepared after successful order creation.
Shipping time depends on the customer's delivery location and the delivery service.
Customers should provide a correct delivery address.
The store is not responsible for delays caused by an incorrect address supplied by
the customer.

DELIVERY POLICY

Customers should check the delivery information associated with their order.
If a package is delayed, customers should contact support with their order ID.
Delivery estimates are not guaranteed and can change because of logistics or external
delivery conditions.

PAYMENT POLICY

Customers must use one of the payment methods supported by the store.
The final amount charged for an order is based on the product price and any applicable
charges shown during checkout.
Customers should not share payment credentials with anyone claiming to represent
the store.

CASH ON DELIVERY POLICY

If cash on delivery is supported, the customer must pay the applicable amount when the
order is delivered.
Availability of cash on delivery can depend on the delivery location and current
store configuration.

PRIVACY POLICY

Customer information is used to provide account, order, and support services.
The store should not expose one customer's order information to another customer.
Authenticated users can access their own orders through protected endpoints.
The backend identifies the customer using the user ID contained in the verified JWT.

SECURITY POLICY

Protected API endpoints require a valid JWT access token.
The backend verifies the JWT before allowing authenticated operations.
Customers should never expose their JWT token publicly.
Passwords are stored as hashes rather than plain text.

AI ASSISTANT POLICY

The AI assistant can answer questions about store policies and available products.
The assistant can help customers search for shoes by product information.
The assistant can show information about the authenticated customer's own orders.
The assistant can place an order when the customer clearly identifies an available product.

The AI assistant must not invent products, prices, orders, refund rules, or store policies.
If information is not available in the supplied store knowledge, the assistant should
say that it does not have enough information instead of inventing an answer.

AI ORDERING POLICY

When a customer asks the AI assistant to order a product, the backend must identify
the product before creating an order.
The authenticated user's ID comes from the verified JWT.
The AI model does not directly access PostgreSQL.
The Python backend performs the actual database operation for creating the order.

CUSTOMER SUPPORT POLICY

Customers can contact support for account problems, order problems, delivery issues,
returns, exchanges, refunds, damaged products, and incorrect products.
Customers should provide their order ID when asking about a specific order.

DATA ACCURACY POLICY

Product availability and prices come from the store database.
Order information comes from the authenticated customer's orders.
Policy answers should be based on the retrieved company policy information.
The AI assistant should clearly state when information is unavailable.

GENERAL CONDITIONS

The store may update its policies when business conditions change.
Customers are expected to follow the current policies displayed or provided by the store.
Specific return, exchange, delivery, and payment decisions may depend on the individual
order and the information available to the store.
"""

async def prerun():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await conn.run_sync(Base.metadata.create_all)

        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = splitter.split_text(POLICY_TEXT)
        vectors = await get_embeddings(chunks)

        async with session.begin() as ssn:
            for content, vector in zip(chunks, vectors):
                ssn.add(PolicyChunk(content=content, embedding=vector))

        print(f"done: {len(chunks)} policy chunks inserted")
    except SQLAlchemyError as e:
        print("database error:", e)


# asyncio.run(prerun())
