import cx_Oracle as ora


user = ''
pas  = ''
db   = ''
rep_date = '01.09.2020'
nrd_date = '01.09.2020'
nrd_notice = '5654645'
ref_kd = '5645464'
list_type = 'OWNL'
sec_isin_list = 'RU0009029540'
storage_list = 'NRDTR'
if_nominal = 82
part = 5
out_path = 'C:/Temp/oracle/'

sql_text = '''
declare
 i_rep_date date := to_date(:rep_date, 'dd.mm.yyyy');
 i_nrd_date date := to_date(:nrd_date, 'dd.mm.yyyy');
 i_nrd varchar2(265) := :nrd_notice;
 i_ref_kd varchar2(265) := :ref_kd;
 i_list_type varchar2(265) := :list_type;
 i_sec_isin_list varchar2(1000) := :sec_isin_list;
 i_storage_list varchar2(1000) := :storage_list;
 i_if_nominal NUMBER := :if_nominal;
 
 
 v_clob CLOB;
 v_inv_doc_num varchar2(100);
 v_dpa_id number;
 i_inq_id number;
 inq_id number;
 i_sec_id number;
 o_err_msg varchar2(1000);
 
    CONST_NDC_PARTY_ID             CONSTANT VARCHAR2(255) := TR_GET.ARTEFACT( i_artefact => 'NDC_PARTY_ID' );

    CONST_ACC_SUB_TYPE_ID_ACD_2    CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'ACC_SUB_TYPE_ID', 'DT_ACD_PAIR' );

    CONST_XXI_ADDR_TYPE_REG        CONSTANT NUMBER(1)     := 0;
    CONST_XXI_ADDR_TYPE_POST       CONSTANT NUMBER(1)     := 1;
    CONST_REZ_TAX_STATUS_CODE      CONSTANT NUMBER(1)     := 1;
    CONST_NOT_REZ_TAX_STATUS_CODE  CONSTANT NUMBER(1)     := 2;
    --CONST_NAT_TAX_TYPE           CONSTANT NUMBER        := 5;
    --CONST_NOT_NAT_TAX_TYPE       CONSTANT NUMBER        := 1;
    --CONST_CAPABLE                CONSTANT NUMBER        := 1;
    --CONST_NOT_CAPABLE            CONSTANT NUMBER        := 3;
    CONST_NATURE_PERSON            CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'NATURE', 'PERSON' );
    CONST_PARTY_TYPE_NATURE        CONSTANT VARCHAR2(4)   := 'INDV';
    CONST_PARTY_TYPE_NOT_NATURE    CONSTANT VARCHAR2(4)   := 'LEGL';
    CONST_LEI                      CONSTANT VARCHAR2(3)   := 'LEI';  -- IXXI-850
    CONST_OGRN                     CONSTANT VARCHAR2(4)   := 'OGRN';

    -->> IXXI-947
    CONST_ADDR_D                   CONSTANT VARCHAR2(10)  := 'д. ';
    CONST_ADDR_KORP                CONSTANT VARCHAR2(10)  := 'корп. ';
    CONST_ADDR_STR                 CONSTANT VARCHAR2(10)  := 'стр. ';
    CONST_ADDR_PD                  CONSTANT VARCHAR2(10)  := 'подъезд. ';
    CONST_ADDR_KV                  CONSTANT VARCHAR2(10)  := 'кв. ';
    CONST_ADDR_OF                  CONSTANT VARCHAR2(10)  := 'оф. ';
    --<< IXXI-947

    CONST_XML_HEADER               CONSTANT VARCHAR2(60)  := '<?xml version="1.0" encoding="windows-1251"?>'||CHR(10);  -- IXXI-953

    CONST_503_OWNER                CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_OWNER        ; -- Счет владельца
    CONST_503_TRADING              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRADING      ; -- Торговый Счет владельца
    CONST_503_NOMINEE              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_NOMINEE      ; -- Cчет номинального держателя
    CONST_503_TRAD_NOMINEE         CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_NOMINEE ; -- Торговый счет номинального держателя
    CONST_503_TRUSTEE              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRUSTEE      ; -- Счет доверительного управляющего
    CONST_503_TRAD_TRUSTEE         CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_TRUSTEE ; -- Торговый счет доверительного управляющего
    CONST_503_EMISSION             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_EMISSION     ; -- Эмиссионный счет
    CONST_503_ISSUER               CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_ISSUER       ; -- Казначейский счет эмитента
    CONST_503_NONE                 CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_NONE         ; -- Счет неустановленных лиц
    CONST_503_DEPOSIT              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOSIT      ; -- Депозитный счет
    CONST_503_FNOMINEE             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_FNOMINEE     ; -- Счет иностранного номинального держателя
    CONST_503_DEPOPROG             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOPROG     ; -- Счет депозитарных программ

    CONST_PICK_LIST_STORAGE        CONSTANT VARCHAR2(50)  := 'PICK_LIST_STORAGE';
    CONST_REFRENCE_KD              CONSTANT VARCHAR2(50)  := 'REFRENCE_KD';
    CONST_DBR                      CONSTANT NUMBER(1)     := 0;
    CONST_ACC_SUBTYPE_ID           CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'ACC_SUB_TYPE_ID', 'DT_ACD_PAIR' );   --IXXI-5526

    --> IXXI-6305
    CONST_DOC_DATE_4EMPTY          CONSTANT VARCHAR2(10)  := '1900-01-01';
    CONST_DOC_NUM_4EMPTY           CONSTANT VARCHAR2(10)  := 'UKWN';
    CONST_CBRF_PARTY_ID            CONSTANT VARCHAR2(255) := TR_GET.ARTEFACT( i_artefact => 'CBRF_PARTY_ID' );
    CONST_BANK_PROP_SWIFT          CONSTANT VARCHAR2(20)  := TR_GET_DICT.PARTY_RECORD
                                                                 ( i_party_id => TR_GET.MASTER_PARTY_ID
                                                                 ).bic_swift;
    CONST_BANK_PROP_B_SWIFT        CONSTANT VARCHAR2(20)  := TR_GET_DICT.PARTY_RECORD
                                                                 ( i_party_id => CONST_NDC_PARTY_ID
                                                                 ).bic_swift;
    CONST_EUR_ID                   CONSTANT VARCHAR2(10)  := to_char( TR_GET_BUFF.FIND_CCY_ID( 'EUR' ) );
    LV_BANK_PROP_RUB_ACC           VARCHAR2(20);
    LV_BANK_PROP_USD_ACC           VARCHAR2(20);
    LV_BANK_PROP_EUR_ACC           VARCHAR2(20);
    --< IXXI-6305

--------------------------------------------------------------------------------
--    Функция, возвращающая дату в формате rrrr-mm-dd
--------------------------------------------------------------------------------
FUNCTION F_GET_FORMATTED_DATE
    ( i_date DATE
    )
RETURN VARCHAR2
IS
BEGIN
    RETURN to_char( i_date, 'rrrr-mm-dd' );

END F_GET_FORMATTED_DATE;

/*
--------------------------------------------------------------------------------
--  Функция, возвращающая порядковый номер выгрузки за день
--------------------------------------------------------------------------------
FUNCTION F_GET_DT_UPLOAD_NUM
RETURN VARCHAR2
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
    v_num INTEGER;
    v_prefix  VARCHAR2(20) := 'RS';

BEGIN
    for i in 1 .. CONST_LOCK_ATTEMPT_COUNT
    loop

        begin
            select num_per_date
              into v_num
              from TR_VALUE_DATE_NUM
             where value_date = trunc( TR_RULE.GET_SYS_DATE )
               and prefix      = v_prefix
               for update nowait;

            exit;

        exception
            when NO_DATA_FOUND
            then
                v_num := 0;

                insert
                  into TR_VALUE_DATE_NUM
                     ( value_date
                     , num_per_date
                     , prefix
                     )
                values
                     ( trunc( TR_RULE.GET_SYS_DATE )
                     , v_num
                     , v_prefix
                     );

            when P_TF_TYPE.RESOURCE_BUSY
            then
                if i < CONST_LOCK_ATTEMPT_COUNT
                then
                    dbms_lock.sleep( CONST_LOCK_PAUSE_SEC );

                else
                    TR_ERROR.SYS_RAISE_ERROR
                        ( 'ДАННЫЕ ЗАНЯТЫ ДРУГИМИ ПОЛЬЗОВАТЕЛЯМИ, ПОВТОРИТЕ ПОПЫТКУ.'
                        ) ;

                end if;

        end;

    end loop;

    v_num := v_num + 1;

    update TR_VALUE_DATE_NUM
       set num_per_date = v_num
     where value_date   = trunc( TR_RULE.GET_SYS_DATE )
       and prefix      = v_prefix;

    COMMIT;

RETURN v_prefix || to_char( TR_RULE.GET_SYS_DATE, 'rrrrmmdd' ) || lpad( v_num, 2, 0 );

EXCEPTION
    WHEN OTHERS
    THEN
        ROLLBACK;

        RAISE;

END F_GET_DT_UPLOAD_NUM; */


--------------------------------------------------------------------------------
--    Функция, возвращающая порядковый номер выгрузки за день
--------------------------------------------------------------------------------
FUNCTION F_GET_DT_UPLOAD_NUM
RETURN   VARCHAR2
IS
    v_num     INTEGER;
    v_prefix  VARCHAR2(255) := 'TR_W_DT_SEC.F_GET_DT_UPLOAD_NUM';  -- IXXI-1159

BEGIN
    v_num := TR_RULE.GET_VALUE_DATE_NUM
                ( i_prefix     => v_prefix
                , i_value_date => trunc( TR_RULE.GET_SYS_DATE )
                ) ;

    RETURN 'RS'|| to_char( TR_RULE.GET_SYS_DATE, 'rrrrmmdd' ) || lpad( v_num, 2, 0 );

END F_GET_DT_UPLOAD_NUM;


--------------------------------------------------------------------------------
--    Функция, возвращающая код ПАРТАД для 503 типа счета
--------------------------------------------------------------------------------
FUNCTION F_GET_PARTAD_CODE
    ( i_account_type VARCHAR2
    )
RETURN VARCHAR2
IS
    v_res VARCHAR2(2) := '';

BEGIN
    if    i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_OWNER
    then
        v_res := '01'; -- Счет владельца

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRADING
    then
        v_res := '01'; -- Торговый Счет владельца

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_NOMINEE
    then
        v_res := '02'; -- Cчет номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_NOMINEE
    then
        v_res := '02'; -- Торговый счет номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRUSTEE
    then
        v_res := '03'; -- Счет доверительного управляющего

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_TRUSTEE
    then
        v_res := '03'; -- Торговый счет доверительного управляющего

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_EMISSION
    then
        v_res := '05'; -- Эмиссионный счет

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_ISSUER
    then
        v_res := '06'; -- Казначейский счет эмитента

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_NONE
    then
        v_res := '07'; -- Счет неустановленных лиц

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOSIT
    then
        v_res := '19'; -- Депозитный счет

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_FNOMINEE
    then
        v_res := '20'; -- Счет иностранного номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOPROG
    then
        v_res := '22'; -- Счет депозитарных программ

    end if;

    RETURN v_res;

END F_GET_PARTAD_CODE;


--------------------------------------------------------------------------------
--    Функция, возвращающая строку адреса
--------------------------------------------------------------------------------
FUNCTION F_GET_ADDRESS_LINE
    ( ir_cus_addr TR_GET_XXI.T_XXI_CUS_ADDR
    )
RETURN VARCHAR2
IS
    v_address       VARCHAR2(210); -- CUS_ADDR.ADDRESS_INLINE%type;
    v_country_name  VARCHAR2(250); -- IXXI-947


    --------------------------------------------------------------------------------
    --  процедура для составления строки адреса из частей
    --------------------------------------------------------------------------------
    PROCEDURE P_ADD_ADDRESS_PART
        ( i_addr_part          VARCHAR2
        , i_part_type          VARCHAR2 := ''
        , io_addr_line  in out VARCHAR2
        )
    IS
    BEGIN
        if i_addr_part is not null
        then
            io_addr_line := io_addr_line
                            || ', '
                            || i_part_type
                            || i_addr_part;

        end if;

        if substr( io_addr_line, 1, 1) = ','
        then
            io_addr_line := substr( io_addr_line, 3, length( io_addr_line ) -2 );

        end if;

    END P_ADD_ADDRESS_PART;


BEGIN

    -->> IXXI-947
    if TR_GET_LOC.IF_GL_XXI
    then
        v_country_name := TR_GET_XXI.GET_COUNTRY_NAME( i_country_id => ir_cus_addr.country );

    else
        v_country_name :='';

    end if;

    P_ADD_ADDRESS_PART
        ( i_addr_part  => v_country_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.reg_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.area
        , io_addr_line => v_address
        );
    --<< IXXI-947

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.city
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.punct_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.infr_name
        , io_addr_line => v_address
        );

    -->> IXXI-947
    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.dom
        , i_part_type  => CONST_ADDR_D
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.korp
        , i_part_type  => CONST_ADDR_KORP
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.stroy
        , i_part_type  => CONST_ADDR_STR
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.porch
        , i_part_type  => CONST_ADDR_PD
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.kv
        , i_part_type  => CONST_ADDR_KV
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.office
        , i_part_type  => CONST_ADDR_OF
        , io_addr_line => v_address
        );
    --<< IXXI-947

    RETURN v_address;

END F_GET_ADDRESS_LINE;


--------------------------------------------------------------------------------
--    Функция, удаляющая последнюю запятую в строке
--------------------------------------------------------------------------------
FUNCTION TRIM_ADDRESS_LINE
    ( i_address_line  VARCHAR2
    )
RETURN  VARCHAR2
IS
BEGIN
    RETURN rtrim( i_address_line, ', ' );
           /*substr
               ( i_address_line
               , 1
               , length ( i_address_line ) - 2
               ) ; */

END TRIM_ADDRESS_LINE;


PROCEDURE CREATE_SHAREHOLDER_LIST
      (i_inq_id  NUMBER
      )
IS

      r_master_party   V_TR_DICT_PARTY%rowtype := TR_GET_DICT.MASTER_PARTY_RECORD;
      r_rep_row        FUND_DB.TR_INQ_REPORT_MRT%rowtype;
      v_row_num        NUMBER := 0;
      v_user_sess_id   NUMBER := TR_ADMIN.GET_FUND_SESSIONID;
      v_ver_rep VARCHAR2(265) := TR_W_MRT.GET_SHOW_VER_2020;
      r_dict_country       V_TR_DICT_COUNTRY%rowtype;  --IXXI-6250
      
BEGIN
     delete FUND_DB.TR_INQ_REPORT_MRT
     where inq_id = i_inq_id;

    for rec
    in ( select SEC.grn                  grn
              , SEC.nrd_code             nrd_code
              , SEC.issuer_id            issuer_id
              , SEC.sec_ccy_id           sec_ccy_id   -- IXXI-6305
              , SEC.sec_type             sec_type     -- IXXI-6864
              , DPA_P.cdpadepo           p_acc_depo
              , PARTY.ref_id             ref_id
              , PARTY.country_id         country_id  --IXXI-6250
              , DPA_P.idpaparty          idpaparty
              , DPA_P.id                 dpa_id
              , DPA_P.idpatype1          idpatype1
              , sum( P_TF_GET_ACC_SHEET.GET_BALANCE_BOOKED
                         ( i_acc_id     => ACC.id
                         , i_value_date => i_rep_date
                         , i_entry_date => i_rep_date -- остатки на вечер, +1 не надо
                         )
                   )                      rest
          from ( select TR_GET_DICT_SEC.GET_EXCH_SEC_CODE
                            ( i_sec_id  => SEC.id
                            , i_exch_id => CONST_NDC_PARTY_ID
                            )                                          nrd_code
                      , SEC.code_registry                              grn
                      , SEC.issuer_id                                  issuer_id
                      , SEC.id                                         id
                      , SEC.face_value_ccy_id                          sec_ccy_id  -- IXXI-6305
                      , SEC.sec_type                                   sec_type    -- IXXI-6864
                   from V_TR_DICT_SEC   SEC
                      , V_TR_INQ_LIST   INQ_SEC
                  where INQ_SEC.inq_id      = i_inq_id
                    and INQ_SEC.list_name   = TR_W_FLT.GET_LOV_MASK_NAME_SEC
                    and SEC.id              = INQ_SEC.id
               ) SEC
               , V_TR_ACC_CAT    ACC
               , V_TR_INQ_LIST   INQ_DPA_A
               , V_TR_DT_DPA     DPA_P
               , V_TR_DICT_PARTY PARTY
           where ACC.sub_type_id     = CONST_ACC_SUBTYPE_ID
             and ACC.pair_dpa_id     = INQ_DPA_A.id
             and INQ_DPA_A.list_name = CONST_PICK_LIST_STORAGE
             and INQ_DPA_A.inq_id    = i_inq_id
             and ACC.asset_id        = SEC.id
             and ACC.dpa_id          = DPA_P.id
             and DPA_P.idpaparty     = PARTY.id
           group
              by SEC.grn
               , SEC.issuer_id
               , SEC.nrd_code
               , SEC.sec_ccy_id     -- IXXI-6305
               , SEC.sec_type       -- IXXI-6864
               , DPA_P.cdpadepo
               , PARTY.ref_id
               , PARTY.country_id   --IXXI-6250
               , DPA_P.idpaparty
               , DPA_P.id
               , DPA_P.idpatype1
           order
              by DPA_P.idpaparty
               , SEC.nrd_code
      )
    loop
        if rec.rest <= 0
        then
            continue;

        end if;

        if not nvl( r_rep_row.col_ab, '0' ) = rec.idpaparty
        then
            r_rep_row := null;

            declare
                r_party            V_TR_DICT_PARTY%rowtype;
                r_docum            V_TR_DICT_PARTY_PERSON_DOCUM%rowtype;
                t_cus_addr_reg     TR_GET_XXI.T_XXI_CUS_ADDR;
                v_ok_sm_reg_name   VARCHAR2(255);
                t_cus_addr_post    TR_GET_XXI.T_XXI_CUS_ADDR;
                v_ok_sm_post_name  VARCHAR2(255);
                v_addr_line        VARCHAR2(500);
                t_cus_ogrn         TR_GET_XXI.T_XXI_CUS;  --IXXI-6680

            begin
                r_party := TR_GET_DICT.PARTY_RECORD
                               ( i_party_id => rec.idpaparty
                               ) ;

                r_rep_row.col_a := rec.ref_id;
                r_rep_row.col_d := r_party.party_name_long;
                r_rep_row.col_i := case r_party.nature
                                   when CONST_NATURE_PERSON
                                   then CONST_PARTY_TYPE_NATURE
                                   else CONST_PARTY_TYPE_NOT_NATURE
                                   end ;
                r_rep_row.col_o := r_party.inn;
                r_rep_row.col_p := to_char( r_party.person_birth_date, 'rrrr-mm-dd' );
                r_rep_row.col_u := r_party.telephone;
                r_rep_row.col_v := case r_party.country_id
                                   when r_master_party.country_id
                                   then CONST_REZ_TAX_STATUS_CODE
                                   else CONST_NOT_REZ_TAX_STATUS_CODE
                                   end;

                --> IXXI-6305
                if r_party.nature = CONST_NATURE_PERSON
                --IXXI-6680 or v_ver_rep      = TR_W_MRT.GET_SHOW_VER_2020
                then
                    r_docum     := TR_GET_DICT.PARTY_PERSON_DOCUM_RECORD
                                       ( i_party_id => rec.idpaparty
                                       ) ;

                    r_rep_row.col_l := r_docum.person_passport_number;
                    r_rep_row.col_m := to_char( r_docum.person_passport_date, 'rrrr-mm-dd' );
                    r_rep_row.col_n := r_docum.person_passport_place;

                else
                    --IXXI-6680
                    if v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                    then
                        t_cus_ogrn := TR_GET_XXI.READ_XXI_CUS( i_xxi_icusnum => rec.ref_id );
                        r_rep_row.col_l := t_cus_ogrn.ccusksiva;
                        r_rep_row.col_m := to_char( t_cus_ogrn.dcusregdate, 'rrrr-mm-dd' );
                        r_rep_row.col_n := t_cus_ogrn.ccusregagency;

                    end if;

                end if;

                if r_party.nature = CONST_NATURE_PERSON
                then
                    --> IXXI-6305
                    if v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                    then
                        if r_party.person_birth_date > trunc(TR_RULE.GET_OPER_DATE)
                        or months_between( TR_RULE.GET_OPER_DATE, r_party.person_birth_date )/12 > 100
                        then
                            r_rep_row.col_p := null;

                        end if;
                        r_rep_row.col_m := nvl( r_rep_row.col_m, CONST_DOC_DATE_4EMPTY );
                        r_rep_row.col_n := nvl( r_rep_row.col_n, CONST_DOC_NUM_4EMPTY );

                    end if;
                    --< IXXI-6305

                    r_rep_row.col_k := r_docum.person_passport_series;

                    if not r_docum.person_doc_type_id is null
                    then
                        r_rep_row.col_j := TR_GET_XXI.GET_PARTAD_DOC_TYPE
                                               ( i_doc_type => r_docum.person_doc_type_id
                                               ) ;

                    end if;

                --> IXXI-6305
                elsif v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                then
                    r_rep_row.col_p := trim(r_party.kpp);
                    r_rep_row.col_j := CONST_OGRN;            --IXXI-6680 r_docum.person_doc_type_id;

                end if;
                --< IXXI-6305

                t_cus_addr_reg   := TR_GET_XXI.GET_CUS_ADDR
                                         ( i_xxi_icusnum => rec.ref_id
                                         , i_addr_type   => CONST_XXI_ADDR_TYPE_REG
                                         ) ;
                v_ok_sm_reg_name  := TR_GET_XXI.GET_COUNTRY_NAME
                                         ( i_country_id => t_cus_addr_reg.country
                                         ) ;

                t_cus_addr_post  := TR_GET_XXI.GET_CUS_ADDR
                                         ( i_xxi_icusnum => rec.ref_id
                                         , i_addr_type   => CONST_XXI_ADDR_TYPE_POST
                                         ) ;
                v_ok_sm_post_name := TR_GET_XXI.GET_COUNTRY_NAME
                                         ( i_country_id => t_cus_addr_post.country
                                         ) ;

                if  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020 --IXXI-6388
                then
                    -->>IXXI-6250
                    r_dict_country   := TR_GET_DICT.COUNTRY_RECORD(i_country_id => rec.country_id);
                    r_rep_row.col_ac := r_dict_country.code_iso;

                    if  --TR_GET_LOC.IF_GL_XXI  --IXXI-6461
                        nvl(t_cus_addr_reg.id_addr,0)=0
                    and v_ok_sm_reg_name is null
                    then
                        /*v_ok_sm_reg_name  := TR_GET_XXI.GET_COUNTRY_NAME          --IXXI-6461
                                                 ( i_country_id => r_rep_row.col_ac
                                                 ) ;*/
                        r_rep_row.col_e := r_rep_row.col_ac;
                    else
                    --<<IXXI-6250
                        r_rep_row.col_e := t_cus_addr_reg.country;

                    end if;
                else
                    r_rep_row.col_e := t_cus_addr_reg.country;

                end if;

                r_rep_row.col_f := t_cus_addr_reg.post_index;
                select TR_W_DT_SEC.TRIM_ADDRESS_LINE
                           (    nvl2(v_ok_sm_reg_name,           v_ok_sm_reg_name                           ||', ' , '')
                             || nvl2(t_cus_addr_reg.reg_name,   t_cus_addr_reg.reg_name                   ||', ' , '')
                             || nvl2(t_cus_addr_reg.area,       t_cus_addr_reg.area                       ||', ' , '')
                             || nvl2(t_cus_addr_reg.city,       t_cus_addr_reg.city                       ||', ' , '')
                             || nvl2(t_cus_addr_reg.punct_name, t_cus_addr_reg.punct_name                 ||', ' , '')
                             || nvl2(t_cus_addr_reg.infr_name,  t_cus_addr_reg.infr_name                  ||', ' , '')
                             || nvl2(t_cus_addr_reg.dom,        CONST_ADDR_D    || t_cus_addr_reg.dom     ||', ' , '')
                             || nvl2(t_cus_addr_reg.korp,       CONST_ADDR_KORP || t_cus_addr_reg.korp    ||', ' , '')
                             || nvl2(t_cus_addr_reg.stroy,      CONST_ADDR_STR  || t_cus_addr_reg.stroy   ||', ' , '')
                             || nvl2(t_cus_addr_reg.porch,      CONST_ADDR_PD   || t_cus_addr_reg.porch   ||', ' , '')
                             || nvl2(t_cus_addr_reg.kv,         CONST_ADDR_KV   || t_cus_addr_reg.kv      ||', ' , '')
                             || nvl2(t_cus_addr_reg.office,     CONST_ADDR_OF   || t_cus_addr_reg.office  ||', ' , '')
                           )
                  into v_addr_line
                  from dual;
                r_rep_row.col_g := substr( v_addr_line, 1  , 255 );
                r_rep_row.col_h := substr( v_addr_line, 256, 255 );

                v_addr_line := null;

                if not t_cus_addr_post.id_addr is null
                then
                    select TR_W_DT_SEC.TRIM_ADDRESS_LINE
                               (    nvl2(v_ok_sm_post_name,          v_ok_sm_post_name                          ||', ' , '')
                                 || nvl2(t_cus_addr_post.reg_name,   t_cus_addr_post.reg_name                   ||', ' , '')
                                 || nvl2(t_cus_addr_post.area,       t_cus_addr_post.area                       ||', ' , '')
                                 || nvl2(t_cus_addr_post.city,       t_cus_addr_post.city                       ||', ' , '')
                                 || nvl2(t_cus_addr_post.punct_name, t_cus_addr_post.punct_name                 ||', ' , '')
                                 || nvl2(t_cus_addr_post.infr_name,  t_cus_addr_post.infr_name                  ||', ' , '')
                                 || nvl2(t_cus_addr_post.dom,        CONST_ADDR_D    || t_cus_addr_post.dom     ||', ' , '')
                                 || nvl2(t_cus_addr_post.korp,       CONST_ADDR_KORP || t_cus_addr_post.korp    ||', ' , '')
                                 || nvl2(t_cus_addr_post.stroy,      CONST_ADDR_STR  || t_cus_addr_post.stroy   ||', ' , '')
                                 || nvl2(t_cus_addr_post.porch,      CONST_ADDR_PD   || t_cus_addr_post.porch   ||', ' , '')
                                 || nvl2(t_cus_addr_post.kv,         CONST_ADDR_KV   || t_cus_addr_post.kv      ||', ' , '')
                                 || nvl2(t_cus_addr_post.office,     CONST_ADDR_OF   || t_cus_addr_post.office  ||', ' , '')
                               )
                      into v_addr_line
                      from dual;

                end if;

                if not v_addr_line is null
                then
                    r_rep_row.col_s := substr( v_addr_line, 1  , 255 );
                    r_rep_row.col_t := substr( v_addr_line, 256, 255 );
                    r_rep_row.col_q := t_cus_addr_post.country;
                    r_rep_row.col_r := t_cus_addr_post.post_index;

                else
                    if v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020    --IXXI-6739
                    then
                        r_rep_row.col_s := null;
                        r_rep_row.col_t := null;
                        r_rep_row.col_q := coalesce( t_cus_addr_reg.country, r_rep_row.col_ac );  --IXXI-6749
                        r_rep_row.col_r := null;

                    else
                        r_rep_row.col_s := r_rep_row.col_g;
                        r_rep_row.col_t := r_rep_row.col_h;
                        r_rep_row.col_q := t_cus_addr_reg.country;
                        r_rep_row.col_r := t_cus_addr_reg.post_index;

                    end if;

                end if;

                /* IXXI-6749
                if  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                and r_rep_row.col_q is null  --IXXI-6474
                then
                    r_rep_row.col_q := r_rep_row.col_ac;

                end if; */

            end;

        end if;

        v_row_num := v_row_num + 1;
        r_rep_row.inq_id     := i_inq_id;
        r_rep_row.session_id := v_user_sess_id;
        r_rep_row.row_num    := v_row_num;
        r_rep_row.col_x      := rec.grn;
        r_rep_row.col_y      := rec.nrd_code;
        r_rep_row.col_z      := rec.rest;
        r_rep_row.col_b      := rec.p_acc_depo;
        r_rep_row.col_c      := case rec.idpatype1
                                when CONST_503_OWNER
                                then '01' -- Счет владельца
                                when CONST_503_TRADING
                                then '01' -- Торговый Счет владельца
                                when CONST_503_NOMINEE
                                then '02' -- Cчет номинального держателя
                                when CONST_503_TRAD_NOMINEE
                                then '02' -- Торговый счет номинального держателя
                                when CONST_503_TRUSTEE
                                then '03' -- Счет доверительного управляющего
                                when CONST_503_TRAD_TRUSTEE
                                then '03' -- Торговый счет доверительного управляющего
                                when CONST_503_EMISSION
                                then '05' -- Эмиссионный счет
                                when CONST_503_ISSUER
                                then '06' -- Казначейский счет эмитента
                                when CONST_503_NONE
                                then '07' -- Счет неустановленных лиц
                                when CONST_503_DEPOSIT
                                then '19' -- Депозитный счет
                                when CONST_503_FNOMINEE
                                then '20' -- Счет иностранного номинального держателя
                                when CONST_503_DEPOPROG
                                then '22' -- Счет депозитарных программ
                                else ''
                                end ;

        r_rep_row.col_aa     := rec.issuer_id ||'_'|| rec.idpaparty || '_' || rec.dpa_id;  -- Для объединения остатков
        r_rep_row.col_ad     := rec.sec_ccy_id;   -- IXXI-6305
        r_rep_row.col_ae     := rec.sec_type;     -- IXXI-6864

        insert
          into FUND_DB.TR_INQ_REPORT_MRT
        values r_rep_row;

    end loop;

    TR_RULE.COMM;

END CREATE_SHAREHOLDER_LIST;

 
begin 
 
 i_inq_id := tr_rule.EXEC_SEQ('INQ');
 
 TR_W_FLT.SET_DATE
            ( i_inq_id => i_inq_id
            , i_label  => 'Дата фиксации'
            , i_value  => i_rep_date
            );
            
 tr_w.SET_VALUE(i_inq_id => i_inq_id,
                i_item   => TR_W_MRT.GET_REFRENCE_KD,
                i_value  => i_ref_kd);
                
 tr_w.SET_VALUE(i_inq_id => i_inq_id,
                i_item   => TR_W_MRT.GET_NRD,
                i_value  => i_nrd);
                
 tr_w.SET_VALUE(i_inq_id => i_inq_id,
                i_item   => TR_W_MRT.GET_LIST_TYPE,
                i_value  => i_list_type);
                
 tr_w.SET_VALUE(i_inq_id => i_inq_id,
                i_item   => TR_W_MRT.GET_NRD_DATE,
                i_value  => to_char(i_nrd_date));
                
 tr_w.SET_VALUE(i_inq_id => i_inq_id,
                i_item   => 'IF_FACE_VALUE_PAYMENT',
                i_value  => i_if_nominal);
                
 for rec in (
             select regexp_substr (str, '[^,         ]+', 1, level) r
             from ( select i_sec_isin_list str
             from DUAL
             ) VAL
             connect
             by instr(str, ',', 1, level-1) > 0
             )
 
 loop
  
 i_sec_id := tr_get_dict_sec.GET_SEC_4CODE_ISIN(i_code_isin => rec.r, o_msg => o_err_msg).id;
 
 tr_util_inq.SET_LIST_VALUE( i_inq_id        => i_inq_id
                           , i_list_name     => TR_W_FLT.GET_LOV_MASK_NAME_SEC
                           , i_id            => i_sec_id);
                           
 end loop;
 
  for rec in (
             select regexp_substr (str, '[^,         ]+', 1, level) r
             from ( select i_storage_list str
             from DUAL
             ) VAL
             connect
             by instr(str, ',', 1, level-1) > 0
             )
 
 loop
  
  select id    id
   into v_dpa_id       
   from v_tr_dt_dpa
   where cDpaDepo = rec.r;
  
  tr_util_inq.SET_LIST_VALUE( i_inq_id        => i_inq_id
                           , i_list_name     => 'PICK_LIST_STORAGE'
                           , i_id            => v_dpa_id);
  
 end loop;
 
      
 CREATE_SHAREHOLDER_LIST(i_inq_id);

 :i_inq_id := i_inq_id;

 :v_inv_doc_num := F_GET_DT_UPLOAD_NUM;
 
end;
'''


