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

ff_criterion_table = Table(
    "FairFrog_Criteria",
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('name', VARCHAR(64)),
    Column('logo', VARCHAR(128)),
    Column('description', VARCHAR(1024), nullable=True),
)

brand_table = Table(
    "Brands",
    metadata,
    Column('Id', SMALLINT(unsigned=True), primary_key=True, unique=True),
    Column('brand_name', VARCHAR(128), index=True),
    Column('description', VARCHAR(4096), nullable=True),
    Column('logo', VARCHAR(256)),
    Column('certifications', VARCHAR(32), default=""),
    Column('meta_title', VARCHAR(256)),
    Column('meta_description', VARCHAR(1024), nullable=True),
    Column('deleted', BOOLEAN, default=False),
)

webshop_table = Table(
    'Webshops',
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('webshop_name', VARCHAR(64), index=True),
    Column('description', VARCHAR(2048), nullable=True),
    Column('url', VARCHAR(128)),
    Column('blog_url', VARCHAR(128), nullable=True),
    Column('webshop_logo', VARCHAR(128)),
    Column('postcode', VARCHAR(8)),
    Column('city', VARCHAR(64)),
    Column('country', VARCHAR(64)),
    Column('address', VARCHAR(256)),
    Column('ff_criteria', VARCHAR(32), nullable=True),
    Column('payment_methods', VARCHAR(32)),
    Column('delivery_info', VARCHAR(2048), nullable=True),
    Column('special_info', VARCHAR(2048), nullable=True),
    Column('meta_title', VARCHAR(256), default=""),
    Column('meta_description', VARCHAR(512), default=""),
    Column('deleted', BOOLEAN, default=False),
)

product_table = Table(
    'Products',
    metadata,
    Column('Id', SMALLINT(unsigned=True), primary_key=True, unique=True),
    Column('title', VARCHAR(256), index=True),
    Column('meta_title', VARCHAR(256)),
    Column('meta_text', VARCHAR(4096), default=""),
    Column('url', VARCHAR(200)),
    Column('images', VARCHAR(4096), nullable=True),
    Column('webshop_name', VARCHAR(64), index=True),
    Column('brand', VARCHAR(128), index=True),
    Column('price', FLOAT(precision=6, scale=2, unsigned=True)),
    Column('discount_price', FLOAT(precision=6, scale=2, unsigned=True)),
    Column('sizes', VARCHAR(128), nullable=True),
    Column('description', TEXT(convert_unicode=True), nullable=True),
    Column('specifics', TEXT(convert_unicode=True), nullable=True),
    Column('categories', VARCHAR(256)),
    Column('tags', VARCHAR(512), index=True),
    Column('deleted', BOOLEAN, default=False),
)

popular_product_table = Table(
    'Popular_Products',
    metadata,
    Column('Id', TINYINT(unsigned=True), primary_key=True, unique=True),
    Column('Product_Id', SMALLINT(unsigned=True), ForeignKey("Products.Id")),
)


