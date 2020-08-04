-- Дата расчетов|Дата расчетов (dd.mm.yyyy)|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки|Дата поставки
-- $delimiter = "|"
-- $threads = 3
/*Описание скрипта / запроса*/
select /*+ INDEX ( DIL I_DL_CAT_SEC_4TRADEDATETM )*/
       DIL.trade_date              TradeDate
     , DIL.short_ticket            TradeNo
     , ( select case DIL.tran
                when 435        -- TR_GET.MINE
                then 'B'
                when 436        -- TR_GET.YOURS
                then 'S'
                else ''
                end
           from dual
       )                           BuySell
     , DIL.clear_ccy_amount        Amount
     , DIL.clear_ccy_aci           AccInt
     , DIL.clear_value_date        SettleDate
  from V_TR_DEAL_CAT_SEC           DIL
 where nvl( DIL.sub_type, 0 )    = 0
   and not DIL.agr_id4not_nostro = 0
   and $date$			-- DIL.clear_value_date_time or DIL.trade_date_time
       between to_date( :date_from || '09:00:00', 'YYYY.MM.DD HH24:MI:SS' )
           and to_date( :date_to   || '03:00:00', 'YYYY.MM.DD HH24:MI:SS' )
   and DIL.exch_id = 176511             -- select TR_GET.MOEX_PARTY_ID from dual
   and mod(ticket_id, :threads_cnt) = :mod