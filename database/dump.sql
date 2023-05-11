--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 14.2

-- Started on 2023-04-28 17:00:47

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

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

--CREATE SCHEMA public;

--
-- TOC entry 3028 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 174655)
-- Name: clusters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clusters (
    name character varying NOT NULL,
    description character varying,
    item character varying NOT NULL,
    data character varying,
    path_cluster_dir character varying NOT NULL
);


--
-- TOC entry 200 (class 1259 OID 174647)
-- Name: hosts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hosts (
    hostname character varying NOT NULL,
    username character varying NOT NULL,
    password character varying,
    status_connect boolean,
    private_key character varying
);


--
-- TOC entry 202 (class 1259 OID 174663)
-- Name: init_files; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.init_files (
    version character varying NOT NULL,
    namefile character varying,
    name character varying NOT NULL,
    license boolean DEFAULT false,
    license_text character varying
);


--
-- TOC entry 204 (class 1259 OID 191030)
-- Name: process; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.process (
    command character varying NOT NULL,
    extid_action character varying NOT NULL,
    is_complite boolean DEFAULT false,
    stdout character varying DEFAULT ''::character varying NOT NULL,
    stderr character varying,
    date_start date NOT NULL,
    code_return bigint,
    id bigint NOT NULL
);


--
-- TOC entry 205 (class 1259 OID 191038)
-- Name: process_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.process ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.process_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 203 (class 1259 OID 182838)
-- Name: user_cm; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_cm (
    username character varying NOT NULL,
    hash_password character varying NOT NULL
);

--
-- TOC entry 3020 (class 0 OID 182838)
-- Dependencies: 203
-- Data for Name: user_cm; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.user_cm VALUES ('admin', '$2b$12$9dlxMDYS2t3lnSUS15qYp.EvA8TT8xmrxz0g39Sai8g3zoT8.LBdq');

