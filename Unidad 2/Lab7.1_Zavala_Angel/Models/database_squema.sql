CREATE TABLE "Database_OOP".users (
	id_user int NOT NULL,
	username varchar NOT NULL,
	passw varchar NOT NULL,
	nombre varchar NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id_user)
);

insert into "Database_OOP".users (id_user, username, passw, nombre) values (1, 'admin', 'admin!123', 'Super admin')

CREATE TABLE "Database_OOP".products (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);

INSERT INTO "Database_OOP".products (nombre, precio, stock) VALUES
('Galletas', 22.00, 50),
('Refresco 600ml', 18.50, 120),
('Sabritas', 20.00, 80),
('Agua 1L', 12.00, 200),
('Chocolate', 15.50, 60);