sql_xml = '''
declare
 i_inq_id number;
 parts_cnt number := :parts_cnt;
 mod_ number := :mod;
 inv_doc_num varchar2(100) := :inv_doc_num;
 
 v_clob CLOB;
 v_dpa_id number;
 i_sec_id number;
 o_err_msg varchar2(1000);
 
    CONST_NDC_PARTY_ID             CONSTANT VARCHAR2(255) := TR_GET.ARTEFACT( i_artefact => 'NDC_PARTY_ID' );

    CONST_ACC_SUB_TYPE_ID_ACD_2    CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'ACC_SUB_TYPE_ID', 'DT_ACD_PAIR' );

    CONST_XXI_ADDR_TYPE_REG        CONSTANT NUMBER(1)     := 0;
    CONST_XXI_ADDR_TYPE_POST       CONSTANT NUMBER(1)     := 1;
    CONST_REZ_TAX_STATUS_CODE      CONSTANT NUMBER(1)     := 1;
    CONST_NOT_REZ_TAX_STATUS_CODE  CONSTANT NUMBER(1)     := 2;
    --CONST_NAT_TAX_TYPE           CONSTANT NUMBER        := 5;
    --CONST_NOT_NAT_TAX_TYPE       CONSTANT NUMBER        := 1;
    --CONST_CAPABLE                CONSTANT NUMBER        := 1;
    --CONST_NOT_CAPABLE            CONSTANT NUMBER        := 3;
    CONST_NATURE_PERSON            CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'NATURE', 'PERSON' );
    CONST_PARTY_TYPE_NATURE        CONSTANT VARCHAR2(4)   := 'INDV';
    CONST_PARTY_TYPE_NOT_NATURE    CONSTANT VARCHAR2(4)   := 'LEGL';
    CONST_LEI                      CONSTANT VARCHAR2(3)   := 'LEI';  -- IXXI-850
	CONST_OGRN                     CONSTANT VARCHAR2(4)   := 'OGRN';

    -->> IXXI-947
    CONST_ADDR_D                   CONSTANT VARCHAR2(10)  := 'д. ';
    CONST_ADDR_KORP                CONSTANT VARCHAR2(10)  := 'корп. ';
    CONST_ADDR_STR                 CONSTANT VARCHAR2(10)  := 'стр. ';
    CONST_ADDR_PD                  CONSTANT VARCHAR2(10)  := 'подъезд. ';
    CONST_ADDR_KV                  CONSTANT VARCHAR2(10)  := 'кв. ';
    CONST_ADDR_OF                  CONSTANT VARCHAR2(10)  := 'оф. ';
    --<< IXXI-947

    CONST_XML_HEADER               CONSTANT VARCHAR2(60)  := '<?xml version="1.0" encoding="windows-1251"?>'||CHR(10);  -- IXXI-953

    CONST_503_OWNER                CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_OWNER        ; -- Счет владельца
    CONST_503_TRADING              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRADING      ; -- Торговый Счет владельца
    CONST_503_NOMINEE              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_NOMINEE      ; -- Cчет номинального держателя
    CONST_503_TRAD_NOMINEE         CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_NOMINEE ; -- Торговый счет номинального держателя
    CONST_503_TRUSTEE              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRUSTEE      ; -- Счет доверительного управляющего
    CONST_503_TRAD_TRUSTEE         CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_TRUSTEE ; -- Торговый счет доверительного управляющего
    CONST_503_EMISSION             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_EMISSION     ; -- Эмиссионный счет
    CONST_503_ISSUER               CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_ISSUER       ; -- Казначейский счет эмитента
    CONST_503_NONE                 CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_NONE         ; -- Счет неустановленных лиц
    CONST_503_DEPOSIT              CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOSIT      ; -- Депозитный счет
    CONST_503_FNOMINEE             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_FNOMINEE     ; -- Счет иностранного номинального держателя
    CONST_503_DEPOPROG             CONSTANT NUMBER        := TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOPROG     ; -- Счет депозитарных программ

    CONST_PICK_LIST_STORAGE        CONSTANT VARCHAR2(50)  := 'PICK_LIST_STORAGE';
    CONST_REFRENCE_KD              CONSTANT VARCHAR2(50)  := 'REFRENCE_KD';
    CONST_DBR                      CONSTANT NUMBER(1)     := 0;
    CONST_ACC_SUBTYPE_ID           CONSTANT NUMBER        := TR_MAJOR.GET_ID( 'ACC_SUB_TYPE_ID', 'DT_ACD_PAIR' );   --IXXI-5526

    --> IXXI-6305
    CONST_DOC_DATE_4EMPTY          CONSTANT VARCHAR2(10)  := '1900-01-01';
    CONST_DOC_NUM_4EMPTY           CONSTANT VARCHAR2(10)  := 'UKWN';
    CONST_CBRF_PARTY_ID            CONSTANT VARCHAR2(255) := TR_GET.ARTEFACT( i_artefact => 'CBRF_PARTY_ID' );
    CONST_BANK_PROP_SWIFT          CONSTANT VARCHAR2(20)  := TR_GET_DICT.PARTY_RECORD
                                                                 ( i_party_id => TR_GET.MASTER_PARTY_ID
                                                                 ).bic_swift;
    CONST_BANK_PROP_B_SWIFT        CONSTANT VARCHAR2(20)  := TR_GET_DICT.PARTY_RECORD
                                                                 ( i_party_id => CONST_NDC_PARTY_ID
                                                                 ).bic_swift;
    CONST_EUR_ID                   CONSTANT VARCHAR2(10)  := to_char( TR_GET_BUFF.FIND_CCY_ID( 'EUR' ) );
    LV_BANK_PROP_RUB_ACC           VARCHAR2(20);
    LV_BANK_PROP_USD_ACC           VARCHAR2(20);
    LV_BANK_PROP_EUR_ACC           VARCHAR2(20);
    --< IXXI-6305			 

--------------------------------------------------------------------------------
--    Функция, возвращающая дату в формате rrrr-mm-dd
--------------------------------------------------------------------------------
FUNCTION F_GET_FORMATTED_DATE
    ( i_date DATE
    )
RETURN VARCHAR2
IS
BEGIN
    RETURN to_char( i_date, 'rrrr-mm-dd' );

END F_GET_FORMATTED_DATE;

/*
--------------------------------------------------------------------------------
--  Функция, возвращающая порядковый номер выгрузки за день
--------------------------------------------------------------------------------
FUNCTION F_GET_DT_UPLOAD_NUM
RETURN VARCHAR2
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
    v_num INTEGER;
    v_prefix  VARCHAR2(20) := 'RS';

BEGIN
    for i in 1 .. CONST_LOCK_ATTEMPT_COUNT
    loop

        begin
            select num_per_date
              into v_num
              from TR_VALUE_DATE_NUM
             where value_date = trunc( TR_RULE.GET_SYS_DATE )
               and prefix      = v_prefix
               for update nowait;

            exit;

        exception
            when NO_DATA_FOUND
            then
                v_num := 0;

                insert
                  into TR_VALUE_DATE_NUM
                     ( value_date
                     , num_per_date
                     , prefix
                     )
                values
                     ( trunc( TR_RULE.GET_SYS_DATE )
                     , v_num
                     , v_prefix
                     );

            when P_TF_TYPE.RESOURCE_BUSY
            then
                if i < CONST_LOCK_ATTEMPT_COUNT
                then
                    dbms_lock.sleep( CONST_LOCK_PAUSE_SEC );

                else
                    TR_ERROR.SYS_RAISE_ERROR
                        ( 'ДАННЫЕ ЗАНЯТЫ ДРУГИМИ ПОЛЬЗОВАТЕЛЯМИ, ПОВТОРИТЕ ПОПЫТКУ.'
                        ) ;

                end if;

        end;

    end loop;

    v_num := v_num + 1;

    update TR_VALUE_DATE_NUM
       set num_per_date = v_num
     where value_date   = trunc( TR_RULE.GET_SYS_DATE )
       and prefix      = v_prefix;

    COMMIT;

RETURN v_prefix || to_char( TR_RULE.GET_SYS_DATE, 'rrrrmmdd' ) || lpad( v_num, 2, 0 );

EXCEPTION
    WHEN OTHERS
    THEN
        ROLLBACK;

        RAISE;

END F_GET_DT_UPLOAD_NUM; */


--------------------------------------------------------------------------------
--    Функция, возвращающая порядковый номер выгрузки за день
--------------------------------------------------------------------------------
FUNCTION F_GET_DT_UPLOAD_NUM
RETURN   VARCHAR2
IS
    v_num     INTEGER;
    v_prefix  VARCHAR2(255) := 'TR_W_DT_SEC.F_GET_DT_UPLOAD_NUM';  -- IXXI-1159

BEGIN
    v_num := TR_RULE.GET_VALUE_DATE_NUM
                ( i_prefix     => v_prefix
                , i_value_date => trunc( TR_RULE.GET_SYS_DATE )
                ) ;

    if mod_ = 0
    then
    RETURN 'RS'|| to_char( TR_RULE.GET_SYS_DATE, 'rrrrmmdd' ) || lpad( v_num, 2, 0 );
    else
    RETURN 'RS'|| to_char( TR_RULE.GET_SYS_DATE, 'rrrrmmdd' ) || lpad( v_num, 2, 0 ) || mod_;
    end if;

END F_GET_DT_UPLOAD_NUM;


--------------------------------------------------------------------------------
--    Функция, возвращающая код ПАРТАД для 503 типа счета
--------------------------------------------------------------------------------
FUNCTION F_GET_PARTAD_CODE
    ( i_account_type VARCHAR2
    )
RETURN VARCHAR2
IS
    v_res VARCHAR2(2) := '';

BEGIN
    if    i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_OWNER
    then
        v_res := '01'; -- Счет владельца

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRADING
    then
        v_res := '01'; -- Торговый Счет владельца

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_NOMINEE
    then
        v_res := '02'; -- Cчет номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_NOMINEE
    then
        v_res := '02'; -- Торговый счет номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRUSTEE
    then
        v_res := '03'; -- Счет доверительного управляющего

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_TRAD_TRUSTEE
    then
        v_res := '03'; -- Торговый счет доверительного управляющего

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_EMISSION
    then
        v_res := '05'; -- Эмиссионный счет

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_ISSUER
    then
        v_res := '06'; -- Казначейский счет эмитента

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_NONE
    then
        v_res := '07'; -- Счет неустановленных лиц

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOSIT
    then
        v_res := '19'; -- Депозитный счет

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_FNOMINEE
    then
        v_res := '20'; -- Счет иностранного номинального держателя

    elsif i_account_type = TR_DT_GET_ACC.DPA_P_TYPE_503_DEPOPROG
    then
        v_res := '22'; -- Счет депозитарных программ

    end if;

    RETURN v_res;

END F_GET_PARTAD_CODE;


--------------------------------------------------------------------------------
--    Функция, возвращающая строку адреса
--------------------------------------------------------------------------------
FUNCTION F_GET_ADDRESS_LINE
    ( ir_cus_addr TR_GET_XXI.T_XXI_CUS_ADDR
    )
RETURN VARCHAR2
IS
    v_address       VARCHAR2(210); -- CUS_ADDR.ADDRESS_INLINE%type;
    v_country_name  VARCHAR2(250); -- IXXI-947


    --------------------------------------------------------------------------------
    --  процедура для составления строки адреса из частей
    --------------------------------------------------------------------------------
    PROCEDURE P_ADD_ADDRESS_PART
        ( i_addr_part          VARCHAR2
        , i_part_type          VARCHAR2 := ''
        , io_addr_line  in out VARCHAR2
        )
    IS
    BEGIN
        if i_addr_part is not null
        then
            io_addr_line := io_addr_line
                            || ', '
                            || i_part_type
                            || i_addr_part;

        end if;

        if substr( io_addr_line, 1, 1) = ','
        then
            io_addr_line := substr( io_addr_line, 3, length( io_addr_line ) -2 );

        end if;

    END P_ADD_ADDRESS_PART;


BEGIN

    -->> IXXI-947
    if TR_GET_LOC.IF_GL_XXI
    then
        v_country_name := TR_GET_XXI.GET_COUNTRY_NAME( i_country_id => ir_cus_addr.country );

    else
        v_country_name :='';

    end if;

    P_ADD_ADDRESS_PART
        ( i_addr_part  => v_country_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.reg_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.area
        , io_addr_line => v_address
        );
    --<< IXXI-947

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.city
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.punct_name
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.infr_name
        , io_addr_line => v_address
        );

    -->> IXXI-947
    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.dom
        , i_part_type  => CONST_ADDR_D
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.korp
        , i_part_type  => CONST_ADDR_KORP
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.stroy
        , i_part_type  => CONST_ADDR_STR
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.porch
        , i_part_type  => CONST_ADDR_PD
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.kv
        , i_part_type  => CONST_ADDR_KV
        , io_addr_line => v_address
        );

    P_ADD_ADDRESS_PART
        ( i_addr_part  => ir_cus_addr.office
        , i_part_type  => CONST_ADDR_OF
        , io_addr_line => v_address
        );
    --<< IXXI-947

    RETURN v_address;

END F_GET_ADDRESS_LINE;


--------------------------------------------------------------------------------
--    Функция, удаляющая последнюю запятую в строке
--------------------------------------------------------------------------------
FUNCTION TRIM_ADDRESS_LINE
    ( i_address_line  VARCHAR2
    )
RETURN  VARCHAR2
IS
BEGIN
    RETURN rtrim( i_address_line, ', ' );
           /*substr
               ( i_address_line
               , 1
               , length ( i_address_line ) - 2
               ) ; */

END TRIM_ADDRESS_LINE;


--------------------------------------------------------------------------------
--    Функция, генерирующая XML файл Распоряжения по сбору списка
--    Рефакторинг для генерации XML при помощи нативных механизмов
--------------------------------------------------------------------------------
FUNCTION GET_XML
    ( i_inq_id  NUMBER
    )
RETURN  CLOB
IS
    v_res            CLOB :='';
    v_xml            XMLTYPE;
    v_xml_header     XMLTYPE;
    v_xml_issuer     XMLTYPE;
    v_xml_register   XMLTYPE;
    --> IXXI-6305
    v_xml_bank_prop_rub  XMLTYPE;
    v_xml_bank_prop_usd  XMLTYPE;
    v_xml_bank_prop_eur  XMLTYPE;
    --< IXXI-6305
								   

    v_docnum             VARCHAR2(100);
    v_out_doc_num        VARCHAR2(100);
    v_out_doc_date       VARCHAR2(100);
    v_ndc_ref            VARCHAR2(100);
    v_num                VARCHAR2(100);
    v_inf_indicator      VARCHAR2(100);

    r_issuer         V_TR_DICT_PARTY%rowtype;
    r_master_party   V_TR_DICT_PARTY%rowtype := TR_GET_DICT.MASTER_PARTY_RECORD;
    r_cus_addr_reg   TR_GET_XXI.T_XXI_CUS_ADDR;
    r_cus_addr_post  TR_GET_XXI.T_XXI_CUS_ADDR;
    v_account_type   VARCHAR2(4)   := null;
    v_report_date    DATE          := TR_W_FLT.GET_REPORT_DATE( i_inq_id => i_inq_id );
    v_bank_city      VARCHAR2(100);
    v_country_name   VARCHAR2(255);
    v_type_active    NUMBER        := TR_DT_GET_ACC.TYPE_ACTIVE;
    v_type_passive   NUMBER        := TR_DT_GET_ACC.TYPE_PASSIVE;
    v_ref_kd         VARCHAR2(255) := TR_W.GET_VALUE
                                          ( i_inq_id => i_inq_id
                                          , i_item   => CONST_REFRENCE_KD
                                          ) ;
    --> IXXI-5526
    r_rep_row        FUND_DB.TR_INQ_REPORT_MRT%rowtype;
    v_row_num        NUMBER := 0;
    v_user_sess_id   NUMBER := TR_ADMIN.GET_FUND_SESSIONID;
    --< IXXI-5526
	
	    r_dict_country       V_TR_DICT_COUNTRY%rowtype;  --IXXI-6250
    v_ver_rep            VARCHAR2(20) := TR_W_MRT.GET_SHOW_VER_2020;               --IXXI-6388

    v_if_face_value_payment NUMBER := to_number( TR_W.GET_VALUE( i_inq_id, TR_W_MRT.GET_IF_FACE_VALUE_PAYMENT ) ); --IXXI-6680


    --------------------------------------------------------------------------------
    --    IXXI-6305  Получение кор.счета
    --------------------------------------------------------------------------------
    PROCEDURE LP_GET_CORR_ACC_4CCY
        ( i_ccy                     NUMBER
        , i_party_id                NUMBER
        , i_acc_sub_type_id         NUMBER
        , io_acc             in out VARCHAR2
        )
    IS
        v_acc_id  NUMBER;

    BEGIN
        if io_acc is null
        then
            TR_GET_ACC.GET_ACC_ID_FOR_INST
                ( i_party_id        => i_party_id
                , i_asset_id        => i_ccy
                , i_trn_type_id     => null
                , o_acc_id          => v_acc_id
                , i_acc_type_id     => TR_GET.ACC_NOSTRO
                , i_acc_sub_type_id => i_acc_sub_type_id
                ) ;

            if not v_acc_id is null
            then
                io_acc := TR_GET_ACC.READ_ACC
                              ( i_acc_id => v_acc_id
                              ).party_acc ;

            end if;

        end if;

    END LP_GET_CORR_ACC_4CCY;


BEGIN
    if TR_GET_LOC.IF_GL_XXI
    then
        r_cus_addr_reg := TR_GET_XXI.GET_CUS_ADDR
                              ( i_xxi_icusnum => r_master_party.ref_id
                              , i_addr_type   => CONST_XXI_ADDR_TYPE_REG
                              );

        v_bank_city    := r_cus_addr_reg.city;
        v_country_name := TR_GET_XXI.GET_COUNTRY_NAME( i_country_id => r_cus_addr_reg.country );

    else
        v_bank_city    := '';
        v_country_name := '';

    end if;

    -- header
    if mod_ = 0
    then
    v_num := inv_doc_num;
    else
    v_num := inv_doc_num||mod_;
    end if;
    
    v_out_doc_num   := TR_W.GET_VALUE
                           ( i_inq_id => i_inq_id
                           , i_item   => TR_W_MRT.GET_NRD
                           );
    v_out_doc_date  := F_GET_FORMATTED_DATE
                           ( i_date => TR_W.GET_VALUE
                                           ( i_inq_id => i_inq_id
                                           , i_item   => TR_W_MRT.GET_NRD_DATE
                                           )
                           );
    v_ndc_ref       := TR_W.GET_VALUE
                           ( i_inq_id => i_inq_id
                           , i_item   => TR_W_MRT.GET_REFRENCE_KD
                           );
    v_inf_indicator := TR_W.GET_VALUE
                           ( i_inq_id
                           , TR_W_MRT.GET_LIST_TYPE
                           );
						   
	--v_ver_rep       := TR_W.GET_VALUE( i_inq_id, TR_W_MRT.GET_ITEM_VER_REP ); --IXXI-6388

    --> IXXI-6305 IXXI-6680
    if  v_ver_rep       = TR_W_MRT.GET_SHOW_VER_2020
    and v_inf_indicator = TR_W_MRT.GET_OWNL
    then
        null;

    else
        LP_GET_CORR_ACC_4CCY
            ( i_ccy             => TR_GET.LOCAL_CCY
            , i_party_id        => CONST_CBRF_PARTY_ID
            , i_acc_sub_type_id => TR_GET.ACC_NOSTRO_ADDIT
            , io_acc            => LV_BANK_PROP_RUB_ACC
            );
        select Xmlelement
                   ( "bank_prop_rub"
                   , Xmlelement
                         ( "pay_name"
                         , r_master_party.party_name
                         )
                   , Xmlelement
                         ( "inn"
                         , r_master_party.inn
                         )
                   , Xmlelement
                         ( "cash_rub_dtls"
                         , xmlelement
                               ( "account"
                               , xmlelement
                                     ( "id"
                                     , '00000000000000000000'
                                     )
                               )
                         , xmlelement
                               ( "bank_name"
                               , r_master_party.party_name
                               )
                         , xmlelement
                               ( "bank_city"
                               , v_bank_city
                               )
                         , xmlelement
                               ( "ruic"
                               , r_master_party.bic_local
                               )
                         , xmlelement
                               ( "bank_corr"
                               , xmlelement
                                     ( "id"
                                     , LV_BANK_PROP_RUB_ACC
                                     )
                               )
                         )
                   )
          into v_xml_bank_prop_rub
          from dual;

    end if;

    if  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
    then
        LP_GET_CORR_ACC_4CCY
            ( i_ccy             => TR_GET.BASE_CCY
            , i_party_id        => CONST_NDC_PARTY_ID
            , i_acc_sub_type_id => TR_GET.ACC_NOSTRO_CENTRAL
            , io_acc            => LV_BANK_PROP_USD_ACC
            );
        LP_GET_CORR_ACC_4CCY
            ( i_ccy             => CONST_EUR_ID
            , i_party_id        => CONST_NDC_PARTY_ID
            , i_acc_sub_type_id => TR_GET.ACC_NOSTRO_CENTRAL
            , io_acc            => LV_BANK_PROP_EUR_ACC
            );
        select Xmlelement
                   ( "bank_prop_curr"
                   , Xmlelement
                         ( "ccy_code"
                         , 'USD'
                         )
                   , Xmlelement
                         ( "ow_acc"
                         , LV_BANK_PROP_USD_ACC
                         )
                   , Xmlelement
                         ( "ow_swift"
                         , CONST_BANK_PROP_SWIFT
                         )
                   , Xmlelement
                         ( "ow_b_swift"
                         , CONST_BANK_PROP_B_SWIFT
                         )
                   )
          into v_xml_bank_prop_usd
          from dual;

        select Xmlelement
                   ( "bank_prop_curr"
                   , Xmlelement
                         ( "ccy_code"
                         , 'EUR'
                         )
                   , Xmlelement
                         ( "ow_acc"
                         , LV_BANK_PROP_EUR_ACC
                         )
                   , Xmlelement
                         ( "ow_swift"
                         , CONST_BANK_PROP_SWIFT
                         )
                   , Xmlelement
                         ( "ow_b_swift"
                         , CONST_BANK_PROP_B_SWIFT
                         )
                   )
          into v_xml_bank_prop_eur
          from dual;

    else
        v_xml_bank_prop_usd := v_xml_bank_prop_rub;
        v_xml_bank_prop_eur := v_xml_bank_prop_rub;

    end if;
    --< IXXI-6305 IXXI-6680


    select xmlconcat
               ( xmlelement
                     ( "version"
                     , '3'
                     )
               , xmlelement
                     ( "header"
                     , xmlelement
                           ( "doc_num"
                           , v_num
                           )
                     , xmlelement
                           ( "doc_date"
                           , xmlelement
                                 ( "date"
                                 , to_char( TR_RULE.GET_SYS_DATE, 'rrrr-mm-dd' )
                                 )
                           )
                     , xmlelement
                           ( "link"
                           , xmlelement
                                 ( "out_doc_num"
                                 , v_out_doc_num
                                 )
                           , xmlelement
                                 ( "in_doc_num"
                                 , CONST_DOC_NUM_4EMPTY   -- IXXI-6305
                                 )
                           , xmlelement
                                 ( "out_doc_date"
                                 , xmlelement
                                       ( "date"
                                       , v_out_doc_date
                                       )
                                 )
                           )
                     )
               )
      into v_xml_header
      from dual;


    -- issuer
    select xmlagg
               ( xmlconcat
                     ( xmlelement
                           ( "issuer"
                           , xmlelement
                                 ( "id"
                                 , xmlelement
                                       ( "id"
                                       , nsd_code
                                       )
                                 )
                           , xmlelement
                                 ( "name"
                                 , party_name
                                 )
                           )
                     , xmlelement
                           ( "account_dtls"
                           , xmlelement
                                 ( "account_id"
                                 , xmlelement
                                       ( "id"
                                       , cdpacoderef
                                       )
                                 )
                           )
                     , xmlelement
                           ( "account_holder"
                           , xmlelement
                                 ( "id"
                                 , xmlelement
                                       ( "id"
                                       , cdpadepocode
                                       )
                                 )
                           )
                     , xmlelement
                           ( "corporate_action_code"
                           , 'DSCL'
                           )
                     , xmlelement
                           ( "corporate_action_reference_NDC"
                           , v_ndc_ref
                           )
                     , xmlelement
                           ( "record_date"
                           , to_char( v_report_date, 'rrrr-mm-dd' )
                           )
                     , xmlelement
                           ( "message_function"
                           , case
                           when mod_ = 0
                           then 'NEWM'
                           else 'AMND'
                           end
                           )
                     , xmlelement
                           ( "information_indicator"
                           , v_inf_indicator
                           )
                     )
               )
      into v_xml_issuer
      from ( select distinct
                    P.nsd_code       nsd_code
                  , P.party_name     party_name
                  , DA.cdpacoderef   cdpacoderef
                  , DA.cdpadepocode  cdpadepocode
               from V_TR_ACC_CAT     ACC
                  , V_TR_INQ_LIST    INQ_DPA_A
                  , V_TR_INQ_LIST    INQ_SEC
                  , V_TR_DICT_SEC    S
                  , V_TR_DICT_PARTY  P
                  , V_TR_DT_DPA      DA
              where ACC.sub_type_id     = CONST_ACC_SUB_TYPE_ID_ACD_2
                and ACC.pair_dpa_id     = INQ_DPA_A.id
                and INQ_DPA_A.list_name = CONST_PICK_LIST_STORAGE
                and INQ_DPA_A.inq_id    = i_inq_id
                and ACC.asset_id        = INQ_SEC.id
                and INQ_SEC.inq_id      = i_inq_id
                and INQ_SEC.list_name   = TR_W_FLT.GET_LOV_MASK_NAME_SEC
                and ACC.asset_id        = S.id
                and P.id                = S.issuer_id
                and ACC.pair_dpa_id     = DA.id
           ) ;

    select xmlagg
               ( Xmlelement
                     ( "shareholder"
                     , XMLElement
                           ( "shareholder_id"
                           ,  xmlelement
                              ( "id"
                              , REP.col_a||REP.col_b
                              )
                           )

                     , Xmlelement
                           ( "account_dtls"
                           , XMLELEMENT
                                 ( "account_id"
                                 , xmlelement
                                   ( "id"
                                   , REP.col_b
                                   )
                                 )
                           , XMLELEMENT
                                 ( "account_type"
                                 , REP.col_c
                                 )
                           )
                         , XMLELEMENT
                               ( "shareholder_info"
                               , Xmlelement
                                     ( "shareholder_dtls"
                                     , xmlelement
                                           ( "id"
                                           , xmlelement
                                                 ( "id"
                                                 , REP.col_a
                                                 )
                                           )
                                     , xmlelement
                                           ( "id"
                                           , xmlelement
                                                 ( "id"
                                                 , r_master_party.code_lei
                                                 )
                                           , xmlelement
                                                 ( "issuer"
                                                 , CONST_LEI
                                                 )
                                           )
                                     , xmlelement
                                           ( "name"
                                           , REP.col_d
                                           )
                                     , xmlelement
                                           ( "address"
                                           , xmlelement
                                                 ( "partad"
                                                 , xmlelement
                                                       ( "country"
                                                       , REP.col_e
                                                       )
                                                 ,case  --IXXI-6388
                                                   when   (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020 and REP.col_f is not null)
                                                       or (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019)
                                                   then
                                                        xmlelement
                                                            ( "index"
                                                            , REP.col_f
                                                            )
                                                   else
                                                       null
                                                   end
                                                 ,case  --IXXI-6388
                                                   when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                                                   then
                                                       xmlelement
                                                          ( "address"
                                                          , nvl(REP.col_g||REP.col_h,'-') --IXXI-6250  REP.col_g||REP.col_h  --IXXI-6461  '='
                                                          )
                                                   else
                                                       xmlelement
                                                          ( "address"
                                                          , REP.col_g||REP.col_h
                                                          )
                                                   end
                                                 )
                                           )
                                     , xmlelement
                                           ( "individual_or_entity"
                                           , REP.col_i
                                           )
                                     , --> IXXI-6305
                                       case
                                       when REP.col_i = CONST_PARTY_TYPE_NATURE
                                         or v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                       then
                                           xmlelement
                                               ( "individual_document"
                                               , xmlelement
                                                     ( "doc_type"
                                                     , xmlelement
                                                           ( "individual_document_type_code"
                                                           , REP.col_j
                                                           )
                                                     )
                                               , case --IXXI-6388
                                                 when (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020 and  REP.col_k is not null)
                                                   or (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019)
                                                 then
                                                     xmlelement
                                                         ( "doc_ser"
                                                         , REP.col_k
                                                         )

                                                 else
                                                     null

                                                 end
                                               , xmlelement
                                                     ( "doc_num"
                                                     , REP.col_l
                                                     )
                                               , xmlelement
                                                     ( "doc_date"
                                                     , REP.col_m
                                                     )
                                               , xmlelement
                                                     ( "org"
                                                     , REP.col_n
                                                     )
                                               , case  --IXXI-6388
                                                 when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                                 then
                                                     xmlelement   --IXXI-6250
                                                         ( "place"
                                                         , ''
                                                         )

                                                 end
                                               )
                                       else
                                           xmlelement
                                               ( "entity_reg_dtls"
                                               , xmlelement
                                                     ( "reg_doc_type"
                                                     , xmlelement
                                                           ( "entity_reg_doc_type_code"
                                                           , REP.col_j
                                                           )
                                                     )
                                               , xmlelement
                                                     ( "reg_num"
                                                     , REP.col_l
                                                     )
                                               , xmlelement
                                                     ( "date_of_incorporation"
                                                     , REP.col_m
                                                     )
                                               , xmlelement
                                                     ( "reg_org"
                                                     , REP.col_n
                                                     )
                                               )

                                       end
                                       --< IXXI-6305
                                     )
                               , case  --IXXI-6388
                                 when (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020 and REP.col_o is not null)
                                   or (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019)
                                 then
                                     Xmlelement
                                         ( "inn"
                                         , REP.col_o
                                         )

                                 else
                                     null

                                 end
                               , --> IXXI-6305
                                 case
                                 when REP.col_p is null
                                  and v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                                 then
                                     null

                                 when REP.col_i = CONST_PARTY_TYPE_NATURE
                                   or v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                 then
                                     Xmlelement
                                         ( "birthday"
                                         , REP.col_p
                                         )

                                 else
                                     Xmlelement
                                         ( "kpp"
                                         , REP.col_p
                                         )

                                 end
                                 --< IXXI-6305
                               , --> IXXI-6552
                                 case
                                 when REP.col_i = CONST_PARTY_TYPE_NATURE
                                 then
                                 --< IXXI-6552
                                     case  --IXXI-6388
                                     when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                     then
                                         Xmlelement
                                             ( "nationality"
                                             , REP.col_e
                                             )

                                     else
                                         Xmlelement
                                             ( "nationality"
                                             , REP.col_ac   --REP.col_e  --IXXI-6250
                                             )

                                     end

                                 end
                               , Xmlelement
                                     ( "postal_name"
                                     , Xmlelement
                                           ( "name"
                                           , REP.col_d
                                           )
                                     , Xmlelement
                                           ( "address"
                                           , Xmlelement
                                                 ( "partad"
                                                 , Xmlelement
                                                       ( "country"
                                                       , REP.col_q
                                                       )
                                                 ,case  --IXXI-6388
                                                  when  (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020 and REP.col_r is not null)
                                                     or (v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019)
                                                  then
                                                      Xmlelement
                                                          ( "index"
                                                          , REP.col_r
                                                          )
                                                  else
                                                      null
                                                  end
                                                 ,case  --IXXI-6388
                                                  when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                                                  then
                                                      Xmlelement
                                                         ( "address"
                                                         , nvl(REP.col_s||REP.col_t,'-') --IXXI-6250  REP.col_s||REP.col_t
                                                         )
                                                  else
                                                      Xmlelement
                                                         ( "address"
                                                         , REP.col_s||REP.col_t
                                                         )
                                                  end
                                                 )
                                           )
                                     )
                               )
                         , case
                           when not REP.col_u is null
                           then
                               Xmlelement
                                   ( "shareholder_contacts"
                                   , Xmlelement
                                         ( "phone_or_fax"
                                         , Xmlelement
                                               ( "phone_num"
                                               , REP.col_u
                                               )
													 
															 
												   
												
                                         ,case  --IXXI-6388
                                          when v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                          then
                                              Xmlelement
                                                 ( "phone_type"
                                                 , ''
                                                 )

                                          end
                                         )
                                   ,case  --IXXI-6388
                                    when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                                    then
                                        Xmlelement
                                           ( "e_mail"
                                           , ''
                                           )

                                    end
                                   )

                           else
                               null

                           end
                         , Xmlelement
                               ( "tax_category"
                               , Xmlelement
                                     ( "tax_status_code"
                                     , REP.col_v
                                     )
                               , Xmlelement
                                     ( "tax_exempt_indicator"
                                     , 'No'
                                     )
                               )
                        , --> IXXI-6305
                           --> IXXI-6864
                           case
                           when v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019
                           then
                               case REP.col_ad
                               when to_char( TR_GET.LOCAL_CCY )
                               then
                                   v_xml_bank_prop_rub

                               when to_char( TR_GET.BASE_CCY )
                               then
                                   v_xml_bank_prop_usd

                               when CONST_EUR_ID
                               then
                                   v_xml_bank_prop_eur

                               else
                                   v_xml_bank_prop_rub

                               end

                           when  v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020
                           then
                               case
                               when v_inf_indicator = TR_W_MRT.GET_OWNL
                               then
                                   case
                                   when REP.col_ad    = to_char( TR_GET.BASE_CCY )
                                   and not REP.col_ae = TR_GET_CONST.GC_SEC_TYPE_QUOTA -- 1524
                                   then
                                       v_xml_bank_prop_usd

                                   when REP.col_ad    = CONST_EUR_ID
                                   and not REP.col_ae = TR_GET_CONST.GC_SEC_TYPE_QUOTA -- 1524
                                   then
                                       v_xml_bank_prop_eur

                                   else
                                       null

                                   end

                               when v_inf_indicator = TR_W_MRT.GET_AUTL
                               then
                                   case REP.col_ad
                                   when to_char( TR_GET.LOCAL_CCY )
                                   then
                                       v_xml_bank_prop_rub

                                   when to_char( TR_GET.BASE_CCY )
                                   then
                                       v_xml_bank_prop_usd

                                   when CONST_EUR_ID
                                   then
                                       v_xml_bank_prop_eur

                                   else
                                       v_xml_bank_prop_rub

                                   end

                               end
                               --< IXXI-6864

                           end
                           --< IXXI-6305
                         , case  --IXXI-6388
                           when ( v_ver_rep = TR_W_MRT.GET_SHOW_VER_2020      --IXXI-6680 and v_inf_indicator = TR_W_MRT.GET_OWNL
                                  and v_if_face_value_payment = TR_GET.BOOL_TRUE
                                )
												 
														
													   
													   
																		 
												  
											
                             or ( v_ver_rep = TR_W_MRT.GET_SHOW_VER_2019 )
                           then
                               xmlelement
                                   ( "payment_from_nominee"
                                   , 'Yes'
                                   )

                           else
                               null

                           end
                         , BAL.xml
                         )
                     )
      into v_xml_register
      from FUND_DB.TR_INQ_REPORT_MRT   REP
         , ( select col_aa    -- Для объединения остатков
                  , min ( row_num ) row_num
                  , xmlagg
                        ( xmlelement
                              ( "security_balances"
                              , xmlelement
                                    ( "security_balance" --IXXI-6250 "security_balances"
                                    , xmlelement
                                          ( "security"
                                          , xmlelement
                                                ( "state_reg_num"
                                                , col_x
                                                )
                                          , xmlelement
                                                ( "proprietary_security_code"
                                                , xmlelement
                                                      ( "id"
                                                      , col_y
                                                      )
                                                , xmlelement
                                                      ( "issuer"
                                                      , 'NADC'
                                                      )
                                                )
                                          )
                                    , xmlelement
                                          ( "total"
                                          , xmlelement
                                                ( "units"
                                                , col_z
                                                )
                                          )
                                    )
                              )
                         order by col_x ) as xml
               from FUND_DB.TR_INQ_REPORT_MRT
              where inq_id  = i_inq_id
              and mod(row_num, parts_cnt) = mod_
              group
                 by col_aa    -- Для объединения остатков
           ) BAL
     where REP.inq_id  = i_inq_id
       and REP.row_num = BAL.row_num
       and mod(REP.row_num, parts_cnt) = mod_;
    --< IXXI-5526 isys.darslanov Переделано

    select Xmlelement
               ("register_list"
               , XMLELEMENT
                     ( "register_list_category"
                     , 'ADD'
                     )
               , v_xml_register
               )
    into v_xml_register
    from dual;


    select xmlelement
               ( "REGISTER_OF_SHAREHOLDERS"
               , v_xml_header
               , v_xml_issuer
               , v_xml_register
               )
      into v_xml
      from dual;


    v_res := CONST_XML_HEADER || v_xml.getClobVal();
    v_res := replace (v_res, chr(38)||'quot;', '"');

    RETURN v_res;

END GET_XML;
 
begin 
 
 
 :v_clob := GET_XML(i_inq_id => :i_inq_id);
 
 
end;
'''



