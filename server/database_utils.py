from server import db, app
from server.models.models import Advertisements, User


def create_advertisement(olx_id: int, ad_name: str, ad_price: int, ad_currency: str, ad_image: str, ad_author_name: str,
                         url: str) -> None:
    with app.app_context():
        advertisement = Advertisements(olx_id=olx_id,
                                       url=url,
                                       name=ad_name,
                                       price=ad_price,
                                       currency=ad_currency,
                                       author_name=ad_author_name,
                                       image=ad_image)

        db.session.add(advertisement)
        db.session.commit()


def get_advertisement(access_category, user: User, sort):
    if access_category.value == 1:
        ads = Advertisements.query.with_entities(Advertisements.olx_id, Advertisements.name,
                                                       Advertisements.price, Advertisements.currency).filter(
            ~Advertisements.id.in_(get_user_hidden_ads(user)))

        if sort == 'price':
            ads = ads.order_by(Advertisements.price.desc()).limit(100).all()
        else:
            ads = ads.order_by(Advertisements.created_at.desc()).limit(100).all()
        return [{'id': ad.olx_id, 'name': ad.name, 'price': ad.price, 'currency': ad.currency} for ad in ads]
    elif access_category.value == 2:
        ads = Advertisements.query.with_entities(Advertisements.olx_id, Advertisements.name,
                                                 Advertisements.price, Advertisements.currency,
                                                 Advertisements.image).filter(
            ~Advertisements.id.in_(get_user_hidden_ads(user)))

        if sort == 'price':
            ads = ads.order_by(Advertisements.price.desc()).limit(100).all()
        else:
            ads = ads.order_by(Advertisements.created_at.desc()).limit(100).all()

        return [{'id': ad.olx_id, 'name': ad.name, 'price': ad.price, 'currency': ad.currency, 'image': ad.image} for ad
                in ads]
    elif access_category.value == 3:
        ads = Advertisements.query.with_entities(Advertisements.olx_id, Advertisements.name,
                                                 Advertisements.price, Advertisements.currency,
                                                 Advertisements.image, Advertisements.author_name).filter(
            ~Advertisements.id.in_(get_user_hidden_ads(user)))

        if sort == 'price':
            ads = ads.order_by(Advertisements.price.desc()).limit(100).all()
        else:
            ads = ads.order_by(Advertisements.created_at.desc()).limit(100).all()

        return [{'id': ad.olx_id, 'name': ad.name, 'price': ad.price, 'currency': ad.currency, 'image': ad.image,
                 'author': ad.author_name} for ad in ads]


def get_user_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()


def hide_ad(user_id: int, ad_id: int):
    with app.app_context():
        ad = Advertisements.query.filter(Advertisements.olx_id == ad_id).first()
        user = User.query.get(user_id)
        user.hidden_ads.append(ad)
        db.session.commit()


def get_user_hidden_ads(user: User):
    return [ad.id for ad in user.hidden_ads]


def get_ads_urls():
    with app.app_context():
        return set([ad.url for ad in Advertisements.query.all()])
