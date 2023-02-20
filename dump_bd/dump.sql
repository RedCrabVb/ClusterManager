--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 14.2

-- Started on 2023-02-20 15:49:55

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3006 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 174655)
-- Name: clusters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clusters (
    name character varying NOT NULL,
    description character varying,
    item character varying NOT NULL,
    data character varying,
    path_cluster_dir character varying NOT NULL
);


ALTER TABLE public.clusters OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 174647)
-- Name: hosts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hosts (
    hostname character varying NOT NULL,
    username character varying NOT NULL,
    password character varying,
    status_connect boolean,
    ssh_pub_key character varying
);


ALTER TABLE public.hosts OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 174663)
-- Name: init_files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.init_files (
    version character varying NOT NULL,
    namefile character varying,
    name character varying NOT NULL
);


ALTER TABLE public.init_files OWNER TO postgres;


--
-- TOC entry 2865 (class 2606 OID 174662)
-- Name: clusters clusters_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_pk PRIMARY KEY (name);


--
-- TOC entry 2863 (class 2606 OID 174654)
-- Name: hosts hosts_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hosts
    ADD CONSTRAINT hosts_pk PRIMARY KEY (hostname, username);


--
-- TOC entry 2867 (class 2606 OID 174670)
-- Name: init_files init_files_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.init_files
    ADD CONSTRAINT init_files_pk PRIMARY KEY (version, name);


--
-- TOC entry 3007 (class 0 OID 0)
-- Dependencies: 201
-- Name: TABLE clusters; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.clusters TO cm_user;


--
-- TOC entry 3008 (class 0 OID 0)
-- Dependencies: 200
-- Name: TABLE hosts; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.hosts TO cm_user;


--
-- TOC entry 3009 (class 0 OID 0)
-- Dependencies: 202
-- Name: TABLE init_files; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.init_files TO cm_user;


-- Completed on 2023-02-20 15:49:55

--
-- PostgreSQL database dump complete
--

