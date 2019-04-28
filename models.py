from sqlalchemy import Column, ForeignKey, MetaData, Table
from sqlalchemy.dialects.mysql import BOOLEAN, FLOAT, SMALLINT, TEXT, TINYINT, VARCHAR

metadata = MetaData()

payment_method_table = Table(
    "Payment_Methods",
    metadata,
    Column('shortName', VARCHAR(4), primary_key=True, unique=True),
    Column('logo', VARCHAR(128)),
    Column('fullName', VARCHAR(64)),
)

certification_table = Table(
    "Certifications_List",
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('name', VARCHAR(64)),
    Column('logo', VARCHAR(128)),
    Column('url', VARCHAR(128)),
)

ff_criteria = Table(
    "FairFrog_Criteria",
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('name', VARCHAR(64)),
    Column('logo', VARCHAR(128)),
    Column('description', VARCHAR(1024), default=''),
)

brand_table = Table(
    "Brands",
    metadata,
    Column('Id', SMALLINT(unsigned=True), primary_key=True, unique=True),
    Column('brand_name', VARCHAR(128), index=True),
    Column('description', VARCHAR(4096), default=''),
    Column('logo', VARCHAR(256)),
    Column('certifications', VARCHAR(32), default=""),
    Column('meta_title', VARCHAR(512)),
    Column('meta_description', VARCHAR(2048), default=''),
    Column('deleted', BOOLEAN, default=False),
)

webshop_table = Table(
    'Webshops',
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('webshop_name', VARCHAR(64), index=True),
    Column('description', TEXT(convert_unicode=True), default=''),
    Column('url', VARCHAR(128)),
    Column('blog_url', VARCHAR(128), default=''),
    Column('webshop_logo', VARCHAR(128)),
    Column('postcode', VARCHAR(8)),
    Column('city', VARCHAR(64)),
    Column('country', VARCHAR(64)),
    Column('address', VARCHAR(256)),
    Column('ff_criteria', VARCHAR(32), default=''),
    Column('payment_methods', VARCHAR(32)),
    Column('delivery_info', VARCHAR(4096), default=''),
    Column('special_info', VARCHAR(4096), default=''),
    Column('meta_title', VARCHAR(256), default=""),
    Column('meta_description', VARCHAR(2048), default=""),
    Column('deleted', BOOLEAN, default=False),
)

product_table = Table(
    'Products',
    metadata,
    Column('Id', SMALLINT(unsigned=True), primary_key=True, unique=True),
    Column('title', VARCHAR(512), index=True),
    Column('meta_title', VARCHAR(256)),
    Column('meta_text', TEXT(convert_unicode=True), default=""),
    Column('url', VARCHAR(200)),
    Column('images', VARCHAR(4096), default=''),
    Column('webshop_name', VARCHAR(128), index=True),
    Column('brand', VARCHAR(128), index=True),
    Column('price', FLOAT(precision=6, scale=2, unsigned=True)),
    Column('discount_price', FLOAT(precision=6, scale=2, unsigned=True)),
    Column('sizes', VARCHAR(128), default=''),
    Column('description', TEXT(convert_unicode=True), default=''),
    Column('specifics', TEXT(convert_unicode=True), default=''),
    Column('categories', VARCHAR(256), default=''),
    Column('tags', VARCHAR(1024), index=True),
    Column('deleted', BOOLEAN, default=False),
)

popular_product_table = Table(
    'Popular_Products',
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('Product_Id', SMALLINT(unsigned=True), ForeignKey("Products.Id")),
)
