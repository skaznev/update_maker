-- ID ������ ��� �������|���� ������|�����������
-- $delimiter = |
-- $threads = 1

begin
  tr_api.EXEC(   id      => $P1
                ,dates   => $P2
                ,strs    => $P3
            );
  commit;
  end;