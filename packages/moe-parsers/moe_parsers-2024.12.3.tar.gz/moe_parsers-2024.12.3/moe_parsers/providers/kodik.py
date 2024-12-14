from typing import List, Literal
from json import loads
from base64 import b64decode
from ..classes import Anime, Parser, ParserParams, Exceptions, M3U8Playlist, Media


class KodikVideo(Media):
    def __init__(self, **kwargs):
        """
        Kodik player cloud video, file access is temporary, should be used only for downloading or otherwise be ready for 403 (Forbidden)
        """
        self.cloud_url: str = kwargs["cloud_url"] if "cloud_url" in kwargs else None
        self.max_quality: int = (
            kwargs["max_quality"] if "max_quality" in kwargs else None
        )
        self.iframe: str = kwargs["iframe"] if "iframe" in kwargs else None
        self.episode_num: int = (
            kwargs["episode_num"] if "episode_num" in kwargs else None
        )
        self.translation_id: int = (
            kwargs["translation_id"] if "translation_id" in kwargs else None
        )
        self.parser: KodikParser = (
            kwargs["parser"] if "parser" in kwargs else KodikParser()
        )

    async def get_m3u8(self) -> str:
        return await self.parser.get_m3u8(self.cloud_url)


class KodikIframe(Media):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser: KodikParser = (
            kwargs["parser"] if "parser" in kwargs else KodikParser()
        )


