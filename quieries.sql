SELECT "shopapp_product"."id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."create_at",
        "shopapp_product"."archived",
        "shopapp_product"."created_by_id",
        "shopapp_product"."preview"
FROM "shopapp_product"
WHERE NOT "shopapp_product"."archived"
ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(); alias=default

SELECT "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."create_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview"
FROM "shopapp_product"
WHERE "shopapp_product"."id" = 2
LIMIT 21; args=(2,); alias=default

SELECT "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."descriptions"
FROM "shopapp_productimage"
WHERE "shopapp_productimage"."product_id" IN (2); args=(2,); alias=default

