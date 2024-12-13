# -*- encoding: utf-8 -*-
"""
@File    :   Public4.py
@Time    :   2024-12-13 10:23
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   获取当前主机的公网IP地址
"""
from requests import get
from loguru import logger


def get_ipv4_public(show=False):
	"""
	获取当前主机所在网络的公网地址

	:param show: 是否打印出获取到的公网IP地址，默认为False
	:return: 返回获取到的公网IP地址字符串，如果获取失败则返回None
	"""
	# 尝试访问第一个API获取公网IP地址
	try:
		req = get('https://checkip.amazonaws.com')
		if req.status_code == 200:
			ip = req.text.strip()
			logger.info(f"当前公网IP: {ip}")
			return ip
	except Exception as e:
		logger.warning(e)

	# 如果第一个API访问失败，尝试访问第二个API获取公网IP地址
	try:
		req = get('http://icanhazip.com')
		if req.status_code == 200:
			if show:
				logger.info(f"当前公网IP: {req.text}")
			return req.text
	except Exception as e:
		logger.warning(e)

	# 如果前两个API都访问失败，尝试访问第三个API获取公网IP地址
	try:
		req = get('http://ip.liumou.site/api')
		if req.status_code == 200:
			if show:
				logger.info(f"当前公网IP: {req.text}")
			return req.text
	except Exception as e:
		logger.warning(e)
	return None


if __name__ == "__main__":
	get_ipv4_public(show=True)
