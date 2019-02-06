-- CREATE TABLE ublic.ping_management
CREATE TABLE public.ping_management (
  id bigserial NOT NULL,
  device_token varchar(255) not null,
  uuid varchar(255),
  ping_status text,
  sent_to_web boolean,
  sent_to_phone boolean,
  phone_responded boolean,
  phone_responded_at timestamp null,
  created_at timestamp not null,
  updated_at timestamp not null,
  sent_to_phone_at timestamp null,
  CONSTRAINT ping_management_pkey PRIMARY KEY (id)
);
-- Permissions
ALTER TABLE public.ping_management OWNER TO ping_management_user;
GRANT ALL ON TABLE public.ping_management TO ping_management_user;
