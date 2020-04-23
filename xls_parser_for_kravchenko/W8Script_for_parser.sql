declare
    v_if_or             NUMBER;
    v_err_msg           VARCHAR2(32000);
    -- ѕодставить значение, строки обрамл€ютс€ в круглые скобки, столбцы раздел€ютс€ ','
    v_in_mess           CLOB := q'[$CLOB$]';
    v_siebel_id         VARCHAR2(50);
    v_counter_party_inn VARCHAR2(12) := '7702165310';
    v_from_date         DATE         := TO_DATE('23.04.2020', 'DD.MM.YYYY');

begin
    for rec_glob
    in  ( select regexp_substr (str, '\(.*?\)', 1, level) r
            from ( select v_in_mess  str
                     from DUAL
                 ) VAL
         connect
              by instr(str, ')(', 1, level-1) > 0

        )
    loop
        for rec
        in ( select trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 1))                    num
                  , trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 2))                    ref_num
                  , regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 3)                          agrnum
                  , trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 4))                    counter_party_inn
                  , to_date(trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 5)), 'dd.mm.rrrr')   from_date
                  , to_date(trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 6)), 'dd.mm.rrrr')   till_date
                  , trim(regexp_substr(substr(r, 2, length(r)-2), '[^,]+', 1, 7))                    sub_type_code
               from ( select to_char(rec_glob.r) r
                        from dual
                    )
           )
        loop
            begin
                select PTY.siebel_id
                  into v_siebel_id
                  from V_TR_DICT_DT_AGR AGR
                  join V_TR_DICT_PARTY  PTY on PTY.id = AGR.party_id
                 where AGR.short_name = rec.agrnum;
             
            exception
                when no_data_found 
                then DBMS_OUTPUT.PUT_LINE
                         ( 'agr_num ='||rec.agrnum
                         ) ;
                    
            end;
             
            TR_API_ESB.ADD_PARTY_PRP_DOC
                ( i_num                =>  nvl(rec.num, 'NULL')
                , i_ref_num            =>  nvl(rec.ref_num, 'NULL')
                , i_siebel_id          =>  v_siebel_id
                , i_counter_party_inn  =>  v_counter_party_inn
                , i_from_date          =>  nvl(rec.from_date, v_from_date)
                , i_till_date          =>  rec.till_date
                , i_sub_type_code      =>  rec.sub_type_code
                , o_if_ok              =>  v_if_or
                , o_err_msg            =>  v_err_msg
                ) ;
            if v_if_or = 0
            then
                DBMS_OUTPUT.PUT_LINE
                    (  'ќшибка при добавлении записи num = "'||rec.num
                    || '": '
                    || v_err_msg
                    ) ;

            end if;
        
        end loop;
        
    end loop;
    ---select * from TR_DICT_PARTY_PROPERTY_DOC where num in ('11-02-16/14600')
    commit;
      
end;