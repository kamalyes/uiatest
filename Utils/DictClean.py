# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DictClean.py
# Author : v_yanqyu
# Desc: Yaml格式文本内容
# Date： 2020/10/9 17:11
'''
import yaml,json
from Logger.GlobalLog import Logger
logger = Logger.write_log()

# 初始化列表、及yaml文件的异常抛出
tmp_list = []
yaml.warnings({'YAMLLoadWarning': False})  # 禁用加载器warnings报警

class YamlHandle():

    @classmethod
    def changetype(self,filepath):
        """
        Json或Yaml格式化
        :param target: 目标文件路径
        :param local:  转化源文件路径
        """
        try:
            with open(filepath, encoding='utf-8') as file:
                data = yaml.safe_load(file)
                dumps = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
                return dumps
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def yamldata(self,filepath):
        """
        定义对应的yaml路径输出dict类型的data、
        :param filepath: 目标文件路径
        :return: data
        """
        try:
            with open(filepath, encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if not isinstance(data, dict):
                    return False
                else:
                    return data
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def getdict(self,key,data):
        """
        输出dict类型的data--value值
        :param filepath: 目标文件路径
        :return: tmp_list
        """
        if not isinstance(data, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
            return 'argv[1] not an dict or argv[-1] not an list '
        logger.info("拆分数据---%s" % (data))
        if key in data.keys():
            tmp_list.append(data[key])

        for value in data.values():
            if isinstance(value, dict):
                self.getdict(key=key, data=value)
            elif isinstance(value, (list, tuple)):
                for mony in value:
                    if isinstance(mony, dict):
                        self.getdict(key=key, data=mony)
                    elif isinstance(mony, (list, tuple)):
                        self.getdict(key, data=mony)
        return tmp_list

    @classmethod
    def writeyaml(self,filepath,data,method):
        """
        将dict类型数据写入yaml
        :param filepath: 目标文件路径
        :param data:     json实体即dict类型的数据
        :param method:   w：全新写入、a：追加数据
        """
        try:
            if method == "w":
                with open(filepath, "w", encoding="utf-8") as file:
                    yaml.dump(data, file)
            elif method == "a":
                with open(filepath, "a+", encoding="utf-8") as file:
                    yaml.dump(data, file)
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def StrToJson(self,method=None,string=None):
        """
        Str文本内容与JSON格式互转
        :param method: 流转方式判断
        :param string: 字符
        :return: result：返回结果集 False：为空时返回
        """
        result = {}
        if method == "BodyToJson":
            str = string.split('&')
            for i in range(0, len(str)):
                string = str[i].split('=')
                result[string[0]] = string[1];
            logger.info(result)
        else:
            logger.error("该内容不支持转换、请检查是否为JSON或Body类型")
        return result

if __name__ == '__main__':
    data = YamlHandle.yamldata(filepath = r'..\YamlData\Register.yaml')
    logger.info(YamlHandle.getdict(key="name", data=data))
    # logger.info(YamlHandle.changetype(filepath=r'..\YamlData\Register.yaml'))
    YamlHandle.writeyaml(filepath = r'..\YamlData\Token.yaml',data={'a':'b'},method="w")
    changetype =  YamlHandle.StrToJson(method="BodyToJson",string="staticpage=https%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fv3Jump.html&charset=UTF-8&token=a4138308fb95245960278f243aa65909&tpl=mn&subpro=&apiver=v3&tt=1602858805524&codestring=&safeflg=0&u=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D1%26tn%3Dbaidu%26wd%3Dpython%2520post%2520api%26oq%3Dpython%252520json%2525E8%2525BD%2525ACurl%26rsv_pq%3Dfb573a98000064de%26rsv_t%3Db9efnU8i%252FPHVpQCoVWWz%252BcBkafNfsnvjP0kjUDHzeV0whPhs9%252BzM7PFP%252FE8%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_dl%3Dtb%26rsv_btype%3Dt%26inputT%3D2303%26rsv_sug3%3D31%26rsv_sug1%3D29%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D3168&isPhone=&detect=1&gid=3B69936-1515-4325-A844-7145741F6EF6&quick_user=0&logintype=dialogLogin&logLoginType=pc_loginDialog&idc=&loginmerge=true&mkey=&splogin=rate&username=proxy.example.com&password=Roeayn14i5gkgjBBCEEJM2%2BXLFhb1SVwCr9NmXF3Lu5YDbOURqKCicIBCgSIoWPLrjWoY2gfcTAltOX24Svx0FUizer0b4uBC4poPVTltFQ%2FFekx3tsCHpB2TZZrh5LHYX1kX6%2Bu5genEUFAu%2BHc%2BffMSQS1Jo7BP6BBeBNcyhU%3D&mem_pass=on&rsakey=r3e4IPPrJC9wvSAmTu1PjlbELueRTIYA&crypttype=12&ppui_logintime=18593&countrycode=&fp_uid=&fp_info=&loginversion=v4&supportdv=1&ds=ywfQIaE7gHSu4SojnEGj9J%2BoM6d1knwWZKekhpUz759ElRoa4szd%2BehKlbBFYMRMjOZCOGX0hAQ9Odp3x0vf%2Bk9uD%2BSDW9qtVBWRZIefUXAUoqI0jk3x%2FXZ%2Fw5b39P7hJzpohSf9LmdiOHEM2oRLc2CWmAQXgsGNY4BqASzEcb6Yg7jTEsZDIj%2B3obfQf1JkXThx9kA1o6VdV7HKeAVAKUUlND2fkUgTx0XEoJMRI7We5C84Go2TNSGVOJvYMGbO9qaTQ13VoGlrE5LIvPM%2BCNxqLV7Mn7TlaS6VTi4QtH8HNK0NLqC9jv7TLMP6KTmzcHrDfcDTIBTUTi4Y9CesyoS1qlO28mRvPYwdnJopi46aPjYNX22So%2F7beL6NjYE9vURmHWXfiapnh%2Bb3bgEXWHSNkervLciAGvnt2Et%2BHFf%2BA2qf0rXuamXj8qNP3v53IQRRyETijh%2Ffgj0x7iZIZmUdELZG2%2BuFvYJkTrCkH6zYuO9JU%2F9Yyr2F%2BJrraUFuyNSSp%2FvFCYx2S9tpSwBth0sdK7M8TUNSouFN5PAagK6OMgyXA46C3ZijPNTYq5KNUukBZjdiOR9BAooy5R%2B%2FlafEl6gYAjRqwabD4hwLy88fR0SQ7rUsvfMx19eJ0VEseiJbOsET86i%2F%2B%2BD7mBMqluGf5qbOr0tUYdaKyTxkeaR1FDTsW2knZSr8wjmkxbFeJOUw4O6K5mwR3If5E7Ea7vJJUJt%2BeH9H2Kk41n26Xtz0wcMf1tKLBlJEnt%2Bj8scFFV978vR%2FVqivGaUiYtLWMWv0KirbJv4ebYq%2Bk5mpsB9gjFgz5enpSmRaRyDAF9ZYBFTciLJSgNfmsjabK4USWg%3D%3D&tk=19950jH9xSfSY7GVxNBukyWA0vSAkZGcixZJ0o2kmvxs0i0xvG19q5IrK1G94KKxka%2BPS%2FJsvt%2FkVEa2vYlGWcE5soviU7Krz4Lgqx%2F0Wcuz6hw%3D&dv=tk0.170610517441676551602858787505%40ddr0Eu5AHX5mpJ7JlsJWt09yx7JyhQ5AtQ9-Fbu96DoIy38kWpDkhZDkoX5GpJ7JlsJWt09yx7JyhQ5AtQ9-Fbu96DoIy38kWODkVZ5AHX5mpJ7JlsJWt09yx7JyhQ5AtQ9-hVH-0-P-6W8kWl51VZDkoX5GpJ7JlsJWt09yx7JyhQ5AtQ9-hVH-0-P-6W8knv5A7yQq__ur0BuDA5-8knvDANX5bNp0EpZDkJO8kN%7E5wvT017l8tChAWRG7JyQ9yhAJtZp5FxQH2tbH-RYHLCZDkNT8kNO0Evl5bNw8tChAWRG7JyQ9yhAJtZp5FxQH2tbH-RYHLCZDkNy8kWp5Evp0bJ%7E5GpJ7JlsJWt09yx7JyhQ5AtQ9TuYHLyZxzzK%7EzC1ZKEQhCri5Gvw8kNTIrvR2Xv81n-5kop5kJp0b7O5Ao-01Jy5Aov51NyDkH%7E0bJv07__irHKmpyPLC3uL3duI7_GrY5mvv8knl5k5X5AW-5EvpDA4v8knvDkqX5AWw5mvpDA4v8knv0kq_&fuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf%2B4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq%2FXx%2BRgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGnM8pC1lL8A968jg2BZc0spVtTBoyc02EPnAtVJLy%2Fw7zgkEzvTndD5TIJMSPsWB3ie1CIdYG93vRnWsgHk0XZA8DwEU0%2Fy7Co%2B45ey7DGF3%2B1GndupQWBh42Q%2FdotBPmRmY%2FbZsltL31yecxX438XQXOMFhzdVk7wLcUko9%2F9Wk6JLwMdIdH%2BeEAlE3PHwsfIZaGhxes%2Bnljx68Dx7ernR3BLhoNACSIWjkgKwIzw9ZfFRJRlLRF5lgkw8bqcKzE0mWEjZTJ4kDpCuhkUx6VHu2dM1L%2BksxZx66zR7vnv9Qw%2BatOF9qyaEMmswVwF%2BhKsAC%2FcsJ%2FVjv98cvc9NJ%2F2%2BJ3%2B7ZUtfiHWcG3HwQXTt4IyFZW%2F7aqNs9XtmFeTet5pZEUR6yjez8pz2f9Re1R81TWweIJ1usJbnJiy5Iz1I8YNmyXsWFMArDuoi7fy8VmKr4NFzxVt%2FuM6I33E97SU51kdSEYdnzasvmNMKwgvBxDAwTSlYPHdP4AvKdsJeaJnEQQPYQGiB5bg%2BLsvIyi0bCQOSOvDt0g4vx4f5qQu9McVgqAaNKAYmDvXsVenTCvzprvx3biIbQO2PlIZs9VSLupreSJxjVFe7rNvkggmnHIZyl4Ta8Doswco0jETA1UqprWp6dHwWMVnsTKjLB9fSXuGhjo502NPUieF8dd25UqH3Fuk14xmFZbz4P4dFSRFxd50Wn%2FLokT6CZ8VG%2BklTgWG1qSn%2BFhTyUoWae0%2BIqHo4ZqOntHnY72VdHXZlgRfXe4z5I%2BYWwRarkCjOEvrQMRQ8ECTh6v0JXDgToejulfHEk0MlL4OWxuq7efgjrm6OWL%2FetDxmTUyOZM6zP36ROo4zi6mydDohar%2FN5lMi0wKAelCG6GviKnveGie7OgmF8kmo9RJfTW%2BIP3sZd%2FDuR%2F5Hpqzck8ARex050OxYQCAmf5kxWsQsjulfPwmSj1e%2Fe5IMej8LeSYUutq68RilSDcVuoSozomZEeqTBGFIlNEyLiQkkf9yWTqlE7aGE7rNGzN5i8XJcI9K4nmjKg6CgI8pcTx9fvdY5nSYCUXWZw%3D%3D&traceid=F90C0001&callback=parent.bd__pcbs__hpowxe&time=1602858806&alg=v3&sig=eFh4clp0cXhtUnNLdk1mQXBOdG9vRTRvRDlLa2RWQkswamFSMElGeWlvckc1WnVnSndscUM1THpMMWxjZzBDOA%3D%3D&elapsed=2&shaOne=008433f0226ff8e28f7e7cb37037720e8edbf9b3")
    changetype =  YamlHandle.StrToJson(method="JsonToBody",string="{'staticpage': 'https%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fv3Jump.html', 'charset': 'UTF-8', 'token': 'a4138308fb95245960278f243aa65909', 'tpl': 'mn', 'subpro': '', 'apiver': 'v3', 'tt': '1602858805524', 'codestring': '', 'safeflg': '0', 'u': 'https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D1%26tn%3Dbaidu%26wd%3Dpython%2520post%2520api%26oq%3Dpython%252520json%2525E8%2525BD%2525ACurl%26rsv_pq%3Dfb573a98000064de%26rsv_t%3Db9efnU8i%252FPHVpQCoVWWz%252BcBkafNfsnvjP0kjUDHzeV0whPhs9%252BzM7PFP%252FE8%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_dl%3Dtb%26rsv_btype%3Dt%26inputT%3D2303%26rsv_sug3%3D31%26rsv_sug1%3D29%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D3168', 'isPhone': '', 'detect': '1', 'gid': '3B69936-1515-4325-A844-7145741F6EF6', 'quick_user': '0', 'logintype': 'dialogLogin', 'logLoginType': 'pc_loginDialog', 'idc': '', 'loginmerge': 'true', 'mkey': '', 'splogin': 'rate', 'username': 'proxy.example.com', 'password': 'Roeayn14i5gkgjBBCEEJM2%2BXLFhb1SVwCr9NmXF3Lu5YDbOURqKCicIBCgSIoWPLrjWoY2gfcTAltOX24Svx0FUizer0b4uBC4poPVTltFQ%2FFekx3tsCHpB2TZZrh5LHYX1kX6%2Bu5genEUFAu%2BHc%2BffMSQS1Jo7BP6BBeBNcyhU%3D', 'mem_pass': 'on', 'rsakey': 'r3e4IPPrJC9wvSAmTu1PjlbELueRTIYA', 'crypttype': '12', 'ppui_logintime': '18593', 'countrycode': '', 'fp_uid': '', 'fp_info': '', 'loginversion': 'v4', 'supportdv': '1', 'ds': 'ywfQIaE7gHSu4SojnEGj9J%2BoM6d1knwWZKekhpUz759ElRoa4szd%2BehKlbBFYMRMjOZCOGX0hAQ9Odp3x0vf%2Bk9uD%2BSDW9qtVBWRZIefUXAUoqI0jk3x%2FXZ%2Fw5b39P7hJzpohSf9LmdiOHEM2oRLc2CWmAQXgsGNY4BqASzEcb6Yg7jTEsZDIj%2B3obfQf1JkXThx9kA1o6VdV7HKeAVAKUUlND2fkUgTx0XEoJMRI7We5C84Go2TNSGVOJvYMGbO9qaTQ13VoGlrE5LIvPM%2BCNxqLV7Mn7TlaS6VTi4QtH8HNK0NLqC9jv7TLMP6KTmzcHrDfcDTIBTUTi4Y9CesyoS1qlO28mRvPYwdnJopi46aPjYNX22So%2F7beL6NjYE9vURmHWXfiapnh%2Bb3bgEXWHSNkervLciAGvnt2Et%2BHFf%2BA2qf0rXuamXj8qNP3v53IQRRyETijh%2Ffgj0x7iZIZmUdELZG2%2BuFvYJkTrCkH6zYuO9JU%2F9Yyr2F%2BJrraUFuyNSSp%2FvFCYx2S9tpSwBth0sdK7M8TUNSouFN5PAagK6OMgyXA46C3ZijPNTYq5KNUukBZjdiOR9BAooy5R%2B%2FlafEl6gYAjRqwabD4hwLy88fR0SQ7rUsvfMx19eJ0VEseiJbOsET86i%2F%2B%2BD7mBMqluGf5qbOr0tUYdaKyTxkeaR1FDTsW2knZSr8wjmkxbFeJOUw4O6K5mwR3If5E7Ea7vJJUJt%2BeH9H2Kk41n26Xtz0wcMf1tKLBlJEnt%2Bj8scFFV978vR%2FVqivGaUiYtLWMWv0KirbJv4ebYq%2Bk5mpsB9gjFgz5enpSmRaRyDAF9ZYBFTciLJSgNfmsjabK4USWg%3D%3D', 'tk': '19950jH9xSfSY7GVxNBukyWA0vSAkZGcixZJ0o2kmvxs0i0xvG19q5IrK1G94KKxka%2BPS%2FJsvt%2FkVEa2vYlGWcE5soviU7Krz4Lgqx%2F0Wcuz6hw%3D', 'dv': 'tk0.170610517441676551602858787505%40ddr0Eu5AHX5mpJ7JlsJWt09yx7JyhQ5AtQ9-Fbu96DoIy38kWpDkhZDkoX5GpJ7JlsJWt09yx7JyhQ5AtQ9-Fbu96DoIy38kWODkVZ5AHX5mpJ7JlsJWt09yx7JyhQ5AtQ9-hVH-0-P-6W8kWl51VZDkoX5GpJ7JlsJWt09yx7JyhQ5AtQ9-hVH-0-P-6W8knv5A7yQq__ur0BuDA5-8knvDANX5bNp0EpZDkJO8kN%7E5wvT017l8tChAWRG7JyQ9yhAJtZp5FxQH2tbH-RYHLCZDkNT8kNO0Evl5bNw8tChAWRG7JyQ9yhAJtZp5FxQH2tbH-RYHLCZDkNy8kWp5Evp0bJ%7E5GpJ7JlsJWt09yx7JyhQ5AtQ9TuYHLyZxzzK%7EzC1ZKEQhCri5Gvw8kNTIrvR2Xv81n-5kop5kJp0b7O5Ao-01Jy5Aov51NyDkH%7E0bJv07__irHKmpyPLC3uL3duI7_GrY5mvv8knl5k5X5AW-5EvpDA4v8knvDkqX5AWw5mvpDA4v8knv0kq_', 'fuid': 'FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf%2B4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq%2FXx%2BRgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGnM8pC1lL8A968jg2BZc0spVtTBoyc02EPnAtVJLy%2Fw7zgkEzvTndD5TIJMSPsWB3ie1CIdYG93vRnWsgHk0XZA8DwEU0%2Fy7Co%2B45ey7DGF3%2B1GndupQWBh42Q%2FdotBPmRmY%2FbZsltL31yecxX438XQXOMFhzdVk7wLcUko9%2F9Wk6JLwMdIdH%2BeEAlE3PHwsfIZaGhxes%2Bnljx68Dx7ernR3BLhoNACSIWjkgKwIzw9ZfFRJRlLRF5lgkw8bqcKzE0mWEjZTJ4kDpCuhkUx6VHu2dM1L%2BksxZx66zR7vnv9Qw%2BatOF9qyaEMmswVwF%2BhKsAC%2FcsJ%2FVjv98cvc9NJ%2F2%2BJ3%2B7ZUtfiHWcG3HwQXTt4IyFZW%2F7aqNs9XtmFeTet5pZEUR6yjez8pz2f9Re1R81TWweIJ1usJbnJiy5Iz1I8YNmyXsWFMArDuoi7fy8VmKr4NFzxVt%2FuM6I33E97SU51kdSEYdnzasvmNMKwgvBxDAwTSlYPHdP4AvKdsJeaJnEQQPYQGiB5bg%2BLsvIyi0bCQOSOvDt0g4vx4f5qQu9McVgqAaNKAYmDvXsVenTCvzprvx3biIbQO2PlIZs9VSLupreSJxjVFe7rNvkggmnHIZyl4Ta8Doswco0jETA1UqprWp6dHwWMVnsTKjLB9fSXuGhjo502NPUieF8dd25UqH3Fuk14xmFZbz4P4dFSRFxd50Wn%2FLokT6CZ8VG%2BklTgWG1qSn%2BFhTyUoWae0%2BIqHo4ZqOntHnY72VdHXZlgRfXe4z5I%2BYWwRarkCjOEvrQMRQ8ECTh6v0JXDgToejulfHEk0MlL4OWxuq7efgjrm6OWL%2FetDxmTUyOZM6zP36ROo4zi6mydDohar%2FN5lMi0wKAelCG6GviKnveGie7OgmF8kmo9RJfTW%2BIP3sZd%2FDuR%2F5Hpqzck8ARex050OxYQCAmf5kxWsQsjulfPwmSj1e%2Fe5IMej8LeSYUutq68RilSDcVuoSozomZEeqTBGFIlNEyLiQkkf9yWTqlE7aGE7rNGzN5i8XJcI9K4nmjKg6CgI8pcTx9fvdY5nSYCUXWZw%3D%3D', 'traceid': 'F90C0001', 'callback': 'parent.bd__pcbs__hpowxe', 'time': '1602858806', 'alg': 'v3', 'sig': 'eFh4clp0cXhtUnNLdk1mQXBOdG9vRTRvRDlLa2RWQkswamFSMElGeWlvckc1WnVnSndscUM1THpMMWxjZzBDOA%3D%3D', 'elapsed': '2', 'shaOne': '008433f0226ff8e28f7e7cb37037720e8edbf9b3'}")