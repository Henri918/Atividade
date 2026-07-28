CREATE DATABASE login;
USE login;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    quantidade INT DEFAULT 0,
    quantidade_estoque INT DEFAULT 0,
    estoque_minimo INT DEFAULT 0,
    preco DECIMAL(10,2) DEFAULT 0,
    foto2 VARCHAR(255),
	data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    produto VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    quantidade INT NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuario (email, senha, tipo)
VALUES
('admin@gmail.com', '$2a$12$AGf2YfT.1rWADLQwwif1KOtLmsT5svgOG2bKzVg6KAiH7QJGlbcXK', 'admin');

INSERT INTO usuario (email, senha, tipo)
VALUES
('user@gmail.com', '$2a$12$AGf2YfT.1rWADLQwwif1KOtLmsT5svgOG2bKzVg6KAiH7QJGlbcXK', 'usuario');