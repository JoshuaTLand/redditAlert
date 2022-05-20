SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE public.posts (
    id integer NOT NULL,
    name character varying NOT NULL,
    author character varying NOT NULL,
    subreddit character varying NOT NULL,
    title character varying NOT NULL,
    url character varying NOT NULL,
    score bigint NOT NULL,
    commentcount bigint NOT NULL,
    postcreatedtime timestamp without time zone NOT NULL,
    entrycreatedtime timestamp without time zone NOT NULL,
    seen boolean DEFAULT false NOT NULL,
    sourcereddit character varying DEFAULT 'r/all'::character varying,
    alertreason character varying DEFAULT 'High Scoring'::character varying NOT NULL,
    discord_post character varying DEFAULT 0 NOT NULL
);


ALTER TABLE public.posts OWNER TO joshua;


CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO joshua;


ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);