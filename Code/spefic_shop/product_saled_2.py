import requests

cookies = {
    # 'xman_t': 'zl7cPt/8e9K/ttH5IrNo3Tyy7X+zlHEutCGEJliccBW3mGLep3YUsYOPA4X2yJEx6nCWnEmndHCDyn6FqN5ZgSuTtFJJAfRIzfxG5CTD4mpDBi9ydwC2UAuxNRSAcnFUjo11GUj3GcXb5zEToV/PzBFAnhmDin6mSP+DlmYXiCuxcLlNZ//GKRtlFKKPbRyV0MmnHRPwsDbEuD0OxAuZpyvI1hEieq98BbfRSr7NCaJYKpD/HwF11Cuz7Zn8afh68XbsOn/mkMCu+Mf0wCljDK+u+MkB0hzGvv6wXzRQKxXSB7UA8KGNBecJfQqQnq1r5VTnerWLaw3M1I9WpblIuRklQnYuImmYGD4ateEQcSEMUC+sJYTukPbRxPWFVcJ/ouPkxMaDq0KBJhq3sS9SYPvaZxyzgh3FCiozYRPSW7oO2OXTiSB6i5yZT34qt7o8saQ9wdcFZMvgNBkvdO6BdKR25aNL7GP40Dyp8FrECME1GyoQvxGGTKFjbyC4N7l8DjJnIFgMtBxtANmJGBoN8azJ+od6vt7LZHynBliQ44gHwgAwZ9IBJxtondrE177USbRKL/LtJABStAwZpwS7rUIdZkHkC1n3YeYXMij6G4e7XVJYElQBXPExcyGSO6I8ixAVZW/OO2wmMqM/T36IozvNjr+tOuWYpyBH1+2ubXyQxrEw+3yIytWDSgZopwc7FqGSVc4AYqCjwPs1bRyqIeef494A3xD2VEc3QMOx2Kg=',
    # 'xman_f': 'g0GpAoaXwuN9ZXI9/EENdxqKaDyU13/4U7yK//0muYX827b+2M+YLjXwrxdRDHo/2ohA39EyQE9IZazBK68i5S7cBIcdVz4CCyTeXlXqsP9vJgQjcrV28BHgPwcGXA4suoDbQ5wI39vg1kvaRigGz3Mbe9kgSEavJhxrL4UOZTJ31obnpTpVLEKCafdsgnaV5d1x8uhD1Pw3EN/BoRLjpIuPOlT9R2skOQu3S1UrsMhBVjraW7X+E81jrz4PUFalVMnxBAt0BHgaXQtasx8wx2oxgZnfpr2vDvYR7wocH5Zm5pI/d0XL2ggxnEGCZvHU9oRpU4dIYrnfUm4KlpNG5N2I0yTcQjM5kFlqi386sKPfxeWIxwXyqWWSrnnZOnhH',
    # 'ali_apache_track': 'mt=1|ms=|mid=us1896755806rtwae',
    # '_history_login_user_info': '{"userName":"zcw1080","avatar":"","accountNumber":"zcw1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1747375588162}',
    # 'aep_usuc_f': 'site=glo&c_tp=USD&x_alimid=6345377806&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2',
    # 'AB_DATA_TRACK': '112185_8922',
    # 'AB_ALG': 'global_union_ab_exp_4%3D0',
    # 'AB_STG': 'st_SE_1736852788277%23stg_4159',
    # '_m_h5_tk': '2a2214162a22df5a919888cf98cc13ba_1744790206488',
    # '_m_h5_tk_enc': '48dacb96c1026c36b334587b2e1475aa',
    # 'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005006622023518',
    # '_gcl_aw': 'GCL.1744787691.Cj0KCQjwh_i_BhCzARIsANimeoF7e-BzPtGicn3WZSalk9W2wqly7e9o4AoXNDrH_0cIOD3_o13rIDsaAqvVEALw_wcB',
    # 'intl_common_forever': 'DuQo0OynC7sZVICRUldgjD+QmvpFBCHOQN6ZiL0VVWe0edj5scjuRg==',
    # '_gat': '1',
    # 'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=1&x_user=US|zcw1080|user|ifm|6345377806&x_lid=us1896755806rtwae&x_c_chg=1&x_c_synced=1&x_as_i=%7B%22aeuCID%22%3A%22aec92e1dfa5340c6a6fcc600b90ae2d2-1744771883777-09502-UneMJZVf%22%2C%22affiliateKey%22%3A%22UneMJZVf%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cv%22%3A%222%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1744771883777%7D&acs_rt=2ef098c256f247729766232524788f5b',
    # '_ga': 'GA1.1.1995285917.1744706971',
    # '_uetsid': '6db1e7a018d111f0b9c2a54a19f8a7d0',
    # '_uetvid': '44d83b80174f11f095c263faaf25bc18',
    # 'JSESSIONID': '554C57636761EB6D19D09DAF0C556407',
    # 'cto_bundle': 'eUGWal9ZelMlMkZtTUFaJTJCb0xMMUVZRUtTcnM0Qlh5SkEzY3Vzb2tXUGd3RnE2STZNcCUyQjBhTWFXSHFzWmxLaTlPY1ZrVGhoSEZoaElTTDlYcmdZeGIlMkJPWVBDWGRsQmJEMzJJciUyQjlSMXJ3WkpJb1RZMEdvbXV3RjhvVDhlR09WYUVZdE9vb3RyS1NMbEVybWRJdFR6eWJ3MmVaaVNIVzFXVTRoRUtuU0FIR1JUUzRHZUlJJTNE',
    # '_ga_VED1YSGNC7': 'GS1.1.1744787690.5.1.1744787716.34.0.0',
    # 'tfstk': 'g_0qHr_4PEL4HY32I74NYn2fttzYSrvQoVw_sfcgG-2clZ6i4AMoGm__5lbZsfEilrGjURcKe5iboo4oZ5PUsiqGoUfxzv71lKKxsNz_Sp9BReGvMPUMdobQGWeY6b2MNob6KPAuSp9BPWB6EtUihLsxuUlue5PGIiDgr8V_ENjmI-qlEWPTSRDiIuYuMSjcnoqGET28sP2iIPAzrbtEifbzOoAs80GWmnF_0Jc0UNlxzSqVDj2PSN0r4oyhd87GS4PqNi7_aw-_KDebAJDkPZzZZ5kzAmJFuAli9cqr7tAjKYmZI7nJQGyEjjiKyu1Gmbua3k0046bstrFiIloJLwN4l0rEumdOEjDQ3D4x16Jjakozv7ql_i4jAXgTxqYVp8ZL_YrI0p7qKg8VB7V8LVnVIGr0w7yBaQlxXHidwj63zGITqyFzdINfXGE0w7yBaQSOXu28aJObG',
    # 'isg': 'BCIimoYqsYJR4K1fnBx6Xa5Lc6iEcyaNQPeU2Wy7ThVAP8K5VAN2nai5b3vDL54l',
    'epssw': '9*mmC6Dm1ecOxoWtV7dSs2zp0yR3A70Imm3tZ7Glvi3tZRDmmm3ta4dImm4ImriLzfBL54QymVuuKniCbnJzVuuBrSvohdq5z0quLuu7uWVcMMPPE-Ot_3NGXJgnpRM50xVaDN07zu9LLuuRHmriE8oZgafEPYoiHgmRvcKVyefY2byhze-cTdapwSHaH-uVeZZrJj1uRzBu7yuYaimmLn1cV7mmLR3QCXmA6ivYa43StHykzZJv7JHFbVG5x_ERqvAFcc40PNR8Q1Sy0F6EjKaqEM4fJKq4PzbOYMQWnR4qr9z1j.',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.aliexpress.com/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'ali_apache_id=33.102.97.193.174469945229.089285.3; account_v=1; _gcl_au=1.1.1184052794.1744706971; intl_locale=en_US; c_csrf=18f78581-2fe9-49df-b26f-f8b6c17929e9; ali_apache_tracktmp=W_signed=Y; lwrid=AgGWPGWcGQbwHYRnnbqsX39uI4bN; join_status=; lwrtk=AAIEZ/+EXoeNaBW0MpMntDNEXYpZL4vAeVJ2dHdmGWbLsVIedGgZm8U=; lwrtk=AAIEZ/+EXoeNaBW0MpMntDNEXYpZL4vAeVJ2dHdmGWbLsVIedGgZm8U=; _fbp=fb.1.1744771880942.198705984578545244; _gid=GA1.2.187256144.1744771881; _gac_UA-17640202-1=1.1744771881.Cj0KCQjwh_i_BhCzARIsANimeoF7e-BzPtGicn3WZSalk9W2wqly7e9o4AoXNDrH_0cIOD3_o13rIDsaAqvVEALw_wcB; _gcl_gs=2.1.k1$i1744771874$u3375712; traffic_se_co=%7B%22src%22%3A%22Google%22%2C%22timestamp%22%3A1744771883779%7D; _pin_unauth=dWlkPU5tTmhOVGRpTTJZdE5qUXpNUzAwTmpCbExXRmxORFF0T1dSak1EZ3dOamMzTnpVeQ; acs_usuc_t=acs_rt=2ef098c256f247729766232524788f5b&x_csrf=fkn48s1a7l8o; cna=+1x6IL1R0BUCAbeyVerUp2ai; xlly_s=1; re_ri_f_p=uShJeMOleEP2rtlcBc0NPq1XEhDxwVdWgNUC/SiNdng4BBK5e21vF8WccDEbK9ZoW9GWtLIEQWMgN/bGsI1R0zUGDmfWZVUitD335K4BwJY=; x_router_us_f=x_alimid=6345377806; xman_us_t=x_lid=us1896755806rtwae&sign=y&rmb_pp=zcw1080@163.com&x_user=LUJ/Dqkw6H44DbaVgoSNEU7o0kffT5TX0EXZRCwKeZE=&ctoken=1b6gmq_agfi_t&l_source=aliexpress; sgcookie=E100Eb7OTvRYIOOmrHNQLVFvN4RMTS2KonTM2sn5F9g/hku7OY6xn75G5Yk08xAzMftEO5PsmaVvU/SKBMrNe3uD/JG+DKEsrWTwgx/ayxvyOmk=; aep_common_f=4lZHYrsvuMBvKfeSkvc7p7Ch8eO5m1XhxA6pDCxWO6avNCtfuJF2xQ==; xman_t=zl7cPt/8e9K/ttH5IrNo3Tyy7X+zlHEutCGEJliccBW3mGLep3YUsYOPA4X2yJEx6nCWnEmndHCDyn6FqN5ZgSuTtFJJAfRIzfxG5CTD4mpDBi9ydwC2UAuxNRSAcnFUjo11GUj3GcXb5zEToV/PzBFAnhmDin6mSP+DlmYXiCuxcLlNZ//GKRtlFKKPbRyV0MmnHRPwsDbEuD0OxAuZpyvI1hEieq98BbfRSr7NCaJYKpD/HwF11Cuz7Zn8afh68XbsOn/mkMCu+Mf0wCljDK+u+MkB0hzGvv6wXzRQKxXSB7UA8KGNBecJfQqQnq1r5VTnerWLaw3M1I9WpblIuRklQnYuImmYGD4ateEQcSEMUC+sJYTukPbRxPWFVcJ/ouPkxMaDq0KBJhq3sS9SYPvaZxyzgh3FCiozYRPSW7oO2OXTiSB6i5yZT34qt7o8saQ9wdcFZMvgNBkvdO6BdKR25aNL7GP40Dyp8FrECME1GyoQvxGGTKFjbyC4N7l8DjJnIFgMtBxtANmJGBoN8azJ+od6vt7LZHynBliQ44gHwgAwZ9IBJxtondrE177USbRKL/LtJABStAwZpwS7rUIdZkHkC1n3YeYXMij6G4e7XVJYElQBXPExcyGSO6I8ixAVZW/OO2wmMqM/T36IozvNjr+tOuWYpyBH1+2ubXyQxrEw+3yIytWDSgZopwc7FqGSVc4AYqCjwPs1bRyqIeef494A3xD2VEc3QMOx2Kg=; xman_f=g0GpAoaXwuN9ZXI9/EENdxqKaDyU13/4U7yK//0muYX827b+2M+YLjXwrxdRDHo/2ohA39EyQE9IZazBK68i5S7cBIcdVz4CCyTeXlXqsP9vJgQjcrV28BHgPwcGXA4suoDbQ5wI39vg1kvaRigGz3Mbe9kgSEavJhxrL4UOZTJ31obnpTpVLEKCafdsgnaV5d1x8uhD1Pw3EN/BoRLjpIuPOlT9R2skOQu3S1UrsMhBVjraW7X+E81jrz4PUFalVMnxBAt0BHgaXQtasx8wx2oxgZnfpr2vDvYR7wocH5Zm5pI/d0XL2ggxnEGCZvHU9oRpU4dIYrnfUm4KlpNG5N2I0yTcQjM5kFlqi386sKPfxeWIxwXyqWWSrnnZOnhH; ali_apache_track=mt=1|ms=|mid=us1896755806rtwae; _history_login_user_info={"userName":"zcw1080","avatar":"","accountNumber":"zcw1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1747375588162}; aep_usuc_f=site=glo&c_tp=USD&x_alimid=6345377806&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2; AB_DATA_TRACK=112185_8922; AB_ALG=global_union_ab_exp_4%3D0; AB_STG=st_SE_1736852788277%23stg_4159; _m_h5_tk=2a2214162a22df5a919888cf98cc13ba_1744790206488; _m_h5_tk_enc=48dacb96c1026c36b334587b2e1475aa; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005006622023518; _gcl_aw=GCL.1744787691.Cj0KCQjwh_i_BhCzARIsANimeoF7e-BzPtGicn3WZSalk9W2wqly7e9o4AoXNDrH_0cIOD3_o13rIDsaAqvVEALw_wcB; intl_common_forever=DuQo0OynC7sZVICRUldgjD+QmvpFBCHOQN6ZiL0VVWe0edj5scjuRg==; _gat=1; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&x_user=US|zcw1080|user|ifm|6345377806&x_lid=us1896755806rtwae&x_c_chg=1&x_c_synced=1&x_as_i=%7B%22aeuCID%22%3A%22aec92e1dfa5340c6a6fcc600b90ae2d2-1744771883777-09502-UneMJZVf%22%2C%22affiliateKey%22%3A%22UneMJZVf%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cv%22%3A%222%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1744771883777%7D&acs_rt=2ef098c256f247729766232524788f5b; _ga=GA1.1.1995285917.1744706971; _uetsid=6db1e7a018d111f0b9c2a54a19f8a7d0; _uetvid=44d83b80174f11f095c263faaf25bc18; JSESSIONID=554C57636761EB6D19D09DAF0C556407; cto_bundle=eUGWal9ZelMlMkZtTUFaJTJCb0xMMUVZRUtTcnM0Qlh5SkEzY3Vzb2tXUGd3RnE2STZNcCUyQjBhTWFXSHFzWmxLaTlPY1ZrVGhoSEZoaElTTDlYcmdZeGIlMkJPWVBDWGRsQmJEMzJJciUyQjlSMXJ3WkpJb1RZMEdvbXV3RjhvVDhlR09WYUVZdE9vb3RyS1NMbEVybWRJdFR6eWJ3MmVaaVNIVzFXVTRoRUtuU0FIR1JUUzRHZUlJJTNE; _ga_VED1YSGNC7=GS1.1.1744787690.5.1.1744787716.34.0.0; tfstk=g_0qHr_4PEL4HY32I74NYn2fttzYSrvQoVw_sfcgG-2clZ6i4AMoGm__5lbZsfEilrGjURcKe5iboo4oZ5PUsiqGoUfxzv71lKKxsNz_Sp9BReGvMPUMdobQGWeY6b2MNob6KPAuSp9BPWB6EtUihLsxuUlue5PGIiDgr8V_ENjmI-qlEWPTSRDiIuYuMSjcnoqGET28sP2iIPAzrbtEifbzOoAs80GWmnF_0Jc0UNlxzSqVDj2PSN0r4oyhd87GS4PqNi7_aw-_KDebAJDkPZzZZ5kzAmJFuAli9cqr7tAjKYmZI7nJQGyEjjiKyu1Gmbua3k0046bstrFiIloJLwN4l0rEumdOEjDQ3D4x16Jjakozv7ql_i4jAXgTxqYVp8ZL_YrI0p7qKg8VB7V8LVnVIGr0w7yBaQlxXHidwj63zGITqyFzdINfXGE0w7yBaQSOXu28aJObG; isg=BCIimoYqsYJR4K1fnBx6Xa5Lc6iEcyaNQPeU2Wy7ThVAP8K5VAN2nai5b3vDL54l; epssw=9*mmC6Dm1ecOxoWtV7dSs2zp0yR3A70Imm3tZ7Glvi3tZRDmmm3ta4dImm4ImriLzfBL54QymVuuKniCbnJzVuuBrSvohdq5z0quLuu7uWVcMMPPE-Ot_3NGXJgnpRM50xVaDN07zu9LLuuRHmriE8oZgafEPYoiHgmRvcKVyefY2byhze-cTdapwSHaH-uVeZZrJj1uRzBu7yuYaimmLn1cV7mmLR3QCXmA6ivYa43StHykzZJv7JHFbVG5x_ERqvAFcc40PNR8Q1Sy0F6EjKaqEM4fJKq4PzbOYMQWnR4qr9z1j.',
}

params = {
    'componentKey': 'allitems_choice',
    # 'deviceId': ' 1x6IL1R0BUCAbeyVerUp2ai',
    'SortType': 'bestmatch_sort',
    'page': '1',
    'pageSize': '30',
    'country': 'US',
    'site': 'glo',
    'sellerId': '2673483062',
    'groupId': '-1',
    'currency': 'USD',
    'locale': 'en_US',
    # 'buyerId': '6345377806',
    'callback': 'jsonp_1744787719354_46679',
}

response = requests.get('https://shoprenderview.aliexpress.com/async/execute', params=params, cookies=cookies, headers=headers)
print(response.text)