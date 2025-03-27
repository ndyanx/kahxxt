from bs4 import BeautifulSoup

from enums import RequestMethod, RequestReturn
from wrappers._aiohttp import AiohttpSG

class DictionaryCambridge:
    
    def _get_headers_webpage(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'es-419,es;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    
    def _get_headers_audio(self,url: str):
        return {
            'Accept': '*/*',
            'Accept-Language': 'es-419,es;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Range': 'bytes=0-',
            'Referer': url,
            'Sec-Fetch-Dest': 'audio',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    
    async def _get_audio(self, accent: str, word: str, soup: BeautifulSoup):
        title = soup.find("title").text
        if not title.lower().startswith(word.lower()):
            raise Exception(f"Word not found: {word}")
        if len(soup.find_all('span', {'class': 'pron-info dpron-info'})) == 1:
            raise Exception(f"Audio not available for word: {word}")
        type_id = 'audio1' if 'uk' == accent else 'audio2'
        audio = soup.find("audio", {"id": type_id})
        path_mp3 = audio.find("source", {"type": "audio/mpeg"})["src"]
        audio_url = f'https://dictionary.cambridge.org{path_mp3}'
        streaming_response = await AiohttpSG.fetch(
            url=audio_url,
            request_method=RequestMethod.GET,
            request_return_type=RequestReturn.AUDIO,
            headers=self._get_headers_audio(audio_url),
        )
        return streaming_response
    
    async def get_audio(self, accent: str, word: str):
        soup = await AiohttpSG.fetch(
            url=f'https://dictionary.cambridge.org/dictionary/english-spanish/{word}',
            request_method=RequestMethod.GET,
            request_return_type=RequestReturn.SOUP,
            headers=self._get_headers_webpage(),
        )
        return await self._get_audio(accent, word, soup)
        
        