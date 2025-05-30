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
