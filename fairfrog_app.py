from flask import jsonify
from flask_sslify import SSLify
from sqlalchemy.sql import and_, or_

from app_setup import app, cache, db_session, engine
from models import (
    brand_table,
    certification_table,
    ff_criterion_table,
    payment_method_table,
    popular_product_table,
    product_table,
    webshop_table,
)
from process_products_funcs import process_product, process_product_array

sslify = SSLify(app)


def get_webshop_dict(webshop):
    webshop = dict(webshop)
    webshop["payment_methods"] = webshop.get("payment_methods").split(",")
    webshop["ff_criteria"] = (
        webshop.get("fairFrog_criteria").split(",")
        if webshop.get("fairFrog_criteria", None)
        else []
    )
    return webshop


def get_brand_dict(brand):
    brand = dict(brand)
    brand["certifications"] = brand.get("certifications").split(",")
    return brand


@app.route("/")
def index():
    return "<h1>Hello FairFrogger!</h1>"


@app.route("/get_products/")
@app.route("/get_products/brand/<string:brand>/")
@app.route("/get_products/cat/<string:cat>/")
@app.route("/get_products/cat/<string:cat>/<string:subcat>/")
@app.route("/get_products/webshop/<string:webshop>/")
@app.route("/get_products/tags/<string:tags>/")
@app.route("/get_products/prod_ids/<string:prod_ids>/")
@cache.cached(timeout=43200)
def get_products(
    brand: str = None,
    cat: str = None,
    subcat: str = None,
    webshop: str = None,
    tags: str = None,
    prod_ids: str = None,
):
    """Get all products, or filtered products.

    Args:
        brand (str, optional): Defaults to None. [description]
        cat (str, optional): Defaults to None. [description]
        subcat (str, optional): Defaults to None. [description]
        webshop (str, optional): Defaults to None. [description]
        tags (str, optional): Defaults to None. [description]
        prod_ids (str, optional): Defaults to None. [description]

    Returns:
        List of products received in the query
    """
    if cat:
        cat = cat.replace("_", " ")
        where_stmts = [product_table.c.categories.contains(cat)]
        if subcat:
            subcat = subcat.replace("_", " ")
            where_stmts.append(product_table.c.categories.contains(subcat))
        statement = product_table.select().where(
            and_(product_table.c.deleted == False, *where_stmts)
        )
    elif webshop:
        webshop = webshop.replace("_", " ")
        app.logger.info("Webshop name: " + webshop)
        statement = product_table.select().where(
            and_(product_table.c.deleted == False, product_table.c.webshop_name.ilike(webshop))
        )
    elif brand:
        app.logger.info("Brand name: " + brand)
        brand = brand.replace("_", " ")
        statement = product_table.select().where(
            and_(product_table.c.deleted == False, product_table.c.brand.ilike(brand))
        )
    elif tags:
        app.logger.info("Tags to search for: " + tags)
        tags = ["%{}%".format(tag.strip()) for tag in tags.split("+")]
        where_stmts = [
            or_(
                product_table.c.title.ilike(tag),
                product_table.c.description.ilike(tag),
                product_table.c.webshop.ilike(tag),
                product_table.c.tags.ilike(tag),
            )
            for tag in tags
        ]
        statement = product_table.select().where(
            and_(product_table.c.deleted == False, *where_stmts)
        )
    elif prod_ids:
        prod_id_query = prod_ids.strip().split(",")
        app.logger.debug("Product ids: " + prod_ids)
        product_query = tuple([int(prod_id) for prod_id in prod_id_query])
        statement = product_table.select().where(
            and_(product_table.c.deleted == False, product_table.c.Id.in_(product_query))
        )
    else:
        statement = product_table.select().where(product_table.c.deleted == False)
    try:
        conn = engine.connect()
        products = conn.execute(statement).fetchall()
    except Exception:
        app.logger.exception("No products.")
        return jsonify(products_list=[])
    finally:
        conn.close()

    return jsonify(products_list=process_product_array(products))


