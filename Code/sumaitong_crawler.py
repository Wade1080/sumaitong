import requests

cookies = {
    'c_csrf': '82e6f37f-7ae6-435c-9664-44226f5f3298',
    'ali_apache_id': '33.80.175.4.1744680277495.562307.9',
    'intl_locale': 'en_US',
    'acs_usuc_t': 'acs_rt=5dee352ea2514573aa18d0936486dd26&x_csrf=otgb1q95rocc',
    'cna': '+1x6IL1R0BUCAbeyVerUp2ai',
    '_gcl_au': '1.1.1271925240.1744680280',
    'xlly_s': '1',
    're_ri_f_p': 'WucG63bcRGExM5t4ly83qJCxUWU8H5IS79fVMXvjJHoYCb2LoQzHFkvequssFEoM+9U56sgseiXVhIIhlrAM5D5Sl+q/5wLfe4NX4I4H2+8=',
    'x_router_us_f': 'x_alimid=6340368875',
    'xman_us_t': 'x_lid=us1893585475dqoae&sign=y&rmb_pp=wade1080@163.com&x_user=DSe9EN8qtIdppAT+RPFiJapkHIckt9wVFQiTpvK1Ekk=&ctoken=13y4f8sf7lfgg&l_source=aliexpress',
    'sgcookie': 'E100zLZN3gXRTE2yxzzoQBGurQX5b/ld7uNTK+8ks/QkVWeFEifzsX/fYZZiThZ3SIPBK4L/qeCl/F18c7mWzOwjTl2vXpI9lRqHqbNaSD5Wyps=',
    'aep_common_f': '+uduWZN5HlrVdlxn9olfEwr9E8iHt4PAIASuK9ZSMehAVKQEobutmQ==',
    'xman_t': 'JroXr+n/flJ6vq9mSE7FfjoF/1J1qJbcDIz8L6NuPN1tGfj2BdBDB4uWYaOAlaR6KmiJrl+tgA8SVm9jNvuhUVsIpH3eC6Ml4uMHwVVjYJBD+8XjNijx2iN9t7nUSEwgyhJbgrc+aikxrW/G2NMb0LSPS/2FR68qKrE/7YkWvUnY44vnWqQ+3W+Y+zjKTeZMaqMvmME2Nc20x4hsEG5F/3dEXSNIDJfnWhWBYRmwGUcErDpo0Ipm+0hY6KhI38ttXiH50dJ7xBi0oop7jMSDWVjESKgmh0d6aNxsd+/eLQYytPEQY17n4lflvQoSs00UfF95NNKumUiGYVXLNubgtKr9bkqwSZZiQhXoBh3xO3RE8Xmj8tD7Wo4SeFCHtmE/FopYS+0TZAGjSwiwKIlYOa6MQ2lsPrcNOahT37wmPKjIBKq8Yx2Do9ndpaVnalPtWepm6t3ZFX/eAl282eRLvpT3c5YCSmYVy1gSgWspsqgNCLFuWyOSBtNmHCc6oCtNZqTJ0uoWlKOjqTDkfHJexD1HU/KkhUlAzPZ+0iq0SrDnngKLQQFhORufBxmTrXWQkQCZWq5yvjI/U9qyceTiNVBwg4GFgdYkIHZg88OZTQeS+8qiTnYG1SHlVOLZhrs1kHW/Tnwup9Yvlng6IvW1Bmwo7PGxGqEcA6gw3Gm9eSNuGpSXLcHFRAeB3siFp7lDYMdHfTlqvU0clsUan2Eh0m4bUAzoFVvnLEVTflAWbrk=',
    'xman_f': 'oelBvWuzCV66cCyVDh7C8gl0rm5ry71Q9mFX94b4/xDxyIcFDZ5+QDjyLqdcUBDHyOleI0ZO5uKsHmTC2TRGrGQQt+j9+NU94BdW0/IDhV9uaw/XApWU5mAEFs+DkWkPI74WGUMt3TkRuFuEvnrczL4YstJ7G0w++XoYY0YBPakc2Bgdcb7zH9XGuCHMmg1pV/MpqHfOnX7LYgDdS+HIMl3U+PRN8yLugGSU0ENkWEe001eCreZvrZrP2J8SPAuY0ouANIqVL32NTsSPmwA3ure9Jt2I59yQaQ1t1C1XLVUrzKtzSBtlVDsnFC8KBrAccEDdEuH+qAew6Hd4Rpvu9/Nw4bUuLN64ocJP+1M13x3Y1FxNkNFg+lty8vUCr1YEkDbdPQwwEoY=',
    'ali_apache_track': 'mt=1|ms=|mid=us1893585475dqoae',
    'ali_apache_tracktmp': 'W_signed=Y',
    '_history_login_user_info': '{"userName":"wade1080","avatar":"","accountNumber":"wade1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1747272313853}',
    'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=1&x_user=US|wade1080|user|ifm|6340368875&x_lid=us1893585475dqoae&x_c_chg=1&acs_rt=5dee352ea2514573aa18d0936486dd26',
    'lwrid': 'AgGWNwz0ADPja4jy2fg%2BX39uI4bN',
    'join_status': '',
    '_gid': 'GA1.2.1411312012.1744680320',
    'aep_usuc_f': 'site=glo&c_tp=USD&x_alimid=6340368875&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2',
    '_pin_unauth': 'dWlkPU9ERTBaVGd4TXpVdE1UWXhNaTAwT0RsbUxUZzNNV1l0WkRka05HWmlZMlUxTURrMQ',
    '_fbp': 'fb.1.1744680347870.912429541388440071',
    'AB_DATA_TRACK': '112185_8922',
    'AB_ALG': 'global_union_ab_exp_4%3D0',
    'AB_STG': 'st_SE_1736852788277%23stg_4159',
    'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005005992120720%091005006457230695%091005002409350841%091005008404213300%091005008666798729%091005008722948277',
    'lwrtk': 'AAIEZ/4q18W6Jhdhjc2Q9fRH//Xadte+C6cqfKfLwZ94jwJYRMP6It4=',
    'lwrtk': 'AAIEZ/4q18W6Jhdhjc2Q9fRH//Xadte+C6cqfKfLwZ94jwJYRMP6It4=',
    'account_v': '1',
    'x5sec': '7b22617365727665722d696e746c3b33223a22307c4350325439373847454f6652744930444d4c69386873542b2f2f2f2f2f77453d222c22733b32223a2237396130646338313835366333326538227d',
    '_m_h5_tk': '28142e706bb146f5c5630ee201c2c12f_1744688393813',
    '_m_h5_tk_enc': 'e2dc459a547f4cacef94c6adb166dedc',
    'intl_common_forever': 'NQkmnnyWcxJ6e8lA/kZxk0rEp0v4RahuHduwRY0zdXMiJ5jhfZnI2Q==',
    '_gat': '1',
    'JSESSIONID': '10D93B4276C348BFE5188E56A3DB7308',
    '_ga_VED1YSGNC7': 'GS1.1.1744686321.2.1.1744686545.42.0.0',
    '_ga': 'GA1.1.821064136.1744680280',
    '_uetsid': '6db1e7a018d111f0b9c2a54a19f8a7d0',
    '_uetvid': '44d83b80174f11f095c263faaf25bc18',
    'cto_bundle': 'Hri2xV9ZelMlMkZtTUFaJTJCb0xMMUVZRUtTcnM0QllCNiUyQk1UTGRwejZ6MGdIZjYyZ1g0anVLZVljc3M4THdCMWMlMkZrTDRVZ1E1cVlMdTNCb0lvMXZUcEwlMkZ0MVV3YURuSklQRUN1OVBURmUlMkZ6cEVoOXRkMkRReEQ5Q2VEWU9yUnJVUnQ3eEdWT2JFb21ZJTJGMlpqajJ3Y0ZVQlk0QVZXbGV6NFJmNWEzeXVPNnlCZHBxV2ZGSSUzRA',
    'isg': 'BOnpzyR6quV6iZZQNWIsQnf4-JVDtt3o3yqPFIveZFAPUglk0gRTuHJMFPbkSnUg',
    'tfstk': 'g2ksqeiuGNb_OfbnjFKUVOLXBewbCq9yHiZxqmBNDReOkZn88h2q_hjxDmg5QOovSqMbJmX47S-iRJE4DoBTHSBLvuz3uhDwjr3Iu2e46fzVhxiY8qWqbqSit4oRQARg3twgn-LyzLJyjc20HO3xV-aivDqvYlUH138Un-Ly8uXBJdwmrBP3-fnpAor0kG3Y6MBL-lBTHPFAJ6EYJrexk5EpplqOMlEYkyKQmyUYH-3Ypb_lVoO_SctGqBKWZMEoXy6AHAp06zi1gtBxdlNsHcUI40kQf5a8tsnZ7A3EDAkgtBCQnDlSlj3J81ztNugQafT5C4ggDmZx5Lj7JAijd5cFqTnQGPGKBWsAHcw3k7lj5F1gWfuQZkFdcLqEzyniBXtcJc3z5RELTLKSvShEI7DwJOw-ZcyZM4LF_Ph7DgzRUztHvssQZtZQzHtCisvvxnDExrxNQ5E3fW-BANh06kqQzHtCisVTxlZyAH_ti',
    'epssw': '9*mmCrpm9T-HUEWcvOdQS2zpqiR3AO7tV73tjmGP7bdSZ3CYHiutG4dtvO3t672tmB_mr2M48EABmOYdQZlkT19LetUjAwFDKu0yFr9LmmNfKnMJVzH7zo05UwsXxbwUsB8NqP9B9R5eHGKP9GE5VKVAymmLeUT4R4HmHYNZdXm6FZmbuc3BwaFCpI69sb3Q5DgS8YagrmJNtSW6gsuL57i2zuiwmmmAxVut_mmAz3utGB7QHiHNSf2iTmg8eC3St-3_yeMuLd3chzt7dHqdASRIqqpEXZdKfo8__Kn7zZPV_0_n8DudZvmhByDPcbmm..',
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
    # 'cookie': 'c_csrf=82e6f37f-7ae6-435c-9664-44226f5f3298; ali_apache_id=33.80.175.4.1744680277495.562307.9; intl_locale=en_US; acs_usuc_t=acs_rt=5dee352ea2514573aa18d0936486dd26&x_csrf=otgb1q95rocc; cna=+1x6IL1R0BUCAbeyVerUp2ai; _gcl_au=1.1.1271925240.1744680280; xlly_s=1; re_ri_f_p=WucG63bcRGExM5t4ly83qJCxUWU8H5IS79fVMXvjJHoYCb2LoQzHFkvequssFEoM+9U56sgseiXVhIIhlrAM5D5Sl+q/5wLfe4NX4I4H2+8=; x_router_us_f=x_alimid=6340368875; xman_us_t=x_lid=us1893585475dqoae&sign=y&rmb_pp=wade1080@163.com&x_user=DSe9EN8qtIdppAT+RPFiJapkHIckt9wVFQiTpvK1Ekk=&ctoken=13y4f8sf7lfgg&l_source=aliexpress; sgcookie=E100zLZN3gXRTE2yxzzoQBGurQX5b/ld7uNTK+8ks/QkVWeFEifzsX/fYZZiThZ3SIPBK4L/qeCl/F18c7mWzOwjTl2vXpI9lRqHqbNaSD5Wyps=; aep_common_f=+uduWZN5HlrVdlxn9olfEwr9E8iHt4PAIASuK9ZSMehAVKQEobutmQ==; xman_t=JroXr+n/flJ6vq9mSE7FfjoF/1J1qJbcDIz8L6NuPN1tGfj2BdBDB4uWYaOAlaR6KmiJrl+tgA8SVm9jNvuhUVsIpH3eC6Ml4uMHwVVjYJBD+8XjNijx2iN9t7nUSEwgyhJbgrc+aikxrW/G2NMb0LSPS/2FR68qKrE/7YkWvUnY44vnWqQ+3W+Y+zjKTeZMaqMvmME2Nc20x4hsEG5F/3dEXSNIDJfnWhWBYRmwGUcErDpo0Ipm+0hY6KhI38ttXiH50dJ7xBi0oop7jMSDWVjESKgmh0d6aNxsd+/eLQYytPEQY17n4lflvQoSs00UfF95NNKumUiGYVXLNubgtKr9bkqwSZZiQhXoBh3xO3RE8Xmj8tD7Wo4SeFCHtmE/FopYS+0TZAGjSwiwKIlYOa6MQ2lsPrcNOahT37wmPKjIBKq8Yx2Do9ndpaVnalPtWepm6t3ZFX/eAl282eRLvpT3c5YCSmYVy1gSgWspsqgNCLFuWyOSBtNmHCc6oCtNZqTJ0uoWlKOjqTDkfHJexD1HU/KkhUlAzPZ+0iq0SrDnngKLQQFhORufBxmTrXWQkQCZWq5yvjI/U9qyceTiNVBwg4GFgdYkIHZg88OZTQeS+8qiTnYG1SHlVOLZhrs1kHW/Tnwup9Yvlng6IvW1Bmwo7PGxGqEcA6gw3Gm9eSNuGpSXLcHFRAeB3siFp7lDYMdHfTlqvU0clsUan2Eh0m4bUAzoFVvnLEVTflAWbrk=; xman_f=oelBvWuzCV66cCyVDh7C8gl0rm5ry71Q9mFX94b4/xDxyIcFDZ5+QDjyLqdcUBDHyOleI0ZO5uKsHmTC2TRGrGQQt+j9+NU94BdW0/IDhV9uaw/XApWU5mAEFs+DkWkPI74WGUMt3TkRuFuEvnrczL4YstJ7G0w++XoYY0YBPakc2Bgdcb7zH9XGuCHMmg1pV/MpqHfOnX7LYgDdS+HIMl3U+PRN8yLugGSU0ENkWEe001eCreZvrZrP2J8SPAuY0ouANIqVL32NTsSPmwA3ure9Jt2I59yQaQ1t1C1XLVUrzKtzSBtlVDsnFC8KBrAccEDdEuH+qAew6Hd4Rpvu9/Nw4bUuLN64ocJP+1M13x3Y1FxNkNFg+lty8vUCr1YEkDbdPQwwEoY=; ali_apache_track=mt=1|ms=|mid=us1893585475dqoae; ali_apache_tracktmp=W_signed=Y; _history_login_user_info={"userName":"wade1080","avatar":"","accountNumber":"wade1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1747272313853}; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&x_user=US|wade1080|user|ifm|6340368875&x_lid=us1893585475dqoae&x_c_chg=1&acs_rt=5dee352ea2514573aa18d0936486dd26; lwrid=AgGWNwz0ADPja4jy2fg%2BX39uI4bN; join_status=; _gid=GA1.2.1411312012.1744680320; aep_usuc_f=site=glo&c_tp=USD&x_alimid=6340368875&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2; _pin_unauth=dWlkPU9ERTBaVGd4TXpVdE1UWXhNaTAwT0RsbUxUZzNNV1l0WkRka05HWmlZMlUxTURrMQ; _fbp=fb.1.1744680347870.912429541388440071; AB_DATA_TRACK=112185_8922; AB_ALG=global_union_ab_exp_4%3D0; AB_STG=st_SE_1736852788277%23stg_4159; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005005992120720%091005006457230695%091005002409350841%091005008404213300%091005008666798729%091005008722948277; lwrtk=AAIEZ/4q18W6Jhdhjc2Q9fRH//Xadte+C6cqfKfLwZ94jwJYRMP6It4=; lwrtk=AAIEZ/4q18W6Jhdhjc2Q9fRH//Xadte+C6cqfKfLwZ94jwJYRMP6It4=; account_v=1; x5sec=7b22617365727665722d696e746c3b33223a22307c4350325439373847454f6652744930444d4c69386873542b2f2f2f2f2f77453d222c22733b32223a2237396130646338313835366333326538227d; _m_h5_tk=28142e706bb146f5c5630ee201c2c12f_1744688393813; _m_h5_tk_enc=e2dc459a547f4cacef94c6adb166dedc; intl_common_forever=NQkmnnyWcxJ6e8lA/kZxk0rEp0v4RahuHduwRY0zdXMiJ5jhfZnI2Q==; _gat=1; JSESSIONID=10D93B4276C348BFE5188E56A3DB7308; _ga_VED1YSGNC7=GS1.1.1744686321.2.1.1744686545.42.0.0; _ga=GA1.1.821064136.1744680280; _uetsid=6db1e7a018d111f0b9c2a54a19f8a7d0; _uetvid=44d83b80174f11f095c263faaf25bc18; cto_bundle=Hri2xV9ZelMlMkZtTUFaJTJCb0xMMUVZRUtTcnM0QllCNiUyQk1UTGRwejZ6MGdIZjYyZ1g0anVLZVljc3M4THdCMWMlMkZrTDRVZ1E1cVlMdTNCb0lvMXZUcEwlMkZ0MVV3YURuSklQRUN1OVBURmUlMkZ6cEVoOXRkMkRReEQ5Q2VEWU9yUnJVUnQ3eEdWT2JFb21ZJTJGMlpqajJ3Y0ZVQlk0QVZXbGV6NFJmNWEzeXVPNnlCZHBxV2ZGSSUzRA; isg=BOnpzyR6quV6iZZQNWIsQnf4-JVDtt3o3yqPFIveZFAPUglk0gRTuHJMFPbkSnUg; tfstk=g2ksqeiuGNb_OfbnjFKUVOLXBewbCq9yHiZxqmBNDReOkZn88h2q_hjxDmg5QOovSqMbJmX47S-iRJE4DoBTHSBLvuz3uhDwjr3Iu2e46fzVhxiY8qWqbqSit4oRQARg3twgn-LyzLJyjc20HO3xV-aivDqvYlUH138Un-Ly8uXBJdwmrBP3-fnpAor0kG3Y6MBL-lBTHPFAJ6EYJrexk5EpplqOMlEYkyKQmyUYH-3Ypb_lVoO_SctGqBKWZMEoXy6AHAp06zi1gtBxdlNsHcUI40kQf5a8tsnZ7A3EDAkgtBCQnDlSlj3J81ztNugQafT5C4ggDmZx5Lj7JAijd5cFqTnQGPGKBWsAHcw3k7lj5F1gWfuQZkFdcLqEzyniBXtcJc3z5RELTLKSvShEI7DwJOw-ZcyZM4LF_Ph7DgzRUztHvssQZtZQzHtCisvvxnDExrxNQ5E3fW-BANh06kqQzHtCisVTxlZyAH_ti; epssw=9*mmCrpm9T-HUEWcvOdQS2zpqiR3AO7tV73tjmGP7bdSZ3CYHiutG4dtvO3t672tmB_mr2M48EABmOYdQZlkT19LetUjAwFDKu0yFr9LmmNfKnMJVzH7zo05UwsXxbwUsB8NqP9B9R5eHGKP9GE5VKVAymmLeUT4R4HmHYNZdXm6FZmbuc3BwaFCpI69sb3Q5DgS8YagrmJNtSW6gsuL57i2zuiwmmmAxVut_mmAz3utGB7QHiHNSf2iTmg8eC3St-3_yeMuLd3chzt7dHqdASRIqqpEXZdKfo8__Kn7zZPV_0_n8DudZvmhByDPcbmm..',
}

params = {
    'componentKey': 'pcShopHead',
    'country': 'US',
    'site': 'glo',
    'sellerId': '2668273644',
    'domainServer': '//www.aliexpress.com',
    'language': 'English',
    'storeName': 'Sensor manufacturer Store',
    'buyerId': '6340368875',
    'locale': 'en_US',
    'shopSignSelected': 'storeName',
    'callback': 'jsonp_1744686547600_6363',
}

response = requests.get('https://shoprenderview.aliexpress.com/async/execute', params=params, cookies=cookies, headers=headers)
print(response.text)