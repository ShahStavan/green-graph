from yahoo_fin import stock_info as si

balancesheet = si.get_balance_sheet("TATASTEEL" + ".NS")
# balancesheet = balancesheet.to_json()
balancesheet = dict(balancesheet)
cashflow = si.get_cash_flow("TATASTEEL" + ".NS")
balance = {}
for i in balancesheet.keys():
    balance[i.date()] = dict(balancesheet[i])
    # print(dict(balancesheet[i]))

for i in cashflow:
    print(i)
    print(cashflow[i])



"""
<!-- <table class="ui purple striped table">
                                    <thead>
                                        <td></td>
                                        {% for i in balancesheet.columns %}
                                            <th>{{ i }}</th>
                                        {% endfor %}
                                    </thead>
                                    {% for i in balancesheet.index %}
                                        <tr>
                                           <th >{{ i }}</th>
                                           87
                                        </tr>
                                        
                                        
                                    {% endfor %}
                                    
                                </table> -->
"""