"""
# Define models
class Payment_Method(Base):
    __tablename__ = "Payment_Methods"
    shortName = Column(VARCHAR(4), primary_key=True, unique=True)
    logo = Column(VARCHAR(128))
    fullName = Column(VARCHAR(64))

    def __repr__(self):
        return f'{self.shortName}: {self.fullName}'


class Certification(Base):
    __tablename__ = "Certifications_List"
    Id = Column(TINYINT(unsigned=True), primary_key=True, unique=True)
    name = Column(VARCHAR(64))
    logo = Column(VARCHAR(128))
    url = Column(VARCHAR(128))

    def __repr__(self):
        return f'{self.Id}: {self.name}'


class FairFrog_Criterion(Base):
    __tablename__ = "FairFrog_Criteria"
    Id = Column(TINYINT(unsigned=True), primary_key=True, unique=True)
    name = Column(VARCHAR(64))
    logo = Column(VARCHAR(128))
    description = Column(VARCHAR(1024), nullable=True)

    def __repr__(self):
        return f'{self.Id}: {self.name}'


class Brand(Base):
    __tablename__ = "Brands"
    Id = Column(SMALLINT(unsigned=True), primary_key=True, unique=True)
    brand_name = Column(VARCHAR(128), index=True)
    description = Column(VARCHAR(4096), nullable=True)
    logo = Column(VARCHAR(256))
    certifications = Column(VARCHAR(32), index=True, default="")
    meta_title = Column(VARCHAR(256))
    meta_description = Column(VARCHAR(1024), nullable=True)
    deleted = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.Id}: {self.brand_name}'


class Webshop(Base):
    __tablename__ = 'Webshops'
    Id = Column(TINYINT(unsigned=True), primary_key=True, unique=True)
    webshop_name = Column(VARCHAR(64), index=True)
    description = Column(VARCHAR(2048), nullable=True)
    url = Column(VARCHAR(128))
    blog_url = Column(VARCHAR(128), nullable=True)
    webshop_logo = Column(VARCHAR(128))
    postcode = Column(VARCHAR(8))
    city = Column(VARCHAR(64))
    country = Column(VARCHAR(64))
    address = Column(VARCHAR(256))
    ff_criteria = Column(VARCHAR(32), index=True, nullable=True)
    payment_methods = Column(VARCHAR(32))
    delivery_info = Column(VARCHAR(2048), nullable=True)
    special_info = Column(VARCHAR(2048), nullable=True)
    meta_title = Column(VARCHAR(256), default="")
    meta_description = Column(VARCHAR(512), default="")
    deleted = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.Id}: {self.webshop_name} - {self.url}'


class Product(Base):
    __tablename__ = 'Products'
    Id = Column(SMALLINT(unsigned=True), primary_key=True, unique=True)
    title = Column(VARCHAR(256), index=True)
    meta_title = Column(VARCHAR(256))
    meta_text = Column(VARCHAR(4096), default="")
    url = Column(VARCHAR(200))
    images = Column(VARCHAR(4096), nullable=True)
    webshop_name = Column(VARCHAR(64), index=True)
    brand = Column(VARCHAR(128), index=True)
    price = Column(FLOAT(precision=6, scale=2, unsigned=True))
    discount_price = Column(FLOAT(precision=6, scale=2, unsigned=True))
    sizes = Column(VARCHAR(128), nullable=True)
    description = Column(TEXT(convert_unicode=True), nullable=True)
    specifics = Column(TEXT(convert_unicode=True), nullable=True)
    categories = Column(VARCHAR(256), index=True)
    tags = Column(VARCHAR(256), index=True)
    deleted = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.Id}: {self.title} - {self.url}'

    @property
    def serialize(self):
        ""Return object data in easily serializeable format""
        return {
            'Id': self.Id,
            'title': self.title,
            'meta_title': self.meta_title.strip(),
            'meta_text': self.meta_text.strip(),
            'webshop_name': self.webshop_name.strip(),
            'url': self.url,
            'image': [img.replace('@', ',').strip() for img in self.images.split(',')],
            'price': self.price,
            'discount_price': self.discount_price,
            'brand': self.brand.strip(),
            'sizes': [size.strip() for size in self.sizes.split(',') if size],
            'categories': [cat.strip() for cat in self.categories.lower().split(',')],
            'tags': [tag.strip() for tag in self.tags.lower().split(',')],
            'description': self.description.strip().split('\n'),
            'specifics': [
                detail.rpartition(':') for detail in self.specifics.strip().split('\n') if detail
            ],
            'deleted': self.deleted,
        }


class Popular_Product(Base):
    __tablename__ = 'Popular_Products'
    Id = Column(TINYINT(unsigned=True), primary_key=True, unique=True)
    Product_Id = Column(SMALLINT(unsigned=True), ForeignKey("Products.Id"))
    product = relationship("Product", lazy="joined", uselist=False, innerjoin=True)
"""
