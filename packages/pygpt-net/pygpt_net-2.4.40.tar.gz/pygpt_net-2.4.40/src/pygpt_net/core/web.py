#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.12.13 00:00:00                  #
# ================================================== #
import os
import uuid

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from pygpt_net.provider.web.base import BaseProvider


class Web:
    def __init__(self, window=None):
        """
        Web access core

        :param window: Window instance
        """
        self.window = window
        self.providers = {
            "search_engine": {},
        }

    def is_registered(self, id: str, type: str = "search_engine") -> bool:
        """
        Check if provider is registered

        :param id: provider id
        :param type: provider type
        :return: True if registered
        """
        if type in self.providers:
            return id in self.providers[type]
        return False

    def get_providers(self, type: str = "search_engine") -> dict:
        """
        Get all providers

        :param type: provider type
        :return: providers dict
        """
        if type in self.providers:
            return self.providers[type]
        return {}

    def get_ids(self, type: str = "search_engine") -> list:
        """
        Get all providers ids

        :param type: provider type
        :return: providers ids list
        """
        if type in self.providers:
            return list(self.providers[type].keys())
        return []

    def get(self, id: str, type: str = "search_engine") -> BaseProvider or None:
        """
        Get provider instance

        :param id: provider id
        :param type: provider type
        :return: provider instance
        """
        if self.is_registered(id, type):
            return self.providers[type][id]
        return None

    def register(self, provider: BaseProvider):
        """
        Register provider

        :param provider: provider instance
        """
        id = provider.id
        type = provider.type
        for t in type:
            if t in self.providers:
                self.providers[t][id] = provider

    def get_main_image(self, url: str) -> str or None:
        """
        Get main image from URL

        :param url: URL to get image from
        :return: image URL
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']

        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']

        link_image = soup.find('link', rel='image_src')
        if link_image and link_image.get('href'):
            return link_image['href']

        images = soup.find_all('img')
        if images:
            images = [img for img in images if 'logo' not in (img.get('src') or '').lower()]
            largest_image = None
            max_area = 0
            for img in images:
                src = img.get('src')
                if not src:
                    continue
                src = requests.compat.urljoin(url, src)
                try:
                    img_response = requests.get(src, stream=True, timeout=5)
                    img_response.raw.decode_content = True

                    from PIL import Image
                    image = Image.open(img_response.raw)
                    width, height = image.size
                    area = width * height
                    if area > max_area:
                        max_area = area
                        largest_image = src
                except:
                    continue
            if largest_image:
                return largest_image
        return None

    def get_links(self, url: str) -> list:
        """
        Get links from URL

        :param url: URL to get links from
        :return: links list
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        urls = []
        for link in soup.find_all('a'):
            try:
                name = link.get_text(strip=True)
                address = link.get('href')
                if address:
                    address = urljoin(url, address)
                    if not name:
                        title = link.get('title')
                        if title:
                            name = title
                        else:
                            name = address
                    if address not in urls:
                        urls.append(address)
                        links.append({name: address})
            except:
                continue
        return links


    def get_images(self, url: str) -> list:
        """
        Get images from URL

        :param url: URL to get images from
        :return: images list
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = []
        for img in soup.find_all('img'):
            try:
                address = img.get('src')
                if address:
                    address = urljoin(url, address)
                    if address not in images:
                        images.append(address)
            except:
                continue
        return images

    def download_image(self, img: str) -> str:
        """
        Download image from URL

        :param img: URL to download image from
        :return: local path to image
        """
        dir = self.window.core.config.get_user_dir("img")
        response = requests.get(img, stream=True)
        name = img.replace("http://", "").replace("https://", "").replace("/", "_")
        path = os.path.join(dir, name)
        if os.path.exists(path):
            name = name + uuid.uuid4().hex[:6].upper()
        download_path = os.path.join(dir, name)
        with open(download_path, 'wb', ) as f:
            f.write(response.content)
        return self.window.core.filesystem.make_local(download_path)
