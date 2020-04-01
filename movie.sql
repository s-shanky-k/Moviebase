CREATE DATABASE movie;

CREATE TABLE users(
    u_name VARCHAR(25) NOT NULL,
    u_email VARCHAR(30) NOT NULL,
    u_pass_word VARCHAR(20) NOT NULL,
    PRIMARY KEY(u_email)
);

CREATE Table liked(
    u_email VARCHAR(30) NOT NULL,
    m_id VARCHAR(20) NOT NULL,
    m_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (u_email,m_id),
    foreign key (u_email) references users(u_email)
    );