--
-- PostgreSQL database dump
--

\restrict KQaboDCVau5N5T5MMddPuQcdplJJ9pdWbtuoVKjr5DWmhTN3xd8Kh2O4FaZOCha

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

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

SET default_table_access_method = heap;

--
-- Name: partners; Type: TABLE; Schema: public; Owner: irwt
--

CREATE TABLE public.partners (
    id integer NOT NULL,
    name character varying NOT NULL,
    contact_email character varying,
    notes text,
    is_active integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.partners OWNER TO irwt;

--
-- Name: partners_id_seq; Type: SEQUENCE; Schema: public; Owner: irwt
--

CREATE SEQUENCE public.partners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.partners_id_seq OWNER TO irwt;

--
-- Name: partners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: irwt
--

ALTER SEQUENCE public.partners_id_seq OWNED BY public.partners.id;


--
-- Name: processed_emails; Type: TABLE; Schema: public; Owner: irwt
--

CREATE TABLE public.processed_emails (
    email_id character varying NOT NULL,
    processed_at timestamp without time zone
);


ALTER TABLE public.processed_emails OWNER TO irwt;

--
-- Name: rental_requests; Type: TABLE; Schema: public; Owner: irwt
--

CREATE TABLE public.rental_requests (
    id character varying NOT NULL,
    status character varying,
    client_name character varying,
    client_email character varying NOT NULL,
    client_vat character varying,
    client_phone character varying,
    pickup_date date,
    return_date date,
    pickup_location character varying,
    return_location character varying,
    vehicle_type character varying,
    special_requests text,
    selected_partner_id character varying,
    selected_partner_name character varying,
    price double precision,
    original_email_id character varying,
    original_email_subject character varying,
    original_email_body text,
    thread_id character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    selected_vehicle_id integer,
    selected_vehicle_description character varying,
    cost_price double precision,
    internal_notes text,
    driver_name character varying,
    artist_project_event character varying,
    destination_cities character varying
);


ALTER TABLE public.rental_requests OWNER TO irwt;

--
-- Name: vehicles; Type: TABLE; Schema: public; Owner: irwt
--

CREATE TABLE public.vehicles (
    id integer NOT NULL,
    partner_id integer NOT NULL,
    category character varying NOT NULL,
    group_code character varying NOT NULL,
    description character varying NOT NULL,
    price_1_3_days double precision,
    price_4_6_days double precision,
    price_7_29_days double precision,
    price_monthly double precision,
    franchise double precision,
    min_age integer,
    license_years integer,
    notes text,
    is_active integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.vehicles OWNER TO irwt;

--
-- Name: vehicles_id_seq; Type: SEQUENCE; Schema: public; Owner: irwt
--

CREATE SEQUENCE public.vehicles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vehicles_id_seq OWNER TO irwt;

--
-- Name: vehicles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: irwt
--

ALTER SEQUENCE public.vehicles_id_seq OWNED BY public.vehicles.id;


--
-- Name: partners id; Type: DEFAULT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.partners ALTER COLUMN id SET DEFAULT nextval('public.partners_id_seq'::regclass);


--
-- Name: vehicles id; Type: DEFAULT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.vehicles ALTER COLUMN id SET DEFAULT nextval('public.vehicles_id_seq'::regclass);


--
-- Data for Name: partners; Type: TABLE DATA; Schema: public; Owner: irwt
--

COPY public.partners (id, name, contact_email, notes, is_active, created_at, updated_at) FROM stdin;
1	Safety Show	\N	\N	1	2025-12-10 09:59:55.691175	2025-12-10 09:59:55.691179
2	Europcar	\N	\N	1	2025-12-10 09:59:55.748771	2025-12-10 09:59:55.748772
3	IN ROCK	\N	\N	1	2025-12-10 09:59:55.76497	2025-12-10 09:59:55.764971
4	WayGo	\N	ddsfzgd	1	2025-12-10 09:59:55.785116	2026-04-08 10:34:31.32215
5	Movida	\N	testfsdadsf	1	2025-12-10 09:59:55.817813	2026-04-08 10:45:50.583781
\.


--
-- Data for Name: processed_emails; Type: TABLE DATA; Schema: public; Owner: irwt
--

COPY public.processed_emails (email_id, processed_at) FROM stdin;
<qEted2yqwXNjq4zfVnFvog@notifications.google.com>	2026-03-20 14:36:52.333427
<20260320144508.e6bad4e1c30d2715@airtable.com>	2026-03-20 14:45:30.235393
<20260320145825.e037580708babd37@airtable.com>	2026-03-20 14:58:50.266397
<cSt8qPpNVXjKXB4EJXiHrg@notifications.google.com>	2026-03-20 15:02:31.37344
<fKYzFMydRyuHW9ubC9uk3Q@notifications.google.com>	2026-03-20 15:05:29.803323
<EFcn7UiqfDSN81_NnXgueA@notifications.google.com>	2026-03-22 14:36:50.409333
<31.EF.28706.26562C96@i-0f5d359962ec32d6b.mta3vrest.sd.prd.sparkpost>	2026-03-24 10:20:32.321428
<nuJOlUpvQMa-oqqTg03I0w@geopod-ismtpd-52>	2026-03-31 21:17:31.235955
<CAFxnAhACQGur=p14NR8z8Pj7OCHr3fHoopX3EvwhttwBgvaEFg@mail.gmail.com>	2026-04-01 13:56:51.177584
<CAFxnAhC+0zZUD0Ox7-UiF4o_04Lbv-05RTuAzv2+ht6aG-yG=w@mail.gmail.com>	2026-04-01 13:57:52.596094
<20260406100033.f3e7c343046be513@airtable.com>	2026-04-06 10:00:51.127553
<11.76.59207.F1835D96@i-0868bd7b6123112eb.mta3vrest.sd.prd.sparkpost>	2026-04-07 17:00:30.263743
<CAFxnAhAAdZHXgnT-PSa51nqHSpOJffOxtnYutNyVVgH22+x7Ag@mail.gmail.com>	2026-04-09 09:33:11.083157
<20260415021954.92798b99aefd9312@airtable.com>	2026-04-15 02:20:11.428637
<CAFxnAhDXos6Pm7Na2hV7PT6s5LWQLaNmuNp85E4_XAeo0Rw=fw@mail.gmail.com>	2026-04-16 09:40:52.135639
<RCug_YPLcqHw7ivptGQNFw@notifications.google.com>	2026-04-16 10:42:11.845323
<979473b8df57c5b0a649fccaf124da0b100510b4-20079005-111437363@google.com>	2026-04-16 10:42:19.267036
<gXdhgWSsU0zBReiv635jxA@notifications.google.com>	2026-04-16 10:42:24.852994
<c6a9f4029b7a5a21eefbdda7b77ee71d1a46c86c-20376446-337030291@google.com>	2026-04-16 10:42:32.630997
<MKg77KKQtr0B-S5HezfYkw@notifications.google.com>	2026-04-16 10:51:10.408748
<pSA2TGnewQkNC92Auje8jA@notifications.google.com>	2026-04-16 10:51:14.089533
<LySeXz5NtbJgn7UtLPW-lw@notifications.google.com>	2026-04-16 10:53:11.574682
<PGQeI2IUzLEyIkdOE8TUEg@notifications.google.com>	2026-04-16 10:55:50.761505
<teVBT4fRG-qf_R_vFCogSQ@notifications.google.com>	2026-04-16 10:57:49.928862
<XGuWx_n1vm49jXxGzVCFQg@notifications.google.com>	2026-04-16 10:57:55.944653
<sFJ4PN5rYp2VHIqw0wJvNw@notifications.google.com>	2026-04-16 11:00:10.177853
<BI3tPyxo_cT6LgBc-H8IEg@notifications.google.com>	2026-04-16 11:03:10.094066
<20260418161008.6c73829bdc93d438@airtable.com>	2026-04-18 16:10:30.517328
<bEvBLOVM4prC53orJdf2iA@notifications.google.com>	2026-04-19 11:00:11.822893
<20260420160014.061b31f8d8840eeb@airtable.com>	2026-04-20 16:00:32.324093
<9gldZcnUS6CnBX-V4yVdGA@geopod-ismtpd-21>	2026-04-20 19:31:11.231256
<010e019dd3be4192-7efab3e0-95fe-47fb-8420-f42a79adc3cb-000000@ap-southeast-1.amazonses.com>	2026-04-28 10:59:29.078343
\.


--
-- Data for Name: rental_requests; Type: TABLE DATA; Schema: public; Owner: irwt
--

COPY public.rental_requests (id, status, client_name, client_email, client_vat, client_phone, pickup_date, return_date, pickup_location, return_location, vehicle_type, special_requests, selected_partner_id, selected_partner_name, price, original_email_id, original_email_subject, original_email_body, thread_id, created_at, updated_at, selected_vehicle_id, selected_vehicle_description, cost_price, internal_notes, driver_name, artist_project_event, destination_cities) FROM stdin;
0bfa288e-042d-4885-8b3f-9bded09c0a6c	invoiced	Andrea Costa	viaturas@inrockwetrust.pt	508479770	+351 934 331 384	2026-08-14	2026-08-16	Porto	Porto	Carrinha de 9 lugares + carrinha com espaço de carga	Combustível: gasóleo; Via Verde: sim.	5	Movida	98.71	<73523D95-4E00-4184-BCDD-9E611DB79860@inrockwetrust.pt>	Re: Aluguer de viatura - Olavo Bilac	Andrea costa\r\n\r\n\r\n\r\nAtentamente,\r\n\r\nAndrea Costa\r\n\r\n￼\r\n\r\n\r\n\r\n@: viaturas@inrockwetrust.pt <mailto:viaturas@inrockwetrust.pt>\r\nT: +351 934 331 384\r\nR: Rua do Casal, 230 | 4435-152 Rio Tinto <https://maps.app.goo.gl/9R9bFafmj62vAMRYA>\r\n\r\n\r\n\r\n\r\n> No dia 25/02/2026, às 17:48, reservas.irwt@gmail.com escreveu:\r\n> \r\n> \r\n> Olá Carla Costa,\r\n> \r\n> Obrigado pelo seu contacto sobre o aluguer de uma carrinha. Para podermos avançar com o seu pedido, precisamos de algumas informações adicionais.\r\n> \r\n> Informação em Falta\r\n> \r\n> O seu nome completo\r\n> Assim que tivermos esses detalhes, tratamos do resto e seguimos com a reserva.\r\n> \r\n> Um abraço,\r\n> Equipa IRWT\r\n> IRWT - Aluguer de Carrinhas\r\n> \r\n> Este email foi enviado automaticamente. Por favor responda diretamente a este email para qualquer questão.\r\n\r\n	1858120230094413695	2026-02-25 17:49:44.566031	2026-02-25 18:03:33.341634	77	IS - Peugeot 308 Auto Híbrido	82.26	\N	Guilherme Rocha	Olavo Bilac	Porto, Borba, Ameixial, Porto
43a264fa-8798-4c69-83c7-c61f527aa3bb	invoiced	Koti Studio	kotistudio.ai@gmail.com	123456789	\N	2026-04-20	2026-04-26	Porto	Porto	Carrinha Mercedes V (9 lugares)	Levantamento às 15h00 no dia 20/04 e devolução às 15h00 no dia 26/04.	5	Movida	194.9	<CAFxnAhC+0zZUD0Ox7-UiF4o_04Lbv-05RTuAzv2+ht6aG-yG=w@mail.gmail.com>	Re: Concerto Elton John - Lamego 25/4	Elton John\r\n\r\n<reservas.irwt@gmail.com> escreveu (quarta, 1/04/2026 à(s) 14:56):\r\n\r\n> [image: IRWT]\r\n> Olá Koti Studio,\r\n>\r\n> Obrigado pelo seu contacto sobre o aluguer de uma carrinha. Para podermos\r\n> avançar com o seu pedido, precisamos de algumas informações adicionais.\r\n> Informação em Falta\r\n>\r\n>    - Nome do Artista/Projeto/Evento*\r\n>\r\n> * Aqui será a vossa referência a colocar na fatura (ex. Rolling Stones -\r\n> Rock in Bifanas - 30 Fevereiro)\r\n>\r\n> Assim que tivermos esses detalhes, tratamos do resto e seguimos com a\r\n> reserva.\r\n>\r\n> Um abraço,\r\n> *Equipa IRWT*\r\n>\r\n> IRWT - Aluguer de Carrinhas\r\n>\r\n> Este email foi enviado automaticamente. Por favor responda diretamente a\r\n> este email para qualquer questão.\r\n>\r\n	1861276712474176219	2026-04-01 13:57:52.669524	2026-04-09 09:44:53.125565	96	EHC - Citroen e-C3 Auto Elétrico	162.42	\N	Marques Mendes	Elton John	Lamego
9a455c29-2727-4b9d-884f-b2252c8b7887	pending_selection	Koti Studio	kotistudio.ai@gmail.com	123456789	\N	2026-04-20	2026-04-26	Porto	Porto	Carrinha Mercedes V (tipo V-Class)	Carrinha para deslocação para concerto em Lamego; levantamento e entrega às 15h00.	4	WayGo	352.66	<CAFxnAhAAdZHXgnT-PSa51nqHSpOJffOxtnYutNyVVgH22+x7Ag@mail.gmail.com>	Concerto Elton John - Lamego 25/4	Boa tarde,\r\n\r\nPreciso de uma Carrinha V para o concerto de Lamego.\r\n\r\nArtista: Elton John\r\nNiPC: 123 456 789\r\nLevantamento: Porto dia 20/4\r\nDevoluçao: Porto dia 26/4\r\nData e hora de levantamento 20/4 15h00\r\nData e hora de entrega 26/4 15h00\r\nCondutor: Marques Mendes\r\nCidades de destino: Lamego\r\n\r\nObrigado.\r\n	1861984891102216130	2026-04-09 09:33:11.099091	2026-04-09 09:54:20.15088	70	T - Mitsubishi L200 Diesel	293.88	\N	Marques Mendes	Elton John	Lamego
bdb107e4-16b0-4e97-bc82-c42f1ff6192f	accepted	Koti Studio	kotistudio.ai@gmail.com	123456789	\N	2026-04-20	2026-04-26	Porto	Porto	Carrinha Mercedes V (9 lugares)	Recolha e entrega às 15h00.	5	Movida	647.78	<CAFxnAhDXos6Pm7Na2hV7PT6s5LWQLaNmuNp85E4_XAeo0Rw=fw@mail.gmail.com>	Concerto Elton John - Avintes	Boa tarde,\r\n\r\nPreciso de uma Carrinha V para o concerto de Lamego.\r\n\r\nArtista: Elton John\r\nNiPC: 123 456 789\r\nLevantamento: Porto dia 20/4\r\nDevoluçao: Porto dia 26/4\r\nData e hora de levantamento 20/4 15h00\r\nData e hora de entrega 26/4 15h00\r\nCondutor: Marques Mendes\r\nCidades de destino: Avintes\r\n\r\nObrigado.\r\n	1862619568206011876	2026-04-16 09:40:52.155197	2026-04-28 10:50:54.237293	93	HJ - VW Multivan Auto Diesel/Gasolina	539.82	\N	Marques Mendes	Elton John	Avintes
\.


--
-- Data for Name: vehicles; Type: TABLE DATA; Schema: public; Owner: irwt
--

COPY public.vehicles (id, partner_id, category, group_code, description, price_1_3_days, price_4_6_days, price_7_29_days, price_monthly, franchise, min_age, license_years, notes, is_active, created_at, updated_at) FROM stdin;
1	1	Ligeiros	A	Renault Clio / VW Polo / Peugeot 208	77.39	72.07	66.48	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.700724	2025-12-10 09:59:55.700726
2	1	Ligeiros	B	Renault Megane / Seat Leon / Fiat Tipo	84.75	79.17	76.38	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.707524	2025-12-10 09:59:55.707527
3	1	Ligeiros	C	Seat Leon STW / Fiat Tipo STW / Ford Focus STW	95.88	90.78	85.17	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.709055	2025-12-10 09:59:55.709057
4	1	Ligeiros	D	BMW Serie 1 / Mercedes Classe A	117.3	108.12	102	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.710607	2025-12-10 09:59:55.710609
5	1	Ligeiros	E	Renault Kadjar / Nissan Qashqai / Audi Q2	104.55	98.94	93.84	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.71196	2025-12-10 09:59:55.711962
6	1	Ligeiros	F1	Dacia Jogger / Citroen C4 Picasso (5+2 Lugares)	127.5	122.4	119.85	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.713523	2025-12-10 09:59:55.713525
7	1	Ligeiros	G	BMW Serie 3 / Peugeot 508	144.84	136.68	131.58	\N	0	22	1	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.715155	2025-12-10 09:59:55.715157
8	1	Ligeiros	G1	BMW Serie 3 STW / Peugeot 508 STW	149.68	139.18	131.3	\N	0	25	2	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.717038	2025-12-10 09:59:55.717039
9	1	Ligeiros	H	BMW Serie 5 STW / Mercedes Classe E STW	167.48	147.18	142.1	\N	0	25	2	Franquia 0€ c/ condutor Safety Show	1	2025-12-10 09:59:55.718511	2025-12-10 09:59:55.718512
10	1	Comerciais	AA	Seat Ibiza 1M3 (450kg)	72.07	70.04	66.99	\N	840	21	1	C:5700 A:890	1	2025-12-10 09:59:55.720023	2025-12-10 09:59:55.720025
11	1	Comerciais	AB	VW Caddy 3M3 (734kg)	73.59	69.27	66.48	\N	840	21	1	C:1780 A:1240 L:1550	1	2025-12-10 09:59:55.721474	2025-12-10 09:59:55.721476
12	1	Comerciais	AD	Renault Trafic / VW Transporter 7M3 (1240kg)	109.11	104.04	91.35	\N	1200	21	1	C:2500 A:1380 L:1690	1	2025-12-10 09:59:55.722821	2025-12-10 09:59:55.722822
13	1	Comerciais	AE	Renault Master 11M3 (1620kg)	124.85	114.19	106.58	\N	1200	21	2	C:3200 A:1890 L:1760	1	2025-12-10 09:59:55.724136	2025-12-10 09:59:55.724137
14	1	Comerciais	AF	Renault Master 13M3 (1530kg)	130	120	110	\N	1800	21	2	C:3680 A:1890 L:1760	1	2025-12-10 09:59:55.72526	2025-12-10 09:59:55.725262
15	1	Comerciais	AR	VW Crafter 15M3 (1100kg)	137.5	127.5	117.5	\N	1800	21	2	C:4600 A:1800 L:1750	1	2025-12-10 09:59:55.726404	2025-12-10 09:59:55.726406
16	1	Comerciais	AG	Iveco 35C13 18M3 (1250kg)	143.5	135.81	125.56	\N	1800	25	2	C:4700 A:2140 L:1760	1	2025-12-10 09:59:55.727768	2025-12-10 09:59:55.727769
17	1	Comerciais	AH	Mercedes Sprinter 20M3 S/Plataforma (900kg)	150	145	140	\N	2000	25	2	C:4300 A:2200 L:2150	1	2025-12-10 09:59:55.729085	2025-12-10 09:59:55.729086
18	1	Comerciais	AI	Mercedes Sprinter 20M3 C/Plataforma (625kg)	164.63	151.5	141.4	\N	2000	25	2	C:4300 A:2200 L:2150	1	2025-12-10 09:59:55.731918	2025-12-10 09:59:55.73192
19	1	Minibus	F	VW Sharan / Seat Alhambra (7 Lugares)	144.64	138.04	135	\N	1250	21	1	\N	1	2025-12-10 09:59:55.73319	2025-12-10 09:59:55.733191
20	1	Minibus	AJ	Toyota Proace 6+Carga	131.3	121.2	111.1	\N	1140	21	1	\N	1	2025-12-10 09:59:55.73436	2025-12-10 09:59:55.734361
21	1	Minibus	AK	Ford Transit 9+Carga	163.2	153	142.8	\N	1000	24	1	\N	1	2025-12-10 09:59:55.735606	2025-12-10 09:59:55.735607
22	1	Minibus	AL	Renault Trafic 9 Lugares	142.8	135.15	127.5	\N	1800	24	1	\N	1	2025-12-10 09:59:55.736933	2025-12-10 09:59:55.736934
23	1	Minibus	AN	Mercedes Vito / Peugeot Traveller 8/9 Lugares	163.2	153	142.8	\N	1800	24	1	\N	1	2025-12-10 09:59:55.738146	2025-12-10 09:59:55.738147
24	1	Minibus	AO	Mercedes V 8 Lugares	237.35	217.15	196.95	\N	4000	25	2	\N	1	2025-12-10 09:59:55.739558	2025-12-10 09:59:55.739559
25	1	Pieter Smit	AP	8/9 Lugares Versão Regular (4M3/1250kg)	160	160	160	2400	1000	\N	\N	Semanal: 875€	1	2025-12-10 09:59:55.740791	2025-12-10 09:59:55.740792
26	1	Pieter Smit	AQ	8/9 Lugares Versão Luxo (5.5M3/800kg)	185	185	185	3300	1000	\N	\N	Semanal: 1015€	1	2025-12-10 09:59:55.742237	2025-12-10 09:59:55.742239
27	1	Pieter Smit	AS	3 Lugares 15M3 (1100kg)	160	160	160	2000	1000	\N	\N	Semanal: 875€	1	2025-12-10 09:59:55.743813	2025-12-10 09:59:55.743815
28	1	Pieter Smit	AT	3 Lugares 20M3 (950kg)	165	165	165	2100	1000	\N	\N	Semanal: 980€	1	2025-12-10 09:59:55.745875	2025-12-10 09:59:55.745877
29	1	Pieter Smit	AU	8 Lugares (7.5M3)	155	155	155	2250	1000	\N	\N	Semanal: 700€	1	2025-12-10 09:59:55.747352	2025-12-10 09:59:55.747353
30	2	Furgoneta	KYIA	Fiat Doblo A/C ou Similar (3M3)	43.3	41.1	36.8	774	100	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.750195	2025-12-10 09:59:55.750197
31	2	Furgões	VPIA	MB Vito 116 CDI (6M3)	57.1	54.2	48.5	1020	150	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.751676	2025-12-10 09:59:55.751677
32	2	Furgões	VGIA	Fiat Ducato (11M3)	69.4	65.9	59	1239	250	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.753178	2025-12-10 09:59:55.753179
33	2	Furgões	VYIA	Fiat Ducato (15M3)	78.6	74.7	66.8	1404	250	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.754676	2025-12-10 09:59:55.754678
34	2	Furgões	VYKA	Iveco Daily 35 C 14 Auto (18M3)	85.1	80.8	72.3	1518	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.756102	2025-12-10 09:59:55.756104
35	2	Chassis Cabine	VGBH	Isuzu (15M3) Chassis Cabine	81.1	77	68.9	1446	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.757428	2025-12-10 09:59:55.75743
36	2	Chassis Cabine	VYBH	Mercedes Sprinter Chassis Cabine (20M3)	103.2	98	87.7	1842	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.758626	2025-12-10 09:59:55.758628
37	2	Chassis Cabine	VYBL	MB Sprinter C/Plat. Elevatória (20M3)	108.3	102.9	92.1	1935	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.759843	2025-12-10 09:59:55.759844
38	2	Mista	VPDA	Ford Transit 6L	95.2	90.4	80.9	1698	150	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.761174	2025-12-10 09:59:55.761175
39	2	Caixa Aberta	VGDA	Iveco 35C12 Dup CX Aberta	79.9	75.9	67.9	1425	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.762311	2025-12-10 09:59:55.762312
40	2	Frigoríficas	VMFS	Fiat Ducato ChCab MultiTemp (11M3)	122.9	116.8	104.5	2196	350	\N	\N	500km/dia, +0.12€/km extra	1	2025-12-10 09:59:55.763534	2025-12-10 09:59:55.763536
41	3	Citadino	EDMD	Mitsubishi Colt ou similar	36.9	36.9	36.9	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.766257	2025-12-10 09:59:55.766259
42	3	Compacto	CWMV	Fiat Tipo SW ou Similar	46.9	46.9	46.9	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.768011	2025-12-10 09:59:55.768013
43	3	Compacto Auto	CWAV	Ford Focus ou similar	50	50	50	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.769532	2025-12-10 09:59:55.769533
44	3	SUV	CWAD	Ford Puma SUV ou similar	57	57	57	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.771143	2025-12-10 09:59:55.771145
45	3	Premium	JWAH	Mercedes-Benz CLA Shooting Brake	122.6	122.6	122.6	\N	0	\N	\N	Via Verde: 1.91€/dia, Híbrido Auto, IVA incluído	1	2025-12-10 09:59:55.772593	2025-12-10 09:59:55.772595
46	3	Minibus Auto	C9L	VW Transporter 9L (Auto Diesel)	138	138	138	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.774353	2025-12-10 09:59:55.77572
47	3	Minibus+Carga	C9L+C	Fiat Ducato 9L (Manual Diesel)	123	123	123	\N	0	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.779853	2025-12-10 09:59:55.779854
48	3	Premium Van	UVAD	Mercedes-Benz Classe V	200	200	200	\N	500	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.781221	2025-12-10 09:59:55.781222
49	3	Premium Sedan	ULAH	Mercedes-Benz Classe E	144	144	144	\N	500	\N	\N	Via Verde: 1.91€/dia, Híbrido Auto, IVA incluído	1	2025-12-10 09:59:55.782519	2025-12-10 09:59:55.782521
50	3	Premium SUV	UFAD	Mercedes-Benz GLC	195	195	195	\N	500	\N	\N	Via Verde: 1.91€/dia, IVA incluído	1	2025-12-10 09:59:55.783896	2025-12-10 09:59:55.783898
51	4	Económico	A1	Fiat 500 ou similar (3P/4L)	17.31	17.31	17.31	459	1500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.786254	2025-12-10 09:59:55.786256
52	4	Económico	A3	Kia Picanto ou similar (5P/4L)	17.31	17.31	17.31	459	1500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.78747	2025-12-10 09:59:55.787472
53	4	Utilitário	B	Opel Corsa 1.2 Gasolina	19.19	19.19	19.19	509	1800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.788812	2025-12-10 09:59:55.788813
54	4	Utilitário Auto	B Auto	Seat Ibiza Auto 1.2 Gasolina	26.12	26.12	26.12	569	1800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.790169	2025-12-10 09:59:55.79017
55	4	SUV Pequeno	BSUV	Renault Captur Gasolina	24.08	24.08	24.08	565	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.791505	2025-12-10 09:59:55.791506
56	4	SUV Auto	BSUV Auto	Seat Arona Auto Gasolina	29.17	29.17	29.17	659	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.792918	2025-12-10 09:59:55.79292
57	4	Utilitário Diesel	BD	Citroen C3 diesel	26.12	26.12	26.12	569	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.794551	2025-12-10 09:59:55.794552
58	4	Familiar	C	VW Golf Gasolina	21.3	21.3	21.3	565	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.796024	2025-12-10 09:59:55.796026
59	4	Familiar+	C+	Peugeot 308 SW Gasolina	24.14	24.14	24.14	589	2200	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.797348	2025-12-10 09:59:55.797349
60	4	SUV Médio Auto	CSUV AUTO	Nissan Qashqai Auto Gasolina	34.04	34.04	34.04	769	2400	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.798695	2025-12-10 09:59:55.798696
61	4	Familiar Diesel	CD	Ford Focus Diesel	31.63	31.63	31.63	689	2200	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.799856	2025-12-10 09:59:55.799857
62	4	Familiar Diesel+	CD+	Ford Focus STW Diesel	31.63	31.63	31.63	689	2400	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.801244	2025-12-10 09:59:55.801245
63	4	Premium	CDX	Mercedes Classe A Diesel	31.63	31.63	31.63	839	2500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.802423	2025-12-10 09:59:55.802424
64	4	Premium Auto	CDXA	Mercedes Classe A Auto Diesel	36.84	36.84	36.84	899	2700	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.803905	2025-12-10 09:59:55.803906
65	4	Minibus 9L	FD	VW Transporter 9L AC	68.36	68.36	68.36	1390	2800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.805508	2025-12-10 09:59:55.805509
66	4	Minibus 9L Auto	FDA	Ford Transit 9L Auto AC	80.8	80.8	80.8	1590	2800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.807086	2025-12-10 09:59:55.807088
67	4	Middlebus	H	Ford Transit 9L	68.36	68.36	68.36	1390	2800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.808496	2025-12-10 09:59:55.808498
68	4	Monovolume 7L	G	Dacia Jogger 7L Gasolina	41.27	41.27	41.27	899	2300	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.809778	2025-12-10 09:59:55.809779
69	4	Monovolume 7L Auto	G Auto	Citroen G.C4 7L Diesel	54.62	54.62	54.62	1149	2800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.811031	2025-12-10 09:59:55.811033
70	4	4x4	T	Mitsubishi L200 Diesel	48.98	48.98	48.98	1299	2800	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.812329	2025-12-10 09:59:55.812331
71	4	Furgão Pequeno	M2	Peugeot Partner Van	38.12	38.12	38.12	569	1500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.813784	2025-12-10 09:59:55.813785
72	4	Furgão Médio	M3	Fiat Scudo 3L	49.69	49.69	49.69	829	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.81498	2025-12-10 09:59:55.814982
73	4	Furgão Grande	M4	Ford Transit 3L	68.01	68.01	68.01	969	2600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.816356	2025-12-10 09:59:55.816358
74	5	Citadino	C	Renault Clio Manual Gasolina	25.7	26.91	24.55	462.21	1200	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.818886	2025-12-10 09:59:55.818887
75	5	Citadino Auto	H	Peugeot 208 Auto Gasolina	27.78	29.09	26.53	503.61	1200	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.820189	2025-12-10 09:59:55.82019
76	5	Compacto	E	Peugeot 308 Manual Gasolina	34.71	36.37	33.13	568	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.821409	2025-12-10 09:59:55.821411
77	5	Compacto Auto	IS	Peugeot 308 Auto Híbrido	41.13	43.11	39.24	777.48	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.822725	2025-12-10 09:59:55.822726
78	5	Familiar	F	Ford Focus SW Manual Gasolina	38.21	40.05	36.46	618	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.824001	2025-12-10 09:59:55.824002
79	5	SUV Pequeno	EF	Renault Captur Manual Gasolina	30.2	31.64	28.84	535	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.825475	2025-12-10 09:59:55.825476
80	5	SUV Pequeno Auto	HEFD	Nissan Juke Auto Gasolina	39.19	43.2	35.18	784.82	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.826866	2025-12-10 09:59:55.826867
81	5	SUV Médio	FQ1	Nissan Qashqai Manual Gasolina	45.3	47.49	43.22	702.71	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.828231	2025-12-10 09:59:55.828233
82	5	SUV Médio	FQ	Peugeot 3008 Manual Diesel	48.48	51.3	45	880.85	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.82938	2025-12-10 09:59:55.829382
83	5	SUV Médio Auto	I1	Nissan Qashqai Auto Híbrido	49.95	52.37	47.64	893.97	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.830854	2025-12-10 09:59:55.830855
84	5	Premium	HEM	BMW 116d Auto Diesel	51.73	54.25	49.34	926.06	2300	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.832242	2025-12-10 09:59:55.832243
85	5	Premium Familiar	T	Mercedes C300d Station Auto Diesel	61.57	64.57	58.71	1629	3500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.833524	2025-12-10 09:59:55.833525
86	5	Premium	HFI	VW Arteon Shooting Brake Auto Diesel	71.62	79.95	69.54	1333	2500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.834843	2025-12-10 09:59:55.834845
87	5	Premium SUV	HFP1	Volvo XC40 Auto Gasolina	71.62	79.95	69.54	1233.96	3000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.83632	2025-12-10 09:59:55.836321
88	5	Premium Sedan	N	Mercedes C 300 Auto Diesel	88.93	101.91	77.66	2097.81	3500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.83817	2025-12-10 09:59:55.838172
89	5	Premium SUV	S	Mercedes GLA Auto Diesel	85.34	92.63	74.4	2003.36	3500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.83963	2025-12-10 09:59:55.839632
90	5	Premium SUV	HN	Audi Q5 Auto Híbrido	117.78	131.99	113.77	2669.52	4000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.841167	2025-12-10 09:59:55.841168
91	5	Premium SUV	HM	Mercedes GLC Coupé Auto Híbrido	123.59	138.52	119.38	2738.35	4500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.8425	2025-12-10 09:59:55.842502
92	5	Monovolume	FJ	Dacia Jogger 7L Manual Diesel/Gasolina	82.57	86.63	78.71	1203.21	2000	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.844009	2025-12-10 09:59:55.844011
93	5	Monovolume Auto	HJ	VW Multivan Auto Diesel/Gasolina	84.91	89.97	79.65	1220.32	2500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.845175	2025-12-10 09:59:55.845176
94	5	Mini Van	G	Renault Trafic Auto Diesel	77.49	81.3	73.87	2297.62	2300	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.846385	2025-12-10 09:59:55.846386
95	5	Mini Van Premium	HG	Mercedes Class V Auto Diesel	83.02	94	82.12	2409.14	3500	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.84783	2025-12-10 09:59:55.847831
96	5	Elétrico Económico	EHC	Citroen e-C3 Auto Elétrico	25.85	27.07	24.7	471	1200	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.849175	2025-12-10 09:59:55.849177
97	5	Elétrico SUV	EHEF	Fiat 600e Auto Elétrico	32.8	34.36	31.31	550	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.850426	2025-12-10 09:59:55.850427
98	5	Elétrico Compacto	EHE	Opel Astra Auto Elétrico	35.43	37.12	33.81	640.88	1600	\N	\N	km ilimitados, s/IVA	1	2025-12-10 09:59:55.851823	2025-12-10 09:59:55.851825
99	5	Comercial	2	Peugeot Partner 3m³ Manual Diesel	25.3	26.5	24.18	454.86	1350	\N	\N	+0.15€/km extra, s/IVA	1	2025-12-10 09:59:55.853318	2025-12-10 09:59:55.853319
100	5	Comercial	2L	Citroen Berlingo Van XL 4m³ Manual Diesel	26.98	28.26	25.78	536.57	1350	\N	\N	+0.15€/km extra, s/IVA	1	2025-12-10 09:59:55.854541	2025-12-10 09:59:55.854543
101	5	Comercial	3	Fiat Scudo 6m³ Manual Diesel	46.13	48.36	44.01	882.2	2000	\N	\N	+0.15€/km extra, s/IVA	1	2025-12-10 09:59:55.856053	2025-12-10 09:59:55.856054
102	5	Comercial	4	Renault Master L3H3 14m³ Manual Diesel	56.64	59.4	54.02	1037.41	3000	\N	\N	+0.15€/km extra, s/IVA	1	2025-12-10 09:59:55.857309	2025-12-10 09:59:55.857311
\.


--
-- Name: partners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: irwt
--

SELECT pg_catalog.setval('public.partners_id_seq', 5, true);


--
-- Name: vehicles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: irwt
--

SELECT pg_catalog.setval('public.vehicles_id_seq', 102, true);


--
-- Name: partners partners_name_key; Type: CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_name_key UNIQUE (name);


--
-- Name: partners partners_pkey; Type: CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_pkey PRIMARY KEY (id);


--
-- Name: processed_emails processed_emails_pkey; Type: CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.processed_emails
    ADD CONSTRAINT processed_emails_pkey PRIMARY KEY (email_id);


--
-- Name: rental_requests rental_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.rental_requests
    ADD CONSTRAINT rental_requests_pkey PRIMARY KEY (id);


--
-- Name: vehicles vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_pkey PRIMARY KEY (id);


--
-- Name: vehicles vehicles_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: irwt
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- PostgreSQL database dump complete
--

\unrestrict KQaboDCVau5N5T5MMddPuQcdplJJ9pdWbtuoVKjr5DWmhTN3xd8Kh2O4FaZOCha

