import cx_Oracle as ora


user = 'SAFONOVD'
pas  = 'SAFONOVD_123'
db   = 'XXI'
rep_date = '31.07.2020'
nrd_date = '03.08.2020'
nrd_notice = '42114184'
ref_kd = '515755'
list_type = 'OWNL'
sec_isin_list = 'RU000A1011S9'
storage_list = 'NRDTR'
part = 1
out_path = 'X:/Инверсия/ФОНД/горелова/'

sql_text = '''
declare
 i_rep_date date := to_date(:rep_date, 'dd.mm.yyyy');
 i_nrd_date date := to_date(:nrd_date, 'dd.mm.yyyy');
 i_nrd varchar2(265) := :nrd_notice;
 i_ref_kd varchar2(265) := :ref_kd;
 i_list_type varchar2(265) := :list_type;
 i_sec_isin_list varchar2(1000) := :sec_isin_list;
 i_storage_list varchar2(1000) := :storage_list;
 
 v_clob CLOB;
 i_inq_id number;
 i_sec_id number;
 o_err_msg varchar2(1000);
 v_dpa_id number;
  
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
               i_item   => 'VER_REP',
               i_value  => TR_W_MRT.GET_SHOW_VER_2020);
                
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
 
:v_clob := TR_W_DT_SEC.GET_XML(i_inq_id => i_inq_id);
 
end;
'''


def execute(USER, PAS, DB, REPORT_DATE, NRD_DATE, NRD_NOTICE, REF_KD, LIST_TYPE, SEC_ISIN_LIST, STORAGE_LIST, OUT_PATH, PART):


    global sql_text

    user = USER
    pas = PAS
    db = DB
    rep_date = REPORT_DATE
    nrd_notice = NRD_NOTICE
    ref_kd = REF_KD
    list_type = LIST_TYPE
    sec_isin_list = SEC_ISIN_LIST
    storage_list = STORAGE_LIST
    out_path = OUT_PATH

    conn = ora.connect(user, pas, db)

    cur = conn.cursor()

    clob = cur.var(ora.CLOB)

    cur.execute(sql_text, {'rep_date':rep_date, 'nrd_date':nrd_date, 'nrd_notice':nrd_notice, 'ref_kd':ref_kd, 'list_type':list_type, 'sec_isin_list':sec_isin_list, 'storage_list':storage_list, 'v_clob':clob})

    with open(out_path + str(rep_date.replace('.', '')) + '_' + str(ref_kd) + '.xml', 'w') as file:
                file.writelines(str(clob.getvalue()))
    
    #   for i in range(part):
    #         a = cur.execute(sql_xml, {'i_inq_id':inq.getvalue(), 'v_clob':clob, 'parts_cnt':part, 'mod':i})
            

            # a = cur.execute(sql_text, {'rep_date':rep_date, 'nrd_date':nrd_date, 'nrd_notice':nrd_notice, 'ref_kd':ref_kd, 'list_type':list_type, 'sec_isin_list':sec_isin_list, 'storage_list':storage_list, 'v_clob':clob, 'parts_cnt':part, 'mod':0})


execute(user, pas, db, rep_date, nrd_date, nrd_notice, ref_kd, list_type, sec_isin_list, storage_list, out_path, part)