@app.route("/get_the_product/<int:prod_id>/<int:deleted>/")
@app.route("/get_the_product/<int:prod_id>/")
def get_the_product(prod_id: int, deleted: int = 0):
    if deleted:
        statement = product_table.select().where(product_table.c.Id == prod_id)
    else:
        statement = product_table.select().where(
            and_(product_table.c.Id == prod_id, product_table.c.deleted == False)
        )
    try:
        conn = engine.connect()
        product = conn.execute(statement).fetchone()
        print(product)
        return jsonify(product=process_product(product))
    except Exception:
        app.logger.exception("Product %s cannot be loaded", prod_id)
        return jsonify(product={})
    finally:
        conn.close()


@app.route("/get_popular_products/")
@cache.cached(timeout=600)
def get_popular_products():
    join_clause = product_table.join(popular_product_table)
    try:
        conn = engine.connect()
        products = conn.execute(product_table.select().select_from(join_clause)).fetchall()
    except Exception:
        app.logger.exception("Can't get popular products.")
        return jsonify(popular_products_list=[])
    finally:
        conn.close()

    return jsonify(popular_products_list=process_product_array(products))


@app.route("/get_brands/")
@app.route("/get_brands/<string:brand_name>/")
@cache.cached(timeout=43200)
def get_brands(brand_name: str = None):
    if brand_name:
        brand_name = brand_name.replace("_", " ")
        app.logger.debug(brand_name)
        statement = brand_table.select().where(
            and_(brand_table.c.brand_name.ilike(brand_name), brand_table.c.deleted == False)
        )
    else:
        statement = brand_table.select().where(brand_table.c.deleted == False)
    try:
        conn = engine.connect()
        all_brands = conn.execute(statement.order_by("brand_name"))
    except Exception:
        app.logger.exception("Couldn't get brands.")
        return jsonify(brands_list=[])
    finally:
        conn.close()
    return jsonify(brands_list=[get_brand_dict(row) for row in all_brands])


@app.route("/get_webshops/")
@app.route("/get_webshops/<string:webshop_name>/")
@cache.cached(timeout=43200)
def get_webshops(webshop_name: str = ""):
    if webshop_name:
        webshop_name = webshop_name.replace("_", " ")
        app.logger.debug(webshop_name)
        statement = webshop_table.select().where(
            and_(webshop_table.c.webshop_name.ilike(webshop_name), webshop_table.c.deleted == False)
        )
    else:
        statement = webshop_table.select().where(webshop_table.c.deleted == False)
    try:
        conn = engine.connect()
        all_webshops = conn.execute(statement.order_by("webshop_name"))
    except Exception:
        app.logger.exception("Webshops were hard to come by.")
        return jsonify(webshops_list=[])
    finally:
        conn.close()
    return jsonify(webshops_list=[get_webshop_dict(row) for row in all_webshops])


@app.route("/get_certifications/")
def get_certifications():
    try:
        conn = engine.connect()
        certifications = conn.execute(certification_table.select())
    except Exception:
        app.logger.exception("No certifications for you.")
        return jsonify(certifications_list=[])
    finally:
        conn.close()
    return jsonify(certifications_list=[dict(row) for row in certifications])


@app.route("/get_payments/")
def get_payments():
    try:
        conn = engine.connect()
        payments = conn.execute(payment_method_table.select())
    except Exception:
        app.logger.exception("Payment didn't go through.")
        return jsonify(payment_methods=[])
    finally:
        conn.close()
    return jsonify(payment_methods=[dict(row) for row in payments])


@app.route("/get_ff_criteria/")
def get_ff_criteria():
    try:
        conn = engine.connect()
        criteria = conn.execute(ff_criterion_table.select())
    except Exception:
        app.logger.exception("Couldn't find FairFrog criteria.")
        return jsonify(ff_criteria=[])
    finally:
        conn.close()
    return jsonify(ff_criteria=[dict(row) for row in criteria])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=8000,
        threaded=True,
        ssl_context=("/home/kush/ssl/fullchain.pem", "/home/kush/ssl/privkey.pem"),
    )