class KodikEpisode(Anime.Episode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser: KodikParser = (
            kwargs["parser"] if "parser" in kwargs else KodikParser()
        )

    async def get_video(
        self, translation_id: str | int = 0
    ) -> KodikVideo | KodikIframe:
        iframe = KodikIframe(
            url=await self.parser.get_iframe(
                self.anime_id, self.id_type, self.episode_num, translation_id
            )
        )
        if iframe not in self.videos:
            self.videos += [iframe]
        return iframe

    async def get_videos(self, translations: list = None) -> List[KodikIframe]:
        if not translations:
            translations = (await self.parser.get_info(self.anime_id, self.id_type))[
                "translations"
            ]
        for translation in translations:
            episodes_translated = (
                translation.get("name", "").split("(")[-1].split(" ")[0]
            )
            if (
                episodes_translated.isdigit()
                and int(episodes_translated) < self.episode_num
            ):
                continue
            iframe = await self.get_video(translation["id"])
            if iframe not in self.videos:
                self.videos += [iframe]
        return self.videos


class KodikAnime(Anime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser: KodikParser = (
            kwargs["parser"] if "parser" in kwargs else KodikParser()
        )

    async def get_info(self) -> dict:
        info = await self.parser.get_info(self.anime_id, self.id_type)
        self.total_episodes = info["episode_count"]
        self.translations = info["translations"]
        await self.get_episodes()
        return info

    async def get_episodes(self) -> List[KodikEpisode]:
        if "total_episodes" not in self.__dict__ or not self.__dict__["total_episodes"]:
            await self.get_info()
        self.episodes: List[KodikEpisode] = [
            KodikEpisode(
                episode_num=x + 1,
                anime_id=self.anime_id,
                parser=self.parser,
                id_type="shikimori",
                anime_url=self.__dict__.get("link", None),
                status=Anime.Episode.Status.RELEASED
                if int(
                    (self.translations[0].get("name", "1").split("(")[-1].split(" ")[0])
                )
                >= x + 1
                else Anime.Episode.Status.UNKNOWN,
            )
            for x in range(self.__dict__.get("total_episodes", 1))
        ]
        return self.episodes

    async def get_translations(self) -> dict:
        self.translations = (await self.parser.get_info(self.anime_id, self.id_type))[
            "translations"
        ]
        return self.translations

    async def get_video(
        self, episode_num: int = 0, translation_id: int = None
    ) -> KodikVideo:
        if not self.episodes:
            await self.get_episodes()
        if not self.translations:
            self.translations = await self.get_translations()
        if not translation_id or str(translation_id) not in [
            translation["id"] for translation in self.translations
        ]:
            translation_id = self.translations[0]["id"]
        for episode in self.episodes:
            if episode.episode_num == episode_num:
                return await episode.get_video(translation_id)

    async def get_videos(self) -> List[KodikVideo]:
        if not self.episodes:
            await self.get_episodes()
        if not self.translations:
            self.translations = await self.get_translations()
        for episode in self.episodes:
            await episode.get_videos(self.translations)
        return [
            [video for video in episode.videos if video] for episode in self.episodes
        ]


class KodikParser(Parser):
    def __init__(self, **kwargs):
        """
        Kodik Parser

        Args:
            **kwargs: Additional keyword arguments to pass to the parent Parser class.

        Original parser code reference: https://github.com/YaNesyTortiK/AnimeParsers
        """
        self.params = ParserParams(
            base_url="https://kodik.info/",
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
            },
            language=Parser.Language.RU,
        )
        self.token = None
        super().__init__(self.params, **kwargs)

    async def convert2anime(self, **kwargs) -> KodikAnime:
        anime = KodikAnime(
            orig_title=kwargs["title_orig"],
            title=kwargs["title"],
            all_titles=kwargs.get("other_title", [])
            + kwargs.get("other_titles_en", [])
            + kwargs.get("other_titles_jp", []),
            anime_id=kwargs["shikimori_id"],
            url="https:" + kwargs["link"],
            parser=self,
            id_type="shikimori",
            language=self.language,
            data=kwargs,
            status=Anime.Status.COMPLETED
            if kwargs.get("all_status", "") == "released"
            else (
                Anime.Status.ONGOING
                if kwargs.get("all_status", "") == "ongoing"
                else (Anime.Status.UNKNOWN)
            ),
            year=kwargs.get("year", None),
            description=kwargs.get("description", None),
            type=Anime.Type.TV
            if kwargs.get("anime_kind", "") == "tv"
            else (
                Anime.Type.MOVIE
                if kwargs.get("anime_kind", "") == "movie"
                else (Anime.Type.UNKNOWN)
            ),
            episode_count=kwargs.get("episode_count", 0),
            translations=kwargs.get("translations", None),
        )
        return anime

    async def obtain_token(self) -> str:
        script_url = "https://kodik-add.com/add-players.min.js?v=2"
        data = await self.get(script_url, text=True)
        token = data[data.find("token=") + 7 :]
        token = token[: token.find('"')]
        self.token = token
        return token

    async def search(
        self,
        query: str | int,
        limit: int = 25,
        id_type: Literal["shikimori", "kinopoisk", "imdb"] = None,
        strict: bool = False,
        with_details: bool = False,
    ) -> List[KodikAnime]:
        if not self.token:
            await self.obtain_token()

        search_params = {
            "token": self.token,
            "limit": limit,
            "with_material_data": "true",
            "strict": "true" if strict else "false",
        }

        if isinstance(query, int) or id_type:
            search_params[f"{id_type}_id"] = query
        else:
            search_params["title"] = query

        response = await self.post("https://kodikapi.com/search", data=search_params)

        if not response["total"]:
            return []

        results = response["results"]
        animes = []
        added_titles = set()

        for result in results:
            if result["type"] not in ["anime-serial", "anime"]:
                continue

            if result["title"] not in added_titles:
                info = {}
                if with_details:
                    info = await self.get_anime_info(result["id"])
                animes.append(
                    {
                        "id": result["id"],
                        "title": result["title"],
                        "title_orig": result.get("title_orig"),
                        "other_title": (result.get("other_title", [])).split(" / "),
                        "type": result.get("type"),
                        "year": result.get("year"),
                        "screenshots": result.get("screenshots"),
                        "shikimori_id": result.get("shikimori_id"),
                        "kinopoisk_id": result.get("kinopoisk_id"),
                        "imdb_id": result.get("imdb_id"),
                        "worldart_link": result.get("worldart_link"),
                        "link": result.get("link"),
                        "all_status": result.get("all_status"),
                        "description": result.get("material_data", {}).get(
                            "description", None
                        ),
                        "other_titles_en": result.get("other_titles_en", []),
                        "other_titles_jp": result.get("other_titles_jp", []),
                        "episode_count": info.get("episode_count", 0),
                        "translations": info.get("translations", None),
                    }
                )
                added_titles.add(result["title"])

        for i, result in enumerate(animes):
            animes[i] = await self.convert2anime(**result)

        return animes

    async def translations(
        self, anime_id: str, id_type: Literal["shikimori", "kinopoisk", "imdb"]
    ) -> list:
        data = await self.get_info(anime_id, id_type)
        return data["translations"]

    async def episode_count(
        self, anime_id: str, id_type: Literal["shikimori", "kinopoisk", "imdb"]
    ) -> int:
        data = await self.get_info(anime_id, id_type)
        return data["episode_count"]

    async def _link_to_info(
        self,
        anime_id: str,
        id_type: Literal["shikimori", "kinopoisk", "imdb"] = "shikimori",
    ) -> str:
        if id_type == "shikimori":
            url = f"https://kodikapi.com/get-player?title=Player&hasPlayer=false&url=https%3A%2F%2Fkodikdb.com%2Ffind-player%3FshikimoriID%3D{anime_id}&token={self.token}&shikimoriID={anime_id}"
        elif id_type == "kinopoisk":
            url = f"https://kodikapi.com/get-player?title=Player&hasPlayer=false&url=https%3A%2F%2Fkodikdb.com%2Ffind-player%3FkinopoiskID%3D{anime_id}&token={self.token}&kinopoiskID={anime_id}"
        elif id_type == "imdb":
            url = f"https://kodikapi.com/get-player?title=Player&hasPlayer=false&url=https%3A%2F%2Fkodikdb.com%2Ffind-player%3FkinopoiskID%3D{anime_id}&token={self.token}&imdbID={anime_id}"
        data = await self.get(url)
        if "error" in data.keys() and data["error"] == "Отсутствует или неверный токен":
            raise Exceptions.PlayerBlocked("Token is invalid")
        elif "error" in data.keys():
            raise Exceptions.PlayerBlocked(data["error"])
        if not data["found"]:
            raise Exceptions.PlayerBlocked(f"Anime {anime_id} ({id_type}) not found")
        return "https:" + data["link"]

    async def get_info(
        self, anime_id: str, id_type: Literal["shikimori", "kinopoisk", "imdb"]
    ) -> dict:
        link = await self._link_to_info(anime_id, id_type)
        data = await self.get(link, text=True)
        soup = await self.soup(data)
        if self._is_serial(link):
            episode_count = len(
                soup.find("div", {"class": "serial-series-box"})
                .find("select")
                .find_all("option")
            )
            try:
                translations_div = (
                    soup.find("div", {"class": "serial-translations-box"})
                    .find("select")
                    .find_all("option")
                )
            except AttributeError:
                translations_div = None
            return {
                "episode_count": episode_count,
                "translations": self._generate_translations_dict(translations_div),
            }
        elif self._is_video(link):
            episode_count = 0
            try:
                translations_div = (
                    soup.find("div", {"class": "movie-translations-box"})
                    .find("select")
                    .find_all("option")
                )
            except AttributeError:
                translations_div = None
            return {
                "episode_count": episode_count,
                "translations": self._generate_translations_dict(translations_div),
            }
        else:
            raise Exceptions.PageNotFound(
                "Unknown link type, the link is not a serial or video."
            )

    def _is_serial(self, iframe_url: str) -> bool:
        return True if iframe_url[iframe_url.find(".info/") + 6] == "s" else False

    def _is_video(self, iframe_url: str) -> bool:
        return True if iframe_url[iframe_url.find(".info/") + 6] == "v" else False

    def _generate_translations_dict(self, translations_div) -> dict:
        translations = []
        if not translations_div:
            return [{"id": "0", "type": "Неизвестно", "name": "Неизвестно"}]
        for translation in translations_div:
            a = {}
            a["id"] = translation["value"]
            a["type"] = translation["data-translation-type"]
            if a["type"] == "voice":
                a["type"] = "Озвучка"
            elif a["type"] == "subtitles":
                a["type"] = "Субтитры"
            a["name"] = translation.text
            translations.append(a)
        if not translations:
            translations = [{"id": "0", "type": "Неизвестно", "name": "Неизвестно"}]
        return translations

    async def get_iframe(
        self,
        anime_id: str | int,
        id_type: Literal["shikimori", "kinopoisk", "imdb"],
        episode_num: int = None,
        translation_id: str | int = "0",
    ) -> tuple[str, int]:
        link = await self._link_to_info(anime_id, id_type)
        data = await self.get(link, text=True)
        soup = await self.soup(data)
        container = soup.find("div", {"class": "serial-translations-box"}).find(
            "select"
        )
        media_hash = None
        media_id = None
        for translation in container.find_all("option"):
            if (
                str(translation.get_attribute_list("data-id")[0]) == str(translation_id)
                or translation_id == "0"
            ):
                media_hash = translation.get_attribute_list("data-media-hash")[0]
                media_id = translation.get_attribute_list("data-media-id")[0]
                break
        url = f"https://kodik.info/serial/{media_id}/{media_hash}/720p?min_age=16&first_url=false&season=1&episode={episode_num}"
        return url

    async def get_video(
        self,
        anime_id: str | int,
        id_type: Literal["shikimori", "kinopoisk", "imdb"],
        episode_num: int = None,
        translation_id: str | int = "0",
    ) -> KodikVideo:
        link = await self._link_to_info(anime_id, id_type)
        data = await self.get(link, text=True)
        urlParams = data[data.find("urlParams") + 13 :]
        urlParams = loads(urlParams[: urlParams.find(";") - 1])
        iframe = await self.get_iframe(anime_id, id_type, episode_num, translation_id)
        data = await self.get(iframe, text=True)
        soup = await self.soup(data)
        script_url = soup.find_all("script")[1].get_attribute_list("src")[0]

        hash_container = soup.find_all("script")[4].text
        video_type = hash_container[hash_container.find(".type = '") + 9 :]
        video_type = video_type[: video_type.find("'")]
        video_hash = hash_container[hash_container.find(".hash = '") + 9 :]
        video_hash = video_hash[: video_hash.find("'")]
        video_id = hash_container[hash_container.find(".id = '") + 7 :]
        video_id = video_id[: video_id.find("'")]
        link_data, max_quality = await self._get_link_with_data(
            video_type, video_hash, video_id, urlParams, script_url
        )
        download_url = str(link_data).replace("https://", "")
        return KodikVideo(
            cloud_url="https:" + download_url[2:-26],
            max_quality=max_quality,
            iframe=iframe,
            episode_num=episode_num,
            translation_id=translation_id,
            parser=self,
        )

    async def _get_link_with_data(
        self,
        video_type: str,
        video_hash: str,
        video_id: str,
        urlParams: dict,
        script_url: str,
    ):
        params = {
            "hash": video_hash,
            "id": video_id,
            "type": video_type,
            "d": urlParams["d"],
            "d_sign": urlParams["d_sign"],
            "pd": urlParams["pd"],
            "pd_sign": urlParams["pd_sign"],
            "ref": "",
            "ref_sign": urlParams["ref_sign"],
            "bad_user": "true",
            "cdn_is_working": "true",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        post_link = await self._get_post_link(script_url)
        data = await self.post(
            f"https://kodik.info{post_link}", data=params, headers=headers
        )
        url = self._convert(data["links"]["360"][0]["src"])
        max_quality = max([int(x) for x in data["links"].keys()])
        try:
            return b64decode(url.encode()), max_quality
        except Exception:
            return str(b64decode(url.encode() + b"==")).replace(
                "https:", ""
            ), max_quality

    def _convert_char(self, char: str):
        low = char.islower()
        alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if char.upper() in alph:
            ch = alph[(alph.index(char.upper()) + 13) % len(alph)]
            if low:
                return ch.lower()
            else:
                return ch
        else:
            return char

    def _convert(self, string: str):
        return "".join(map(self._convert_char, list(string)))

    async def _get_post_link(self, script_url: str):
        data = await self.get("https://kodik.info" + script_url, text=True)
        url = data[data.find("$.ajax") + 30 : data.find("cache:!1") - 3]
        return b64decode(url.encode()).decode()

    async def get_m3u8(self, cloud_url: str) -> M3U8Playlist:
        page_content = await self.get(cloud_url, text=True)
        for quality in ["720", "480", "360"]:
            if f"{quality}.mp4" in page_content:
                playlist_content = await self.get(
                    f"{cloud_url}{quality}.mp4:hls:manifest.m3u8", text=True
                )
                break
        else:
            raise ValueError("No valid quality found in page content.")

        for quality in ["720", "480", "360"]:
            if f"{quality}.mp4" in playlist_content:
                filename = f"./{quality}.mp4:hls"
                playlist_content = playlist_content.replace(
                    filename, filename.replace("./", cloud_url)
                )
                break

        return M3U8Playlist(cloud_url, playlist_content)