def execute(USER, PAS, DB, REPORT_DATE, NRD_DATE, NRD_NOTICE, REF_KD, LIST_TYPE, SEC_ISIN_LIST, STORAGE_LIST, IF_NOMINAL, OUT_PATH, PART):


      global sql_text

      user = USER
      pas = PAS
      db = DB
      rep_date = REPORT_DATE
      nrd_date = NRD_DATE
      nrd_notice = NRD_NOTICE
      ref_kd = REF_KD
      list_type = LIST_TYPE
      sec_isin_list = SEC_ISIN_LIST
      storage_list = STORAGE_LIST
      if_nominal = IF_NOMINAL
      out_path = OUT_PATH
      part = int(PART)

      conn = ora.connect(user, pas, db)

      cur = conn.cursor()

      clob = cur.var(ora.CLOB)
      inq = cur.var(ora.NUMBER)
      inv_doc_num = cur.var(ora.STRING)

      cur.execute(sql_text, {'rep_date':rep_date, 'nrd_date':nrd_date, 'nrd_notice':nrd_notice, 'ref_kd':ref_kd, 'list_type':list_type, 'sec_isin_list':sec_isin_list, 'storage_list':storage_list, 'if_nominal':if_nominal, 'i_inq_id':inq, 'v_inv_doc_num':inv_doc_num})

      for i in range(part):
            print(int(inq.getvalue()))
            a = cur.execute(sql_xml, {'i_inq_id':int(inq.getvalue()), 'inv_doc_num':inv_doc_num.getvalue(), 'v_clob':clob, 'parts_cnt':part, 'mod':i})
            with open(out_path + str(rep_date.replace('.', '')) + '_' + str(ref_kd) + '_' + str(i) + '.xml', 'w') as file:
                  file.writelines(str(clob.getvalue()))

            # a = cur.execute(sql_text, {'rep_date':rep_date, 'nrd_date':nrd_date, 'nrd_notice':nrd_notice, 'ref_kd':ref_kd, 'list_type':list_type, 'sec_isin_list':sec_isin_list, 'storage_list':storage_list, 'v_clob':clob, 'parts_cnt':part, 'mod':0})


# execute(user, pas, db, rep_date, nrd_date, nrd_notice, ref_kd, list_type, sec_isin_list, storage_list, if_nominal, out_path, part)