DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ordering'
   ) THEN
      CREATE ROLE ordering WITH LOGIN PASSWORD 'fastfoodpwd';
   END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE ordering TO ordering;

CREATE SEQUENCE IF NOT EXISTS "ordering".public.order_number_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
