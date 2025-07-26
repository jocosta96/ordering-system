from src.application.repositories.product_repository import ProductRepository
from src.application.dto.implementation.product_dto import ProductCreateRequest, ProductUpdateRequest, ProductListResponse, ProductResponse
from src.application.exceptions import ProductNotFoundException, ProductAlreadyExistsException, ProductValidationException, ProductBusinessRuleException
from src.entities.product import Product, ProductCategory
from src.entities.value_objects.sku import SKU
from src.app_logs import get_logger
import uuid

class ProductCreateUseCase:
    """
    Use case for creating a new product.

    This use case:
    - Contains business logic for product creation
    - Validates business rules
    - Orchestrates between domain and repository
    - Is independent of infrastructure (uses repository interface)
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductCreateUseCase")

    def execute(self, request: ProductCreateRequest) -> ProductResponse:
        """Execute the create product use case"""
        self.logger.info(
            "Creating new product", name=request.name, price=request.price, category=request.category, sku=request.sku)

        # Create product entity from DTO
        product = Product.create_registered(
            name=request.name,
            price=request.price,
            category=request.category,
            sku=request.sku,
            default_ingredient=request.default_ingredient,
        )

        # Business rule: Check if product with same SKU already exists
        if self.product_repository.exists_by_sku(product.sku):
            self.logger.warning(
                "Product creation failed - SKU already exists", sku=product.sku)
            raise ProductAlreadyExistsException(
                f"Product with SKU {product.sku} already exists")

        # Save product to repository
        self.product_repository.save(product)

        # Return product response
        return ProductResponse.from_entity(product)


class ProductReadUseCase:
    """
    Use case for reading a product.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductReadUseCase")

    def execute(self, product_id: uuid.UUID) -> ProductResponse:
        """Execute the read product use case"""
        self.logger.info("Reading product", product_id=product_id)

        # Find product by ID
        product = self.product_repository.find_by_id(product_id)

        if not product:
            self.logger.warning("Product not found", product_id=product_id)
            raise ProductNotFoundException(
                f"Product with ID {product_id} not found")

        # Return product response
        return ProductResponse.from_entity(product)

class ProductUpdateUseCase:
    """
    Use case for updating a product.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductUpdateUseCase")

    def execute(self, request: ProductUpdateRequest) -> ProductResponse:
        """Execute the update product use case"""
        self.logger.info("Updating product", product_id=request.id)

        # Convert string ID to UUID
        try:
            product_uuid = uuid.UUID(request.id)
        except ValueError:
            raise ProductValidationException("Invalid product ID format. Product ID must be a valid UUID.")

        # Find product by ID
        product = self.product_repository.find_by_id(product_uuid)

        if not product:
            self.logger.warning("Product not found", product_id=request.id)
            raise ProductNotFoundException(
                f"Product with ID {request.id} not found")

        # Update product entity from DTO
        product.update(
            name=request.name,
            price=request.price,
            category=request.category,
            sku=request.sku,
            default_ingredient=request.default_ingredient,
        )

        # Business rule: Check if product with same SKU already exists
        if self.product_repository.exists_by_sku(product.sku):
            self.logger.warning(
                "Product update failed - SKU already exists", sku=product.sku)
            raise ProductAlreadyExistsException(
                f"Product with SKU {product.sku} already exists")

        # Save product to repository
        self.product_repository.save(product)

        # Return product response
        return ProductResponse.from_entity(product)

class ProductDeleteUseCase:
    """
    Use case for deleting a product.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductDeleteUseCase")

    def execute(self, product_id: uuid.UUID) -> bool:
        """Execute the delete product use case"""
        self.logger.info("Deleting product", product_id=product_id)

        # Find product by ID
        product = self.product_repository.find_by_id(product_id)

        if not product:
            self.logger.warning("Product not found", product_id=product_id)
            raise ProductNotFoundException(
                f"Product with ID {product_id} not found")

        # Delete product from repository
        self.product_repository.delete(product_id)

        return True

class ProductListUseCase:
    """
    Use case for listing products.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductListUseCase")

    def execute(self) -> ProductListResponse:
        """Execute the list product use case"""
        self.logger.info("Listing products")

        # Find all products
        products = self.product_repository.find_all()

        # Return product list response
        return ProductListResponse.from_entity(products)

class ProductGetActiveUseCase:
    """
    Use case for getting active products.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductGetActiveUseCase")

    def execute(self) -> ProductListResponse:
        """Execute the get active products use case"""
        self.logger.info("Getting active products")

        # Find all active products
        products = self.product_repository.find_all_active()

        # Return product list response
        return ProductListResponse.from_entity(products)

class ProductReadBySkuUseCase:
    """
    Use case for reading a product by SKU.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductReadBySkuUseCase")

    def execute(self, sku: str) -> ProductResponse:
        """Execute the read product by SKU use case"""
        self.logger.info("Reading product by SKU", sku=sku)

        # Create SKU value object
        sku_obj = SKU(sku)

        # Find product by SKU
        product = self.product_repository.find_by_sku(sku_obj)

        if not product:
            self.logger.warning("Product not found", sku=sku)
            raise ProductNotFoundException(
                f"Product with SKU {sku} not found")

        # Return product response
        return ProductResponse.from_entity(product)

class ProductListByCategoryUseCase:
    """
    Use case for listing products by category.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductListByCategoryUseCase")

    def execute(self, category: str) -> ProductListResponse:
        """Execute the list products by category use case"""
        self.logger.info("Listing products by category", category=category)

        # Convert string to ProductCategory enum
        try:
            product_category = ProductCategory(category)
        except ValueError:
            raise ProductValidationException(f"Invalid category: {category}")

        # Find all products and filter by category
        all_products = self.product_repository.find_all()
        filtered_products = [p for p in all_products if p.category == product_category]

        # Return product list response
        return ProductListResponse.from_entity(filtered_products)

class ProductListByActiveStatusUseCase:
    """
    Use case for listing products by active status.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = get_logger("ProductListByActiveStatusUseCase")

    def execute(self, is_active: bool) -> ProductListResponse:
        """Execute the list products by active status use case"""
        self.logger.info("Listing products by active status", is_active=is_active)

        if is_active:
            # Find all active products
            products = self.product_repository.find_all_active()
        else:
            # Find all products and filter inactive ones
            all_products = self.product_repository.find_all()
            products = [p for p in all_products if not p.is_active]

        # Return product list response
        return ProductListResponse.from_entity(products)