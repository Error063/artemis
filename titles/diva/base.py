import datetime
from typing import Any, List, Dict
import logging
import json
import urllib
from threading import Thread

from core.config import CoreConfig
from titles.diva.config import DivaConfig
from titles.diva.const import DivaConstants
from titles.diva.database import DivaData


class DivaBase:
    def __init__(self, cfg: CoreConfig, game_cfg: DivaConfig) -> None:
        self.core_cfg = cfg  # Config file
        self.game_config = game_cfg
        self.data = DivaData(cfg)  # Database
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("diva")
        self.game = DivaConstants.GAME_CODE
        self.version = DivaConstants.VER_PROJECT_DIVA_ARCADE_FUTURE_TONE

        dt = datetime.datetime.now()
        self.time_lut = urllib.parse.quote(dt.strftime("%Y-%m-%d %H:%M:%S:16.0"))

    def handle_test_request(self, data: Dict) -> Dict:
        return ""

    def handle_game_init_request(self, data: Dict) -> Dict:
        return f""

    def handle_attend_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            "atnd_prm1": "0,1,1,0,0,0,1,0,100,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
            "atnd_prm2": "30,10,100,4,1,50,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
            "atnd_prm3": "100,0,1,1,1,1,1,1,1,1,2,3,4,1,1,1,3,4,5,1,1,1,4,5,6,1,1,1,5,6,7,4,4,4,9,10,14,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,5,10,10,25,20,50,30,90,10,30,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
            "atnd_lut": f"{self.time_lut}",
        }

        encoded += urllib.parse.urlencode(params)
        encoded = encoded.replace("%2C", ",")

        return encoded

    def handle_ping_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            "ping_b_msg": f"Welcome to {self.core_cfg.server.name} network!",
            "ping_m_msg": "xxx",
            "atnd_lut": f"{self.time_lut}",
            "fi_lut": f"{self.time_lut}",
            "ci_lut": f"{self.time_lut}",
            "qi_lut": f"{self.time_lut}",
            "pvl_lut": "2021-05-22 12:08:16.0",
            "shp_ctlg_lut": "2020-06-10 19:44:16.0",
            "cstmz_itm_ctlg_lut": "2019-10-08 20:23:12.0",
            "ngwl_lut": "2019-10-08 20:23:12.0",
            "rnk_nv_lut": "2020-06-10 19:51:30.0",
            "rnk_ps_lut": f"{self.time_lut}",
            "bi_lut": "2020-09-18 10:00:00.0",
            "cpi_lut": "2020-10-25 09:25:10.0",
            "bdlol_lut": "2020-09-18 10:00:00.0",
            "p_std_hc_lut": "2019-08-01 04:00:36.0",
            "p_std_i_n_lut": "2019-08-01 04:00:36.0",
            "pdcl_lut": "2019-08-01 04:00:36.0",
            "pnml_lut": "2019-08-01 04:00:36.0",
            "cinml_lut": "2019-08-01 04:00:36.0",
            "rwl_lut": "2019-08-01 04:00:36.0",
            "req_inv_cmd_num": "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
            "req_inv_cmd_prm1": "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
            "req_inv_cmd_prm2": "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
            "req_inv_cmd_prm3": "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
            "req_inv_cmd_prm4": "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
            "pow_save_flg": 0,
            "nblss_dnt_p": 100,
            "nblss_ltt_rl_vp": 1500,
            "nblss_ex_ltt_flg": 1,
            "nblss_dnt_st_tm": "2019-07-15 12:00:00.0",
            "nblss_dnt_ed_tm": "2019-09-17 12:00:00.0",
            "nblss_ltt_st_tm": "2019-09-18 12:00:00.0",
            "nblss_ltt_ed_tm": "2019-09-22 12:00:00.0",
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

        return response

    def handle_shop_catalog_request(self, data: Dict) -> Dict:
        catalog = ""

        shopList = self.data.static.get_enabled_shops(self.version)
        if not shopList:
            with open(r"titles/diva/data/ShopCatalog.dat", encoding="utf-8") as shop:
                lines = shop.readlines()
                for line in lines:
                    line = urllib.parse.quote(line) + ","
                    catalog += f"{urllib.parse.quote(line)}"

        else:
            for shop in shopList:
                line = (
                    str(shop["shopId"])
                    + ","
                    + str(shop["unknown_0"])
                    + ","
                    + shop["name"]
                    + ","
                    + str(shop["points"])
                    + ","
                    + shop["start_date"]
                    + ","
                    + shop["end_date"]
                    + ","
                    + str(shop["type"])
                )
                line = urllib.parse.quote(line) + ","
                catalog += f"{urllib.parse.quote(line)}"

        catalog = catalog.replace("+", "%20")

        response = f"&shp_ctlg_lut={self.time_lut}"
        response += f"&shp_ctlg={catalog[:-3]}"

        return response

    def handle_buy_module_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        module = self.data.static.get_enabled_shop(self.version, int(data["mdl_id"]))

        # make sure module is available to purchase
        if not module:
            return f"&shp_rslt=0&vcld_pts={profile['vcld_pts']}"

        # make sure player has enough vocaloid points to buy module
        if profile["vcld_pts"] < int(data["mdl_price"]):
            return f"&shp_rslt=0&vcld_pts={profile['vcld_pts']}"

        new_vcld_pts = profile["vcld_pts"] - int(data["mdl_price"])

        self.data.profile.update_profile(profile["user"], vcld_pts=new_vcld_pts)
        self.data.module.put_module(data["pd_id"], self.version, data["mdl_id"])

        # generate the mdl_have string
        mdl_have = self.data.module.get_modules_have_string(data["pd_id"], self.version)

        response = "&shp_rslt=1"
        response += f"&mdl_id={data['mdl_id']}"
        response += f"&mdl_have={mdl_have}"
        response += f"&vcld_pts={new_vcld_pts}"

        return response

    def handle_cstmz_itm_ctlg_request(self, data: Dict) -> Dict:
        catalog = ""

        itemList = self.data.static.get_enabled_items(self.version)
        if not itemList:
            with open(r"titles/diva/data/ItemCatalog.dat", encoding="utf-8") as item:
                lines = item.readlines()
                for line in lines:
                    line = urllib.parse.quote(line) + ","
                    catalog += f"{urllib.parse.quote(line)}"

        else:
            for item in itemList:
                line = (
                    str(item["itemId"])
                    + ","
                    + str(item["unknown_0"])
                    + ","
                    + item["name"]
                    + ","
                    + str(item["points"])
                    + ","
                    + item["start_date"]
                    + ","
                    + item["end_date"]
                    + ","
                    + str(item["type"])
                )
                line = urllib.parse.quote(line) + ","
                catalog += f"{urllib.parse.quote(line)}"

        catalog = catalog.replace("+", "%20")

        response = f"&cstmz_itm_ctlg_lut={self.time_lut}"
        response += f"&cstmz_itm_ctlg={catalog[:-3]}"

        return response

    def handle_buy_cstmz_itm_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        item = self.data.static.get_enabled_item(
            self.version, int(data["cstmz_itm_id"])
        )

        # make sure module is available to purchase
        if not item:
            return f"&shp_rslt=0&vcld_pts={profile['vcld_pts']}"

        # make sure player has enough vocaloid points to buy the customize item
        if profile["vcld_pts"] < int(data["cstmz_itm_price"]):
            return f"&shp_rslt=0&vcld_pts={profile['vcld_pts']}"

        new_vcld_pts = profile["vcld_pts"] - int(data["cstmz_itm_price"])

        # save new Vocaloid Points balance
        self.data.profile.update_profile(profile["user"], vcld_pts=new_vcld_pts)

        self.data.customize.put_customize_item(
            data["pd_id"], self.version, data["cstmz_itm_id"]
        )

        # generate the cstmz_itm_have string
        cstmz_itm_have = self.data.customize.get_customize_items_have_string(
            data["pd_id"], self.version
        )

        response = "&shp_rslt=1"
        response += f"&cstmz_itm_id={data['cstmz_itm_id']}"
        response += f"&cstmz_itm_have={cstmz_itm_have}"
        response += f"&vcld_pts={new_vcld_pts}"

        return response

    def handle_festa_info_request(self, data: Dict) -> Dict:
        encoded = "&"
        params = {
            "fi_id": "1,2",
            "fi_name": f"{self.core_cfg.server.name} Opening,Project DIVA Festa",
            # 0=PINK, 1=GREEN
            "fi_kind": "1,0",
            "fi_difficulty": "-1,-1",
            "fi_pv_id_lst": "ALL,ALL",
            "fi_attr": "7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "fi_add_vp": "20,5",
            "fi_mul_vp": "1,2",
            "fi_st": "2019-01-01 00:00:00.0,2019-01-01 00:00:00.0",
            "fi_et": "2029-01-01 00:00:00.0,2029-01-01 00:00:00.0",
            "fi_lut": "{self.time_lut}",
        }

        encoded += urllib.parse.urlencode(params)
        encoded = encoded.replace("+", "%20")
        encoded = encoded.replace("%2C", ",")

        return encoded

    def handle_contest_info_request(self, data: Dict) -> Dict:
        response = ""

        response += f"&ci_lut={self.time_lut}"
        response += "&ci_str=%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A,%2A%2A%2A"

        return response

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
                line = (
                    str(quests["questId"])
                    + ","
                    + str(quests["quest_order"])
                    + ","
                    + str(quests["kind"])
                    + ","
                    + str(quests["unknown_0"])
                    + ","
                    + quests["start_datetime"]
                    + ","
                    + quests["end_datetime"]
                    + ","
                    + quests["name"]
                    + ","
                    + str(quests["unknown_1"])
                    + ","
                    + str(quests["unknown_2"])
                    + ","
                    + str(quests["quest_enable"])
                )
                quest += f"{urllib.parse.quote(line)}%0A,"

            responseline = f"{quest[:-1]},"
            for i in range(len(questList), 59):
                responseline += "%2A%2A%2A%0A,"

            response = ""
            response += f"&qi_lut={self.time_lut}"
            response += f"&qhi_str={responseline}%2A%2A%2A"

        response += "&qrai_str=%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1,%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1,%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1%2C%2D1"

        return response

    def handle_nv_ranking_request(self, data: Dict) -> Dict:
        return f""

    def handle_ps_ranking_request(self, data: Dict) -> Dict:
        return f""

    def handle_ng_word_request(self, data: Dict) -> Dict:
        return f""

    def handle_rmt_wp_list_request(self, data: Dict) -> Dict:
        return f""

    def handle_pv_def_chr_list_request(self, data: Dict) -> Dict:
        return f""

    def handle_pv_ng_mdl_list_request(self, data: Dict) -> Dict:
        return f""

    def handle_cstmz_itm_ng_mdl_lst_request(self, data: Dict) -> Dict:
        return f""

    def handle_banner_info_request(self, data: Dict) -> Dict:
        return f""

    def handle_banner_data_request(self, data: Dict) -> Dict:
        return f""

    def handle_cm_ply_info_request(self, data: Dict) -> Dict:
        return f""

    def handle_pstd_h_ctrl_request(self, data: Dict) -> Dict:
        return f""

    def handle_pstd_item_ng_lst_request(self, data: Dict) -> Dict:
        return f""

    def handle_pre_start_request(self, data: Dict) -> str:
        profile = self.data.profile.get_profile(data["aime_id"], self.version)
        profile_shop = self.data.item.get_shop(data["aime_id"], self.version)

        if profile is None:
            return f"&ps_result=-3"
        else:
            response = "&ps_result=1"
            response += "&accept_idx=100"
            response += "&nblss_ltt_stts=-1"
            response += "&nblss_ltt_tckt=-1"
            response += "&nblss_ltt_is_opn=-1"
            response += f"&pd_id={data['aime_id']}"
            response += f"&player_name={profile['player_name']}"
            response += f"&sort_kind={profile['player_name']}"
            response += f"&lv_efct_id={profile['lv_efct_id']}"
            response += f"&lv_plt_id={profile['lv_plt_id']}"
            response += f"&lv_str={profile['lv_str']}"
            response += f"&lv_num={profile['lv_num']}"
            response += f"&lv_pnt={profile['lv_pnt']}"
            response += f"&vcld_pts={profile['vcld_pts']}"
            response += f"&skn_eqp={profile['use_pv_skn_eqp']}"
            response += f"&btn_se_eqp={profile['btn_se_eqp']}"
            response += f"&sld_se_eqp={profile['sld_se_eqp']}"
            response += f"&chn_sld_se_eqp={profile['chn_sld_se_eqp']}"
            response += f"&sldr_tch_se_eqp={profile['sldr_tch_se_eqp']}"
            response += f"&passwd_stat={profile['passwd_stat']}"

            # Store stuff to add to rework
            response += f"&mdl_eqp_tm={self.time_lut}"

            mdl_eqp_ary = "-999,-999,-999"

            # get the common_modules from the profile shop
            if profile_shop:
                mdl_eqp_ary = profile_shop["mdl_eqp_ary"]

            response += f"&mdl_eqp_ary={mdl_eqp_ary}"

            return response

    def handle_registration_request(self, data: Dict) -> Dict:
        self.data.profile.create_profile(
            self.version, data["aime_id"], data["player_name"]
        )
        return f"&cd_adm_result=1&pd_id={data['aime_id']}"

    def handle_start_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        profile_shop = self.data.item.get_shop(data["pd_id"], self.version)
        if profile is None:
            return

        mdl_have = "F" * 250
        # generate the mdl_have string if "unlock_all_modules" is disabled
        if not self.game_config.mods.unlock_all_modules:
            mdl_have = self.data.module.get_modules_have_string(
                data["pd_id"], self.version
            )

        cstmz_itm_have = "F" * 250
        # generate the cstmz_itm_have string if "unlock_all_items" is disabled
        if not self.game_config.mods.unlock_all_items:
            cstmz_itm_have = self.data.customize.get_customize_items_have_string(
                data["pd_id"], self.version
            )

        response = f"&pd_id={data['pd_id']}"
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
        response += f"&mdl_have={mdl_have}"
        response += f"&cstmz_itm_have={cstmz_itm_have}"
        response += f"&use_pv_mdl_eqp={int(profile['use_pv_mdl_eqp'])}"
        response += f"&use_mdl_pri={int(profile['use_mdl_pri'])}"
        response += f"&use_pv_skn_eqp={int(profile['use_pv_skn_eqp'])}"
        response += f"&use_pv_btn_se_eqp={int(profile['use_pv_btn_se_eqp'])}"
        response += f"&use_pv_sld_se_eqp={int(profile['use_pv_sld_se_eqp'])}"
        response += f"&use_pv_chn_sld_se_eqp={int(profile['use_pv_chn_sld_se_eqp'])}"
        response += f"&use_pv_sldr_tch_se_eqp={int(profile['use_pv_sldr_tch_se_eqp'])}"
        response += f"&vcld_pts={profile['lv_efct_id']}"
        response += f"&nxt_pv_id={profile['nxt_pv_id']}"
        response += f"&nxt_dffclty={profile['nxt_dffclty']}"
        response += f"&nxt_edtn={profile['nxt_edtn']}"
        response += f"&dsp_clr_brdr={profile['dsp_clr_brdr']}"
        response += f"&dsp_intrm_rnk={profile['dsp_intrm_rnk']}"
        response += f"&dsp_clr_sts={profile['dsp_clr_sts']}"
        response += f"&rgo_sts={profile['rgo_sts']}"

        # Contest progress
        response += f"&cv_cid=-1,-1,-1,-1"
        response += f"&cv_sc=-1,-1,-1,-1"
        response += f"&cv_bv=-1,-1,-1,-1"
        response += f"&cv_bv=-1,-1,-1,-1"
        response += f"&cv_bf=-1,-1,-1,-1"

        # Contest now playing id, return -1 if no current playing contest
        response += f"&cnp_cid={profile['cnp_cid']}"
        response += f"&cnp_val={profile['cnp_val']}"
        # border can be 0=bronzem 1=silver, 2=gold
        response += f"&cnp_rr={profile['cnp_rr']}"
        # only show contest specifier if it is not empty
        response += f"&cnp_sp={profile['cnp_sp']}" if profile["cnp_sp"] != "" else ""

        # To be fully fixed
        if "my_qst_id" not in profile:
            response += f"&my_qst_id=-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
            response += f"&my_qst_sts=0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        else:
            response += f"&my_qst_id={profile['my_qst_id']}"
            response += f"&my_qst_sts={profile['my_qst_sts']}"

        response += f"&my_qst_prgrs=0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        response += f"&my_qst_et=2022-06-19%2010%3A28%3A52.0,2022-06-19%2010%3A28%3A52.0,2022-06-19%2010%3A28%3A52.0,2100-01-01%2008%3A59%3A59.0,2100-01-01%2008%3A59%3A59.0,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx"

        # define a helper class to store all counts for clear, great,
        # excellent and perfect
        class ClearSet:
            def __init__(self):
                self.clear = 0
                self.great = 0
                self.excellent = 0
                self.perfect = 0

        # create a dict to store the ClearSets per difficulty
        clear_set_dict = {
            0: ClearSet(),  # easy
            1: ClearSet(),  # normal
            2: ClearSet(),  # hard
            3: ClearSet(),  # extreme
            4: ClearSet(),  # exExtreme
        }

        # get clear status from user scores
        pv_records = self.data.score.get_best_scores(data["pd_id"])
        clear_status = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

        if pv_records is not None:
            for score in pv_records:
                if score["edition"] == 0:
                    # cheap and standard both count to "clear"
                    if score["clr_kind"] in {1, 2}:
                        clear_set_dict[score["difficulty"]].clear += 1
                    elif score["clr_kind"] == 3:
                        clear_set_dict[score["difficulty"]].great += 1
                    elif score["clr_kind"] == 4:
                        clear_set_dict[score["difficulty"]].excellent += 1
                    elif score["clr_kind"] == 5:
                        clear_set_dict[score["difficulty"]].perfect += 1
                else:
                    # 4=ExExtreme
                    if score["clr_kind"] in {1, 2}:
                        clear_set_dict[4].clear += 1
                    elif score["clr_kind"] == 3:
                        clear_set_dict[4].great += 1
                    elif score["clr_kind"] == 4:
                        clear_set_dict[4].excellent += 1
                    elif score["clr_kind"] == 5:
                        clear_set_dict[4].perfect += 1

            # now add all values to a list
            clear_list = []
            for clear_set in clear_set_dict.values():
                clear_list.append(clear_set.clear)
                clear_list.append(clear_set.great)
                clear_list.append(clear_set.excellent)
                clear_list.append(clear_set.perfect)

            clear_status = ",".join(map(str, clear_list))

        response += f"&clr_sts={clear_status}"

        # Store stuff to add to rework
        response += f"&mdl_eqp_tm={self.time_lut}"

        mdl_eqp_ary = "-999,-999,-999"
        c_itm_eqp_ary = "-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999"
        ms_itm_flg_ary = "1,1,1,1,1,1,1,1,1,1,1,1"

        # get the common_modules, customize_items and customize_item_flags
        # from the profile shop
        if profile_shop:
            mdl_eqp_ary = profile_shop["mdl_eqp_ary"]
            c_itm_eqp_ary = profile_shop["c_itm_eqp_ary"]
            ms_itm_flg_ary = profile_shop["ms_itm_flg_ary"]

        response += f"&mdl_eqp_ary={mdl_eqp_ary}"
        response += f"&c_itm_eqp_ary={c_itm_eqp_ary}"
        response += f"&ms_itm_flg_ary={ms_itm_flg_ary}"

        return response

    def handle_pd_unlock_request(self, data: Dict) -> Dict:
        return f""

    def handle_spend_credit_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)
        if profile is None:
            return

        response = ""

        response += "&cmpgn_rslt=-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x,-1,-1,x,-1,-1,x,x,-1,x"
        response += "&cmpgn_rslt_num=0"
        response += f"&vcld_pts={profile['vcld_pts']}"
        response += f"&lv_str={profile['lv_str']}"
        response += f"&lv_efct_id={profile['lv_efct_id']}"
        response += f"&lv_plt_id={profile['lv_plt_id']}"

        return response

    def _get_pv_pd_result(
        self,
        song: int,
        pd_db_song: Dict,
        pd_db_ranking: Dict,
        pd_db_customize: Dict,
        edition: int,
    ) -> str:
        """
        Helper function to generate the pv_result string for every song, ranking and edition
        """
        global_ranking = -1
        if pd_db_ranking:
            # make sure there are enough max scores to calculate a ranking
            if pd_db_ranking["ranking"] != 0:
                global_ranking = pd_db_ranking["ranking"]

        # pv_no
        pv_result = f"{song},"
        # edition
        pv_result += f"{edition},"
        # rslt
        pv_result += f"{pd_db_song['clr_kind']}," if pd_db_song else "-1,"
        # max_score
        pv_result += f"{pd_db_song['score']}," if pd_db_song else "-1,"
        # max_atn_pnt
        pv_result += f"{pd_db_song['atn_pnt']}," if pd_db_song else "-1,"
        # challenge_kind
        pv_result += f"{pd_db_song['sort_kind']}," if pd_db_song else "0,"

        module_eqp = "-999,-999,-999"
        customize_eqp = "-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999"
        customize_flag = "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"
        # skin, btn_se, sld_se, chsld_se, sldtch_se
        pv_settings = "-1,-1,-1,-1,-1"
        if pd_db_customize:
            module_eqp = pd_db_customize["mdl_eqp_ary"]
            customize_eqp = pd_db_customize["c_itm_eqp_ary"]
            customize_flag = pd_db_customize["ms_itm_flg_ary"]
            pv_settings = (
                f"{pd_db_customize['skin']},"
                f"{pd_db_customize['btn_se']},"
                f"{pd_db_customize['sld_se']},"
                f"{pd_db_customize['chsld_se']},"
                f"{pd_db_customize['sldtch_se']}"
            )

        pv_result += f"{module_eqp},"
        pv_result += f"{customize_eqp},"
        pv_result += f"{customize_flag},"
        pv_result += f"{pv_settings},"
        # rvl_pd_id, rvl_score, rvl_attn_pnt, -1, -1
        pv_result += "-1,-1,-1,-1,-1,"
        # countrywide_ranking
        pv_result += f"{global_ranking},"
        # rgo_purchased
        pv_result += "1,1,1,"
        # rgo_played
        pv_result += "0,0,0"

        return pv_result

    def task_generateScoreData(self, data: Dict, pd_by_pv_id, song):
        
        if int(song) > 0:
            # the request do not send a edition so just perform a query best score and ranking for each edition.
            # 0=ORIGINAL, 1=EXTRA
            pd_db_song_0 = self.data.score.get_best_user_score(
                data["pd_id"], int(song), data["difficulty"], edition=0
            )
            pd_db_song_1 = self.data.score.get_best_user_score(
                data["pd_id"], int(song), data["difficulty"], edition=1
            )

            pd_db_ranking_0, pd_db_ranking_1 = None, None
            if pd_db_song_0:
                pd_db_ranking_0 = self.data.score.get_global_ranking(
                    data["pd_id"], int(song), data["difficulty"], edition=0
                )

            if pd_db_song_1:
                pd_db_ranking_1 = self.data.score.get_global_ranking(
                    data["pd_id"], int(song), data["difficulty"], edition=1
                )

            pd_db_customize = self.data.pv_customize.get_pv_customize(
                data["pd_id"], int(song)
            )

            # generate the pv_result string with the ORIGINAL edition and the EXTRA edition appended
            pv_result = self._get_pv_pd_result(
                int(song), pd_db_song_0, pd_db_ranking_0, pd_db_customize, edition=0
            )
            pv_result += "," + self._get_pv_pd_result(
                int(song), pd_db_song_1, pd_db_ranking_1, pd_db_customize, edition=1
            )

            self.logger.debug(f"pv_result = {pv_result}")
            pd_by_pv_id.append(urllib.parse.quote(pv_result))
        else:
            pd_by_pv_id.append(urllib.parse.quote(f"{song}***"))
        pd_by_pv_id.append(",")

    def handle_get_pv_pd_request(self, data: Dict) -> Dict:
        song_id = data["pd_pv_id_lst"].split(",")
        pv = ""

        threads = []
        pd_by_pv_id = []

        for song in song_id:
            thread_ScoreData = Thread(target=self.task_generateScoreData(data, pd_by_pv_id, song))
            threads.append(thread_ScoreData)

        for x in threads:
            x.start()

        for x in threads:
            x.join()

        for x in pd_by_pv_id:
            pv += x

        response = ""
        response += f"&pd_by_pv_id={pv[:-1]}"
        response += "&pdddt_flg=0"
        response += f"&pdddt_tm={self.time_lut}"

        return response

    def handle_stage_start_request(self, data: Dict) -> Dict:
        return f""

    def handle_stage_result_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)

        pd_song_list = data["stg_ply_pv_id"].split(",")
        pd_song_difficulty = data["stg_difficulty"].split(",")
        pd_song_edition = data["stg_edtn"].split(",")
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
                profile_pd_db_song = self.data.score.get_best_user_score(
                    data["pd_id"],
                    pd_song_list[index],
                    pd_song_difficulty[index],
                    pd_song_edition[index],
                )
                if profile_pd_db_song is None:
                    self.data.score.put_best_score(
                        data["pd_id"],
                        self.version,
                        pd_song_list[index],
                        pd_song_difficulty[index],
                        pd_song_edition[index],
                        pd_song_max_score[index],
                        pd_song_max_atn_pnt[index],
                        pd_song_ranking[index],
                        pd_song_sort_kind,
                        pd_song_cool_cnt[index],
                        pd_song_fine_cnt[index],
                        pd_song_safe_cnt[index],
                        pd_song_sad_cnt[index],
                        pd_song_worst_cnt[index],
                        pd_song_max_combo[index],
                    )
                    self.data.score.put_playlog(
                        data["pd_id"],
                        self.version,
                        pd_song_list[index],
                        pd_song_difficulty[index],
                        pd_song_edition[index],
                        pd_song_max_score[index],
                        pd_song_max_atn_pnt[index],
                        pd_song_ranking[index],
                        pd_song_sort_kind,
                        pd_song_cool_cnt[index],
                        pd_song_fine_cnt[index],
                        pd_song_safe_cnt[index],
                        pd_song_sad_cnt[index],
                        pd_song_worst_cnt[index],
                        pd_song_max_combo[index],
                    )
                elif int(pd_song_max_score[index]) >= int(profile_pd_db_song["score"]):
                    self.data.score.put_best_score(
                        data["pd_id"],
                        self.version,
                        pd_song_list[index],
                        pd_song_difficulty[index],
                        pd_song_edition[index],
                        pd_song_max_score[index],
                        pd_song_max_atn_pnt[index],
                        pd_song_ranking[index],
                        pd_song_sort_kind,
                        pd_song_cool_cnt[index],
                        pd_song_fine_cnt[index],
                        pd_song_safe_cnt[index],
                        pd_song_sad_cnt[index],
                        pd_song_worst_cnt[index],
                        pd_song_max_combo[index],
                    )
                    self.data.score.put_playlog(
                        data["pd_id"],
                        self.version,
                        pd_song_list[index],
                        pd_song_difficulty[index],
                        pd_song_edition[index],
                        pd_song_max_score[index],
                        pd_song_max_atn_pnt[index],
                        pd_song_ranking[index],
                        pd_song_sort_kind,
                        pd_song_cool_cnt[index],
                        pd_song_fine_cnt[index],
                        pd_song_safe_cnt[index],
                        pd_song_sad_cnt[index],
                        pd_song_worst_cnt[index],
                        pd_song_max_combo[index],
                    )
                elif int(pd_song_max_score[index]) != int(profile_pd_db_song["score"]):
                    self.data.score.put_playlog(
                        data["pd_id"],
                        self.version,
                        pd_song_list[index],
                        pd_song_difficulty[index],
                        pd_song_edition[index],
                        pd_song_max_score[index],
                        pd_song_max_atn_pnt[index],
                        pd_song_ranking[index],
                        pd_song_sort_kind,
                        pd_song_cool_cnt[index],
                        pd_song_fine_cnt[index],
                        pd_song_safe_cnt[index],
                        pd_song_sad_cnt[index],
                        pd_song_worst_cnt[index],
                        pd_song_max_combo[index],
                    )

        # Profile saving based on registration list

        # Calculate new level
        best_scores = self.data.score.get_best_scores(data["pd_id"])

        total_atn_pnt = 0
        for best_score in best_scores:
            total_atn_pnt += best_score["atn_pnt"]

        new_level = (total_atn_pnt // 13979) + 1
        new_level_pnt = round((total_atn_pnt % 13979) / 13979 * 100)

        response = "&chllng_kind=-1"
        response += f"&lv_num_old={int(profile['lv_num'])}"
        response += f"&lv_pnt_old={int(profile['lv_pnt'])}"

        # update the profile and commit changes to the db
        self.data.profile.update_profile(
            profile["user"],
            lv_num=new_level,
            lv_pnt=new_level_pnt,
            vcld_pts=int(data["vcld_pts"]),
            hp_vol=int(data["hp_vol"]),
            btn_se_vol=int(data["btn_se_vol"]),
            sldr_se_vol2=int(data["sldr_se_vol2"]),
            sort_kind=int(data["sort_kind"]),
            nxt_pv_id=int(data["ply_pv_id"]),
            nxt_dffclty=int(data["nxt_dffclty"]),
            nxt_edtn=int(data["nxt_edtn"]),
            my_qst_id=data["my_qst_id"],
            my_qst_sts=data["my_qst_sts"],
        )

        response += f"&lv_num={new_level}"
        response += f"&lv_str={profile['lv_str']}"
        response += f"&lv_pnt={new_level_pnt}"
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

        return response

    def handle_end_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)

        self.data.profile.update_profile(
            profile["user"], my_qst_id=data["my_qst_id"], my_qst_sts=data["my_qst_sts"]
        )
        return f""

    def handle_shop_exit_request(self, data: Dict) -> Dict:
        self.data.item.put_shop(
            data["pd_id"],
            self.version,
            data["mdl_eqp_cmn_ary"],
            data["c_itm_eqp_cmn_ary"],
            data["ms_itm_flg_cmn_ary"],
        )
        if int(data["use_pv_mdl_eqp"]) == 1:
            self.data.pv_customize.put_pv_customize(
                data["pd_id"],
                self.version,
                data["ply_pv_id"],
                data["mdl_eqp_pv_ary"],
                data["c_itm_eqp_pv_ary"],
                data["ms_itm_flg_pv_ary"],
            )
        else:
            self.data.pv_customize.put_pv_customize(
                data["pd_id"],
                self.version,
                data["ply_pv_id"],
                "-1,-1,-1",
                "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
                "1,1,1,1,1,1,1,1,1,1,1,1",
            )

        response = "&shp_rslt=1"
        return response

    def handle_card_procedure_request(self, data: Dict) -> str:
        profile = self.data.profile.get_profile(data["aime_id"], self.version)
        if profile is None:
            return "&cd_adm_result=0"

        response = "&cd_adm_result=1"
        response += "&chg_name_price=100"
        response += "&accept_idx=100"
        response += f"&pd_id={profile['user']}"
        response += f"&player_name={profile['player_name']}"
        response += f"&lv_num={profile['lv_num']}"
        response += f"&lv_pnt={profile['lv_pnt']}"
        response += f"&lv_str={profile['lv_str']}"
        response += f"&lv_efct_id={profile['lv_efct_id']}"
        response += f"&lv_plt_id={profile['lv_plt_id']}"
        response += f"&vcld_pts={profile['vcld_pts']}"
        response += f"&passwd_stat={profile['passwd_stat']}"

        return response

    def handle_change_name_request(self, data: Dict) -> str:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)

        # make sure user has enough Vocaloid Points
        if profile["vcld_pts"] < int(data["chg_name_price"]):
            return "&cd_adm_result=0"

        # update the vocaloid points and player name
        new_vcld_pts = profile["vcld_pts"] - int(data["chg_name_price"])
        self.data.profile.update_profile(
            profile["user"], player_name=data["player_name"], vcld_pts=new_vcld_pts
        )

        response = "&cd_adm_result=1"
        response += "&accept_idx=100"
        response += f"&pd_id={profile['user']}"
        response += f"&player_name={data['player_name']}"

        return response

    def handle_change_passwd_request(self, data: Dict) -> str:
        profile = self.data.profile.get_profile(data["pd_id"], self.version)

        # TODO: return correct error number instead of 0
        if data["passwd"] != profile["passwd"]:
            return "&cd_adm_result=0"

        # set password to true and update the saved password
        self.data.profile.update_profile(
            profile["user"], passwd_stat=1, passwd=data["new_passwd"]
        )

        response = "&cd_adm_result=1"
        response += "&accept_idx=100"
        response += f"&pd_id={profile['user']}"

        return response
