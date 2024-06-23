-- auto-generated definition
create table option_data
(
    id          bigserial
        constraint option_data_pk
            primary key,
    code        varchar,
    name        varchar,
    create_time timestamp not null,
    update_time timestamp
);

alter table option_data
    owner to postgres;

-- auto-generated definition
create table processed_codes
(
    id          bigserial
        primary key,
    code        varchar(255) not null
        unique,
    create_time timestamp    not null,
    update_time timestamp
);

alter table processed_codes
    owner to postgres;

