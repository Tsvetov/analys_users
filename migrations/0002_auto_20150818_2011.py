# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analys_users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
                CREATE OR REPLACE FUNCTION add_ip_user() RETURNS
                TRIGGER AS $$
                DECLARE
                    ip_new varchar(30);
                    ip_new_tmp varchar(30) ARRAY;
                    ar_sub_network varchar(30) ARRAY;
                    ip_new_tmp_2 varchar(30) ARRAY;
                BEGIN
                    ip_new_tmp = string_to_array(text(NEW.ip_address), '.');

                    ip_new_tmp_2 = string_to_array(ip_new_tmp[4], '/');

                    ip_new = array_to_string(ip_new_tmp[0:3], '.') || '.' || ip_new_tmp_2[1];

                    IF (SELECT count(*) FROM analys_users_userip WHERE user_id = NEW.user_id) > 0 THEN
                        ar_sub_network = (SELECT ips FROM analys_users_userip WHERE user_id = NEW.user_id);
                        IF ip_new <> ALL (ar_sub_network)  THEN
                            UPDATE analys_users_userip SET ips=array_append(ar_sub_network, ip_new) where user_id = NEW.user_id;
                        END IF;
                        RETURN NEW;
                    ELSE
                        INSERT INTO analys_users_userip(user_id, ips) values (NEW.user_id,array[ip_new]);
                        RETURN NEW;
                    END IF;
                END;
                $$ LANGUAGE plpgsql;
            """
        ),
        migrations.RunSQL(
            '''
                CREATE TRIGGER t_user
                AFTER INSERT ON
                analys_users_iptable FOR EACH ROW EXECUTE PROCEDURE add_ip_user();
            '''
        ),
        migrations.RunSQL(
            '''
                CREATE INDEX analys_users_userip_user_id_idx
                ON analys_users_userip
                USING hash
                (user_id);
            '''
        )
    ]
