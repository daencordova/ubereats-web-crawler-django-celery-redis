from django_redis import get_redis_connection


class RedisCache:
    @classmethod
    def get_connection(cls):
        return get_redis_connection()

    @classmethod
    def add_member(cls, key, member):
        connection = cls.get_connection()
        return connection.sadd(key, member)


class RestaurantCache(RedisCache):
    @classmethod
    def add_member(cls, url):
        member = f"{url}"
        key = f"ubereats.restaurant.{member}"

        return super().add_member(key, member)


class CategoryRestaurantCache(RedisCache):
    @classmethod
    def add_member(cls, category_id, restaurant_id):
        member = f"{category_id}|{restaurant_id}"
        key = f"ubereats.category_restaurant.{member}"

        return super().add_member(key, member)
