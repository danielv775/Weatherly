-- Adminer 4.6.3-dev PostgreSQL dump

\connect "depts5vkc9t2i7";

DROP TABLE IF EXISTS "comments";
DROP SEQUENCE IF EXISTS comments_id_seq;
CREATE SEQUENCE comments_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."comments" (
    "id" integer DEFAULT nextval('comments_id_seq') NOT NULL,
    "comment" character varying NOT NULL,
    "user_id" integer,
    "location_id" integer,
    CONSTRAINT "comments_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "comments_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(id) NOT DEFERRABLE,
    CONSTRAINT "comments_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "locations";
DROP SEQUENCE IF EXISTS locations_id_seq;
CREATE SEQUENCE locations_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."locations" (
    "id" integer DEFAULT nextval('locations_id_seq') NOT NULL,
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" numeric NOT NULL,
    "long" numeric NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "locations_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "pw_hash" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-12 03:04:48.203796+00
