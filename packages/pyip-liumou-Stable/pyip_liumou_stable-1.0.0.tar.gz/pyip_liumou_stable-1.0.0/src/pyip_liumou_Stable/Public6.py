#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Public6.py
@Time    :   2024-12-13 10:28
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import platform
import re
import socket
from subprocess import getstatusoutput

from loguru import logger


def _socket_get_ipv6_public(show: bool):
	"""
	使用socket编程获取IPv6公网地址。

	参数:
	show (bool): 是否显示日志信息。

	返回:
	str: 成功时返回IPv6公网地址，失败时返回None。
	"""
	try:
		# 尝试通过socket编程获取IPv6地址
		sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		sock.connect(('test6.ustc.edu.cn', 443))
		ip = sock.getsockname()[0]
		sock.close()
		# 如果show为True，打印调试日志
		if show:
			logger.debug(f"当前IPv6公网地址是: {ip}")
		return ip
	except Exception as e:
		# 如果show为True，打印警告日志
		if show:
			logger.warning(f"通过socket请求的方式获取IPV6失败: {str(e)}")
	return None


def _linux_get_ipv6_public_ip_a(show: bool):
	"""
	获取Linux系统的IPv6公网地址。

	参数:
	show (bool): 是否显示IPv6地址的调试信息。

	返回:
	str: IPv6地址字符串，如果获取失败则返回None。
	"""
	# 检测是否存在ip a命令
	res = getstatusoutput("which ip")
	if res[0] != 0:
		logger.warning("未检测到ip a命令,请自行安装...")
		return None

	# 执行ip a命令获取IPv6地址信息，并进行过滤和格式化
	txt = getstatusoutput(
		"ip a | grep inet6 | grep global| grep ^24 | awk '{print $2}' | awk -F / '{print $1}' | sed -n 1p")
	if txt[0] == 0:
		ip = txt[1].strip()
		# 如果show参数为True，则记录调试信息
		if show:
			logger.debug(f"当前IPv6公网地址是: {ip}")
		return ip
	else:
		logger.warning("通过 ip a 命令获取IPV6失败...")


def _linux_get_ipv6_public_ifconfig(show: bool):
	"""
	使用ifconfig命令获取Linux系统的IPv6公网地址。

	参数:
	show (bool): 是否打印日志信息。

	返回:
	str: IPv6公网地址，如果获取失败则返回None。
	"""
	# 检测是否存在ifconfig命令
	res = getstatusoutput("which ifconfig")
	if res[0] != 0:
		# 如果没有找到ifconfig命令，记录警告日志并返回None
		logger.warning("未检测到ifconfig命令,请自行安装...")
		return None

	# 执行ifconfig命令并解析输出，提取IPv6地址
	txt = getstatusoutput("ifconfig  | grep inet6 | awk '{print $2}' | grep ^240").split("\n")
	if txt[0] == 0:
		# 提取成功，根据show参数决定是否打印日志
		ip_ = txt[0].strip()
		if show:
			logger.debug(f"当前IPv6公网地址是: {ip_}")
		return ip_
	else:
		# 提取失败，记录警告日志
		logger.warning("通过 ifconfig 命令获取IPV6失败...")


def _windows_get_ipv6_public(show: bool):
	"""
	在Windows系统中获取公网IPv6地址。

	该函数通过执行ipconfig命令来获取系统的所有IP配置信息，然后从中寻找以240开头的IPv6地址，
	这通常是中国移动分配的公网IPv6地址。如果找到匹配的IPv6地址，函数会返回该地址；如果未找到，
	或者执行命令失败，则返回None。

	参数:
	show (bool): 一个布尔值，指示是否在找到IPv6地址时打印日志信息。如果为True，则打印；
				 如果为False，则不打印。

	返回:
	str: 找到的IPv6公网地址，如果没有找到或获取失败，则返回None。
	"""
	# 执行ipconfig /all命令获取IP配置信息
	res, txt = getstatusoutput("ipconfig")
	# 如果命令执行失败，记录警告日志并返回None
	if res != 0:
		logger.warning("通过 ipconfig 命令获取IPV6失败...")
		return None
	# 使用正则匹配240开头的IPV6地址
	pattern = re.compile(r".*240.*")
	# 遍历每一行输出，寻找匹配的IPv6地址
	for line in txt.split("\n"):
		match = pattern.match(line)
		if match:
			# 找到匹配的IPv6地址
			ip_ = match.group(0).split(" ")[-1]
			# 如果show参数为True，打印当前IPv6公网地址的日志信息
			if show:
				logger.debug(f"当前IPv6公网地址是: {ip_}")
			# 返回找到的IPv6地址
			return ip_
	logger.warning("通过ipconfig命令未找到IPV6公网地址...")
	# 如果没有找到匹配的IPv6地址，返回None
	return None


def get_ipv6_public(show=False):
	"""
	获取本机的IPv6公共地址。

	本函数尝试通过多种方法获取本机的IPv6公共地址。首先，它尝试使用一个私有方法
	_socket_get_ipv6_public(show) 来获取地址。如果该方法失败，它将根据操作系统的类型
	使用特定的方法来获取IPv6地址。

	参数:
	show (bool): 一个可选的布尔参数，决定是否显示获取IPv6地址的过程信息。默认为False。

	返回:
	str: 本机的IPv6公共地址，如果无法获取，则返回None。
	"""
	# 记录获取IPv6公共地址的开始
	logger.debug("开始获取本机IPV6地址")

	# 尝试通过私有方法获取IPv6公共地址
	ipv6_public = _socket_get_ipv6_public(show)
	if ipv6_public:
		return ipv6_public

	# 根据操作系统类型选择合适的获取IPv6地址的方法
	os_name = platform.system()
	if os_name == "Linux":
		# 对于Linux系统，优先使用'ip a'命令，备选使用'ifconfig'
		return _linux_get_ipv6_public_ip_a(show) or _linux_get_ipv6_public_ifconfig(show)
	elif os_name == "Windows":
		# 对于Windows系统，使用特定的Windows方法
		return _windows_get_ipv6_public(show)


if __name__ == '__main__':
	print(get_ipv6_public(show=True))
