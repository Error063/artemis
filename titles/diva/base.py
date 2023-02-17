import datetime
from typing import Any, List, Dict
import logging 
import json
import urllib

from core.config import CoreConfig
from titles.diva.config import DivaConfig
from titles.diva.const import DivaConstants
from titles.diva.database import DivaData

class DivaBase():
    def __init__(self, cfg: CoreConfig, game_cfg: DivaConfig) -> None:
        self.core_cfg = cfg # Config file
        self.game_config = game_cfg
        self.data = DivaData(cfg) # Database
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("diva")
        self.game = DivaConstants.GAME_CODE
        self.version = DivaConstants.VER_PROJECT_DIVA_ARCADE_FUTURE_TONE

        dt = datetime.datetime.now()
        self.time_lut=urllib.parse.quote(dt.strftime("%Y-%m-%d %H:%M:%S:16.0"))
    
    def handle_test_request(self, data: Dict) -> Dict:
        return ""

    def handle_game_init_request(self, data: Dict) -> Dict:
        return ( f'' )

    def handle_attend_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            'atnd_prm1': '0,1,1,0,0,0,1,0,100,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1', 
            'atnd_prm2': '30,10,100,4,1,50,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1',
            'atnd_prm3': '100,0,1,1,1,1,1,1,1,1,2,3,4,1,1,1,3,4,5,1,1,1,4,5,6,1,1,1,5,6,7,4,4,4,9,10,14,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,10,30,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0',
            'atnd_lut': f'{self.time_lut}',
        }
        
        encoded += urllib.parse.urlencode(params)
        encoded = encoded.replace("%2C", ",")

        return encoded

    def handle_ping_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            'ping_b_msg': f'Welcome to {self.core_cfg.server.name} network!', 
            'ping_m_msg': 'xxx',
            'atnd_lut': f'{self.time_lut}',
            'fi_lut': f'{self.time_lut}',
            'ci_lut': f'{self.time_lut}',
            'qi_lut': f'{self.time_lut}',
            'pvl_lut': '2021-05-22 12:08:16.0',
            'shp_ctlg_lut': '2020-06-10 19:44:16.0',
            'cstmz_itm_ctlg_lut': '2019-10-08 20:23:12.0',
            'ngwl_lut': '2019-10-08 20:23:12.0',
            'rnk_nv_lut': '2020-06-10 19:51:30.0',
            'rnk_ps_lut': f'{self.time_lut}',
            'bi_lut': '2020-09-18 10:00:00.0',
            'cpi_lut': '2020-10-25 09:25:10.0',
            'bdlol_lut': '2020-09-18 10:00:00.0',
            'p_std_hc_lut': '2019-08-01 04:00:36.0',
            'p_std_i_n_lut': '2019-08-01 04:00:36.0',
            'pdcl_lut': '2019-08-01 04:00:36.0',
            'pnml_lut': '2019-08-01 04:00:36.0',
            'cinml_lut': '2019-08-01 04:00:36.0',
            'rwl_lut': '2019-08-01 04:00:36.0',
            'req_inv_cmd_num': '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
            'req_inv_cmd_prm1': '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
            'req_inv_cmd_prm2': '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
            'req_inv_cmd_prm3': '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
            'req_inv_cmd_prm4': '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
            'pow_save_flg': 0,
            'nblss_dnt_p': 100,
            'nblss_ltt_rl_vp': 1500,
            'nblss_ex_ltt_flg': 1,
            'nblss_dnt_st_tm': "2019-07-15 12:00:00.0",
            'nblss_dnt_ed_tm': "2019-09-17 12:00:00.0",
            'nblss_ltt_st_tm': "2019-09-18 12:00:00.0",
            'nblss_ltt_ed_tm': "2019-09-22 12:00:00.0",
        }
        
        encoded += urllib.parse.urlencode(params)
        encoded = encoded.replace("+", "%20")
        encoded = encoded.replace("%2C", ",")

        return encoded

    def handle_pv_list_request(self, data: Dict) -> Dict:
        pvlist = ""
        with open(r"titles/diva/data/PvList0.dat", encoding="utf-8") as shop:
            lines = shop.readlines()
            for line in lines:
                pvlist += f"{line}"
        pvlist += ","

        with open(r"titles/diva/data/PvList1.dat", encoding="utf-8") as shop:
            lines = shop.readlines()
            for line in lines:
                pvlist += f"{line}"
        pvlist += ","

        with open(r"titles/diva/data/PvList2.dat", encoding="utf-8") as shop:
            lines = shop.readlines()
            for line in lines:
                pvlist += f"{line}"
        pvlist += ","

        with open(r"titles/diva/data/PvList3.dat", encoding="utf-8") as shop:
            lines = shop.readlines()
            for line in lines:
                pvlist += f"{line}"
        pvlist += ","

        with open(r"titles/diva/data/PvList4.dat", encoding="utf-8") as shop:
            lines = shop.readlines()
            for line in lines:
                pvlist += f"{line}"

        response = ""
        response += f"&pvl_lut={self.time_lut}"
        response += f"&pv_lst={pvlist}"

        return ( response )

    def handle_shop_catalog_request(self, data: Dict) -> Dict:
        catalog = ""

        shopList = self.data.static.get_enabled_shop(self.version)
        if not shopList:
            with open(r"titles/diva/data/ShopCatalog.dat", encoding="utf-8") as shop:
                lines = shop.readlines()
                for line in lines:
                    line = urllib.parse.quote(line) + ","
                    catalog += f"{urllib.parse.quote(line)}"
            catalog = catalog.replace("+", "%20")

            response = ""
            response += f"&shp_ctlg_lut={self.time_lut}"
            response += f"&shp_ctlg={catalog[:-3]}"
        else:
            for shop in shopList:
                line = str(shop["shopId"]) + "," + str(shop['unknown_0']) + "," + shop['name'] + "," + str(shop['points']) + "," + shop['start_date'] + "," + shop['end_date'] + "," + str(shop["type"])
                line = urllib.parse.quote(line) + ","
                catalog += f"{urllib.parse.quote(line)}"

            catalog = catalog.replace("+", "%20")
                
            response = ""
            response += f"&shp_ctlg_lut={self.time_lut}"
            response += f"&shp_ctlg={catalog[:-3]}"

        return ( response )

    def handle_cstmz_itm_ctlg_request(self, data: Dict) -> Dict:
        catalog = ""

        itemList = self.data.static.get_enabled_items(self.version)
        if not itemList:
            with open(r"titles/diva/data/ItemCatalog.dat", encoding="utf-8") as item:
                lines = item.readlines()
                for line in lines:
                    line = urllib.parse.quote(line) + ","
                    catalog += f"{urllib.parse.quote(line)}"
            catalog = catalog.replace("+", "%20")

            response = ""
            response += f"&cstmz_itm_ctlg_lut={self.time_lut}"
            response += f"&cstmz_itm_ctlg={catalog[:-3]}"
        else:
            for item in itemList:
                line = str(item["itemId"]) + "," + str(item['unknown_0']) + "," + item['name'] + "," + str(item['points']) + "," + item['start_date'] + "," + item['end_date'] + "," + str(item["type"])
                line = urllib.parse.quote(line) + ","
                catalog += f"{urllib.parse.quote(line)}"

            catalog = catalog.replace("+", "%20")

            response = ""
            response += f"&cstmz_itm_ctlg_lut={self.time_lut}"
            response += f"&cstmz_itm_ctlg={catalog[:-3]}"

        return ( response )

    def handle_festa_info_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            'fi_id': '1,-1',
            'fi_name': f'{self.core_cfg.server.name} Opening,xxx',
            'fi_kind': '0,0',
            'fi_difficulty': '-1,-1',
            'fi_pv_id_lst': 'ALL,ALL',
            'fi_attr': '7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
            'fi_add_vp': '10,0',
            'fi_mul_vp': '1,1',
            'fi_st': '2022-06-17 17:00:00.0,2014-07-08 18:10:11.0',
            'fi_et': '2029-01-01 10:00:00.0,2014-07-08 18:10:11.0',
            'fi_lut': '{self.time_lut}',
        }
        
        encoded += urllib.parse.urlencode(params)
        encoded = encoded.replace("+", "%20")
        encoded = encoded.replace("%2C", ",")

        return encoded
        
    def handle_contest_info_request(self, data: Dict) -> Dict:
        response = ""

        response += f"&ci_lut={self.time_lut}"
        response += "&ci_str=%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A"
        
        return ( response )
        
    def handle_qst_inf_request(self, data: Dict) -> Dict:
        quest = ""

        questList = self.data.static.get_enabled_quests(self.version)
        if not questList:
            with open(r"titles/diva/data/QuestInfo.dat", encoding="utf-8") as shop:
                lines = shop.readlines()
                for line in lines:
                    quest += f"{urllib.parse.quote(line)},"

            response = ""
            response += f"&qi_lut={self.time_lut}"
            response += f"&qhi_str={quest[:-1]}"
        else:
            for quests in questList:
                line = str(quests["questId"]) + "," + str(quests['quest_order']) + "," + str(quests['kind']) + "," + str(quests['unknown_0']) + "," + quests['start_datetime'] + "," + quests['end_datetime'] + "," + quests["name"] + "," + str(quests["unknown_1"]) + "," + str(quests["unknown_2"]) + "," + str(quests["quest_enable"])
                quest += f"{urllib.parse.quote(line)}%0A,"

            responseline = f"{quest[:-1]},"
            for i in range(len(questList),59):
                responseline += "%2A%2A%2A%0A,"

            response = ""
            response += f"&qi_lut={self.time_lut}"
            response += f"&qhi_str={responseline}%2A%2A%2A"

        response += "&qrai_str=%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1,%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1,%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1"

        return ( response )
        
    def handle_nv_ranking_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_ps_ranking_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_ng_word_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_rmt_wp_list_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_pv_def_chr_list_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_pv_ng_mdl_list_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_cstmz_itm_ng_mdl_lst_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_banner_info_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_banner_data_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_cm_ply_info_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_pstd_h_ctrl_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_pstd_item_ng_lst_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_pre_start_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["aime_id"], self.version)
        profile_shop = self.data.item.get_shop(data["aime_id"], self.version)
        if profile is None:
            return ( f"&ps_result=-3")
        else:
            response = ""
            response += "&ps_result=1"
            response += f"&pd_id={data['aime_id']}"
            response += "&nblss_ltt_stts=-1"
            response += "&nblss_ltt_tckt=-1"
            response += "&nblss_ltt_is_opn=-1"
            response += f"&vcld_pts={profile['vcld_pts']}"
            response += f"&player_name={profile['player_name']}"
            response += f"&lv_efct_id={profile['lv_efct_id']}"
            response += f"&lv_plt_id={profile['lv_plt_id']}"
            response += f"&lv_str={profile['lv_str']}"
            response += f"&lv_num={profile['lv_num']}"
            response += f"&lv_pnt={profile['lv_pnt']}"

            #Store stuff to add to rework
            response += f"&mdl_eqp_tm={self.time_lut}"

            if profile_shop:
                response += f"&mdl_eqp_ary={profile_shop['mdl_eqp_ary']}"

            response += f"&c_itm_eqp_ary=-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999"
            response += f"&ms_itm_flg_ary=1,1,1,1,1,1,1,1,1,1,1,1"

            return ( response )
            
    def handle_registration_request(self, data: Dict) -> Dict: #DONE
        self.data.profile.create_profile(self.version, data["aime_id"], data["player_name"])
        return ( f"&cd_adm_result=1&pd_id={data['aime_id']}")
        
    def handle_start_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        profile_shop = self.data.item.get_shop(data["pd_id"], self.version)
        if profile is None: return
        
        response = ""
        response += f"&pd_id={data['pd_id']}"
        response += "&start_result=1"

        response += "&accept_idx=100"
        response += f"&hp_vol={profile['hp_vol']}"
        response += f"&btn_se_vol={profile['btn_se_vol']}"
        response += f"&btn_se_vol2={profile['btn_se_vol2']}"
        response += f"&sldr_se_vol2={profile['sldr_se_vol2']}"
        response += f"&sort_kind={profile['sort_kind']}"
        response += f"&player_name={profile['player_name']}"
        response += f"&lv_num={profile['lv_num']}"
        response += f"&lv_pnt={profile['lv_pnt']}"
        response += f"&lv_efct_id={profile['lv_efct_id']}"
        response += f"&lv_plt_id={profile['lv_plt_id']}"
        response += "&mdl_have=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        response += "&cstmz_itm_have=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        response += f"&use_pv_mdl_eqp={profile['use_pv_mdl_eqp']}"
        response += f"&use_pv_btn_se_eqp={profile['use_pv_btn_se_eqp']}"
        response += f"&use_pv_sld_se_eqp={profile['use_pv_sld_se_eqp']}"
        response += f"&use_pv_chn_sld_se_eqp={profile['use_pv_chn_sld_se_eqp']}"
        response += f"&use_pv_sldr_tch_se_eqp={profile['use_pv_sldr_tch_se_eqp']}"
        response += f"&vcld_pts={profile['lv_efct_id']}"
        response += f"&nxt_pv_id={profile['nxt_pv_id']}"
        response += f"&nxt_dffclty={profile['nxt_dffclty']}"
        response += f"&nxt_edtn={profile['nxt_edtn']}"
        response += f"&dsp_clr_brdr={profile['dsp_clr_brdr']}"
        response += f"&dsp_intrm_rnk={profile['dsp_intrm_rnk']}"
        response += f"&dsp_clr_sts={profile['dsp_clr_sts']}"
        response += f"&rgo_sts={profile['rgo_sts']}"

        #To be fully fixed
        if "my_qst_id" not in profile:
            response += f"&my_qst_id=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
            response += f"&my_qst_sts=0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        else:
            response += f"&my_qst_id={profile['my_qst_id']}"
            response += f"&my_qst_sts={profile['my_qst_sts']}"

        response += f"&my_qst_prgrs=0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += f"&my_qst_et=2022-06-19%2010%3A28%3A52.0,2022-06-19%2010%3A28%3A52.0,2022-06-19%2010%3A28%3A52.0,2100-01-01%2008%3A59%3A59.0,2100-01-01%2008%3A59%3A59.0,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx"
        response += f"&clr_sts=0,0,0,0,0,0,0,0,56,52,35,6,6,3,1,0,0,0,0,0"

        #Store stuff to add to rework
        response += f"&mdl_eqp_tm={self.time_lut}"

        if profile_shop:
            response += f"&mdl_eqp_ary={profile_shop['mdl_eqp_ary']}"

        response += f"&c_itm_eqp_ary=-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999"
        response += f"&ms_itm_flg_ary=1,1,1,1,1,1,1,1,1,1,1,1"
        
        return ( response )

    def handle_pd_unlock_request(self, data: Dict) -> Dict:
        return ( f'' )
        
    def handle_spend_credit_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        if profile is None: return

        response = ""

        response += "&cmpgn_rslt=-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x"
        response += "&cmpgn_rslt_num=0"
        response += f"&vcld_pts={profile['vcld_pts']}"
        response += f"&lv_str={profile['lv_str']}"
        response += f"&lv_efct_id={profile['lv_efct_id']}"
        response += f"&lv_plt_id={profile['lv_plt_id']}"

        return ( response )

    def handle_get_pv_pd_request(self, data: Dict) -> Dict:
        song_id = data["pd_pv_id_lst"].split(",")
        pv = ""

        for song in song_id:
            if int(song) > 0:
                pd_db_song = self.data.score.get_best_score(data["pd_id"], int(song), data["difficulty"])
                if pd_db_song is not None:

                    pv += urllib.parse.quote(f"{song},0,{pd_db_song['clr_kind']},{pd_db_song['score']},{pd_db_song['atn_pnt']},{pd_db_song['sort_kind']},-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1337,1,1,1,0,0,0")

                else:
                    #self.logger.debug(f"No score saved for ID: {song}!")
                    pv += urllib.parse.quote(f"{song},0,-1,-1,-1,0,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,0,0,0")
                
                #pv_no, edition, rslt, max_score, max_atn_pnt, challenge_kind, module_eqp[-999,-999,-999], customize_eqp[-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999], customize_flag[1,1,1,1,1,1,1,1,1,1,1,1], skin, btn_se, sld_se, chsld_se, sldtch_se, rvl_pd_id, rvl_score, rvl_attn_pnt, countrywide_ranking, rgo_hispeed, rgo_hidden, rgo_sudden, rgo_hispeed_cleared, rgo_hidden_cleared, rgo_sudden_cleared, chain_challenge_num, chain_challenge_max, chain_challenge_open, version
            else:
                pv += urllib.parse.quote(f"{song}***")
            pv += ","

        response = ""
        response += f"&pd_by_pv_id={pv[:-1]}"
        response += "&pdddt_flg=0"
        response += f"&pdddt_tm={self.time_lut}"

        return ( response )

    def handle_stage_start_request(self, data: Dict) -> Dict:
        return ( f'' )

    def handle_stage_result_request(self, data: Dict) -> Dict:

        profile = self.data.profile.get_profile(data["pd_id"], self.version)

        pd_song_list = data["stg_ply_pv_id"].split(",")
        pd_song_difficulty = data["stg_difficulty"].split(",")
        pd_song_max_score = data["stg_score"].split(",")
        pd_song_max_atn_pnt = data["stg_atn_pnt"].split(",")
        pd_song_ranking = data["stg_clr_kind"].split(",")
        pd_song_sort_kind = data["sort_kind"]
        pd_song_cool_cnt = data["stg_cool_cnt"].split(",")
        pd_song_fine_cnt = data["stg_fine_cnt"].split(",")
        pd_song_safe_cnt = data["stg_safe_cnt"].split(",")
        pd_song_sad_cnt = data["stg_sad_cnt"].split(",")
        pd_song_worst_cnt = data["stg_wt_wg_cnt"].split(",")
        pd_song_max_combo = data["stg_max_cmb"].split(",")

        for index, value in enumerate(pd_song_list):
            if "-1" not in pd_song_list[index]:
                profile_pd_db_song = self.data.score.get_best_score(data["pd_id"], pd_song_list[index], pd_song_difficulty[index])
                if profile_pd_db_song is None:
                    self.data.score.put_best_score(data["pd_id"], self.version, pd_song_list[index], pd_song_difficulty[index], pd_song_max_score[index], pd_song_max_atn_pnt[index], pd_song_ranking[index], pd_song_sort_kind, pd_song_cool_cnt[index], pd_song_fine_cnt[index], pd_song_safe_cnt[index], pd_song_sad_cnt[index], pd_song_worst_cnt[index], pd_song_max_combo[index])
                    self.data.score.put_playlog(data["pd_id"], self.version, pd_song_list[index], pd_song_difficulty[index], pd_song_max_score[index], pd_song_max_atn_pnt[index], pd_song_ranking[index], pd_song_sort_kind, pd_song_cool_cnt[index], pd_song_fine_cnt[index], pd_song_safe_cnt[index], pd_song_sad_cnt[index], pd_song_worst_cnt[index], pd_song_max_combo[index])
                elif int(pd_song_max_score[index]) >= int(profile_pd_db_song["score"]):
                    self.data.score.put_best_score(data["pd_id"], self.version, pd_song_list[index], pd_song_difficulty[index], pd_song_max_score[index], pd_song_max_atn_pnt[index], pd_song_ranking[index], pd_song_sort_kind, pd_song_cool_cnt[index], pd_song_fine_cnt[index], pd_song_safe_cnt[index], pd_song_sad_cnt[index], pd_song_worst_cnt[index], pd_song_max_combo[index])
                    self.data.score.put_playlog(data["pd_id"], self.version, pd_song_list[index], pd_song_difficulty[index], pd_song_max_score[index], pd_song_max_atn_pnt[index], pd_song_ranking[index], pd_song_sort_kind, pd_song_cool_cnt[index], pd_song_fine_cnt[index], pd_song_safe_cnt[index], pd_song_sad_cnt[index], pd_song_worst_cnt[index], pd_song_max_combo[index])
                elif int(pd_song_max_score[index]) != int(profile_pd_db_song["score"]):
                    self.data.score.put_playlog(data["pd_id"], self.version, pd_song_list[index], pd_song_difficulty[index], pd_song_max_score[index], pd_song_max_atn_pnt[index], pd_song_ranking[index], pd_song_sort_kind, pd_song_cool_cnt[index], pd_song_fine_cnt[index], pd_song_safe_cnt[index], pd_song_sad_cnt[index], pd_song_worst_cnt[index], pd_song_max_combo[index])

        # Profile saving based on registration list

        old_level = int(profile['lv_num'])
        new_level = (int(data["ttl_vp_add"]) + int(profile["lv_pnt"])) / 12

        self.data.profile.update_profile(data["pd_id"], int(new_level), int(profile["lv_pnt"]) + int(data["ttl_vp_add"]), int(data["vcld_pts"]), int(data["hp_vol"]), int(data["btn_se_vol"]), int(data["btn_se_vol2"]), int(data["sldr_se_vol2"]), int(data["sort_kind"]), int(data["use_pv_mdl_eqp"]), profile["use_pv_btn_se_eqp"], profile["use_pv_sld_se_eqp"], profile["use_pv_chn_sld_se_eqp"], profile["use_pv_sldr_tch_se_eqp"], int(data["ply_pv_id"]), int(data["nxt_dffclty"]), int(data["nxt_edtn"]), profile["dsp_clr_brdr"], profile["dsp_intrm_rnk"], profile["dsp_clr_sts"], profile["rgo_sts"], profile["lv_efct_id"], profile["lv_plt_id"], data["my_qst_id"], data["my_qst_sts"])

        response = ""

        response += "&chllng_kind=-1"
        response += f"&lv_num_old={int(old_level)}"
        response += f"&lv_pnt_old={int(profile['lv_pnt'])}"
        response += f"&lv_num={int(profile['lv_num'])}"
        response += f"&lv_str={profile['lv_str']}"
        response += f"&lv_pnt={int(profile['lv_pnt']) + int(data['ttl_vp_add'])}"
        response += f"&lv_efct_id={int(profile['lv_efct_id'])}"
        response += f"&lv_plt_id={int(profile['lv_plt_id'])}"
        response += f"&vcld_pts={int(data['vcld_pts'])}"
        response += f"&prsnt_vcld_pts={int(profile['vcld_pts'])}"
        response += "&cerwd_kind=-1"
        response += "&cerwd_value=-1"
        response += "&cerwd_str_0=***"
        response += "&cerwd_str_1=***"
        response += "&ttl_str_ary=xxx,xxx,xxx,xxx,xxx"
        response += "&ttl_plt_id_ary=-1,-1,-1,-1,-1"
        response += "&ttl_desc_ary=xxx,xxx,xxx,xxx,xxx"
        response += "&skin_id_ary=xxx,xxx,xxx,xxx,xxx"
        response += "&skin_name_ary=xxx,xxx,xxx,xxx,xxx"
        response += "&skin_illust_ary=xxx,xxx,xxx,xxx,xxx"
        response += "&skin_desc_ary=xxx,xxx,xxx,xxx,xxx"
        if "my_qst_id" not in profile:
            response += f"&my_qst_id=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        else:
            response += f"&my_qst_id={profile['my_qst_id']}"
        response += "&my_qst_r_qid=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += "&my_qst_r_knd=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += "&my_qst_r_vl=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += "&my_qst_r_nflg=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += "&my_ccd_r_qid=-1,-1,-1,-1,-1"
        response += "&my_ccd_r_hnd=-1,-1,-1,-1,-1"
        response += "&my_ccd_r_vp=-1,-1,-1,-1,-1"

        return ( response )

    def handle_end_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        self.data.profile.update_profile(data["pd_id"], profile["lv_num"], profile["lv_pnt"], profile["vcld_pts"], profile["hp_vol"], profile["btn_se_vol"], profile["btn_se_vol2"], profile["sldr_se_vol2"], profile["sort_kind"], profile["use_pv_mdl_eqp"], profile["use_pv_btn_se_eqp"], profile["use_pv_sld_se_eqp"], profile["use_pv_chn_sld_se_eqp"], profile["use_pv_sldr_tch_se_eqp"], profile["nxt_pv_id"], profile["nxt_dffclty"], profile["nxt_edtn"], profile["dsp_clr_brdr"], profile["dsp_intrm_rnk"], profile["dsp_clr_sts"], profile["rgo_sts"], profile["lv_efct_id"], profile["lv_plt_id"], data["my_qst_id"], data["my_qst_sts"])
        return ( f'' )

    def handle_shop_exit_request(self, data: Dict) -> Dict:
        self.data.item.put_shop(data["pd_id"], self.version, data["mdl_eqp_cmn_ary"])

        response = ""
        response += "&shp_rslt=1"
        return ( response )
