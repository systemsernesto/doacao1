-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS doacoes_db;
USE doacoes_db;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de instituições
CREATE TABLE instituicoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    url_doacao VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo
INSERT INTO usuarios (nome, endereco, telefone, email, cpf, senha) VALUES
('Carlos Silva', 'Rua A, 100', '(11) 99999-1111', '123.456.789-00', 'senha123'),
('Maria Oliveira', 'Av. B, 200', '(11) 99999-2222', 'maria@email.com', '987.654.321-00', 'senha123'),
('Pedro Santos', 'Rua C, 300', '(11) 99999-3333', 'pedro@email.com', '456.789.123-00', 'senha123'),
('Ana Costa', 'Av. D, 400', '(11) 99999-4444', 'ana@email.com', '321.654.987-00', 'senha123');

INSERT INTO instituicoes (nome, endereco, telefone, url_doacao, cnpj) VALUES
('Criança Feliz', 'Rua X, 50', '(11) 3333-1111', 'https://instituicao1.com', '12.345.678/0001-01'),
('Casa de Apoio', 'Av. Y, 150', '(11) 3333-2222', 'https://instituicao2.com', '98.765.432/0001-02'),
('Lar dos Idosos', 'Rua Z, 250', '(11) 3333-3333', 'https://instituicao3.com', '45.678.912/0001-03'),
('Escola Comunitária', 'Av. W, 350', '(11) 3333-4444', 'https://instituicao4.com', '32.165.987/0001-04');