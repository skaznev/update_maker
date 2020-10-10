declare
 i_rep_date       date := to_date(:v_rep_date,      'dd.mm.yyyy'); -- Дата отчета
 i_payment_date   date := to_date(:v_pay_rep_date,  'dd.mm.yyyy'); -- Дата выплаты
 i_last_rep_date  date := to_date(:v_last_rep_date, 'dd.mm.yyyy'); -- Последний день приема
 i_sec_isin       VARCHAR2(30) := :v_sec_isin;                     -- ISIN ценной бумаги
 i_doc_ref        VARCHAR2(30) := :v_doc_ref;                      -- Номер первичного документа
 i_request_no     VARCHAR2(30) := :v_request_no;                   -- Уникальный ID запроса
 
 v_clob CLOB;
 i_inq_id number;
 
 begin
      i_inq_id := tr_rule.EXEC_SEQ('INQ');
 
      TR_W_FLT.SET_DATE
          ( i_inq_id => i_inq_id
          , i_label  => 'Дата отчета'
          , i_value  => i_rep_date
          ) ;
      TR_W_FLT.SET_DATE
          ( i_inq_id => i_inq_id
          , i_item   => TR_W_REPORT_FATCA_ASSET.GET_CONST_PAYMENT_DATE
          , i_value  => i_payment_date
          ) ;
      TR_W_FLT.SET_DATE
          ( i_inq_id => i_inq_id
          , i_item   => TR_W_REPORT_FATCA_ASSET.GET_CONST_LAST_REP_DATE
          , i_value  => i_last_rep_date
          ) ;  
      TR_W.SET_VALUE  
          ( i_inq_id => i_inq_id
          , i_item   => TR_W_REPORT_FATCA_ASSET.GET_CONST_SEC_ISIN
          , i_value  => i_sec_isin
          ) ; 
      TR_W.SET_VALUE  
          ( i_inq_id => i_inq_id
          , i_item   => TR_W_REPORT_FATCA_ASSET.GET_CONST_DOC_REF
          , i_value  => i_doc_ref
          ) ;
      TR_W.SET_VALUE  
          ( i_inq_id => i_inq_id
          , i_item   => TR_W_REPORT_FATCA_ASSET.GET_CONST_REQUEST_NO
          , i_value  => i_request_no
          ) ;    
  
      :v_clob := TR_W_REPORT_FATCA_ASSET.GET_XML( i_inq_id );
                
 end;
 
